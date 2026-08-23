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
- **Scrolls inside the chat container (not the page)**  
- **No crashes, no resets, no lost progress**

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

---

## ⭐ How to Find Your Copilot Chat ID

Every Copilot conversation has a unique chat ID in the URL.

When you open a Copilot chat inside the debugging Edge window, look at the URL bar:

```
https://copilot.microsoft.com/chats/<CHAT_ID>
```

Example:

```
https://copilot.microsoft.com/chats/DEQT7ugWBYhHeD4o1FEin
```

The chat ID is:

```
DEQT7ugWBYhHeD4o1FEin
```

You will also see this same URL in the tab list printed by the extractor:

```
Available tabs:
[1] https://copilot.microsoft.com/chats/DEQT7ugWBYhHeD4o1FEin
```

Select the tab containing the chat you want to export.

---

## ⭐ Usage

### 1. Launch Edge in debugging mode  
**PowerShell (single line):**
```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --user-data-dir="C:\edge-debug" --remote-debugging-port=9222
```

A new Edge window opens.

### 2. In that window, open your Copilot chat  
Example:

```
https://copilot.microsoft.com/chats/<your-chat-id>
```

### 3. Run the extractor  
```bash
python export_personal_copilot.py
```

### 4. Pick the Copilot tab  
You’ll see:

```
Available tabs:
[0] https://copilot.microsoft.com/chats/...
Enter the number of the tab you want to use:
```

Choose the correct tab.

### 5. Let it run  
It will scroll for a long time.  
It will not crash.  
It will stream messages into:

```
copilot_chat_full.txt
copilot_chat_full.md
```

---

## ⭐ Output Format

### TXT
```
You said
Hello Copilot

Copilot said
Hi, how can I help today?
```

### Markdown
```markdown
### You
Hello Copilot

### Copilot
Hi, how can I help today?
```

---

## ⭐ Limitations

- Must run Edge in debugging mode  
- Must manually open Copilot inside that window  
- Extraction speed depends on thread length  

---

## ⭐ Known Issues

- **Must run Edge in debugging mode**  
  The extractor connects to Edge using CDP. Normal Edge windows will not work.

- **Must open Copilot inside the debugging window**  
  The extractor can only see tabs inside the special Edge instance.

- **Multiple Python installations may cause Playwright errors**  
  If you see `ModuleNotFoundError: No module named 'playwright'`, run the script using the full path to the Python that has Playwright installed.

- **Extraction speed depends on thread length**  
  Very long conversations may take several minutes to scroll.

---

## ⭐ Troubleshooting

### Playwright not found
If you see:

```
ModuleNotFoundError: No module named 'playwright'
```

Run the script using the Python installation that has Playwright installed:

```powershell
& "C:\Path\To\Your\Python.exe" export_personal_copilot.py
```

### Edge command fails in PowerShell
Use the PowerShell version of the command:

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --user-data-dir="C:\edge-debug" --remote-debugging-port=9222
```

### Extractor cannot find the Copilot tab
Make sure the Copilot chat is opened **inside the debugging Edge window**, not your normal browser.

---

## ⭐ Success Example

When the extractor finishes, you will see:

```
Extraction complete.
TXT saved to: copilot_chat_full.txt
MD saved to:  copilot_chat_full.md
```

These files appear in the same folder where you ran the script.

---

## ⭐ Why Edge?

Copilot runs inside Edge’s WebView2 environment and uses Edge‑specific rendering behavior.

Using Edge with CDP ensures:

- stable access to the chat container  
- consistent DOM structure  
- predictable hydration behavior  
- reliable infinite scroll handling  

Chrome or other browsers will not work for Copilot extraction.

---

## ⭐ License

MIT — free to use, modify, and distribute.

---

## ⭐ Contributions

Pull requests welcome.  
Issues welcome.  
Feature requests welcome.

---

## ⭐ Why this exists

Copilot is becoming a second brain for millions of people — but there is no way to export your conversations.

This tool is the missing link between:

- Copilot  
- your personal knowledge base  
- your second brain  
- your institutional memory  
- your long‑term AI workflow
