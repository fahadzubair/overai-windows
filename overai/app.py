"""
app.py
Core window and UI logic for OverAI Windows overlay.

Uses pywebview for the WebView2-based window. Loads AI sites directly and
injects an HTML overlay toolbar (drag bar, AI selector, transparency controls)
into each page via JavaScript — mirroring how the macOS version layers native
AppKit controls on top of WKWebView.
"""

import ctypes
import ctypes.wintypes
import webview

from .constants import (
    AI_SERVICES,
    APP_TITLE,
    CORNER_RADIUS,
    DRAG_AREA_HEIGHT,
    MIN_ALPHA,
    MAX_ALPHA,
    ALPHA_STEP,
    WEBSITE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)

# Win32 constants
WDA_EXCLUDEFROMCAPTURE = 0x11
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x02
WM_NCLBUTTONDOWN = 0x00A1
HTCAPTION = 0x0002

user32 = ctypes.windll.user32
SetWindowLongPtrW = user32.SetWindowLongPtrW
GetWindowLongPtrW = user32.GetWindowLongPtrW
SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity

# JavaScript/HTML/CSS injected into every loaded page to create the toolbar overlay.
# This replicates the macOS drag bar + controls but in pure web tech.
TOOLBAR_JS = r"""
(function() {
    if (document.getElementById('overai-toolbar')) return;

    var bar = document.createElement('div');
    bar.id = 'overai-toolbar';
    bar.innerHTML = `
        <button id="overai-close" class="overai-btn" title="Hide">&#x2715;</button>
        <select id="overai-selector">
            <option value="Grok">Grok</option>
            <option value="Gemini">Gemini</option>
            <option value="ChatGPT">ChatGPT</option>
            <option value="Claude">Claude</option>
            <option value="DeepSeek">DeepSeek</option>
        </select>
        <div style="flex:1"></div>
        <button id="overai-dec" class="overai-btn" title="Less opaque">&#x2212;</button>
        <button id="overai-inc" class="overai-btn" title="More opaque">&#x2b;</button>
    `;

    var style = document.createElement('style');
    style.textContent = `
        #overai-toolbar {
            position: fixed; top: 0; left: 0; right: 0;
            height: """ + str(DRAG_AREA_HEIGHT) + r"""px;
            display: flex; align-items: center; padding: 0 6px;
            background: #1e293b; z-index: 2147483647;
            user-select: none; cursor: grab;
            border-radius: """ + str(CORNER_RADIUS) + r"""px """ + str(CORNER_RADIUS) + r"""px 0 0;
            font-family: 'Segoe UI', sans-serif;
        }
        #overai-toolbar:active { cursor: grabbing; }
        #overai-toolbar .overai-btn {
            width: 22px; height: 22px; border: none; border-radius: 50%;
            cursor: pointer; display: flex; align-items: center;
            justify-content: center; font-size: 12px; font-weight: bold;
            color: #e2e8f0; background: rgba(255,255,255,0.12);
        }
        #overai-toolbar .overai-btn:hover { background: rgba(255,255,255,0.25); }
        #overai-toolbar #overai-close { margin-right: 6px; }
        #overai-toolbar #overai-selector {
            height: 22px; border: none; border-radius: 4px;
            background: rgba(255,255,255,0.12); color: #e2e8f0;
            font-size: 12px; padding: 0 6px; cursor: pointer; outline: none;
        }
        #overai-toolbar #overai-selector option { background: #1e293b; color: #e2e8f0; }
        body { margin-top: """ + str(DRAG_AREA_HEIGHT) + r"""px !important; }
    `;
    document.head.appendChild(style);
    document.body.appendChild(bar);

    // Dragging via Win32 SendMessage trick
    bar.addEventListener('mousedown', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.tagName === 'SELECT') return;
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.start_drag();
        }
    });

    document.getElementById('overai-close').addEventListener('click', function() {
        if (window.pywebview && window.pywebview.api) window.pywebview.api.hide_window();
    });
    document.getElementById('overai-selector').addEventListener('change', function(e) {
        if (window.pywebview && window.pywebview.api) window.pywebview.api.switch_ai(e.target.value);
    });
    document.getElementById('overai-dec').addEventListener('click', function() {
        if (window.pywebview && window.pywebview.api) window.pywebview.api.decrease_transparency();
    });
    document.getElementById('overai-inc').addEventListener('click', function() {
        if (window.pywebview && window.pywebview.api) window.pywebview.api.increase_transparency();
    });

    // Sync the dropdown to the current AI service
    var currentUrl = window.location.href;
    var sel = document.getElementById('overai-selector');
    var services = {SERVICES_JSON};
    for (var name in services) {
        if (currentUrl.indexOf(new URL(services[name]).hostname) !== -1) {
            sel.value = name;
            break;
        }
    }
})();
"""

