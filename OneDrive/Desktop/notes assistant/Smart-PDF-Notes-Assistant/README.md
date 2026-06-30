# 📚 Smart PDF Notes Assistant

Smart PDF Notes Assistant is a modern, modular Streamlit web application designed to help users upload study notes, generate intelligent summaries, and ask questions using AI. 

The project is architected specifically for production-ready Retrieval-Augmented Generation (RAG) using LangChain, OpenAI, and FAISS vector search.

---

## 🏗️ Project Structure

```text
Smart-PDF-Notes-Assistant/
│
├── app.py                  # Main Streamlit entrypoint and page layout
├── requirements.txt        # Project dependencies
├── .env.example            # Environment variables template
├── README.md               # Project documentation
├── uploads/                # Directory for storing uploaded PDF files
├── vectorstore/            # Directory for storing persisted FAISS vector index
├── assets/                 # Custom CSS and UI static assets
│   └── style.css
│
├── utils/                  # Modular backend & RAG logic components
│   ├── __init__.py
│   ├── pdf_loader.py       # Document loading utilities
│   ├── text_splitter.py    # Text chunking & token splitting
│   ├── embeddings.py       # Embedding model configuration
│   ├── vector_store.py     # FAISS index persistence and retrieval setup
│   ├── retriever.py        # Context retrieval algorithms
│   ├── summarizer.py       # Map-reduce / Refine summary chains
│   ├── chatbot.py          # Conversational retrieval chains
│   └── prompts.py          # Custom prompt templates
│
└── components/             # Reusable Streamlit UI components
    ├── __init__.py
    ├── sidebar.py          # App configuration sidebar
    ├── upload_section.py   # PDF file upload interface
    ├── summary_section.py  # Intelligent summary display card
    └── chat_section.py     # Conversational QA interface & retrieved sources
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ installed on your system.

### 2. Setup Virtual Environment
```bash
# Navigate to project directory
cd Smart-PDF-Notes-Assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🛠️ Implementation Roadmap
- [x] Implement PyPDF loader in `utils/pdf_loader.py`
- [x] Setup RecursiveCharacterTextSplitter in `utils/text_splitter.py`
- [x] Connect OpenAI Embeddings in `utils/embeddings.py`
- [x] Persist FAISS vector store in `utils/vector_store.py`
- [x] Connect LangChain RetrievalQA chain in `utils/chatbot.py`

