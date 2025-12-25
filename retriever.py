import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (CPU-friendly)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load FAISS index
index = faiss.read_index("travel_faiss.index")

def retrieve_context(query, top_k=5):
    """
    Retrieve top-k relevant text chunks for a query
    """
    query_vec = embedder.encode([query])
    D, I = index.search(np.array(query_vec).astype("float32"), top_k)

    results = []
    for idx in I[0]:
        if idx != -1:
            results.append(chunks[idx]["text"])

    return "\n".join(results)
