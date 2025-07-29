import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

def evaluate(question: str):
    # Configure Gemini API key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise EnvironmentError("Please set your Google API key in the environment as GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # Load Gemini model
    rag_model = genai.GenerativeModel("gemini-2.5-flash")

    # Load embedding model
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load FAISS index
    index = faiss.read_index("index/faiss_index")

    # Load metadata
    with open("index/chunks_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Load chat history from file (if exists)
    chat_history = []
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r", encoding="utf-8") as f:
            chat_history = json.load(f)

    # Normalize helper
    def normalize(vectors):
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    # Embed and normalize query
    query_vec = embed_model.encode([question])
    query_vec = normalize(query_vec)

    # FAISS top-k search
    D, I = index.search(query_vec.astype("float32"), k=3)
    top_chunks = [metadata[i]["text"] for i in I[0]]

    # Prepare prompt
    context = "\n\n".join(top_chunks)
    memory_str = "\n".join(chat_history) if chat_history else "No previous conversation found."

    prompt = f"""
    You are a helpful assistant answering student admin questions at Monash University.

    Answer the following question using ONLY the context provided below.
    -------------------
    ### Context:
    {context}

    -------------------
    ### Memory:
    {memory_str}

    -------------------

    ### User Question:
    {question}
    """

    # Generate streamed response
    response_stream = rag_model.generate_content(prompt, stream=True)

    full_response = ""
    for chunk in response_stream:
        try:
            if hasattr(chunk, "parts") and chunk.parts:
                text = ''.join([p.text for p in chunk.parts if hasattr(p, "text")])
                yield text
        except Exception as e:
            print(f"Warning: Skipped invalid chunk: {e}")

    # Save conversation
    chat_history.append(f"User: {question}")
    chat_history.append(f"Assistant: {full_response.strip()}")

    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)
