from sentence_transformers import CrossEncoder

model_name = "cross-encoder/ms-marco-MiniLM-L6-v2"

"""This model "cross-encoder/ms-marco-MiniLM-L6-v2" is a reranking model, perticularly
used for reranking in rag-systems, it is not a embedding model it is a Cross-Encoder
it takes 2 pices of text together (Query and Result) and produces a relevence score
indicating how well the document or result answers the query. """

reranker = CrossEncoder(model_name)

def rerank_results(query:str, results:list[dict],top_k:int=5)->list[dict]:
    # Rerank authorized results by Cross-Encoder
    if not results:
        return []

    pairs = [ (query, result["metadata"].get("chunk_text","")) for result in results]

    scores =  reranker.predict(pairs, show_progress_bar=False)

    reranked_results = []

    for result, score in zip(results,scores):

        items = result.copy()
        # copying because we wont make changes in the retrived results

        items["rrf_rank"] = result["rank"]
        # because we want to keep the rrf rank stored and we will assign the new reranked rank 

        items["rerank_score"] = float(score)

        reranked_results.append(items)

    reranked_results.sort(key = lambda x: x["rerank_score"],reverse=True)

    reranked_results = reranked_results[:top_k]

    for rank, result in enumerate(reranked_results,start=1):
        result["rank"] = rank

    return reranked_results
