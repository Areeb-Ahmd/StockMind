import os
import base64
import streamlit as st

def get_base64_image(image_path: str) -> str:
    """Convert an image file to base64 string for HTML embedding (supports PNG, SVG, JPEG)."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            ext = os.path.splitext(image_path)[1].lower().replace(".", "")
            if ext == "svg":
                mime_type = "image/svg+xml"
            elif ext in ["jpg", "jpeg"]:
                mime_type = "image/jpeg"
            else:
                mime_type = f"image/{ext}"
            return f"data:{mime_type};base64,{base64.b64encode(data).decode()}"
    return ""

def get_asset_svg_b64(filename: str, fill_color: str = None) -> str:
    """Load an SVG icon from frontend/assets, ensure width/height & fill, and convert to base64 data URI."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    file_path = os.path.join(assets_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            svg = f.read().strip()
            if 'width=' not in svg:
                svg = svg.replace('<svg ', '<svg width="24" height="24" ', 1)
            if fill_color and 'fill=' not in svg and 'style=' not in svg:
                svg = svg.replace('<path ', f'<path fill="{fill_color}" ', 1)
            b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    return ""

def load_theme_css():
    """Load theme.css stylesheet for the StockMind Light Theme."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "css", "theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

