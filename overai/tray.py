"""
tray.py
System tray icon and menu for OverAI on Windows.
Uses pystray for the tray icon and Pillow for the icon image.
Mirrors the macOS NSStatusBar menu functionality.
"""

import threading
import pystray
from PIL import Image, ImageDraw

from .constants import APP_TITLE, AI_SERVICES, LOGO_PATH
from .launcher import install_startup, uninstall_startup

_tray_icon = None


def _create_default_icon():
    """Generate a simple fallback icon if logo.png is missing."""
    img = Image.new("RGBA", (64, 64), (30, 41, 59, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse([12, 12, 52, 52], fill=(99, 102, 241, 255))
    draw.text((22, 18), "O", fill=(255, 255, 255))
    return img


def _load_icon():
    """Load the tray icon from logo.png or fall back to a generated one."""
    try:
        return Image.open(LOGO_PATH)
    except Exception:
        return _create_default_icon()


def setup_tray(api):
    """Build and run the system tray icon + menu in a background thread."""
    global _tray_icon

    def show(icon, item):
        api.show_window()

    def hide(icon, item):
        api.hide_window()

    def go_home(icon, item):
        api.go_home()

    def clear_cache(icon, item):
        api.clear_cache()

    def do_install(icon, item):
        install_startup()

    def do_uninstall(icon, item):
        uninstall_startup()

    def quit_app(icon, item):
        icon.stop()
        api.quit_app()

    def switch_ai_factory(name):
        def handler(icon, item):
            api.switch_ai(name)
        return handler

    ai_menu = pystray.Menu(
        *[pystray.MenuItem(name, switch_ai_factory(name)) for name in AI_SERVICES]
    )

    menu = pystray.Menu(
        pystray.MenuItem(f"Show {APP_TITLE}", show, default=True),
        pystray.MenuItem(f"Hide {APP_TITLE}", hide),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Switch AI", ai_menu),
        pystray.MenuItem("Home", go_home),
        pystray.MenuItem("Clear Web Cache", clear_cache),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Install Startup", do_install),
        pystray.MenuItem("Uninstall Startup", do_uninstall),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", quit_app),
    )

    icon_image = _load_icon()
    _tray_icon = pystray.Icon(APP_TITLE, icon_image, APP_TITLE, menu)

    tray_thread = threading.Thread(target=_tray_icon.run, daemon=True)
    tray_thread.start()
