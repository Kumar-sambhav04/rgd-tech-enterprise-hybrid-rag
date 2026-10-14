import json
from pathlib import Path

from app.retrieval.bm25_encoder import fit_bm25


chunks = json.loads(
    Path("data/chunk_preview.json").read_text(
        encoding="utf-8"
    )
)

texts = [
    chunk["chunk_text"]
    for chunk in chunks
]

print("Total chunks:", len(texts))

bm25 = fit_bm25(texts)

print("\nBM25 fitted successfully.")

print("Documents fitted:", bm25.n_docs)
print("Average document length:", bm25.avgdl)


# Test one document
sparse_vector = bm25.encode_documents(
    texts[0]
)

print("\nSparse vector:")
print("Indices:", sparse_vector["indices"][:10])
print("Values :", sparse_vector["values"][:10])

print(
    "\nSparse dimensions used:",
    len(sparse_vector["indices"])
)