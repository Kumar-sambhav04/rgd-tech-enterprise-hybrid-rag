import json
from pathlib import Path

from app.retrieval.dense_encoder import embeddings


CHUNK_FILE = Path("data/chunk_preview.json")

chunks = json.loads(
    CHUNK_FILE.read_text(encoding="utf-8")
)

first_chunk = chunks[0]

text = first_chunk["chunk_text"]

print("Chunk ID:", first_chunk["id"])
print("Text length:", len(text))

vector = embeddings.embed_query(text)

print("Embedding dimension:", len(vector))
print("First 5 values:", vector[:5])