import os
import streamlit as st
from utils.assets import get_base64_image

def render_header(chatbot_logo_path: str):
    """Render main top heading featuring chatbot logo icon alongside StockMind brand typography."""
    icon_b64 = get_base64_image(chatbot_logo_path)
    icon_html = f'<img src="{icon_b64}" class="main-heading-icon" alt="StockMind Icon" />' if icon_b64 else '📈'

    header_html = f"""<div class="main-page-heading">
    {icon_html}
    <div class="main-heading-brand">
        <div class="main-brand-title">
            <span class="brand-text-navy">Stock</span><span class="brand-text-copper">Mind</span>
        </div>
        <div class="main-brand-tagline">AGENTIC STOCK MARKET ASSISTANT</div>
    </div>
</div>""".strip()

    if hasattr(st, "html"):
        st.html(header_html)
    else:
        st.markdown(header_html, unsafe_allow_html=True)
