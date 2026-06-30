"""
Smart PDF Notes Assistant - Main Application Entrypoint.

A modern Streamlit application designed for uploading PDF study notes,
generating intelligent summaries, and interacting with document content via RAG AI.
"""

import os
import streamlit as st

# Import custom reusable components
from components.sidebar import render_sidebar
from components.upload_section import render_upload_section
from components.summary_section import render_summary_section
from components.chat_section import render_chat_section


def load_custom_css() -> None:
    """Load custom CSS styling from assets/style.css if available."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_session_state() -> None:
    """Initialize Streamlit session state keys for application persistence."""
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "upload_status" not in st.session_state:
        st.session_state["upload_status"] = "No document uploaded"
    if "uploaded_filename" not in st.session_state:
        st.session_state["uploaded_filename"] = None
    if "summary" not in st.session_state:
        st.session_state["summary"] = None
    if "vector_store" not in st.session_state:
        st.session_state["vector_store"] = None


def main() -> None:
    # 1. Page Configuration (Wide layout)
    st.set_page_config(
        page_title="Smart PDF Notes Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Inject custom stylesheet & initialize state
    load_custom_css()
    init_session_state()

    # 3. Render Sidebar Component
    render_sidebar()

    # 4. Main Content Layout
    # Hero Section
    st.markdown("<h1 class='hero-title'>📚 Smart PDF Notes Assistant</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='hero-subtitle'>Upload your study notes, generate intelligent summaries, "
        "and chat with your documents using AI.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    # Layout Grid: Top row for Upload and Summary Cards
    col_upload, col_summary = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        render_upload_section()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_summary:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        render_summary_section()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom row for Chat and Sources Cards
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    render_chat_section()
    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Footer
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(
        "<p class='footer-text'>Powered by Streamlit • LangChain • FAISS • OpenAI</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
