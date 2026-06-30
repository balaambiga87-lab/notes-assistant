"""
Vector Store Module.
Handles index creation, persisting, and loading of FAISS vector databases.
"""

import os
from typing import List, Any, Optional
from langchain_community.vectorstores import FAISS


def create_vector_store(
    chunks: List[Any],
    embeddings: Any,
    save_path: str = "vectorstore/"
) -> Any:
    """
    Create a FAISS vector store index from document chunks and save locally.

    Args:
        chunks (List[Any]): List of document chunk objects.
        embeddings (Any): Initialized embedding model instance.
        save_path (str, optional): Directory path to persist vector index. Defaults to "vectorstore/".

    Returns:
        Any: Initialized FAISS vector store object.
    """
    if not chunks:
        raise ValueError("Cannot create vector store with empty chunks list.")

    os.makedirs(save_path, exist_ok=True)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(save_path)
    return vector_store


def load_vector_store(
    embeddings: Any,
    save_path: str = "vectorstore/"
) -> Optional[Any]:
    """
    Load an existing FAISS vector store index from local disk.

    Args:
        embeddings (Any): Initialized embedding model instance.
        save_path (str, optional): Directory path of persisted vector index.

    Returns:
        Optional[Any]: FAISS vector store object if found, else None.
    """
    if os.path.exists(save_path) and os.path.exists(os.path.join(save_path, "index.faiss")):
        return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
    return None

