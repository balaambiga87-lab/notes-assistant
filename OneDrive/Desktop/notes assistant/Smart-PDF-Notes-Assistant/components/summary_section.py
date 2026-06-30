"""
Summary Section Component.
Renders the intelligent document summary card interface.
"""

import os
import streamlit as st
from utils.summarizer import generate_summary
from utils.exporter import generate_pdf, generate_docx



def render_summary_section() -> None:
    """Render intelligent PDF summary card UI with export options."""
    st.subheader("📝 Document Summary")
    
    with st.container():
        if st.session_state.get("upload_status") == "Ready":
            summary_content = st.session_state.get("summary")
            if not summary_content:
                raw_docs = st.session_state.get("raw_documents", [])
                llm_model = st.session_state.get("llm_model", "gpt-4o-mini")
                progress_status = st.empty()
                def update_progress(msg: str):
                    progress_status.info(f"⚙️ **Status:** {msg}")
                summary_content = generate_summary(raw_docs, model_name=llm_model, progress_callback=update_progress)
                st.session_state["summary"] = summary_content
                progress_status.empty()
            
            # Display Markdown summary content
            st.markdown(summary_content)
            
            st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
            
            # Setup export generation
            pdf_bytes = None
            docx_bytes = None
            uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Generate PDF content
            try:
                pdf_path = os.path.join(uploads_dir, "temp_export.pdf")
                generate_pdf(summary_content, pdf_path)
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
            except Exception as e:
                st.error(f"Error preparing PDF download: {e}")

            # Generate DOCX content
            try:
                docx_path = os.path.join(uploads_dir, "temp_export.docx")
                generate_docx(summary_content, docx_path)
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                if os.path.exists(docx_path):
                    os.remove(docx_path)
            except Exception as e:
                st.error(f"Error preparing DOCX download: {e}")

            # Render download controls
            col_pdf, col_docx = st.columns(2)
            with col_pdf:
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download Study Guide (PDF)",
                        data=pdf_bytes,
                        file_name="Smart_Study_Guide.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            with col_docx:
                if docx_bytes:
                    st.download_button(
                        label="📥 Download Study Guide (DOCX)",
                        data=docx_bytes,
                        file_name="Smart_Study_Guide.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
        else:
            st.info("💡 Upload and process a PDF document to generate an automated intelligent summary.")


