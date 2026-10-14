from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.state import RagState
from app.graph.nodes import (resolve_query_node,
                             dense_retrieval_node,
                             bm25_retrieval_node,
                             rrf_results_node,
                             access_control_node,
                             reranker_node,
                             relevance_node,
                             rag_context_builder_node,
                             rag_response_generator_node,
                             route_after_relevance,
                             no_context_node,
                             sql_query_generator_node,
                             sql_validator_node,
                             sql_result_node,
                             sql_context_node,
                             router_query_node,
                             route_after_router_node,
                             sql_response_generator_node,
                             hybrid_responce_generator_node,
                             rag_ready,
                             sql_ready,
                             route_after_rag_context,
                             route_after_sql_context,
                             evidence_checker_node,
                             route_after_evidence_checker_node,
                             hybrid_corrective_reterieval_node)

def build_graph():
    graph = StateGraph(RagState)


    graph.add_node("query_resolver",resolve_query_node)
    graph.add_node("query_router",router_query_node)
    graph.add_node("dense_retrieval",dense_retrieval_node)
    graph.add_node("bm25_retrieval",bm25_retrieval_node)
    graph.add_node("rrf",rrf_results_node)
    graph.add_node("access_control",access_control_node)
    graph.add_node("reranking",reranker_node)
    graph.add_node("check_relevance",relevance_node)
    graph.add_node("rag_context_builder",rag_context_builder_node)
    graph.add_node("rag_response_generator",rag_response_generator_node)
    graph.add_node("no_context",no_context_node)
    graph.add_node("sql_query_generator",sql_query_generator_node)
    graph.add_node("sql_query_validator",sql_validator_node)
    graph.add_node("sql_result",sql_result_node)
    graph.add_node("sql_context",sql_context_node)
    graph.add_node("sql_response_generator",sql_response_generator_node)
    graph.add_node("hybrid_response_generator",hybrid_responce_generator_node)
    graph.add_node("rag_ready",rag_ready)
    graph.add_node("sql_ready",sql_ready)
    graph.add_node("evidence_checker",evidence_checker_node)
    graph.add_node("hybrid_corrective_retrieval",hybrid_corrective_reterieval_node)

    graph.add_edge(START,"query_resolver")
    graph.add_edge("query_resolver","query_router")
    graph.add_conditional_edges("query_router",route_after_router_node,{
                                            "dense_retrieval":"dense_retrieval","bm25_retrieval":"bm25_retrieval",
                                            "sql_query_generator":"sql_query_generator"})
    graph.add_edge(["dense_retrieval","bm25_retrieval"],"rrf")
    graph.add_edge("rrf","access_control")
    graph.add_edge("access_control","reranking")
    graph.add_edge("reranking","check_relevance")
    graph.add_conditional_edges("check_relevance",route_after_relevance,
                                {"build_context":"rag_context_builder",
                                "no_context":"no_context"})
    graph.add_edge("no_context",END)
    graph.add_conditional_edges("rag_context_builder",route_after_rag_context,{
                                        "rag_response_generator":"rag_response_generator","rag_ready":"rag_ready"})
    graph.add_edge("rag_response_generator",END)
    #graph.add_edge("rag_ready","hybrid_response_generator")
    graph.add_edge("sql_query_generator","sql_query_validator")
    graph.add_edge("sql_query_validator","sql_result")
    graph.add_edge("sql_result","sql_context")
    graph.add_conditional_edges("sql_context",route_after_sql_context,{
                                        "sql_response_generator":"sql_response_generator","sql_ready":"sql_ready"})
    graph.add_edge("sql_response_generator",END)
    graph.add_edge(["rag_ready","sql_ready"],"evidence_checker")
    graph.add_conditional_edges("evidence_checker",route_after_evidence_checker_node,
                                {"answer":"hybrid_response_generator",
                                 "corrective_retrieval":"hybrid_corrective_retrieval"})
    graph.add_edge("hybrid_corrective_retrieval","evidence_checker")
    graph.add_edge("hybrid_response_generator",END)


    checkpointer = InMemorySaver()
    workflow = graph.compile(checkpointer=checkpointer)
    return workflow
    
