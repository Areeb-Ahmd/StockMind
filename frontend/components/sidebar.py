import os
import requests
import streamlit as st
from components.footer import render_sidebar_footer

def render_sidebar(base_url: str):
    """Render left sidebar dedicated to document knowledge base ingestion and platform metadata."""
    with st.sidebar:
        sidebar_intro_html = """<div class="sidebar-main-heading-wrap">
<div class="sidebar-main-heading">
<span class="sidebar-heading-navy">Document</span> <span class="sidebar-heading-copper">Library</span>
</div>
<div class="sidebar-heading-accent-bar"></div>
</div>

<div class="sidebar-kb-card">
<div class="sidebar-kb-desc">
Upload trading guides, SEC filings, financial reports, research notes and other documents. StockMind will read and analyze them to answer your questions.
</div>
</div>""".strip()

        if hasattr(st, "html"):
            st.html(sidebar_intro_html)
        else:
            st.markdown(sidebar_intro_html, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload your research files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Drop PDFs or DOCX files here, or browse your computer. Maximum 200MB per file.",
            label_visibility="collapsed"
        )

        if st.button("Upload & Process", use_container_width=True, key="btn_ingest_docs"):
            if uploaded_files:
                files = []
                for f in uploaded_files:
                    file_data = f.read()
                    if not file_data:
                        continue
                    files.append(("files", (getattr(f, "name", "document.pdf"), file_data, f.type)))

                if files:
                    try:
                        with st.spinner("Uploading and processing documents..."):
                            response = requests.post(f"{base_url}/upload", files=files, timeout=60)
                            if response.status_code == 200:
                                st.session_state.ingested_count += len(files)
                                st.success(f"Successfully uploaded and processed {len(files)} document(s)!")
                                st.rerun()
                            else:
                                st.error(f"Upload failed ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
                else:
                    st.warning("Selected files appear empty.")
            else:
                st.info("Select research files before processing.")

        # Render Compact Executive Sidebar Footer
        render_sidebar_footer()

