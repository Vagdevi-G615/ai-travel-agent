import os
import json
import faiss
import torch
from sentence_transformers import SentenceTransformer
from groq import Groq
import streamlit as st  # For secrets

# ----------------- Load API Key -----------------
# Works locally if .streamlit/secrets.toml exists, and on Streamlit Cloud
GROQ_API_KEY = st.secrets["GROQ"]["api_key"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ----------------- Load Knowledge Base -----------------
# Load FAISS index
faiss_index_path = "travel_faiss.index"
index = faiss.read_index(faiss_index_path)

# Load chunk metadata
with open("chunk_metadata.pkl", "rb") as f:
    chunk_metadata = torch.load(f)

# Load chunk texts
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load SentenceTransformer model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# ----------------- Retrieval Function -----------------
def retrieve(query, k=5):
    """
    Retrieve top-k relevant chunks from FAISS index based on query.
    """
    query_embedding = embed_model.encode([query])
    D, I = index.search(query_embedding, k)
    results = []
    for idx in I[0]:
        if idx < len(chunks):
            results.append(chunks[idx])
    return results

# ----------------- Generate Answer -----------------
def generate_answer(query):
    """
    Generate an answer using Groq LLM based on retrieved context.
    """
    context_chunks = retrieve(query)
    context_text = "\n".join(context_chunks)

    prompt = f"""
You are a helpful travel assistant. Use the following context to answer the question.

Context:
{context_text}

Question: {query}

Answer:
"""
    response = client.chat.completions.create(
        model="llama3-8b",  # Update model if deprecated
        messages=[{"role": "user", "content": prompt}],
        max_output_tokens=500
    )
    answer = response.choices[0].message["content"]
    return answer

# ----------------- Optional: Agent Decision -----------------
def agent_decision(query):
    """
    Simple domain detection for RAG vs general reasoning.
    """
    domains = ["adventure", "solo", "budget", "eco", "luxury"]
    if any(word.lower() in query.lower() for word in domains):
        return "retrieve_knowledge"
    return "general_reasoning"
