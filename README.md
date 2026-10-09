# Ultimate Toolbox Pro v3.1

A comprehensive desktop toolbox for Windows, Linux, and macOS.

## ✨ Features

- 50+ tools distributed across 11 categories: General, System, Files, Text, Security, Media, Finance & Time, Productivity, Developer, Services, and Data.
- Complete support for 10 languages with RTL compatibility (Arabic, English, Chinese, Hindi, Spanish, French, Bengali, Portuguese, Russian, and Urdu).
- True black/red themed UI generated from a JSON color theme using `ctk.set_default_color_theme()`, with both light and dark modes.
- Fully offline operation — no network access unless APIs are explicitly used, and no tracking or analytics.
- Quick command palette (`Ctrl+K`), favorites, and recent tool history.
- Full crash protection: any optional missing library shows a clear message instead of crashing the app.

## 🏗️ PolyBuild Integration

The app includes a dedicated Developer section to control PolyBuild Pro — a multi-language build and packaging tool (`polybuild.py`).

- Automatic detection of the `polybuild.py` script from the same folder or from settings.
- Automatic project language detection (Python, Java, JS/TS, C/C++, C#, Go, Rust, Kotlin, etc.).
- Build options: `onefile`, console mode, target OS, and backend selection per language.
- Advanced options: `hidden-imports`, `add-data`, and freeform extra arguments.
- Check Build Tools: instant verification of available build tools (`pyinstaller`, `nuitka`, `node`, `java`, `gradle`, `gcc`, `cargo`, `flutter`, etc.).
- Build Presets: save, load, and delete reusable build settings.
- Build History: track the last 100 build operations (time, language, target, exit result, duration).
- Stop button to cancel an active build, with a watchdog that kills any process exceeding one hour.
- Automatic color-coding for build output (green for success, yellow for warning, red for error).

Set the `polybuild.py` path from Settings → PolyBuild if it is not detected automatically.

## 🚀 Running the App

```bash
python toolbox.py
```

## 📦 Dependencies

| Type | Libraries | Install |
|------|-----------|---------|
| Core | `customtkinter`, `psutil` | `pip install customtkinter psutil` |
| Optional | `requests`, `qrcode`, `Pillow` | `pip install requests qrcode[pil] Pillow` |

Python 3.9+ is required (the app uses `zoneinfo` and `dataclasses`).

## 📁 Local Storage

All data is saved in the same folder as the application, with no cloud sync:

- `ultimate_toolbox_settings.json` — settings, language, favorites, API keys
- `ultimate_toolbox_tasks.json` — task list
- `ultimate_toolbox_notes.txt` — notes
- `ultimate_toolbox_theme.json` — generated color theme file
- `polybuild_history.json` — PolyBuild history log

## 🔒 Privacy

- No cloud storage.
- No tracking or analytics.
- No network access unless APIs are explicitly used from the Services section (weather, currency, translation, etc.). These tools only connect when used intentionally.
- No telemetry or background reporting.

## ⚙️ Project Philosophy

Ultimate Toolbox Pro is designed to be:

- fast and lightweight
- fully local-first
- easy to extend
- practical for both power users and developers
- resilient to missing dependencies and environment differences

## 🧩 Notes

This project is built as a personal desktop productivity and developer toolkit. It emphasizes privacy, offline reliability, and usability across multiple platforms.

---

To get started quickly, run the app from the project folder with Python 3.9+ and install the required dependencies listed above.
