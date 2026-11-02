# Ultimate Toolbox Pro

A comprehensive desktop toolkit for Windows, Linux, and macOS.

## Overview

Ultimate Toolbox Pro is a privacy-first productivity and developer desktop application designed to bring together useful utilities in one local, easy-to-use interface. It combines everyday tools, system utilities, file operations, text processing, security-related tools, media utilities, developer workflows, and API-based services in a single app.

The project is built for users who want a fast, offline-friendly, and highly practical toolkit without relying on cloud services or external trackers.

## Highlights

- 50+ tools grouped into 11 categories: General, System, Files, Text, Security, Media, Finance & Time, Productivity, Developer, Services, and Data.
- Support for 10 languages with RTL compatibility: Arabic, English, Chinese, Hindi, Spanish, French, Bengali, Portuguese, Russian, and Urdu.
- True black/red themed UI generated with `ctk.set_default_color_theme()`, with both light and dark modes.
- Fully offline-first behavior: no cloud sync, no analytics, and no background tracking.
- Quick command palette (`Ctrl+K`), favorites manager, and recent tools history.
- Resilient behavior: missing optional libraries produce clear warnings instead of crashing the app.

## Build the Windows EXE locally

Double-click **`build.bat`** (needs Python 3 on PATH). It creates a `.venv`, installs `requirements.txt` + PyInstaller, checks syntax and builds **`dist\Toolbox.exe`** with the same options as the GitHub workflow.

The EXE only contains packages that were installed when it was built. `build.bat` and the GitHub workflow therefore try to add **llama-cpp-python** (prebuilt CPU wheel, Python 3.12 or older) so the in-process LLM backend works inside the EXE. If no wheel exists for your Python, the EXE still builds and the Local LLM tool works through the **llama.cpp Server (auto-start)** backend, which needs no extra package.

Settings, downloaded models and the llama-server binary are stored next to the EXE (`ultimate_toolbox_settings.json`, `toolbox_data/`). To reuse existing ones, copy them next to `Toolbox.exe`.

## Context menu & input shortcuts (every tool)

Right-click (or press the Menu key / Shift+F10) in **any** text field or output box in the app, including plugins, to get a context menu: Undo, Redo, Cut, Copy, Paste, Delete, Select all, Copy all, Save to file… and Clear. Items that don't apply are disabled; read-only output boxes offer Copy, Select all, Copy all and Save to file; password fields never offer Cut or Copy. The menu is built into the app itself, so it works the same whether you start it with `python toolbox.py` or from the compiled EXE. On macOS use two-finger click or Ctrl+click.

Also available everywhere: **Ctrl+A** selects all in any field, **Ctrl+Z / Ctrl+Y** undo and redo inside text boxes, and the field you are typing in gets a highlighted border.

Chat input: **Enter** sends, **Shift+Enter** adds a new line (a switch turns "Enter sends" off, then Ctrl+Enter sends), **Esc** stops generation, **↑ / ↓** recall your previous messages when the box is empty. 📎 *Attach file* pastes a text file you choose into your message, ✨ *Quick prompts* inserts ready-made templates, and a counter shows characters and estimated tokens (it turns orange near the context limit). Answers are rendered with Markdown styling (headings, bold, italic, inline code, code blocks, lists, quotes, links) while the saved chat text stays plain Markdown.

## Local LLM page layout

The Local LLM tool is organised into four tabs: **Chat**, **Model** (engine, server, model files and downloads), **Configuration** and **Agent**. A status chip at the top always shows the loaded model (or "generating" / "downloading"). The page opens on Chat when a model or server is already available, otherwise on Model. In the chat, your messages, the assistant's replies, tool calls and token stats use different colours, and the message box sits next to the Send and Stop buttons.

## LLM agent mode (internet & device access, with your permission)

In **Local LLM → 🛡 Agent mode** you can let the model use tools. It is **off by default**; when you turn it on, the model can ask to:

