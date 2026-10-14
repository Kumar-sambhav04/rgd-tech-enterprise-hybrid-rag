from app.retrieval.bm25_encoder import encode_query
from app.retrieval.pinecone_client import bm25_index

def bm25_retriever(query:str, top_k:int=5)->list[dict:]:

    sparse_vector = encode_query(query=query)

    response = bm25_index.query(
        sparse_vector=sparse_vector,
        top_k=top_k,
        include_metadata=True,
        include_values=False
    )

    result = []
    for rank,match in enumerate(response.matches,start=1):
        result.append({
            "id": match.id,
            "score": float(match.score),
            "rank": rank,
            "source":"BM25",
            "metadata":match.metadata})
    return result
