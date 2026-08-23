from playwright.sync_api import sync_playwright
import time
import textwrap
import hashlib

CDP_URL = "http://localhost:9222"

OUTPUT_TXT = "copilot_chat_full.txt"
OUTPUT_MD = "copilot_chat_full.md"


def pick_tab(browser):
    """Let the user choose which tab to scrape."""
    all_pages = []
    for ctx in browser.contexts:
        for p in ctx.pages:
            all_pages.append(p)

    if not all_pages:
        raise RuntimeError("No tabs found in Edge. Open Copilot in the debugging window first.")

    print("\nAvailable tabs:")
    for i, p in enumerate(all_pages):
        print(f"[{i}] {p.url}")

    print("")
    choice = input("Enter the number of the tab you want to use: ").strip()

    try:
        idx = int(choice)
        return all_pages[idx]
    except:
        raise RuntimeError("Invalid selection. Please enter a valid tab number.")


def connect_to_edge():
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(CDP_URL)

    page = pick_tab(browser)

    print(f"\nSelected tab: {page.url}\n")
    return pw, browser, page


def find_chat_container(page):
    js_find_container = """
        () => {
            const candidates = document.querySelectorAll('div, main, section');
            for (const el of candidates) {
                const style = window.getComputedStyle(el);
                if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
                    if (el.querySelector('h6[id$="-author"][aria-label]')) {
                        return el;
                    }
                }
            }
            return null;
        }
    """
    container = page.evaluate_handle(js_find_container)
    if not container:
        raise RuntimeError("Could not find Copilot chat container.")
    return container


def extract_visible_messages(page):
    js = """
(() => {
  const nodes = document.querySelectorAll('h6[id$="-author"][aria-label]');
  const messages = [];
  for (const h of nodes) {
    const role = h.getAttribute('aria-label') || '';
    let contentNode = h.nextElementSibling;
    if (!contentNode) {
      contentNode = h.parentElement;
    }
    let text = '';
    if (contentNode) {
      text = contentNode.innerText || '';
    }
    text = text.trim();
    if (!text) continue;

    messages.push({ role, text });
  }
  return messages;
})();
"""
    return page.evaluate(js)


def hash_message(role, text):
    return hashlib.sha256((role + text).encode("utf-8")).hexdigest()


def append_to_files(messages, seen_hashes):
    with open(OUTPUT_TXT, "a", encoding="utf-8") as txt, \
         open(OUTPUT_MD, "a", encoding="utf-8") as md:

        for msg in messages:
            role = msg["role"]
            text = msg["text"]
            h = hash_message(role, text)

            if h in seen_hashes:
                continue
            seen_hashes.add(h)

            # TXT
            txt.write(f"{role}\n{text}\n\n")

            # MD
            if "Copilot said" in role:
                header = "### Copilot"
            elif "You said" in role:
                header = "### You"
            else:
                header = f"### {role}"

            md.write(header + "\n\n")
            md.write(textwrap.fill(text, width=100) + "\n\n")


def chunked_scroll(page, container, pause=0.5, max_iterations=5000):
    """
    Scrolls the chat container upward in small chunks.
    Extracts visible messages after each chunk.
    Streams them directly to disk.
    """

    seen_hashes = set()
    last_scroll_top = None
    stable_rounds = 0

    for i in range(max_iterations):
        # Extract visible messages
        messages = extract_visible_messages(page)
        append_to_files(messages, seen_hashes)

        # Scroll upward a bit
        page.evaluate("""
            (container) => {
                container.scrollTop = container.scrollTop - 300;
            }
        """, container)

        time.sleep(pause)

        scroll_top = page.evaluate("(container) => container.scrollTop", container)

        # Stop if no movement
        if scroll_top == last_scroll_top:
            stable_rounds += 1
            if stable_rounds >= 20:
                print("Reached top of chat.")
                break
        else:
            stable_rounds = 0

        last_scroll_top = scroll_top

        if i % 50 == 0:
            print(f"Progress: {i} chunks processed...")

    print("Chunked scroll complete.")


def main():
    print("Connecting to Edge at", CDP_URL)
    pw, browser, page = connect_to_edge()

    try:
        print("Locating chat container...")
        container = find_chat_container(page)

        print("Beginning chunked extraction (this may take a long time)...")
        chunked_scroll(page, container)

        print(f"\nExtraction complete.")
        print(f"TXT saved to: {OUTPUT_TXT}")
        print(f"MD saved to:  {OUTPUT_MD}")

    finally:
        pw.stop()


if __name__ == "__main__":
    main()
