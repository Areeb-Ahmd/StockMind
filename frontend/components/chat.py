import os
import requests
import streamlit as st

def render_chat_interface(chatbot_logo_path: str, extra_logo_path: str, base_url: str, prompt_from_chip: str = None):
    """Render a modern AI chat stream where messages scroll inside the viewport and chat_input stays fixed at the bottom."""
    avatar_assistant = chatbot_logo_path if os.path.exists(chatbot_logo_path) else "🤖"

    # 1. Render All Conversation Messages
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else avatar_assistant
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # 2. Fixed Bottom Chat Input Control
    user_input = st.chat_input("Ask StockMind financial analysis, stock insights, or document queries...")

    # 3. Process Active Query (from st.chat_input or prompt chip)
    active_query = user_input or prompt_from_chip

    if active_query:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": active_query})

        # Render User Message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_query)

        # Generate Assistant Response & Append to session state
        with st.chat_message("assistant", avatar=avatar_assistant):
            with st.spinner("StockMind AI analyzing market data & knowledge base..."):
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
