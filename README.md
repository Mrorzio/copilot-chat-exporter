# Copilot Chat Exporter

A robust, memory‑safe extractor for long Copilot conversations.

Copilot does not provide a native way to export your chat history, and long threads often crash the browser due to lazy hydration, virtualized DOMs, and memory pressure.

This tool solves that.

---

## ⭐ Features

- **Chunked streaming extraction** — survives multi‑hour scrolls  
- **Memory‑safe** — never hydrates the full DOM  
- **Works on extremely long Copilot threads**  
- **Exports both TXT and Markdown**  
- **Deduplicates messages automatically**  
- **Uses Playwright + Edge CDP**  
- **Tab picker** — choose the exact Copilot tab  
- Scrolls inside the chat container (not the page)
- Manual filename override — ensures correct naming even on share‑links 
- **No crashes, no resets, no lost progress**
- Stable output directory (C:\CopilotExports)

---

## ⭐ Why this works

Copilot uses:

- virtualized DOM  
- lazy hydration  
- infinite scroll  
- memory‑heavy rendering  

Traditional scrapers fail because they try to load the entire conversation at once.

This extractor scrolls the chat in small chunks, extracts only the visible messages, streams them directly to disk, and never allows the browser to accumulate more than a few dozen hydrated nodes.

This makes it stable for massive conversations.

---

## ⭐ Installation

### 1. Install Python 3.10+
https://www.python.org/downloads/

### 2. Install Playwright
```bash
pip install playwright
playwright install
```

### 3. Clone the repo
```bash
git clone https://github.com/Mrorzio/copilot-chat-exporter.git
cd copilot-chat-exporter
```
⭐ Launch Edge in debugging mode
PowerShell (single line):

powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --user-data-dir="C:\edge-debug" --remote-debugging-port=9222
A new Edge window opens.

⭐ Open your Copilot chat inside that window
Example:

Code
https://copilot.microsoft.com/chats/<your-chat-id>
You must open the chat inside the debugging Edge window, not your normal browser.

⭐ Run the extractor
powershell
python export_personal_copilot.py
You will see:

Code
Available tabs:
[0] https://copilot.microsoft.com/chats/...
Enter the number of the tab you want to use:
Pick the correct tab.

⭐ Naming your export files (IMPORTANT)
Copilot share pages do not expose the real chat title in the DOM.
Because of this, the extractor always prompts you to enter a custom name:

Code
Detected chat title (may be inaccurate on share pages): 🔥 Section‑by‑Section Placement of Your Comments
Enter a custom name for this chat (recommended):
You should enter the name you want:

Code
TALU PRD To Engineering Comments
Your files will be saved as:

Code
C:\CopilotExports\TALU PRD To Engineering Comments.txt
C:\CopilotExports\TALU PRD To Engineering Comments.md
If you press Enter, the detected title will be used — but this is often inaccurate on share‑links.

⭐ Output Directory
All exports are saved to:

Code
C:\CopilotExports
This avoids OneDrive virtualization issues and ensures files are visible immediately.

⭐ Output Format
TXT
Code
You said
Hello Copilot

Copilot said
Hi, how can I help today?
Markdown
markdown
### You
Hello Copilot

### Copilot
Hi, how can I help today?
⭐ Limitations
Must run Edge in debugging mode

Must manually open Copilot inside that window

Auto‑detected titles are unreliable on share‑links

Manual naming is recommended for every export

⭐ Troubleshooting
Playwright not found
Code
ModuleNotFoundError: No module named 'playwright'
Run the script using the Python installation that has Playwright installed.

Extractor cannot find the Copilot tab
Make sure the chat is opened inside the debugging Edge window.

Wrong filename detected
Use the manual naming prompt.

⭐ Why Edge?
Copilot runs inside Edge’s WebView2 environment and uses Edge‑specific rendering behavior.

Using Edge with CDP ensures:

stable access to the chat container

consistent DOM structure

predictable hydration behavior

reliable infinite scroll handling

Chrome or other browsers will not work for Copilot extraction.

⭐ Upcoming Additions
The following project assets are planned for future releases to improve clarity, onboarding, and long-term maintainability:

