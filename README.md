# Copilot Chat Exporter

A robust, memory‑safe extractor for long Copilot conversations.

Copilot does not provide a native way to export your chat history, and long threads often crash the browser due to lazy hydration, virtualized DOMs, and memory pressure.

This tool solves that.

---

## ⭐ Features

- Chunked streaming extraction — survives multi‑hour scrolls  
- Memory‑safe — never hydrates the full DOM  
- Works on extremely long Copilot threads  
- Exports both TXT and Markdown  
- Deduplicates messages automatically  
- Uses Playwright + Edge CDP  
- Tab picker — choose the exact Copilot tab  
- Scrolls inside the chat container (not the page)  
- Manual filename override for accurate naming  
- No crashes, no resets, no lost progress  
- Stable output directory (`C:\CopilotExports`)

---

## ⭐ Why this works

Copilot uses:

- virtualized DOM  
- lazy hydration  
- infinite scroll  
- memory‑heavy rendering  

Traditional scrapers fail because they try to load the entire conversation at once.

This extractor scrolls the chat in controlled increments, extracts only visible messages, streams them directly to disk, and never hydrates the full DOM.

This makes it stable for massive conversations.

---

## ⭐ Installation

### 1. Install Python 3.10+
https://www.python.org/downloads/

### 2. Install Playwright
```bash
pip install playwright
playwright install

3. Clone the repo
bash
git clone https://github.com/Mrorzio/copilot-chat-exporter.git
cd copilot-chat-exporter

⭐ Launch Edge in debugging mode
PowerShell:

powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --user-data-dir="C:\edge-debug" --remote-debugging-port=9222
A new Edge window opens.

⭐ Open your Copilot chat inside that window
Example:

text
https://copilot.microsoft.com/chats/<your-chat-id>
You must open the chat inside the debugging Edge window — normal Edge windows are invisible to CDP.

⭐ Run the extractor
powershell
python export_personal_copilot.py

You will see:

text
Available tabs:
[0] https://copilot.microsoft.com/chats/...
Enter the number of the tab you want to use:
Pick the correct tab.

⭐ Naming your export files (IMPORTANT)
Copilot share pages often hide the real chat title.

The extractor will prompt:
Detected chat title (may be inaccurate on share pages):
Enter a custom name for this chat (recommended):

⭐ Output Directory
All exports are saved to:
C:\CopilotExports

This avoids OneDrive virtualization issues and ensures files appear immediately.

⭐ Output Format
TXT
You said
Hello Copilot

Copilot said
Hi, how can I help today?

Markdown
### You
Hello Copilot

### Copilot
Hi, how can I help today?

⭐ Limitations
Must run Edge in debugging mode

Must manually open Copilot inside that window

Auto‑detected titles are unreliable on share‑links

Manual naming recommended

⭐ Troubleshooting
Playwright not found

ModuleNotFoundError: No module named 'playwright'

Use the Python installation that has Playwright installed.

Extractor cannot find the Copilot tab
Open the chat inside the debugging Edge window.

Wrong filename detected
Use the manual naming prompt.

Smart App Control (SAC) blocks DLLs
If you see:
ImportError: DLL load failed while importing _greenlet

Disable Smart App Control:

Windows Security → App & Browser Control → Smart App Control → Off

Restart your PC.

⭐ Why Edge?
Copilot runs inside Edge’s WebView2 environment.

Using Edge with CDP ensures:

stable access to the chat container

consistent DOM structure

predictable hydration behavior

reliable infinite scroll handling

Chrome or other browsers will not work.

⭐ Upcoming Additions
These items are planned for future releases:

📘 Changelog

🤝 Contributing Guide

🧭 Roadmap

🎨 Project Logo

🧩 Architecture Diagram

These will be introduced gradually starting with v1.2.0.

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

your business brain

your institutional memory

your long‑term AI workflow

⭐ Roadmap (v1.3.0)
JSON export
HTML export
Automatic chat title detection
Multi-chat batch export
GUI wrapper
