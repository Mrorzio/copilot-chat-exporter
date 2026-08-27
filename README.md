<div align="center">

??      ??
??        ¦¦¦¦¦¦¦¦¦¦¦        ??
¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
¦¦¦¦¦¦   ¦¦¦¦¦¦¦¦   ¦¦¦¦¦¦
¦¦¦¦¦     ¦¦¦¦¦¦¦¦¦¦     ¦¦¦¦¦
¦¦¦¦       ¦¦¦¦¦¦¦¦¦¦¦¦       ¦¦¦¦
¦¦¦         ¦¦¦¦¦¦¦¦¦¦¦¦         ¦¦¦
¦¦¦       ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦        ¦¦¦
¦¦¦    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦      ¦¦¦
¦¦¦     ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦    ¦¦¦
¦¦¦     ¦¦¦¦¦¦¦¦¦¦¦¦    ¦¦¦
¦¦¦¦     ¦¦¦¦¦¦¦    ¦¦¦¦
¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
??        ¦¦¦¦¦¦¦¦¦¦¦        ??

?--------------------?
¦ ~~~~~  ~~~~~  ~~~~ ¦
?---¦ ~~~~~~ ~~~~~~ ~~~~ ¦---?
¦   ¦ ~~~~~  ~~~~~  ~~~~ ¦   ¦
?---¦ ~~~~~~ ~~~~~~ ~~~~ ¦---?
?--------------------?

# **Copilot Chat Exporter**  
Founder OS ? Pomegranium Studio ? Bacalar Edition

</div>

---

<details>
<summary><strong>?? Table of Contents</strong></summary>

- [Overview](#overview)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Batch Export Mode](#batch-export-mode)  
- [Roadmap](#roadmap)  
- [Contributing](#contributing)  
- [License](#license)

</details>

---

## Overview

Copilot Chat Exporter is a **Founder-grade extraction engine** designed to pull your Copilot chats into structured, ingestible formats for your **Founder OS**, **Pomegranium Studio**, and **capital stack workflows**.

This tool is built for:

- founders  
- operators  
- institutional architects  
- systems engineers  
- anyone building a multi-layer OS in Obsidian, Notion, or custom stacks  

It supports **single-chat export**, **batch export**, and **multi-file ingestion**.

---

## Features

- ?? **One-click chat export**  
- ?? **Batch export mode**  
- ?? **Founder OS-ready formatting**  
- ??? **Automatic file naming**  
- ?? **Metadata extraction**  
- ?? **CLI + PowerShell support**  
- ?? **Zero external dependencies**

---

## Installation

Clone the repo:

git clone https://github.com/Mrorzio/copilot-chat-exporter.git (github.com in Bing)
cd copilot-chat-exporter


---

## Usage

Single export:

python exporter.py --chat-id <ID>


Batch export:

python exporter.py --batch ./input/

---

## Batch Export Mode

Place your .json or .html Copilot chat exports into /input.

Run:

python exporter.py --batch ./input


Outputs land in /output.

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md).

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

MIT License.

