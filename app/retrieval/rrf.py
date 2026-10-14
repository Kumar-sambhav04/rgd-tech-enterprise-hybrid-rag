# RRF stands for Reciprocal Rank Fusion

def reciprocal_rank_fusion(dense_results:list[dict],bm25_results:list[dict],k:int=60)->list[dict]:

    fused = {}

    all_results = [dense_results,bm25_results]

    for result_list in all_results:
        for result in result_list:
            chunk_id = result["id"]
            rank = result["rank"]

            rrf_score = 1 / (k + rank)

            if chunk_id not in fused:
                fused[chunk_id] = {
                    "id": chunk_id,
                    "rrf_score": 0.0,
                    "metadata": result["metadata"],
                    "sources": []
                }
            fused[chunk_id]["rrf_score"] += rrf_score
            fused[chunk_id]["sources"].append(result["source"])

    fused_result = list(fused.values())

    fused_result.sort(key= lambda x : x["rrf_score"],reverse=True)

    for rank, result in enumerate(fused_result,start=1):
        result["rank"]= rank

    return fused_result
