"""
Chatbot Module.
Manages conversational retrieval QA chains and LLM interaction.
"""

import os
from typing import List, Any, Dict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from utils.prompts import QA_PROMPT_TEMPLATE

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)


def _generate_local_answer(query: str, raw_documents: Optional[List[Any]], vector_store: Any = None, chat_history: List[Dict[str, str]] = None) -> str:
    """Generate structured answers locally using Ollama (llama2) if available, else fallback to substring matching."""
    if not raw_documents:
        return "⚠️ Please upload a PDF document first to extract answer insights."

    try:
        from langchain_community.llms import Ollama
        from utils.retriever import retrieve_documents
        
        # Retrieve relevant chunks using our local matching retriever
        docs = retrieve_documents(query, vector_store)
        if docs:
            context_text = "\n\n".join([
                f"--- Source ({doc['metadata']['source']} Page {doc['metadata']['page']}) ---\n" + doc['page_content']
                for doc in docs
            ])
        else:
            context_text = "No document pages retrieved."

        # Format chat history
        history_str = ""
        if chat_history:
            for msg in chat_history[-5:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_str += f"{role}: {msg['content']}\n"
        if not history_str:
            history_str = "No history yet."

        llm = Ollama(model="llama2")
        prompt = PromptTemplate(template=QA_PROMPT_TEMPLATE, input_variables=["chat_history", "context", "question"])
        formatted_prompt = prompt.format(chat_history=history_str, context=context_text, question=query)
        
        response = llm.invoke(formatted_prompt)
        ai_response = response.content if hasattr(response, "content") else str(response)
        
        return ai_response
    except Exception as e:
        print(f"Ollama local Q&A failed, falling back to local extractor: {e}")

        combined = " ".join([getattr(d, "page_content", str(d)) for d in raw_documents])
        lines = [line.strip() for line in combined.split("\n") if len(line.strip()) > 25]

        query_lower = query.lower()
        is_question_gen = any(k in query_lower for k in ["question", "questions", "quiz", "exam", "test", "important"])

        if is_question_gen:
            sample_headers = [l for l in lines if any(char.isupper() for char in l[:5]) and len(l) < 100][:10]
            if len(sample_headers) < 5:
                sample_headers = lines[:10]
            
            q_list = []
            for i in range(min(5, len(sample_headers))):
                topic = sample_headers[i].strip(":-• ")
                q_list.append(f"{i+1}. **Question {i+1}**: Explain the core concepts and principles behind *\"{topic[:80]}\"* as discussed in the PDF notes?")
            
            return (
                f"### 🎯 5 Important Study Questions (Free Local Engine Fallback)\n\n"
                f"Extracted directly from your uploaded PDF notes:\n\n" +
                "\n\n".join(q_list) +
                "\n\n_Tip: Re-review the corresponding sections in your PDF to prepare complete answers for exam prep!_"
            )
        else:
            matching = [l for l in lines if any(word in l.lower() for word in query_lower.split() if len(word) > 3)]
            excerpt = "\n\n• ".join(matching[:3]) if matching else "\n\n• " + "\n• ".join(lines[:3])
            
            return (
                f"### 💡 Document Analysis for: *\"{query}\"*\n\n"
                f"**Relevant Excerpts Extracted from PDF:**\n\n• {excerpt}\n\n"
                f"_Note: Powered by 100% Free Local Analyzer Fallback (No API key required)._"
            )


def answer_question(
    query: str,
    vector_store: Any,
    chat_history: List[Dict[str, str]],
    model_name: str = "gpt-4o-mini",
    raw_documents: Optional[List[Any]] = None
) -> str:
    """
    Generate an AI response to a user query based on retrieved vector context, raw document pages, and chat history.
    """
    if model_name == "free-local-nlp" or "local" in model_name:
        return _generate_local_answer(query, raw_documents, vector_store, chat_history)

    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        return _generate_local_answer(query, raw_documents, vector_store, chat_history)

    try:
        docs = []
        if vector_store and vector_store != "MockVectorStoreInstance" and vector_store != "LocalVectorStoreInstance":
            try:
                if hasattr(vector_store, "similarity_search"):
                    docs = vector_store.similarity_search(query, k=5)
                elif hasattr(vector_store, "get_relevant_documents"):
                    docs = vector_store.get_relevant_documents(query)
                elif hasattr(vector_store, "invoke"):
                    docs = vector_store.invoke(query)
            except Exception as vs_err:
                print(f"Vector store search failed, using fallback documents: {vs_err}")

        if not docs and raw_documents:
            docs = raw_documents[:10]

        if docs:
            context_text = "\n\n".join([
                f"--- Source (Page {getattr(d, 'metadata', {}).get('page', i+1)}) ---\n" + getattr(d, "page_content", str(d))
                for i, d in enumerate(docs)
            ])
        else:
            context_text = "Note: No specific document pages retrieved."

        # Format chat history for context-aware Q&A
        history_str = ""
        if chat_history:
            for msg in chat_history[-5:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_str += f"{role}: {msg['content']}\n"
        if not history_str:
            history_str = "No history yet."

        llm = ChatOpenAI(temperature=0.3, model=model_name, openai_api_key=api_key)
        prompt = PromptTemplate(template=QA_PROMPT_TEMPLATE, input_variables=["chat_history", "context", "question"])
        formatted_prompt = prompt.format(chat_history=history_str, context=context_text, question=query)
        
        response = llm.invoke(formatted_prompt)
        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        print(f"OpenAI QA failed, falling back to local engine: {e}")
        return _generate_local_answer(query, raw_documents, vector_store, chat_history)



