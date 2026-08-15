import os
import base64
import streamlit as st

def get_base64_image(image_path: str) -> str:
    """Convert an image file to base64 string for HTML embedding."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    return ""

def load_theme_css():
    """Load theme.css stylesheet for the StockMind Light Theme."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "css", "theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