import json
TOOLBAR_INJECT = TOOLBAR_JS.replace("{SERVICES_JSON}", json.dumps(AI_SERVICES))


class Api:
    """Python API exposed to JavaScript via pywebview's JS bridge."""

    def __init__(self) -> None:
        self.window: object | None = None
        self._hwnd: int | None = None
        self._alpha: int = MAX_ALPHA
        self._visible: bool = True

    def set_window(self, window: object) -> None:
        self.window = window

    def _get_hwnd(self) -> int | None:
        if self._hwnd is None and self.window:
            try:
                self._hwnd = self.window.hwnd
            except AttributeError:
                self._hwnd = user32.FindWindowW(None, self.window.title)
        return self._hwnd

    def hide_window(self) -> None:
        if self.window:
            self.window.hide()
            self._visible = False

    def show_window(self) -> None:
        if self.window:
            self.window.show()
            self.window.on_top = True
            self._visible = True

    def toggle_window(self) -> None:
        if self.window:
            if self._visible:
                self.hide_window()
            else:
                self.show_window()

    def switch_ai(self, name: str) -> None:
        url = AI_SERVICES.get(name)
        if url and self.window:
            self.window.load_url(url)

    def increase_transparency(self) -> None:
        """Make window MORE opaque (less transparent)."""
        self._alpha = min(self._alpha + ALPHA_STEP, MAX_ALPHA)
        self._apply_alpha()

    def decrease_transparency(self) -> None:
        """Make window LESS opaque (more transparent)."""
        self._alpha = max(self._alpha - ALPHA_STEP, MIN_ALPHA)
        self._apply_alpha()

    def _apply_alpha(self) -> None:
        hwnd = self._get_hwnd()
        if hwnd:
            ex_style = GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
            SetWindowLongPtrW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)
            SetLayeredWindowAttributes(hwnd, 0, self._alpha, LWA_ALPHA)

    def start_drag(self) -> None:
        """Initiate Win32 window drag from the injected toolbar."""
        hwnd = self._get_hwnd()
        if hwnd:
            user32.ReleaseCapture()
            user32.SendMessageW(hwnd, WM_NCLBUTTONDOWN, HTCAPTION, 0)

    def quit_app(self) -> None:
        if self.window:
            self.window.destroy()

    def go_home(self) -> None:
        if self.window:
            self.window.load_url(WEBSITE)

    def clear_cache(self) -> None:
        if self.window:
            self.window.evaluate_js("""
                if (caches) {
                    caches.keys().then(function(names) {
                        names.forEach(function(name) { caches.delete(name); });
                    });
                }
            """)


def _setup_window(window: object, api: Api) -> None:
    """Called once the window is shown; applies Win32 tweaks and injects toolbar."""
    api.set_window(window)
    hwnd = api._get_hwnd()
    if hwnd:
        SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
    _inject_toolbar(window)


def _inject_toolbar(window: object) -> None:
    """Inject the floating toolbar overlay into the current page."""
    try:
        window.evaluate_js(TOOLBAR_INJECT)
    except Exception:
        pass


def _on_loaded(window: object) -> None:
    """Re-inject toolbar every time a new page loads."""
    _inject_toolbar(window)


def create_app(tray_setup_fn: callable | None = None, hotkey_setup_fn: callable | None = None) -> None:
    """
    Create and run the OverAI overlay window.
    tray_setup_fn and hotkey_setup_fn are optional callables that receive the Api
    instance for wiring up system tray and global hotkeys.
    """
    api = Api()

    window = webview.create_window(
        APP_TITLE,
        url=WEBSITE,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        frameless=True,
        on_top=True,
        js_api=api,
    )

    window.events.loaded += lambda: _on_loaded(window)

    _initialized = [False]

    def _on_shown():
        if _initialized[0]:
            return
        _initialized[0] = True
        _setup_window(window, api)
        if tray_setup_fn:
            tray_setup_fn(api)
        if hotkey_setup_fn:
            hotkey_setup_fn(api)

    window.events.shown += _on_shown

    webview.start()
