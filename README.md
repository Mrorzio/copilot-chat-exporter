Copilot Chat Exporter

A robust, memory‑safe extractor for long Copilot conversations.
Copilot does not provide a native way to export your chat history and long threads often crash the browser due to lazy hydration, virtualized DOMs, and memory pressure.

This tool solves that.

⭐ Features
Chunked streaming extraction - survives multi‑hour scrolls

Memory‑safe - never hydrates the full DOM

Works on extremely long Copilot threads

Extracts both TXT and Markdown

Deduplicates messages automatically

Uses Playwright + Edge CDP

Tab picker - choose the exact Copilot tab

Scrolls inside the chat container (not the page)

No crashes, no resets, no lost progress

⭐ Why this works
Copilot uses:

virtualized DOM
lazy hydration
infinite scroll
memory‑heavy rendering

Traditional scrapers fail because they try to load the entire conversation at once.

This extractor scrolls the chat in small chunks, extracts only the visible messages, streams them directly to disk, and never allows the browser to accumulate more than a few dozen hydrated nodes.

This makes it stable for massive conversations.

⭐ Installation
1. Install Python 3.10+
https://www.python.org/downloads/

2. Install Playwright
Code
pip install playwright
playwright install

3. Clone the repo
Code
git clone https://github.com/Mrorzio/copilot-chat-exporter.git
cd copilot-chat-exporter

⭐ Usage
1. Launch Edge in debugging mode
Code
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" ^
  --user-data-dir="C:\edge-debug" ^
  --remote-debugging-port=9222
A new Edge window opens.

2. In that window, open your Copilot chat
Example:

Code
https://copilot.microsoft.com/chats/<your-chat-id>

3. Run the extractor
Code
python export_personal_copilot.py

4. Pick the Copilot tab
You’ll see:

Code
Available tabs:
[0] https://copilot.microsoft.com/chats/...
Enter the number of the tab you want to use:
Choose the correct tab.

5. Let it run
It will scroll for a long time.
It will not crash.
It will stream messages into:

copilot_chat_full.txt

copilot_chat_full.md

⭐ Output Format
TXT
Code
You said
Hello Copilot

Copilot said
Hi Mrorzio, how can I help today?
Markdown
Code
### You
Hello Copilot

### Copilot
Hi Mrorzio, how can I help today?
⭐ Limitations
Must run Edge in debugging mode

Must manually open Copilot inside that window
Extraction speed depends on thread length

⭐ License
MIT — free to use, modify, and distribute.

⭐ Contributions
Pull requests welcome.
Issues welcome.
Feature requests welcome.

⭐ Why this exists
Copilot is becoming a second brain for millions of people but there is no way to export your conversations.

This tool is the missing link between:

Copilot
your personal knowledge base
your second brain
your institutional memory
your long‑term AI workflow
