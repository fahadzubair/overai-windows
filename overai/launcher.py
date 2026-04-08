"""
launcher.py
Startup/login utilities for OverAI on Windows.
Uses the Windows Registry (HKCU\\...\\Run) to install/uninstall auto-launch,
replacing the macOS LaunchAgent approach.
"""

import os
import sys
import winreg

from .constants import APP_TITLE

REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
REGISTRY_VALUE_NAME = APP_TITLE


def get_executable():
    """Return the command that launches OverAI (frozen exe or python -m)."""
    if getattr(sys, "frozen", False):
        return sys.executable
    return f'"{sys.executable}" -m {APP_TITLE.lower()}'


def install_startup():
    """Add OverAI to Windows login startup via the Registry."""
    try:
        cmd = get_executable()
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, REGISTRY_VALUE_NAME, 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)
        print(f"OverAI installed as startup app (Registry: HKCU\\{REGISTRY_KEY}\\{REGISTRY_VALUE_NAME}).")
        return True
    except Exception as e:
        print(f"Failed to install startup: {e}")
        return False


def uninstall_startup():
    """Remove OverAI from Windows login startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, REGISTRY_VALUE_NAME)
        winreg.CloseKey(key)
        print("OverAI removed from startup.")
        return True
    except FileNotFoundError:
        print("OverAI is not in startup. Nothing to uninstall.")
        return False
    except Exception as e:
        print(f"Failed to uninstall startup: {e}")
        return False


def is_startup_installed():
    """Check if OverAI is currently registered as a startup app."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_READ
        )
        winreg.QueryValueEx(key, REGISTRY_VALUE_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False