📘 Changelog (coming soon)
A structured version history documenting all changes across releases, including fixes, enhancements, and major updates.

🤝 Contributing Guide (coming soon)
A clear set of guidelines for contributors, covering development workflow, coding standards, and how to propose improvements.

🧭 Roadmap (coming soon)
A forward-looking outline of planned features, architectural improvements, and long-term goals for the exporter.

🎨 Project Logo (future release)
A simple, recognizable visual identity for the repository and documentation.

🧩 Architecture Diagram (future release)
A visual overview of how the exporter interacts with Edge, CDP, hydration, and the extraction pipeline.

These items will be introduced gradually in upcoming versions (starting with v1.2.0) to keep the project clean, consistent, and easy to navigate.

⭐ License
MIT — free to use, modify, and distribute.

⭐ Contributions
Pull requests welcome.
Issues welcome.
Feature requests welcome.

⭐ Why this exists
Copilot is becoming a second brain for millions of people — but there is no way to export your conversations.

This tool is the missing link between:

Copilot

your personal knowledge base

your second brain

your business brain formation from personal brain

your institutional memory

your long‑term AI workflow

---
## Roadmap (v1.2.0)
- JSON export
- HTML export
- Automatic chat title detection for non-share pages
- Multi-chat batch export
- GUI wrapper

🔥 Full-Thread Extraction (v1.1.1)
Copilot conversations often exceed what the browser hydrates by default. Long threads use:

virtualized DOM

lazy hydration

infinite scroll

memory-heavy rendering

Traditional scrapers fail because they try to load the entire conversation at once — causing resets, crashes, or partial exports.

v1.1.1 introduces a robust full-thread scroll loop that reliably extracts complete Copilot conversations.

✔ What’s new
Bottom-start scroll traversal

Large upward scroll increments

Hydration-change detection

Duplicate message hashing

Stable-pass detection (stops only when the true top is reached)

Full-thread extraction validated on real Copilot chats

Clean multi-file segmentation with Obsidian-ready Markdown

✔ Verified performance
A real Copilot thread produced:

161 messages extracted

22 chunks written

Complete export

This update resolves the long-standing issue where exports stopped after ~20–30 messages.

⭐ Why This Works
Copilot’s DOM is virtualized and only hydrates a small portion of the conversation at any given time.
This extractor:

scrolls the chat container in controlled increments

waits for hydration

extracts only visible messages

streams them directly to disk

never hydrates the full DOM

never accumulates more than a few dozen nodes

This makes it stable for massive conversations.

🛠️ Usage (unchanged, but clarified)
1. Launch Edge in debugging mode
powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --user-data-dir="C:\edge-debug" --remote-debugging-port=9222
2. Open Copilot inside that window
This is required — normal Edge windows are invisible to CDP.

3. Run the extractor
powershell
python export_personal_copilot.py
4. Select the Copilot tab
The extractor will list all tabs inside the debugging Edge window.

5. Follow prompts
You’ll choose:

folder naming mode

chunk size

file prefix

The extractor will:

hydrate the full thread

extract all messages

write chunked .md and .txt files

store everything under:

Code
C:\CopilotExports
🧩 Output Format
Each chunk includes:

Obsidian frontmatter

Dates covered

Source URL

Role headers (### You, ### Copilot)

Wrapped text at 100 characters

Timestamped .txt logs

Files are named:

Code
01 - PREFIX.md
02 - PREFIX.md
...
Earliest messages appear in the lowest-numbered file.

🛡️ Troubleshooting
Smart App Control (SAC) blocks Playwright DLLs
If you see:

Code
ImportError: DLL load failed while importing _greenlet
Disable Smart App Control:

Windows Security → App & Browser Control → Smart App Control → Off

Restart your PC.

PythonCore / Microsoft Store Python
If python resolves to:

Code
C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\python.exe
Install Python from python.org and ensure:

“Add Python to PATH”

“Install for all users”

are checked.

Exporter sees only extension tabs
You must open Copilot inside the debugging Edge window, not your normal browser.

🗺️ Roadmap (v1.2.0)
JSON export

HTML export

Automatic chat title detection for non-share pages

Multi-chat batch export

GUI wrapper
