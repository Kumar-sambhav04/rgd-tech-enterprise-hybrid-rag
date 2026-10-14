import json
from pathlib import Path

from app.retrieval.dense_encoder import embed_chunk


chunks = json.loads(
    Path("data/chunk_preview.json").read_text(
        encoding="utf-8"
    )
)

# Only test 5 chunks
test_chunks = chunks[:5]

texts = [
    chunk["chunk_text"]
    for chunk in test_chunks
]

dense_vectors = embed_chunk(texts)

print("Chunks:", len(test_chunks))
print("Vectors:", len(dense_vectors))
print("Dimension:", len(dense_vectors[0]))

assert len(dense_vectors) == 5
assert all(len(vector) == 768 for vector in dense_vectors)

print("Batch embedding test successful.")