import streamlit as st

def render_metrics_and_chips() -> str:
    """Render modern financial analysis hub and quick action prompt chips."""
    
    # Financial Intelligence Hero Banner
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">Financial Intelligence & Research Hub</div>
            <div class="hero-subtitle">Analyze market trends, company earnings, sector momentum, or ingested financial documents.</div>
        </div>
    """, unsafe_allow_html=True)

    # Clean Quick Action Prompt Chips
    st.markdown('<div class="chip-section-title">Recommended Analyses</div>', unsafe_allow_html=True)
    
    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)

    prompt_selected = None

    with chip_col1:
        if st.button("NIFTY 50 Benchmark", use_container_width=True):
            prompt_selected = "Provide a comprehensive market analysis and outlook for NIFTY 50."
    with chip_col2:
        if st.button("Sector Momentum & Leaders", use_container_width=True):
            prompt_selected = "What are the top performing stock sectors right now and key growth drivers?"
    with chip_col3:
        if st.button("Earnings & Report Summary", use_container_width=True):
            prompt_selected = "Summarize key findings, risks, and financial metrics from the ingested document reports."
    with chip_col4:
        if st.button("Portfolio Risk Strategy", use_container_width=True):
            prompt_selected = "Explain key risk management strategies for stock portfolio allocation."

    return prompt_selected
