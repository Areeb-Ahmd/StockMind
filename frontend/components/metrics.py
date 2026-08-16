import os
import streamlit as st
from utils.assets import get_base64_image

def render_metrics_and_chips() -> str:
    """Render authentic financial intelligence intro dashboard card based on StockMind architecture."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    polygon_logo_path = os.path.join(assets_dir, "Polygon.io.jpeg")
    polygon_b64 = get_base64_image(polygon_logo_path)
    polygon_icon_html = f'<img src="{polygon_b64}" class="pillar-img-icon" alt="Polygon.io Logo" />' if polygon_b64 else '📊'

    pinecone_logo_path = os.path.join(assets_dir, "pinecone.svg")
    pinecone_b64 = get_base64_image(pinecone_logo_path)
    pinecone_icon_html = f'<img src="{pinecone_b64}" class="pillar-img-icon" alt="Pinecone Logo" />' if pinecone_b64 else '📁'

    tavily_logo_path = os.path.join(assets_dir, "tavily.svg")
    tavily_b64 = get_base64_image(tavily_logo_path)
    tavily_icon_html = f'<img src="{tavily_b64}" class="pillar-img-icon" alt="Tavily Logo" />' if tavily_b64 else '🌐'

    hero_html = f"""<div class="hero-intro-card">
<div class="hero-intro-header">
<h2 class="hero-title">Your AI Financial Research Assistant</h2>
<p class="hero-subtitle">Ask questions about stocks, companies, markets, financial reports, or your uploaded research.</p>
</div>
<div class="hero-pillars-grid">
<div class="hero-pillar-card">
<div class="pillar-icon">{polygon_icon_html}</div>
<div class="pillar-content">
<div class="pillar-title">Company Financials</div>
<div class="pillar-desc">Review revenue, earnings, balance sheets, cash flow, and other key metrics to understand a company's financial performance. Powered by Polygon.io.</div>
</div>
</div>
<div class="hero-pillar-card">
<div class="pillar-icon">{pinecone_icon_html}</div>
<div class="pillar-content">
<div class="pillar-title">Document Analysis</div>
<div class="pillar-desc">Analyze your uploaded reports, filings, and research documents to find financial metrics, key insights, risks, and important details. Powered by Pinecone.</div>
</div>
</div>
<div class="hero-pillar-card">
<div class="pillar-icon">{tavily_icon_html}</div>
<div class="pillar-content">
<div class="pillar-title">Live Web Search</div>
<div class="pillar-desc">Stay up to date with the latest market news, company updates, sector trends, and economic developments. Powered by Tavily.</div>
</div>
</div>
</div>
</div>""".strip()

    if hasattr(st, "html"):
        st.html(hero_html)
    else:
        st.markdown(hero_html, unsafe_allow_html=True)

    return None
