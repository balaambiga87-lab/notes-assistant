"""
Text Splitter Module.
Handles chunking documents into smaller manageable segments for embedding generation.
"""

from typing import List, Any
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_documents(
    documents: List[Any],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Any]:
    """
    Split document objects into smaller text chunks suitable for vector storage.

    Args:
        documents (List[Any]): List of loaded document objects.
        chunk_size (int, optional): Maximum characters per chunk. Defaults to 1000.
        chunk_overlap (int, optional): Overlap characters between chunks. Defaults to 200.

    Returns:
        List[Any]: List of document chunk objects.
    """
    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = splitter.split_documents(documents)
    return chunks

