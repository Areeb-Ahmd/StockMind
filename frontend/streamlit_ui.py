import os
import sys
import streamlit as st

# Add current directory to path for clean modular component imports
sys.path.insert(0, os.path.dirname(__file__))

from utils.assets import load_theme_css
from components.sidebar import render_sidebar
from components.header import render_header
from components.metrics import render_metrics_and_chips
from components.chat import render_chat_interface

# 1. Environment & Asset Paths
BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8080").rstrip("/")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

CHATBOT_LOGO_PATH = os.path.join(ASSETS_DIR, "chatbot_logo.png")

# 2. Streamlit Page Config
st.set_page_config(
    page_title="StockMind – Agentic Stock Market Assistant",
    page_icon=CHATBOT_LOGO_PATH if os.path.exists(CHATBOT_LOGO_PATH) else "📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 3. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ingested_count" not in st.session_state:
    st.session_state.ingested_count = 0

# 4. Load Light Theme Stylesheet from frontend/static/css/theme.css
load_theme_css()

# 5. Render Modular Layout Components
render_sidebar(BASE_URL)
render_header(CHATBOT_LOGO_PATH)
prompt_from_chip = render_metrics_and_chips()
render_chat_interface(CHATBOT_LOGO_PATH, BASE_URL, prompt_from_chip)