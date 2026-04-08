# Changelog

All notable changes to OverAI for Windows will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-07

### Added

- Frameless, always-on-top overlay window using pywebview + Edge WebView2
- AI service switching between Grok, ChatGPT, Claude, Gemini, and DeepSeek
- Injected HTML/CSS/JS toolbar overlay with drag, close, selector, and transparency controls
- Global hotkey (Ctrl+G) for toggling overlay visibility via `keyboard` library
- Customizable hotkey persistence to `%APPDATA%/overai/custom_trigger.json`
- System tray icon and context menu via `pystray`
- Window hidden from screen capture using `SetWindowDisplayAffinity`
- Adjustable window transparency via Win32 `SetLayeredWindowAttributes`
- Windows Registry startup install/uninstall (`HKCU\...\Run`)
- Crash loop detection with counter file and configurable threshold
- Error logging to `%APPDATA%/overai/overai_error_log.txt`
- Centralized rotating file logger (`overai/logger.py`)
- `pyproject.toml` for PEP 621 packaging with console script entry point
- MIT License
