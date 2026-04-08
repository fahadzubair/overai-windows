# OverAI for Windows

A sleek, always-on-top Windows overlay that brings AI chat services (Grok, ChatGPT, Claude, Gemini, DeepSeek) directly to your desktop.

## Features

- **Floating overlay** — frameless, always-on-top window with adjustable transparency
- **Hidden from screen share** — invisible in Zoom, Teams, Meet, and other screen-sharing tools
- **AI service switching** — switch between Grok, ChatGPT, Claude, Gemini, and DeepSeek via dropdown
- **Global hotkey** — toggle visibility with Ctrl+G (customizable)
- **System tray** — access all controls from the Windows system tray
- **Launch at login** — optional auto-start via Windows Registry

## Requirements

- Windows 10 (version 2004+) or Windows 11
- Python 3.9+
- Edge WebView2 Runtime (pre-installed on modern Windows)

## Installation

```bash
pip install -r requirements.txt
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
