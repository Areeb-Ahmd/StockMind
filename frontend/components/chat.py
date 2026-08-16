import os
import requests
import streamlit as st

def render_chat_interface(chatbot_logo_path: str, base_url: str, prompt_from_chip: str = None):
    """Render a modern AI chat stream where messages scroll inside the viewport and chat_input stays fixed at the bottom."""
    avatar_assistant = chatbot_logo_path if os.path.exists(chatbot_logo_path) else "🤖"

    prompt_from_starter = None

    # 1. Render Permanent Research Canvas & 4 Interactive Capability Starter Cards in ONE Outer Card
    canvas_container = st.container()
    with canvas_container:
        empty_state_html = """<div class="chat-canvas-anchor"></div>
<div class="empty-canvas-header">
<div class="empty-canvas-title">What would you like to research today?</div>
<div class="empty-canvas-desc">Ask about a company, stock, market trend, financial report, or anything in your research library.</div>
</div>""".strip()

        if hasattr(st, "html"):
            st.html(empty_state_html)
        else:
            st.markdown(empty_state_html, unsafe_allow_html=True)

        # 4 Interactive Capability Starter Sub-Cards
        starter_col1, starter_col2 = st.columns(2)
        with starter_col1:
            if st.button(":material/trending_up: What's the current market sentiment, and what is driving the NIFTY 50 right now?", use_container_width=True, key="starter_btn_1"):
                prompt_from_starter = "What's the current market sentiment, and what is driving the NIFTY 50 right now?"
            if st.button(":material/description: Summarize the key risk factors and earnings highlights from my uploaded files.", use_container_width=True, key="starter_btn_2"):
                prompt_from_starter = "Summarize the key risk factors and earnings highlights from my uploaded files."
        with starter_col2:
            if st.button(":material/bar_chart: Analyze Apple's latest financial statements and evaluate its overall financial health.", use_container_width=True, key="starter_btn_3"):
                prompt_from_starter = "Analyze Apple's latest financial statements and evaluate its overall financial health."
            if st.button(":material/language: Can you search for real-time market trends and top-performing sectors?", use_container_width=True, key="starter_btn_4"):
                prompt_from_starter = "Can you search for real-time market trends and top-performing sectors?"

    # 2. Render Active Conversation Stream underneath starter cards
    if st.session_state.messages:
        for message in st.session_state.messages:
            avatar = ":material/person_pin:" if message["role"] == "user" else avatar_assistant
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # 2. Fixed Bottom Chat Input Control
    user_input = st.chat_input("Ask about a stock, company, market, or your uploaded documents...")

    # 3. Process Active Query (from st.chat_input, prompt chip, or empty state starter card)
    active_query = user_input or prompt_from_chip or prompt_from_starter

    if active_query:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": active_query})

        # Render User Message immediately
        with st.chat_message("user", avatar=":material/account_circle:"):
            st.markdown(active_query)

        # Generate Assistant Response & Append to session state
        with st.chat_message("assistant", avatar=avatar_assistant):
            with st.spinner("StockMind AI analyzing market data & research documents..."):
                try:
                    res = requests.post(f"{base_url}/query", json={"question": active_query}, timeout=90)
                    if res.status_code == 200:
                        answer = res.json().get("answer", "No response content returned.")
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        err_msg = f"❌ Backend query error ({res.status_code}): {res.text}"
                        st.error(err_msg)
                        st.session_state.messages.append({"role": "assistant", "content": err_msg})
                except Exception as e:
                    err_msg = f"❌ Error connecting to backend server at `{base_url}`: {e}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})

        # Rerun script to render clean updated message sequence
        st.rerun()
