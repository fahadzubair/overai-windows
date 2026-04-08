"""
main.py
CLI entry point and application bootstrap for OverAI Windows overlay.
Mirrors the macOS main.py structure: argparse for --install/--uninstall-startup,
then boots the pywebview app with tray and hotkey support.
"""

import argparse

from .constants import APP_TITLE
from .app import create_app
from .launcher import install_startup, uninstall_startup
from .health_checks import health_check_decorator
from .hotkey import setup_hotkey
from .tray import setup_tray


@health_check_decorator
def main():
    parser = argparse.ArgumentParser(
        description=f"Windows {APP_TITLE} Overlay App — AI chat overlay summoned with a keyboard shortcut."
    )
    parser.add_argument(
        "--install-startup",
        action="store_true",
        help=f"Install {APP_TITLE} to run at login",
    )
    parser.add_argument(
        "--uninstall-startup",
        action="store_true",
        help=f"Uninstall {APP_TITLE} from running at login",
    )
    args = parser.parse_args()

    if args.install_startup:
        install_startup()
        return

    if args.uninstall_startup:
        uninstall_startup()
        return

    print()
    print(f"Starting Windows {APP_TITLE} overlay.")
    print()
    print(f"To run at login, use:      python -m {APP_TITLE.lower()} --install-startup")
    print(f"To remove from login, use: python -m {APP_TITLE.lower()} --uninstall-startup")
    print()

    create_app(
        tray_setup_fn=setup_tray,
        hotkey_setup_fn=setup_hotkey,
    )


if __name__ == "__main__":
    main()
