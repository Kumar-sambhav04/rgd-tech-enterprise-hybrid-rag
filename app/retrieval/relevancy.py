
def filter_relevant_results(results:list[dict],threshold:int=0.0)->list[dict]:

    ## check the relevancey of the chunks by comparing the reranker_score with threshold value
    ## (which is decided by doing many tryals and evluations )

    relevant_result = [result for result in results 
                       if result["rerank_score"] >= threshold]
    return relevant_result

def has_relevent_context(results:list[dict])->bool:
    return len(results)>=0