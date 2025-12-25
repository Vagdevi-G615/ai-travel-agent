import os
import json

INPUT_DIR = "knowledge_base"
OUTPUT_FILE = "chunks.json"

CHUNK_SIZE = 500   # characters
OVERLAP = 100

chunks = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".txt"):
        continue

    theme = file.replace(".txt", "")
    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        text = f.read()

    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end]

        if len(chunk_text.strip()) > 50:
            chunks.append({
                "theme": theme,
                "text": chunk_text
            })

        start = end - OVERLAP

print(f"Total chunks created: {len(chunks)}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("✅ Chunking completed and saved to chunks.json")