| Tool | What it does | Permission |
|------|--------------|------------|
| `web_search`, `web_fetch` | search the web / read a page through **your** internet connection (no API keys; DuckDuckGo, Wikipedia fallback) | Off · Ask each time · Allow this session |
| `read_file`, `list_dir` | read a text file ~6 KB at a time from any byte offset (the reply says where to continue) / list folders | Off · Ask each time · Allow this session |
| `analyze_file` | process a **large** file completely: your model reads it part by part (sized to the model's context), keeps running notes, and returns a condensed result. Slow but unlimited in file size; progress is shown and **Stop** cancels (it tells you the offset to resume from) | same as reading files |
| `write_file` | create / overwrite / append a text file | Off · Ask each time (**always asks**) |
| `run_command` | run a program (no shell, 60 s limit) | Off · Ask each time (**always asks**) |
| `system_info` | OS, CPU, RAM, disk (no user/host name) | Off · Ask each time · Allow this session |

Every request opens a window showing the exact URL / path / command / file content, with **Allow once**, **Allow for this session** (where permitted) and **Deny**. No answer within 3 minutes counts as Deny. Works with any model — tools use a plain-text `<tool_call>` protocol, no special model support needed.

Safety rules built in:
- Writing and running commands can never be "allowed for the session".
- Once the model has read local data (files, command output, system info), internet access asks again every time, so data can't be sent out silently.
- Local/private addresses (localhost, 192.168.x.x, 10.x.x.x…) always ask.
- API keys, encrypted vaults, `.ssh`, `.gnupg`, `.aws` and `.kube` can never be read or written by the agent.
- Web pages and files are labelled as untrusted data in the prompt; max 6 tool calls per answer; results are size-limited.
- Session permissions live in memory only and are cleared on restart ("Revoke session permissions" clears them immediately).

Plugins and the rest of the app are unchanged. Small local models are less reliable at tool use than large ones — if one ignores the protocol, try a larger model.

## Bigger font, free APIs and fixes

- **Bigger, adjustable font** — default is now ~15% larger. Change it in Settings → Font size (Small / Normal / Large / Extra large); "Save & restart" applies it. Plugins can use `toolbox_api.font(size)` to follow the setting.
- **New free, key-less API tools** (Dictionary, Countries, Public Holidays, Wikipedia, Books, ISS) plus keyless fallbacks for Weather, Currency and News.
- **Fixes**
  - Settings/tasks/history are written atomically, so a crash can no longer corrupt them; a damaged settings file no longer blocks startup.
  - "Next birthday" in Date & Age was computed from the wrong date; it now counts from today.
  - Calculator: `factorial()` is range-limited so a huge input can't freeze the UI.
  - Unit converter: more precise factors (lb, oz, km/h, knot, acre, ft², cup, gallon, pint, stone).
  - Bulk Rename: Preview now shows exactly what a real run does (skips clashing targets, allows case-only renames).
  - Vault: files with a tampered iteration count are rejected instead of hanging the app.
  - `requirements.txt` was empty; it now lists the dependencies.

## Features

### General & Productivity

- Quick access tools for common tasks and daily operations
- Favorite tool shortcuts
- Recently used tool tracking
- Intuitive command palette search

### System & Utilities

- OS-level system information and monitoring
- Process and resource awareness
- Hardware and environment checks
- Safe utility control for common desktop tasks

### Files & Data

- File management utilities
- Local data handling and export options
- Organized storage for task and note files

### Text & Editing

- Text manipulation helpers
- Formatting and conversion utilities
- Useful repeated text actions for developers and power users

### Security

- Local security-related utilities
- Safe operational checks for sensitive tasks
- Warning-based handling when optional security modules are unavailable

### Media

- Media helpers and file-related processing
- Tools for working with common media formats and resources

### Finance & Time

- Date/time utilities
- Financial and conversion helpers
- Local calculation and tracking features

### Developer Tools

- Code and project support tools
- Build workflow automation
- Project packaging controls
- Language detection and build orchestration

### Services & APIs

- Optional API-driven utilities such as weather, currency, translation, and other external services
- Explicitly user-initiated network access only

Free, keyless APIs (chosen from the [public-apis](https://github.com/public-apis/public-apis) list):

| Tool | API | Key |
|------|-----|-----|
| Weather (fallback) | Open-Meteo | none |
| Currency (fallback) | open.er-api.com, Frankfurter | none |
| News (fallback) | Hacker News (Firebase) | none |
| Dictionary | dictionaryapi.dev | none |
| Countries | REST Countries | none |
| Public Holidays | Nager.Date | none |
| Wikipedia | Wikipedia REST | none |
| Books | Open Library | none |
| ISS Tracker | wheretheiss.at | none |
| Fun APIs (trivia, facts, dog) | Open Trivia DB, Useless Facts, Dog CEO | none |

Optional keys (OpenWeather, NewsAPI, ipinfo, GitHub, OpenAI) are still supported in Settings.

## PolyBuild Integration

The app includes a dedicated developer section for PolyBuild Pro, a multi-language build and packaging utility powered by `polybuild.py`.

### PolyBuild Features

- Automatic detection of `polybuild.py` from the same folder or from app settings
- Automatic project language detection for Python, Java, JS/TS, C/C++, C#, Go, Rust, Kotlin, and more
- Build options including `onefile`, console mode, target OS, and backend selection per language
- Advanced configuration for `hidden-imports`, `add-data`, and freeform extra arguments
- Build tool validation for `pyinstaller`, `nuitka`, `node`, `java`, `gradle`, `gcc`, `cargo`, `flutter`, and similar tools
- Saved build presets for reusable configurations
- Build history for the most recent 100 build operations, including time, language, target, result, and duration
- Stop action for active builds
- Watchdog protection to terminate stuck builds after one hour
- Automatic output color-coding: green for success, yellow for warnings, red for errors

Set the `polybuild.py` path from Settings → PolyBuild if the app does not detect it automatically.

## Quick Start

```bash
python toolbox.py
```

## Requirements

- Python 3.9+
- Operating system: Windows, Linux, or macOS

## Dependencies

| Type | Libraries | Install |
|------|-----------|---------|
| Core | `customtkinter`, `psutil` | `pip install customtkinter psutil` |
| Optional | `requests`, `qrcode`, `Pillow`, `cryptography` | `pip install -r requirements.txt` |

Python 3.9+ is required, and the project uses `zoneinfo` and `dataclasses` where applicable.

## Local Storage

All user data is stored locally in the same folder as the app, with no cloud synchronization:

- `ultimate_toolbox_settings.json` — app settings, language, favorites, API keys
- `ultimate_toolbox_tasks.json` — task list
- `ultimate_toolbox_notes.txt` — notebook/notes
- `ultimate_toolbox_theme.json` — generated theme configuration
- `polybuild_history.json` — PolyBuild execution history

## Privacy & Security

- No cloud storage
- No tracking or analytics
- No background telemetry
- No network access unless an API tool is explicitly used
- External API tools are only used when the user intentionally invokes them

This app is designed around local-first privacy and user control.

- Backups exclude API keys (re-enter them after restoring); importing a backup can never switch on the LLM agent mode or erase existing keys.
- On Linux/macOS the settings file (which holds API keys) is created readable by you only.
- The generic HTTP tools only accept `http://` and `https://` URLs.

## Project Philosophy

Ultimate Toolbox Pro is built to be:

- fast and lightweight
- local-first and privacy respecting
- easy to extend and customize
- practical for developers and advanced users
- resilient to missing dependencies or environment differences

## Notes

This project is intended as a personal desktop productivity and developer toolkit. It emphasizes privacy, offline reliability, usability, and a minimal-friction workflow across multiple platforms.

---

To get started quickly, run the app from the project folder with Python 3.9+ and install the dependencies listed above.
