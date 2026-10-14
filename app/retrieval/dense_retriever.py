from app.retrieval.dense_encoder import embed_query
from app.retrieval.pinecone_client import dense_index

def dense_retriever(query:str,top_k:int = 5)-> list[dict]:
    """This function retrieve top_k result by symantic search"""

    query_vector = embed_query(query=query) # convert user query to 768 dimenction vector

    response = dense_index.query(
        vector=query_vector,
        top_k=top_k,
        include_values=False,
        include_metadata= True
    )

    result = []

    for rank,match in enumerate(response.matches,start=1):
        result.append({
            "id": match.id,
            "score": float(match.score),
            "rank": rank,
            "source": "dense",
            "metadata": match.metadata
        })
    return result


