"""
PDF Loader Module.
Handles loading and extracting content from PDF documents.
"""

from typing import List, Any
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(file_path: str) -> List[Any]:
    """
    Load a PDF file and return a list of LangChain Document objects.

    Args:
        file_path (str): The absolute or relative path to the PDF file.

    Returns:
        List[Any]: A list of loaded document page objects.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at path: {file_path}")

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error loading PDF with PyPDFLoader: {e}")
        # Fallback minimal document creation if loader fails
        return [
            Document(
                page_content=f"Error reading PDF contents. File: {os.path.basename(file_path)}",
                metadata={"source": file_path, "page": 1}
            )
        ]

