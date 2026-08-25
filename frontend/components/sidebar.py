import os
import time
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
                        with st.status("Initiating document upload...", expanded=True) as status_box:
                            response = requests.post(f"{base_url}/upload", files=files, timeout=30)
                            if response.status_code == 202:
                                task_data = response.json()
                                task_id = task_data.get("task_id")
                                status_box.write("📁 Files uploaded to server. Processing ingestion...")

                                # Poll task status until completed or failed
                                while True:
                                    time.sleep(1.5)
                                    poll_res = requests.get(f"{base_url}/upload/status/{task_id}", timeout=10)
                                    if poll_res.status_code == 200:
                                        task_info = poll_res.json()
                                        task_status = task_info.get("status")
                                        msg = task_info.get("message", "Processing...")
                                        curr_b = task_info.get("current_batch", 0)
                                        tot_b = task_info.get("total_batches", 0)

                                        if tot_b > 0:
                                            status_box.update(label=f"Ingestion progress: Batch {curr_b}/{tot_b}", state="running")
                                            status_box.write(msg)
                                        else:
                                            status_box.update(label=msg, state="running")

                                        if task_status == "completed":
                                            status_box.update(label=f"Successfully processed {len(files)} document(s)!", state="complete", expanded=False)
                                            if "ingested_count" in st.session_state:
                                                st.session_state.ingested_count += len(files)
                                            st.success(f"Successfully uploaded and processed {len(files)} document(s)!")
                                            time.sleep(1)
                                            st.rerun()
                                            break
                                        elif task_status == "failed":
                                            err = task_info.get("error", "Unknown ingestion error")
                                            status_box.update(label="Ingestion failed", state="error", expanded=True)
                                            st.error(f"Ingestion failed: {err}")
                                            break
                                    else:
                                        status_box.update(label="Failed to fetch ingestion status", state="error")
                                        st.error(f"Status check failed ({poll_res.status_code}): {poll_res.text}")
                                        break
                            else:
                                status_box.update(label=f"Upload failed ({response.status_code})", state="error")
                                st.error(f"Upload failed ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
                else:
                    st.warning("Selected files appear empty.")
            else:
                st.info("Select research files before processing.")

        # Render Compact Executive Sidebar Footer
        render_sidebar_footer()

