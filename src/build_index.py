# Now we will perform chunking of the data

import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-large-en")

def normalize(vectors):
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

# Load cleaned data
documents = []
metadata = []

# Chunking
for filename in os.listdir("cleaned"):
    if filename.endswith(".clean.txt"):
        with open(f"cleaned/{filename}", encoding="utf-8") as f:
            text = f.read()

        # Chunking (500 chars per chunk with 100 char overlap)
        for i in range(0, len(text), 400):
            chunk = text[i:i + 500]
            if len(chunk.strip()) < 100:
                continue
            documents.append(chunk)
            metadata.append({
                "source": filename,
                "offset": i,
                "text": chunk
            })

# Compute embeddings
print(f"Embedding {len(documents)} chunks...")

# Normalize the embeddings to use cosine similarity
embeddings = normalize(model.encode(documents, show_progress_bar=True))

# Store the embedding in FAISS
dim = embeddings[0].shape[0]

# Use inner product index for cosine similarity
index = faiss.IndexFlatIP(dim)
index.add(np.array(embeddings))

# Save the index and metadata
os.makedirs("index", exist_ok=True)
faiss.write_index(index, "index/faiss_index")
with open("index/chunks_metadata.json", "w") as f:
    json.dump(metadata, f)

print("FAISS built successfully.")
