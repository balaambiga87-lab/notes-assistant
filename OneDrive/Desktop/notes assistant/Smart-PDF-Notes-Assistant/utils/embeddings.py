"""
Embeddings Module.
Initializes vector embedding models for converting text into dense vector representations.
"""

import os
from typing import Any, Optional
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)


def create_embeddings(model_name: str = "text-embedding-3-small") -> Any:
    """
    Initialize and return an embedding model instance.
    """
    if "local" in model_name or model_name == "free-local-nlp":
        return "LocalVectorStoreInstance"

    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError(
            "OpenAI API Key is not configured."
        )

    return OpenAIEmbeddings(model=model_name, openai_api_key=api_key)



