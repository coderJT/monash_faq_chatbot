import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

def evaluate():
    # Configuration steps. Here we use Gemini API due to the free API access.
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise EnvironmentError("Please set your Google API key in the environment as GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # LLM model configuration
    # Gemini-2.5-flash allows for higher speed compared to pro model.
    rag_model = genai.GenerativeModel("gemini-2.5-flash")

    # Embedding model configuration
    # BAAI/bge-large-en is used for higher accuracy, better fuzzy matching.
    # Alternatively, MiniLM-L6-v2 can be used as a fast and lightweight solution.
    embed_model = SentenceTransformer("BAAI/bge-large-en")
    embed_model.save("saved_models/bge-large-en")

    # Load FAISS index
    print("Loading index and metadata...")
    index = faiss.read_index("index/faiss_index")

    # Load metadata for improved accuracy
    with open("index/chunks_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # We also keep track of chat history as calling API won't store conversation in memory
    chat_history = []

    # Normalize FAISS vectors as we are using cosine similarity for similarity search
    def normalize(vectors):
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    # The main chat function begins here.
    print("Hi, feel free to ask me any student related questions about Monash University. Press Enter to exit.")
    while True:
        question = input("\n❓ Whats your question? ").strip()
        if not question:
            print("Thank you. Bye.")
            break

        try:
            # Embed and normalize the query
            query_vec = embed_model.encode([question])
            query_vec = normalize(query_vec)

            # Search the FAISS index for the top 5 most similar chunks to the query
            D, I = index.search(query_vec.astype("float32"), k=5)

            # Retrieve the corresponding text for each top chunk from the metadata
            top_chunks = [metadata[i]["text"] for i in I[0]]

            # Create a context string
            context = "\n\n".join(top_chunks)

            # Create the memory string if available
            memory_str = "\n".join(chat_history)
            if not memory_str: 
                memory_str = "No previous conversation found."

            # Create the final prompt
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

            # Generate the output with the llm
            response = rag_model.generate_content(prompt)
            print("\n Bot says:\n", response.text.strip())

            # Update the conversation history
            chat_history.append(f"User: {question}")
            chat_history.append(f"Assistant: {response.text.strip()}")

            # Save chat history to a file
            with open("chat_history.json", "w", encoding="utf-8") as f:
                json.dump(chat_history, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print("Error detected:", e)
