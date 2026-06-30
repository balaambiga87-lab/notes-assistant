"""
Upload Section Component.
Renders the PDF document upload card with processing controls and status indicators.
"""

import os
import streamlit as st
from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store
from utils.summarizer import generate_summary


def render_upload_section() -> None:
    """Render PDF document upload UI card."""
    st.subheader("📤 Document Upload")
    
    with st.container():
        uploaded_file = st.file_uploader(
            "Choose a PDF file to analyze",
            type=["pdf"],
            help="Upload your lecture slides, textbook chapters, or study notes (PDF format only)."
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            upload_btn = st.button("🚀 Process PDF", use_container_width=True, type="primary")
        with col2:
            clear_btn = st.button("🗑️ Clear File", use_container_width=True)

        if upload_btn:
            if uploaded_file is not None:
                with st.spinner("⏳ Reading and processing PDF document..."):
                    try:
                        # 1. Ensure uploads directory exists and save file
                        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
                        os.makedirs(uploads_dir, exist_ok=True)
                        file_path = os.path.join(uploads_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # 2. Extract PDF text pages
                        documents = load_pdf(file_path)
                        st.session_state["raw_documents"] = documents

                        # 3. Chunk text
                        chunk_size = st.session_state.get("chunk_size", 1000)
                        chunk_overlap = st.session_state.get("chunk_overlap", 200)
                        chunks = split_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                        st.session_state["document_chunks"] = chunks

                        # 4. Generate summary (with graceful quota handling)
                        llm_model = st.session_state.get("llm_model", "gpt-4o-mini")
                        try:
                            progress_status = st.empty()
                            def update_progress(msg: str):
                                progress_status.info(f"⚙️ **Status:** {msg}")
                                
                            summary_text = generate_summary(documents, model_name=llm_model, progress_callback=update_progress)
                            st.session_state["summary"] = summary_text
                            progress_status.empty()
                        except Exception as sum_err:
                            if "insufficient_quota" in str(sum_err) or "429" in str(sum_err):
                                st.session_state["summary"] = "⚠️ **OpenAI Quota Exceeded**: Your OpenAI account has run out of API credits. Please check your billing details at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)."
                            else:
                                st.session_state["summary"] = f"⚠️ Could not generate summary: {sum_err}"

                        # 5. Build vector store
                        embedding_model = st.session_state.get("embedding_model", "text-embedding-3-small")
                        try:
                            embeddings = create_embeddings(model_name=embedding_model)
                            if embeddings == "LocalVectorStoreInstance":
                                st.session_state["vector_store"] = "LocalVectorStoreInstance"
                            else:
                                vector_store_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")
                                vs = create_vector_store(chunks, embeddings, save_path=vector_store_dir)
                                st.session_state["vector_store"] = vs
                        except Exception as ve:
                            if "insufficient_quota" in str(ve) or "429" in str(ve):
                                st.warning("⚠️ OpenAI API Quota Exceeded. Add credits to your OpenAI account to activate vector embeddings.")
                            else:
                                st.warning(f"⚠️ Vector search setup note: {ve}")
                            st.session_state["vector_store"] = "MockVectorStoreInstance"

                        st.session_state["upload_status"] = "Ready"
                        st.session_state["uploaded_filename"] = uploaded_file.name
                        st.success(f"Successfully loaded '{uploaded_file.name}'!")
                        st.rerun()

                    except Exception as e:
                        if "insufficient_quota" in str(e) or "429" in str(e):
                            st.error("⚠️ **OpenAI API Quota Exceeded (Error 429)**: Your OpenAI account has zero remaining API credits. Please add a billing method or prepaid credits at platform.openai.com.")
                        else:
                            st.error(f"Error processing PDF: {e}")

            else:
                st.error("Please select a valid PDF file first.")

        if clear_btn:
            st.session_state["upload_status"] = "No document uploaded"
            st.session_state["uploaded_filename"] = None
            st.session_state["summary"] = None
            st.session_state["vector_store"] = None
            st.session_state["raw_documents"] = None
            st.session_state["document_chunks"] = None
            st.info("Uploaded document cleared.")

        # Status display
        if st.session_state.get("uploaded_filename"):
            st.caption(f"📁 Active File: **{st.session_state['uploaded_filename']}**")

