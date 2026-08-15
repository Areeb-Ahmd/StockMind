import os
import streamlit as st
from utils.assets import get_base64_image

def render_sidebar_footer():
    """Render a compact, executive sidebar footer with product description, tech stack badges, developer social links, and copyright info."""
    sidebar_footer_html = """<div class="sidebar-footer-container">
<div class="sidebar-footer-divider"></div>

<div class="sidebar-footer-section">
    <div class="sidebar-brand-desc">
        Next-generation agentic stock market intelligence platform powered by real-time RAG, quantitative market models, and autonomous AI analytics.
    </div>
</div>

<div class="sidebar-footer-section">
    <div class="sidebar-footer-heading">Platform Tech Stack</div>
    <div class="sidebar-tech-tags">
        <span class="tech-tag">⚡ FastAPI</span>
        <span class="tech-tag">🤖 Vector RAG</span>
        <span class="tech-tag">📊 Streamlit</span>
        <span class="tech-tag">🐍 Python 3.11</span>
    </div>
</div>

<div class="sidebar-footer-section">
    <div class="sidebar-footer-heading">Support & Developer</div>
    <div class="sidebar-social-links">
        <a href="https://github.com/Areeb-Ahmd" target="_blank" rel="noopener noreferrer" class="sidebar-social-link">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            <span>GitHub Profile</span>
        </a>
        <a href="https://www.linkedin.com/in/areeb-ahmad7" target="_blank" rel="noopener noreferrer" class="sidebar-social-link">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="#0A66C2"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
            <span>LinkedIn Network</span>
        </a>
        <a href="mailto:ahmad.syedareeb7@gmail.com" class="sidebar-social-link">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="#EA4335"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
            <span>Gmail Contact</span>
        </a>
    </div>
</div>

<div class="sidebar-copyright">
    <div>StockMind &copy; 2026 Syed Areeb Ahmad</div>
    <div class="sidebar-ver">v2.4.0-prod</div>
</div>
</div>""".strip()

    if hasattr(st, "html"):
        st.html(sidebar_footer_html)
    else:
        st.markdown(sidebar_footer_html, unsafe_allow_html=True)
