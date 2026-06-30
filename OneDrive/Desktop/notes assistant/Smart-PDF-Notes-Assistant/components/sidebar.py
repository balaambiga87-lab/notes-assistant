"""
Sidebar Component.
Renders the Streamlit sidebar containing application title, description, status indicators, and future settings.
"""

import streamlit as st


def render_sidebar() -> None:
    """Render application sidebar elements."""
    with st.sidebar:
        st.title("📚 PDF Assistant")
        st.markdown(
            "Welcome to **Smart PDF Notes Assistant**! Upload your PDF study materials to generate smart summaries "
            "and ask instant questions."
        )

        st.divider()

        # Upload status placeholder
        st.subheader("📊 Document Status")
        status = st.session_state.get("upload_status", "No document uploaded")
        if status == "Ready":
            st.success("📄 Document loaded & indexed")
        elif status == "Processing":
            st.warning("⏳ Processing document...")
        else:
            st.info("ℹ️ Waiting for PDF upload...")

        st.divider()

        # AI Mode & Engine Selection Section
        st.subheader("🤖 AI Engine Mode")
        st.session_state["ai_mode"] = st.radio(
            "Select Processing Mode:",
            ["⚡ Free Local Engine (No API Key Required)", "🔑 OpenAI API (Paid Key)"],
            index=0 if st.session_state.get("ai_mode", "").startswith("⚡") else (1 if st.session_state.get("ai_mode", "").startswith("🔑") else 0),
            help="Free mode processes and answers questions directly from your PDF without requiring any paid API key or billing."
        )

        st.divider()

        # Advanced settings section
        with st.expander("⚙️ Advanced Settings", expanded=False):
            st.session_state["chunk_size"] = st.slider(
                "Chunk Size", min_value=200, max_value=2000, value=st.session_state.get("chunk_size", 1000), step=100
            )
            st.session_state["chunk_overlap"] = st.slider(
                "Chunk Overlap", min_value=0, max_value=500, value=st.session_state.get("chunk_overlap", 200), step=50
            )
            if "OpenAI" in st.session_state.get("ai_mode", ""):
                st.session_state["embedding_model"] = st.selectbox(
                    "Embedding Model", ["text-embedding-3-small", "text-embedding-3-large"], index=0
                )
                st.session_state["llm_model"] = st.selectbox(
                    "LLM Model", ["gpt-4o-mini", "gpt-4o"], index=0
                )
            else:
                st.session_state["embedding_model"] = "local-tfidf"
                st.session_state["llm_model"] = "free-local-nlp"
                st.session_state["ollama_model"] = st.selectbox(
                    "Ollama LLM Model", ["llama2", "llama3", "llama3.1:8b", "qwen2.5:7b", "gemma3:4b"],
                    index=0,
                    help="Choose your locally running Ollama model. Recommended: qwen2.5:7b or llama3.1:8b"
                )
                st.info("💡 Free Local Mode active: Processing powered by local Ollama LLM and documents retriever.")


