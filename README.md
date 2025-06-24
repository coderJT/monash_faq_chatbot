# 🎓 Monash Student Chatbot (RAG-based FAQ Assistant)

An intelligent chatbot powered by Retrieval-Augmented Generation (RAG) that answers student administrative questions about Monash University using real university policy documents. Built with Gemini API, FAISS vector search, and Streamlit for an interactive web interface.

## 🚀 Features

- ✅ **Retrieval-Augmented Generation (RAG)** pipeline for accurate, context-aware answers
- 🔍 **Semantic Search** using FAISS + SentenceTransformers
- 💬 **Chat Interface** powered by Streamlit with **real-time streaming** replies
- 🧠 **Memory Context** from previous conversation rounds
- 🌐 Uses **Gemini 2.5 Flash** (Google Generative AI) for fast and cost-effective responses
- 🧾 Saves chat history and relevant metadata

---

## 🧱 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Gemini 2.5 Flash (via `google.generativeai`)
- **Embedding Model**: `all-MiniLM-L6-v2` (via `sentence-transformers`)
- **Vector Store**: FAISS
- **Document Pipeline**: Custom scrapers + text cleaner
