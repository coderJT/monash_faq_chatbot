import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# --- Configuration ---

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("❌ Set your Google API key in the environment as GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
rag_model = genai.GenerativeModel("gemini-2.5-flash")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Load FAISS index and metadata ---
print("📦 Loading index and metadata...")
index = faiss.read_index("index/faiss_index")
with open("index/chunks_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

chat_history = []

# --- Normalize FAISS vectors if cosine similarity used ---
def normalize(vectors):
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

# --- Chat loop ---
print("💬 Ask your Monash Uni questions. Press Enter to exit.")
while True:
    question = input("\n❓ Your question: ").strip()
    if not question:
        print("👋 Exiting.")
        break

    try:
        # 1. Embed and normalize the query
        query_vec = embed_model.encode([question])
        query_vec = normalize(query_vec)

        # 2. Retrieve top-k similar chunks
        D, I = index.search(query_vec.astype("float32"), k=5)
        top_chunks = [metadata[i]["text"] for i in I[0]]
        context = "\n\n".join(top_chunks)

        memory_str = "\n".join(chat_history)
        if not memory_str: # Add a placeholder if memory is empty for the first turn
            memory_str = "No previous conversation."

        # 3. Construct prompt
        prompt = f"""You are a helpful assistant answering student admin questions at Monash University.

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

        # 4. Generate answer
        response = rag_model.generate_content(prompt)
        print("\n🤖 Gemini says:\n", response.text.strip())

        chat_history.append(f"User: {question}")
        chat_history.append(f"Assistant: {response.text.strip()}")


    except Exception as e:
        print("❌ Error:", e)
