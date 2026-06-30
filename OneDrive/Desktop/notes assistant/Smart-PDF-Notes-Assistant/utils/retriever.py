"""
Retriever Module.
Handles document search and similarity retrieval from the vector store.
"""

from typing import List, Dict, Any


import streamlit as st

def retrieve_documents(
    query: str,
    vector_store: Any,
    k: int = 4
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant document chunks from the vector store matching the query.

    Args:
        query (str): The search query or user question.
        vector_store (Any): The FAISS vector store instance.
        k (int, optional): Number of top documents to retrieve. Defaults to 4.

    Returns:
        List[Dict[str, Any]]: List of retrieved document dictionaries with page_content and metadata.
    """
    if not vector_store or vector_store == "MockVectorStoreInstance" or vector_store == "LocalVectorStoreInstance":
        chunks = st.session_state.get("document_chunks")
        if chunks:
            # Simple keyword-based ranking
            query_words = [w.lower() for w in query.split() if len(w) > 2]
            if not query_words:
                matched_chunks = chunks[:k]
            else:
                scored_chunks = []
                for doc in chunks:
                    content_lower = doc.page_content.lower()
                    score = sum(content_lower.count(word) for word in query_words)
                    scored_chunks.append((score, doc))
                
                scored_chunks.sort(key=lambda x: x[0], reverse=True)
                matched_chunks = [doc for score, doc in scored_chunks[:k]]

            formatted_docs = []
            for doc in matched_chunks:
                source_path = doc.metadata.get("source", "Unknown document")
                source_name = source_path.replace("\\", "/").split("/")[-1]
                page_num = doc.metadata.get("page", doc.metadata.get("page_number", 1))
                
                formatted_docs.append({
                    "page_content": doc.page_content,
                    "metadata": {
                        "source": source_name,
                        "page": page_num
                    }
                })
            return formatted_docs

        return [
            {
                "page_content": f"Sample excerpt content matching query '{query}'. This page details key concepts from your PDF notes.",
                "metadata": {"source": "sample_document.pdf", "page": 1}
            },
            {
                "page_content": "Another relevant sample section providing context for AI-generated answers.",
                "metadata": {"source": "sample_document.pdf", "page": 3}
            }
        ]

    try:
        docs = vector_store.similarity_search(query, k=k)
        formatted_docs = []
        for doc in docs:
            # Handle source filename formatting (basename only)
            source_path = doc.metadata.get("source", "Unknown document")
            source_name = source_path.replace("\\", "/").split("/")[-1]
            page_num = doc.metadata.get("page", doc.metadata.get("page_number", 1))
            
            formatted_docs.append({
                "page_content": doc.page_content,
                "metadata": {
                    "source": source_name,
                    "page": page_num
                }
            })
        return formatted_docs
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []


