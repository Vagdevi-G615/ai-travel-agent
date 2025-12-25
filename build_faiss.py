import json
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# ----------------------------
# CONFIG
# ----------------------------
CHUNKS_FILE = "chunks.json"
FAISS_INDEX_FILE = "travel_faiss.index"
METADATA_FILE = "chunk_metadata.pkl"

# ----------------------------
# LOAD CHUNKS
# ----------------------------
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metadata = [{"theme": c["theme"]} for c in chunks]

print(f"Total chunks loaded: {len(texts)}")

# ----------------------------
# EMBEDDING MODEL (LIGHTWEIGHT)
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# CREATE EMBEDDINGS
# ----------------------------
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=32
)

# ----------------------------
# FAISS INDEX
# ----------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ----------------------------
# SAVE FILES
# ----------------------------
faiss.write_index(index, FAISS_INDEX_FILE)

with open(METADATA_FILE, "wb") as f:
    pickle.dump(metadata, f)

print("✅ FAISS index and metadata saved successfully")
