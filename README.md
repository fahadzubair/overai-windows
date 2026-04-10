# OverAI for Windows

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D6.svg)](https://www.microsoft.com/windows)

A sleek, always-on-top Windows overlay that brings AI chat services (Grok, ChatGPT, Claude, Gemini, DeepSeek) directly to your desktop.

## Features

- **Floating overlay** - frameless, always-on-top window with adjustable transparency
- **Hidden from screen share** - invisible in Zoom, Teams, Meet, and other screen-sharing tools
- **AI service switching** - switch between Grok, ChatGPT, Claude, Gemini, and DeepSeek via dropdown
- **Global hotkey** - toggle visibility with Ctrl+G (customizable)
- **System tray** - access all controls from the Windows system tray
- **Launch at login** - optional auto-start via Windows Registry
- **Crash protection** - built-in crash loop detection and error logging

## Architecture

```
overai/
├── main.py           # CLI entry point and argparse bootstrap
├── app.py            # Core window logic, Win32 API, JS toolbar injection
├── constants.py      # App-wide constants (AI URLs, dimensions, hotkeys)
├── hotkey.py         # Global keyboard shortcut registration
├── tray.py           # System tray icon and context menu
├── launcher.py       # Windows Registry startup install/uninstall
├── health_checks.py  # Crash loop detection and error logging
├── logger.py         # Centralized rotating file logger
├── assets/
│   └── index.html    # Loading screen UI
└── about/
    ├── version.txt
    ├── author.txt
    └── description.txt
```

## Requirements

- Windows 10 (version 2004+) or Windows 11
- Python 3.9+
- Edge WebView2 Runtime (pre-installed on modern Windows)

## Installation

```bash
# Clone the repository
git clone https://github.com/fahadzubair/overai-windows.git
cd overai-windows

# Install dependencies
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install .
```

## Usage

```bash
python -m overai
```

### CLI Options

```bash
python -m overai --install-startup    # Run at login
python -m overai --uninstall-startup  # Remove from login
```

## Controls

| Action | Method |
|--------|--------|
| Show/Hide | Ctrl+G (or custom hotkey) |
| Switch AI | Dropdown in title bar |
| Transparency | +/- buttons in title bar |
| Move window | Drag the title bar |
| All options | Right-click system tray icon |

## Supported AI Services

| Service | URL |
|---------|-----|
| Grok | grok.com |
| Gemini | gemini.google.com |
| ChatGPT | chat.openai.com |
| Claude | claude.ai |
| DeepSeek | chat.deepseek.com |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'feat: add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
