from app.retrieval.dense_retriever import dense_retriever
from app.retrieval.bm25_retriever import bm25_retriever
from app.retrieval.rrf import reciprocal_rank_fusion
from app.authorization.access_control import apply_ac,UserRole
from app.retrieval.reranker import rerank_results
from app.retrieval.relevancy import filter_relevant_results
from app.rag.context_builder import build_context


TARGET_CHUNK = "DOC002-2026.1-003"


def debug_target(stage: str, results: list[dict]):
    print(f"\n========== {stage} ==========")

    found = False

    for position, result in enumerate(results, start=1):
        if result["id"] == TARGET_CHUNK:
            found = True

            print("TARGET FOUND")
            print("POSITION:", position)
            print("ID:", result["id"])
            print("SCORE:", result.get("score"))
            print("RRF SCORE:", result.get("rrf_score"))
            print("RERANK SCORE:", result.get("rerank_score"))
            print("SOURCE:", result.get("source"))
            print("SOURCES:", result.get("sources"))

            metadata = result.get("metadata", {})
            print("FILE:", metadata.get("file_name"))
            print("SECTION:", metadata.get("section"))

    if not found:
        print("TARGET NOT FOUND:", TARGET_CHUNK)

    print("\nALL RESULT IDs:")
    for position, result in enumerate(results, start=1):
        print(position, result["id"])
# this function can be used to debug this corrective rag pipeline by calling the function after every stage 
# like "debug_target("Reranker Stage",reranked_results)"


def corrective_rag_pipeline(query:str,role:str)->dict:
    dense_results = dense_retriever(query=query,top_k=5)
    bm25_results = bm25_retriever(query=query,top_k=5)
    rrf_results = reciprocal_rank_fusion(dense_results=dense_results,bm25_results=bm25_results)
    authorized_result = apply_ac(results=rrf_results,role=UserRole(role))
    reranked_results = rerank_results(query=query, results= authorized_result,top_k=5)
    relevant_result = filter_relevant_results(results=reranked_results,threshold=0.0)
    #debug_target("Relevancy Stage", relevant_result)
    #context = build_context(results=relevant_result)

    return {"result":relevant_result}



def merge_rag_results(old_context:str,new_context:str)->str:
    output = []
    merged_results = []
    seen_ids = set()
    for result in old_context + new_context:
        chunk_ids = result["id"]
        if chunk_ids not in seen_ids:
            merged_results.append(result)
            seen_ids.add(chunk_ids)
    return merged_results