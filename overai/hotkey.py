"""
hotkey.py
Global keyboard hotkey for toggling the OverAI overlay on Windows.
Uses the `keyboard` library for system-wide key interception.
Supports customizable hotkeys saved to %APPDATA%/overai/custom_trigger.json.
"""

import json
import keyboard

from .constants import DEFAULT_HOTKEY
from .health_checks import LOG_DIR

TRIGGER_FILE = LOG_DIR / "custom_trigger.json"
_current_hotkey = None
_hotkey_id = None


def load_custom_hotkey():
    """Load a user-defined hotkey from disk, or return the default."""
    global _current_hotkey
    if TRIGGER_FILE.exists():
        try:
            with open(TRIGGER_FILE, "r") as f:
                data = json.load(f)
            _current_hotkey = data.get("hotkey", DEFAULT_HOTKEY)
            print(f"Custom OverAI hotkey loaded: {_current_hotkey}", flush=True)
            return _current_hotkey
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to load custom hotkey: {e}. Using default.", flush=True)
    _current_hotkey = DEFAULT_HOTKEY
    return _current_hotkey


def save_custom_hotkey(hotkey_str):
    """Persist a new hotkey string to disk."""
    global _current_hotkey
    TRIGGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRIGGER_FILE, "w") as f:
        json.dump({"hotkey": hotkey_str}, f)
    _current_hotkey = hotkey_str
    print(f"New OverAI hotkey saved: {hotkey_str}", flush=True)


def register_hotkey(api):
    """Register the global hotkey that toggles the overlay."""
    global _hotkey_id, _current_hotkey
    hotkey_str = load_custom_hotkey()
    _unregister()
    try:
        _hotkey_id = keyboard.add_hotkey(hotkey_str, api.toggle_window)
        print(f"Global hotkey registered: {hotkey_str}", flush=True)
    except Exception as e:
        print(f"Failed to register hotkey '{hotkey_str}': {e}", flush=True)


def _unregister():
    """Remove the currently registered hotkey if any."""
    global _hotkey_id
    if _hotkey_id is not None:
        try:
            keyboard.remove_hotkey(_hotkey_id)
        except (KeyError, ValueError):
            pass
        _hotkey_id = None


def set_custom_hotkey(api, new_hotkey):
    """Change the hotkey at runtime: unregister old, save, register new."""
    save_custom_hotkey(new_hotkey)
    register_hotkey(api)


def setup_hotkey(api):
    """Entry point called from main to wire up the global hotkey."""
    register_hotkey(api)
