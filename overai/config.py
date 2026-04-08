"""
config.py
Persistent user settings manager for OverAI Windows overlay.
Stores preferences as JSON in %APPDATA%/overai/config.json.
"""

import json
from pathlib import Path
from typing import Any

from .health_checks import LOG_DIR

CONFIG_FILE = LOG_DIR / "config.json"

_DEFAULTS: dict[str, Any] = {
    "default_ai": "Grok",
    "hotkey": "ctrl+g",
    "transparency": 255,
    "window_width": 550,
    "window_height": 580,
    "start_minimized": False,
    "launch_at_login": False,
}


class Config:
    """Read/write user preferences backed by a JSON file."""

    def __init__(self, path: Path = CONFIG_FILE) -> None:
        self._path = path
        self._data: dict[str, Any] = dict(_DEFAULTS)
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                self._data.update(stored)
            except (json.JSONDecodeError, OSError):
                pass

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    def reset(self) -> None:
        """Restore all settings to defaults."""
        self._data = dict(_DEFAULTS)
        self.save()

    @property
    def default_ai(self) -> str:
        return self._data["default_ai"]

    @default_ai.setter
    def default_ai(self, value: str) -> None:
        self.set("default_ai", value)

    @property
    def transparency(self) -> int:
        return self._data["transparency"]

    @transparency.setter
    def transparency(self, value: int) -> None:
        self.set("transparency", max(50, min(255, value)))

    def __repr__(self) -> str:
        return f"Config({self._data})"
