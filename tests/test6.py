from app.retrieval.bm25_encoder import load_bm25
bm25 = load_bm25()

print("Documents:", bm25.n_docs)
print("Average length:", bm25.avgdl)
print("Doc freq loaded:", bm25.doc_freq is not None)