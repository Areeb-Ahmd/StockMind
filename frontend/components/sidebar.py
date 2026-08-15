import os
import requests
import streamlit as st
from utils.assets import get_base64_image
from components.footer import render_sidebar_footer

def render_sidebar(main_logo_path: str, base_url: str):
    """Render sidebar panel with brand logo, document intelligence hub, and sidebar footer."""
    with st.sidebar:
        main_b64 = get_base64_image(main_logo_path)

        if main_b64:
            st.markdown(f"""
                <div class="sidebar-header">
                    <img src="{main_b64}" class="sidebar-logo" alt="StockMind Logo" />
                </div>
            """, unsafe_allow_html=True)
        else:
            st.title("StockMind")

        ingested_count = st.session_state.get("ingested_count", 0)

        st.markdown(f"""
            <div class="sidebar-kb-header">
                <div class="sidebar-kb-title">Document Intelligence</div>
                <div class="sidebar-kb-badge">
                    <span class="kb-badge-dot"></span> {ingested_count} Indexed
                </div>
            </div>
            <p class="sidebar-kb-desc">
                Ingest SEC 10-K/10-Q filings, earnings transcripts, or research PDFs to power vector RAG analytics.
            </p>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload Financial Documents",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Supported formats: PDF, DOCX (Max 200MB per file)",
            label_visibility="collapsed"
        )

        if st.button("Index Financial Documents", use_container_width=True, key="btn_ingest_docs"):
            if uploaded_files:
                files = []
                for f in uploaded_files:
                    file_data = f.read()
                    if not file_data:
                        continue
                    files.append(("files", (getattr(f, "name", "document.pdf"), file_data, f.type)))

                if files:
                    try:
                        with st.spinner("Processing & indexing vector embeddings..."):
                            response = requests.post(f"{base_url}/upload", files=files, timeout=60)
                            if response.status_code == 200:
                                st.session_state.ingested_count += len(files)
                                st.success(f"Successfully indexed {len(files)} document(s)")
                                st.rerun()
                            else:
                                st.error(f"Upload failed ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
                else:
                    st.warning("Selected files appear empty.")
            else:
                st.info("Select financial documents before indexing.")

        # Render Compact Executive Sidebar Footer
        render_sidebar_footer()
