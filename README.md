# Ultimate Toolbox Pro v3.1

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
| Optional | `requests`, `qrcode`, `Pillow` | `pip install requests qrcode[pil] Pillow` |

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
