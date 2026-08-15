import os
import sys
import streamlit as st
import requests

# Backend endpoint (dynamically loaded from environment variable, fallback to localhost:8080)
BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8080").rstrip("/")

st.set_page_config(
    page_title="StockMind – Agentic Stock Market Assistant",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("📈 StockMind – Agentic Stock Market Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: Upload documents
with st.sidebar:
    st.header("📄 Upload Documents")
    st.markdown("Upload **stock market PDFs or DOCX** to create knowledge base.")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Upload and Ingest"):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                file_data = f.read()
                if not file_data:
                    continue
                files.append(("files", (getattr(f, "name", "file.pdf"), file_data, f.type)))

            if files:
                try:
                    with st.spinner("Uploading and processing files..."):
                        response = requests.post(f"{BASE_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success("✅ Files uploaded and processed successfully!")
                        else:
                            st.error("❌ Upload failed: " + response.text)
                except Exception as e:
                    st.error(f"❌ Error connecting to backend: {e}")
            else:
                st.warning("Some files were empty or unreadable.")

# Display chat history using native Streamlit chat bubbles
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bottom chat input
if prompt := st.chat_input("Ask StockMind a question (e.g. Tell me about NIFTY 50)..."):
    # Append and render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BASE_URL}/query", json={"question": prompt})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("❌ Bot failed to respond: " + response.text)
            except Exception as e:
                st.error(f"❌ Error connecting to backend: {e}")