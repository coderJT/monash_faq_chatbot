# 🎓 Monash Student Chatbot (RAG-based FAQ Assistant)

<img width="1113" height="717" alt="Screenshot 2025-07-29 at 9 03 43 PM" src="https://github.com/user-attachments/assets/25b215da-0103-444c-8ed1-9e3d89daba42" />

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

TODO:
1. Improved chat inteface for user questions.
2. Faster search time, probably cache the embedding model.
3. Add evaluation metrics (Precision@K)
4. Benchmarks latencies (startup, response, token throughput, embedding, FAISS search time)
5. Faithfulness and Groundedness test.
6. Probably allow minimal conversation logic to be more user-friendly (prompt engineering, however caution must be taken on memory injection, else hallucination will be an issue.)
