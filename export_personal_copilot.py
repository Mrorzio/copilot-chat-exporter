from playwright.sync_api import sync_playwright
import time
import hashlib
import textwrap
import os
import re
import json
from datetime import datetime

CDP_URL = "http://localhost:9222"
BASE_OUTPUT_ROOT = r"C:\CopilotExports"


# ============================================================
# Utility Helpers
# ============================================================

def hash_message(role, text):
    return hashlib.sha256((role + text).encode("utf-8")).hexdigest()


def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    if not name:
        name = "copilot_chat"
    return name


def ensure_output_root():
    if not os.path.exists(BASE_OUTPUT_ROOT):
        os.makedirs(BASE_OUTPUT_ROOT, exist_ok=True)


# ============================================================
# V2: Multi‑Chat Tab Detection
# ============================================================

def get_all_copilot_tabs(browser):
    """Return all tabs that contain Copilot chat URLs."""
    tabs = []
    for ctx in browser.contexts:
        for p in ctx.pages:
            if "copilot.microsoft.com/chats" in p.url:
                tabs.append(p)
    return tabs


def auto_folder_name_from_title(raw_title):
    """Auto-name folders using Option D: <ChatTitle> <YYYY-MM-DD>"""
    base = sanitize_filename(raw_title)
    date_str = datetime.utcnow().date().isoformat()
    return f"{base} {date_str}"


def auto_file_prefix_from_title(raw_title):
    """Auto file prefix: <ChatTitle>-<YYYYMMDD>"""
    base = sanitize_filename(raw_title)
    date_str = datetime.utcnow().strftime("%Y%m%d")
    return f"{base}-{date_str}"


# ============================================================
# DOM Helpers
# ============================================================

def find_chat_container(page):
    js = """
    () => {
        const primary = document.querySelector('div[data-testid="conversation-scroll-container"]');
        if (primary) return primary;

        const selectors = [
            'main[data-testid="conversation"]',
            'div[class*="scroll"]',
            'div[class*="Scrollable"]',
            'div[class*="scrollable"]'
        ];

        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) return el;
        }

        const candidates = document.querySelectorAll('div, main, section');
        for (const el of candidates) {
            const style = window.getComputedStyle(el);
            if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
                return el;
            }
        }

        return null;
    }
    """
    container = page.evaluate_handle(js)
    is_null = page.evaluate("(c) => c === null", container)
    if is_null:
        raise RuntimeError("Could not find chat scroll container.")
    return container


def extract_visible_messages(page):
    js = """
    (() => {
        const selectors = [
            '[data-message-id]',
            '[data-message-author]',
            'div[class*="message"]',
            'div[class*="bubble"]',
            'div[class*="markdown"]',
            'article'
        ];

        let nodes = [];
        for (const sel of selectors) {
            nodes = document.querySelectorAll(sel);
            if (nodes.length > 0) break;
        }

        const messages = [];

        for (const node of nodes) {
            const text = node.innerText?.trim();
            if (!text) continue;

            let role = 'Unknown';
            const author = node.getAttribute('data-message-author') || '';

            if (author.toLowerCase().includes('user')) role = 'You said';
            if (author.toLowerCase().includes('assistant')) role = 'Copilot said';

            messages.push({ role, text });
        }

        return messages;
    })();
    """
    return page.evaluate(js)


# ============================================================
# Hydration Pipeline
# ============================================================

def super_scroll_to_top(page, container, pause=1.2, max_rounds=200):
    print("\n[Phase 1] Aggressive pre-scroll to top...")

    last_height = None
    stable_rounds = 0
    MAX_STABLE = 15

    for i in range(max_rounds):

        page.evaluate(
            """
            (container) => {
                if (!container) return;
                container.scrollTop = container.scrollTop - 5000;
                if (container.scrollTop < 0) container.scrollTop = 0;
            }
            """,
            container
        )

        page.evaluate("window.scrollBy(0, -5000)")
        time.sleep(pause)

        current_height = page.evaluate("(c) => c.scrollHeight", container)

        if current_height == last_height:
            stable_rounds += 1
        else:
            stable_rounds = 0

        last_height = current_height

        print(f"[SuperScroll {i}] Height={current_height} | Stable={stable_rounds}")

        at_top = page.evaluate("(c) => c.scrollTop === 0", container)
        if at_top and stable_rounds >= MAX_STABLE:
            print("[Phase 1] Reached top of thread. Hydration complete.")
            break

    print("[Phase 1] Super-scroll complete.\n")


def hybrid_scroll_and_collect(page, container, pause=1.2, max_iterations=2000):
    seen_hashes = set()
    json_buffer = []

    last_height = None
    last_count = 0
    stable_rounds = 0
    MAX_STABLE_ROUNDS = 10

    page.evaluate(
        """
        (container) => {
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }
        """,
        container
    )
    time.sleep(pause)

    for i in range(max_iterations):
        messages = extract_visible_messages(page)

        for msg in messages:
            role = msg["role"]
            text = msg["text"]
            h = hash_message(role, text)
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            json_buffer.append({
                "role": role,
                "text": text,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })

        current_count = len(seen_hashes)

        scroll_top = page.evaluate(
            """
            (container) => {
                if (!container) return null;
                container.scrollTop = container.scrollTop - 1600;
                if (container.scrollTop < 0) container.scrollTop = 0;
                return container.scrollTop;
            }
            """,
            container
        )

        page.evaluate("window.scrollBy(0, -800)")

        if scroll_top is None:
            print("Container vanished; stopping.")
            break

        time.sleep(pause)

        current_height = page.evaluate("(c) => c.scrollHeight", container)

        hydration_happened = (
            current_height != last_height or
            current_count != last_count
        )

        if not hydration_happened:
            stable_rounds += 1
            if stable_rounds >= MAX_STABLE_ROUNDS:
                print("No new messages after multiple scrolls — reached top of thread.")
                break
        else:
            stable_rounds = 0

        last_height = current_height
        last_count = current_count

        if i % 10 == 0:
            print(f"[Pass {i}] Messages: {current_count} | Height: {current_height} | Stable rounds: {stable_rounds}")

        at_top = page.evaluate("(c) => c.scrollTop === 0", container)
        if at_top and stable_rounds >= MAX_STABLE_ROUNDS:
            print("Container at top and stable — stopping.")
            break

    print("Hybrid scroll complete.")
    return json_buffer


