import os

APP_TITLE = "OverAI"
WEBSITE = "https://www.grok.com"

AI_SERVICES = {
    "Grok": "https://grok.com",
    "Gemini": "https://gemini.google.com",
    "ChatGPT": "https://chat.openai.com",
    "Claude": "https://claude.ai/chat",
    "DeepSeek": "https://chat.deepseek.com",
}

CORNER_RADIUS = 15
DRAG_AREA_HEIGHT = 30

DEFAULT_HOTKEY = "ctrl+g"

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
INDEX_HTML_PATH = os.path.join(ASSETS_DIR, "index.html")

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 580
MIN_ALPHA = 50
MAX_ALPHA = 255
ALPHA_STEP = 25
