from app.graph.workflow import build_graph


def extract_sources(results:list[dict])->list[dict]:
    sources = []
    for index, result in enumerate(results,start=1):
        metadata = result.get("metadata",[])
        sources.append({
            "source_id": f"SOURCE_{index}",
            "chunk_id": result["id"],
            "file_name":metadata["file_name"],
            "section": metadata["section"],
            "page_number":metadata["page_number"]  })
    return sources

workflow = build_graph()

def run_rgd_assistant(query:str,role:str,thread_id:str)->dict:
    config = {"configurable":{"thread_id":thread_id}}
    result = workflow.invoke(
        {"raw_query":query, "role":role},
        config = config )
    sources = extract_sources(results=result.get("relevant_results",[]))
    return {
        "answer": result["answer"],
        "route":result.get("route"),
        "sources": sources
    }