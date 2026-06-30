"""
Chat Section Component.
Renders interactive Q&A chat interface card and retrieved sources card.
"""

import streamlit as st
from utils.chatbot import answer_question
from utils.retriever import retrieve_documents


def render_chat_section() -> None:
    """Render conversational chat history, input controls, and sources cards."""
    st.subheader("💬 Chat with your PDF")
    
    # Initialize chat state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "last_query" not in st.session_state:
        st.session_state["last_query"] = None

    # Top header bar for Chat section with Clear Chat button
    col_title, col_clear = st.columns([3, 1])
    with col_title:
        st.markdown("### Conversational Q&A")
    with col_clear:
        if st.session_state["chat_history"]:
            if st.button("🗑️ Clear History", key="clear_chat_btn", use_container_width=True):
                st.session_state["chat_history"] = []
                st.session_state["last_query"] = None
                st.rerun()

    # 1. Display Chat History Feed
    chat_container = st.container()
    with chat_container:
        if not st.session_state["chat_history"]:
            st.info("💡 **No message history yet.** Type a question below in the chat box and press **Enter** to receive an immediate answer preview.")
        else:
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"]):
                    if msg["role"] == "assistant":
                        st.markdown(f'<div class="ai-answer-box">\n\n{msg["content"]}\n\n</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(msg["content"])


    # 2. Native Chat Input (Modern Streamlit widget)
    prompt = st.chat_input("Ask a question about your uploaded PDF notes...")
    if prompt:
        query_text = prompt.strip()
        
        # Append user message
        st.session_state["chat_history"].append({"role": "user", "content": query_text})
        
        # Generate AI answer
        llm_model = st.session_state.get("llm_model", "gpt-4o-mini")
        ai_response = answer_question(
            query_text,
            st.session_state.get("vector_store"),
            st.session_state["chat_history"],
            model_name=llm_model,
            raw_documents=st.session_state.get("raw_documents")
        )

        
        # Append assistant message
        st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
        st.session_state["last_query"] = query_text
        
        # Rerun to update UI
        st.rerun()


    st.markdown("---")

    # 3. Context Sources & Citations Card
    st.subheader("📌 Context Sources & Citations")
    active_query = st.session_state.get("last_query")
    
    with st.container():
        if active_query:
            retrieved_sources = retrieve_documents(active_query, st.session_state.get("vector_store"))
            st.markdown(f"**Retrieved Page Sources for active query:** *\"{active_query}\"*")
            for doc in retrieved_sources:
                with st.expander(f"📄 Source: {doc['metadata']['source']} (Page {doc['metadata']['page']})"):
                    st.write(doc["page_content"])
        else:
            st.info("🔍 Retrieved document pages and reference citations will appear here after you ask a question above.")
