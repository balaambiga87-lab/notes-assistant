"""
Summarizer Module.
Generates comprehensive, high-quality academic study guides using a hierarchical Map-Reduce pipeline.
"""

import os
from typing import List, Any, Callable, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from utils.prompts import CHUNK_SUMMARY_TEMPLATE, MERGE_SUMMARIES_TEMPLATE, FINAL_STUDY_GUIDE_TEMPLATE

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)


def _generate_local_summary(documents: List[Any]) -> str:
    """Extract key sentences and generate a clean local summary without external APIs."""
    total_pages = len(documents)
    all_text = []
    for d in documents:
        all_text.append(getattr(d, "page_content", str(d)))
    
    combined = " ".join(all_text)
    words = combined.split()
    total_words = len(words)

    # Extract non-empty lines for key points
    lines = [line.strip() for line in combined.split("\n") if len(line.strip()) > 30]
    sample_points = lines[:5] if lines else ["Document text analyzed successfully."]

    bullets = "\n".join([f"• **Key Section**: {p[:120]}..." for p in sample_points[:4]])

    return (
        f"📌 **Document Summary (Free Local Engine)**\n\n"
        f"📊 **Overview**: Analyzed **{total_pages} pages** (~{total_words} words).\n\n"
        f"**Core Highlights Extracted from Notes:**\n"
        f"{bullets}\n\n"
        f"_Note: Powered by 100% Free Local Document Analyzer (No API key or billing required)._"
    )


def summarize_chunk(chunk_text: str, llm: Any) -> str:
    """Summarize a single chunk of text, retaining technical details."""
    prompt = PromptTemplate(template=CHUNK_SUMMARY_TEMPLATE, input_variables=["text"])
    formatted_prompt = prompt.format(text=chunk_text)
    response = llm.invoke(formatted_prompt)
    return response.content if hasattr(response, "content") else str(response)


def merge_summaries(summaries: List[str], llm: Any) -> str:
    """Combine and merge multiple chunk summaries together to fit a standard text size."""
    if not summaries:
        return ""
    if len(summaries) == 1:
        combined_text = summaries[0]
        if len(combined_text) > 12000:
            combined_text = combined_text[:12000]
        prompt = PromptTemplate(template=MERGE_SUMMARIES_TEMPLATE, input_variables=["text"])
        formatted_prompt = prompt.format(text=combined_text)
        response = llm.invoke(formatted_prompt)
        return response.content if hasattr(response, "content") else str(response)

    combined_text = "\n\n".join(summaries)
    if len(combined_text) <= 12000:
        prompt = PromptTemplate(template=MERGE_SUMMARIES_TEMPLATE, input_variables=["text"])
        formatted_prompt = prompt.format(text=combined_text)
        response = llm.invoke(formatted_prompt)
        return response.content if hasattr(response, "content") else str(response)
    
    # Recursive merge in groups if too large
    group_size = 4
    merged_groups = []
    for i in range(0, len(summaries), group_size):
        sub_group = summaries[i:i+group_size]
        sub_combined = "\n\n".join(sub_group)
        prompt = PromptTemplate(template=MERGE_SUMMARIES_TEMPLATE, input_variables=["text"])
        formatted_prompt = prompt.format(text=sub_combined)
        response = llm.invoke(formatted_prompt)
        val = response.content if hasattr(response, "content") else str(response)
        merged_groups.append(val)
        
    return merge_summaries(merged_groups, llm)



def generate_final_study_guide(combined_summary: str, llm: Any) -> str:
    """Synthesize consolidated notes into the 16-section professional academic study guide."""
    prompt = PromptTemplate(template=FINAL_STUDY_GUIDE_TEMPLATE, input_variables=["text"])
    formatted_prompt = prompt.format(text=combined_summary)
    response = llm.invoke(formatted_prompt)
    return response.content if hasattr(response, "content") else str(response)


def generate_summary(
    documents: List[Any],
    model_name: str = "gpt-4o-mini",
    progress_callback: Optional[Callable[[str], None]] = None
) -> str:
    """
    Generate an intelligent hierarchical study notes summary from loaded document pages.
    Processes the entire document using chunk-based Map-Reduce summarization.
    """
    if not documents:
        return "⚠️ No document content available to summarize. Please upload a PDF."

    # Step 1: Extract all text pages
    if progress_callback:
        progress_callback("Extracting all document pages...")
    
    # Step 2: Split text into chunks using recursive splitter
    is_local = (model_name == "free-local-nlp" or "local" in model_name)
    target_chunk_size = 4000 if is_local else 6000
    target_overlap = 500 if is_local else 1000

    if progress_callback:
        progress_callback(f"Splitting document into structured chunks (size={target_chunk_size}, overlap={target_overlap})...")
        
    from utils.text_splitter import split_documents
    chunks = split_documents(documents, chunk_size=target_chunk_size, chunk_overlap=target_overlap)
    total_chunks = len(chunks)
    
    if total_chunks == 0:
        return "⚠️ Extracted document has no content chunks."

    # Step 3: Initialize LLM
    is_local = (model_name == "free-local-nlp" or "local" in model_name)
    api_key = None
    ollama_model = "llama2"
    
    if not is_local:
        load_dotenv(dotenv_path=env_path, override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            is_local = True  # Fallback to local if key is missing

    if is_local:
        try:
            from langchain_community.llms import Ollama
            import streamlit as st
            # Retrieve configured local model from state
            ollama_model = st.session_state.get("ollama_model", "llama2")
            if progress_callback:
                progress_callback(f"Initializing local Ollama model '{ollama_model}'...")
            llm = Ollama(model=ollama_model)
        except Exception as e:
            print(f"Failed to load Ollama, falling back to local string matcher: {e}")
            return _generate_local_summary(documents)
    else:
        if progress_callback:
            progress_callback(f"Initializing OpenAI model '{model_name}'...")
        llm = ChatOpenAI(temperature=0.2, model=model_name, openai_api_key=api_key)

    # Step 4: Map step - Summarize each chunk
    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        if progress_callback:
            progress_callback(f"Summarizing section {idx + 1} of {total_chunks}...")
        try:
            summary = summarize_chunk(chunk.page_content, llm)
            chunk_summaries.append(summary)
        except Exception as chunk_err:
            print(f"Error summarizing chunk {idx}: {chunk_err}")
            # Fallback to page text if LLM call fails
            chunk_summaries.append(chunk.page_content[:200] + "...")

    # Step 5: Reduce step - Merge individual summaries
    if progress_callback:
        progress_callback("Consolidating and merging section summaries...")
    try:
        merged_text = merge_summaries(chunk_summaries, llm)
    except Exception as merge_err:
        print(f"Error merging summaries: {merge_err}")
        merged_text = "\n\n".join(chunk_summaries)

    # Step 6: Final format step - Study Guide Generation
    if progress_callback:
        progress_callback("Formatting and generating final 16-section study guide...")
    try:
        final_guide = generate_final_study_guide(merged_text, llm)
    except Exception as guide_err:
        print(f"Error generating final guide: {guide_err}")
        # Return merged summaries if formatting fails
        return f"⚠️ Study notes consolidation complete (Format failed: {guide_err}):\n\n" + merged_text

    model_tag = f"Ollama (`{ollama_model}`)" if is_local else f"OpenAI (`{model_name}`)"
    return f"🤖 **Study notes prepared by {model_tag}**\n\n" + final_guide




