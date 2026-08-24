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
