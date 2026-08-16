import os
import streamlit as st
from utils.assets import get_asset_svg_b64

def render_sidebar_footer():
    """Render a compact sidebar footer with social connect icons loaded directly from assets folder."""
    github_b64 = get_asset_svg_b64("github.svg", "#0F172A")
    linkedin_b64 = get_asset_svg_b64("linkedin.svg")
    gmail_b64 = get_asset_svg_b64("gmail.svg")

    github_icon_html = f'<img src="{github_b64}" class="sidebar-social-icon" width="16" height="16" alt="GitHub" />' if github_b64 else ''
    linkedin_icon_html = f'<img src="{linkedin_b64}" class="sidebar-social-icon" width="16" height="16" alt="LinkedIn" />' if linkedin_b64 else ''
    gmail_icon_html = f'<img src="{gmail_b64}" class="sidebar-social-icon" width="16" height="16" alt="Gmail" />' if gmail_b64 else ''

    sidebar_footer_html = f"""<div class="sidebar-footer-container">
<div class="sidebar-footer-divider"></div>

<div class="sidebar-footer-section">
    <div class="sidebar-footer-heading">ABOUT STOCKMIND</div>
    <div class="sidebar-brand-desc">
        Your AI-powered financial assistant. StockMind combines live market data, web research, and your personal documents to deliver clear stock insights.
    </div>
</div>

<div class="sidebar-footer-section">
    <div class="sidebar-footer-heading">Support & Connect</div>
    <div class="sidebar-social-links">
        <a href="https://github.com/Areeb-Ahmd" target="_blank" rel="noopener noreferrer" class="sidebar-social-link">
            {github_icon_html}
            <span>GitHub Profile</span>
        </a>
        <a href="https://www.linkedin.com/in/areeb-ahmad7" target="_blank" rel="noopener noreferrer" class="sidebar-social-link">
            {linkedin_icon_html}
            <span>LinkedIn Network</span>
        </a>
        <a href="mailto:ahmad.syedareeb7@gmail.com" class="sidebar-social-link">
            {gmail_icon_html}
            <span>Gmail Contact</span>
        </a>
    </div>
</div>

<div class="sidebar-copyright">
    <div>StockMind &copy; 2026. All rights reserved.</div>
</div>
</div>""".strip()

    if hasattr(st, "html"):
        st.html(sidebar_footer_html)
    else:
        st.markdown(sidebar_footer_html, unsafe_allow_html=True)