# ============================================================
# Chunking + File Writing
# ============================================================

def build_frontmatter(file_title, dates_covered, source_url):
    dates_yaml = "\n  - ".join(dates_covered) if dates_covered else ""
    if dates_yaml:
        dates_block = f"\ndates_covered:\n  - {dates_yaml}"
    else:
        dates_block = ""

    fm = f"""---
title: {file_title}{dates_block}
source: {source_url}
---

"""
    return fm


def segment_and_write_files(json_buffer, chunk_size_words, folder_path, file_prefix, source_url):
    def parse_ts(ts):
        try:
            return datetime.fromisoformat(ts.replace("Z", ""))
        except:
            return datetime.utcnow()

    messages = sorted(json_buffer, key=lambda m: parse_ts(m["timestamp"]))

    chunks = []
    current_chunk = []
    current_words = 0

    for msg in messages:
        words = len(msg["text"].split())
        if current_words + words > chunk_size_words and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_words = 0
        current_chunk.append(msg)
        current_words += words

    if current_chunk:
        chunks.append(current_chunk)

    total_chunks = len(chunks)
    if total_chunks == 0:
        print("No messages to write.")
        return

    print(f"\nTotal chunks: {total_chunks}")

    for idx, chunk in enumerate(chunks, start=1):
        file_index = str(idx).zfill(len(str(total_chunks)))
        file_title = f"{file_prefix} {file_index}"
        filename_md = os.path.join(folder_path, f"{file_index} - {file_prefix}.md")
        filename_txt = os.path.join(folder_path, f"{file_index} - {file_prefix}.txt")

        dates = sorted({parse_ts(m["timestamp"]).date().isoformat() for m in chunk})
        frontmatter = build_frontmatter(file_title, dates, source_url)

        with open(filename_md, "w", encoding="utf-8") as md:
            md.write(frontmatter)
            for msg in chunk:
                role = msg["role"]
                text = msg["text"]

                if "Copilot" in role:
                    header = "### Copilot"
                elif "You" in role:
                    header = "### You"
                else:
                    header = f"### {role}"

                md.write(header + "\n\n")
                md.write(textwrap.fill(text, width=100) + "\n\n")

        with open(filename_txt, "w", encoding="utf-8") as txt:
            for msg in chunk:
                role = msg["role"]
                text = msg["text"]
                txt.write(f"{role}\n{text}\n\n")

        print(f"Wrote chunk {file_index}: {filename_md}")


# ============================================================
# V2 MAIN — Multi‑Chat Batch Export (Option D)
# ============================================================

def main():
    print("Working directory:", os.getcwd())
    print("Connecting to Edge at", CDP_URL)

    ensure_output_root()

    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(CDP_URL)

    # ---------------------------
    # Detect ALL Copilot chats
    # ---------------------------
    copilot_tabs = get_all_copilot_tabs(browser)

    if not copilot_tabs:
        pw.stop()
        raise RuntimeError("No Copilot chats found. Open Copilot inside the debugging Edge window first.")

    print(f"\nDetected {len(copilot_tabs)} Copilot chat tabs.")
    print("Beginning batch export...\n")

    for idx, page in enumerate(copilot_tabs, start=1):
        print("=" * 80)
        print(f"[Chat {idx}/{len(copilot_tabs)}] URL: {page.url}")
        print("=" * 80)

        # ---------------------------
        # Auto-detect chat title
        # ---------------------------
        raw_title = page.evaluate("""
            () => {
                const selectors = [
                    '[data-testid="chat-title"]',
                    'h1',
                    'div[class*="title"]',
                    'span[class*="title"]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText) return el.innerText.trim();
                }
                return document.title;
            }
        """)

        chat_title = sanitize_filename(raw_title)
        folder_name = auto_folder_name_from_title(chat_title)
        file_prefix = auto_file_prefix_from_title(chat_title)

        folder_path = os.path.join(BASE_OUTPUT_ROOT, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        print(f"Auto folder name: {folder_name}")
        print(f"Auto file prefix: {file_prefix}\n")

        # ---------------------------
        # Hydrate + extract
        # ---------------------------
        print("Locating chat container...")
        container = find_chat_container(page)

        print("Beginning aggressive pre-scroll to hydrate full thread...")
        super_scroll_to_top(page, container)

        print("Beginning hybrid scroll + extraction (full thread)...")
        json_buffer = hybrid_scroll_and_collect(page, container)

        print(f"\nTotal messages collected: {len(json_buffer)}")
        print("Segmenting into multi-file export...")

        # Fixed chunk size for v2 (2500 words)
        chunk_size_words = 2500

        segment_and_write_files(
            json_buffer=json_buffer,
            chunk_size_words=chunk_size_words,
            folder_path=folder_path,
            file_prefix=file_prefix,
            source_url=page.url,
        )

        print(f"\nExport complete for chat: {chat_title}")
        print(f"Folder: {folder_path}\n")

    print("\nAll chats exported successfully.")
    pw.stop()


if __name__ == "__main__":
    main()
