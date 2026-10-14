from app.graph.state import RagState
from langchain_core.messages import HumanMessage,AIMessage

from app.routing.query_resolver import resolve_query
from app.retrieval.dense_retriever import dense_retriever
from app.retrieval.bm25_retriever import bm25_retriever
from app.retrieval.rrf import reciprocal_rank_fusion
from app.authorization.access_control import apply_ac,UserRole
from app.retrieval.reranker import rerank_results
from app.retrieval.relevancy import filter_relevant_results, has_relevent_context
from app.rag.context_builder import build_context
from app.rag.generator import generate_answer
from app.database.connection import DBRole
from app.database.sql_generator import generate_sql_query
from app.database.sql_validator import validate_sql
from app.database.sql_executor import execute_sql
from app.routing.query_router import route_query
from app.database.sql_context_builder import sql_context_builder
from app.rag.sql_response_generator import sql_responce_generator
from app.rag.hybrid_responce_generator import hybrid_responce_generator
from app.routing.evidence_checker import check_hybrid_evidence
from app.retrieval.corrective_rag_retrival import corrective_rag_pipeline,merge_rag_results
from app.retrieval.corrective_sql_retrieval import corrective_sql_pipeline,merge_sql_context


def resolve_query_node(state:RagState)->str:
    new_query = resolve_query(raw_query=state['raw_query'],
                              message_history=state.get("messages",[]))
    return {"query": new_query,"hybrid_retry_count":0}

def router_query_node(state:RagState)->dict:
    responce = route_query(state['query'])

    return {"route": responce,
            "messages":[HumanMessage(content=state["raw_query"])]}

def route_after_router_node(state:RagState)->str:
    if state['route'] == "rag":
        return ["dense_retrieval", "bm25_retrieval"]
    if state["route"] == "sql":
        return "sql_query_generator"
    if state["route"] == "hybrid":
        return ["dense_retrieval","bm25_retrieval","sql_query_generator"]

def dense_retrieval_node(state:RagState)->dict:
    results = dense_retriever(state['query'], top_k=10)

    return {'dense_results': results}

def bm25_retrieval_node(state:RagState)->dict:
    results = bm25_retriever(state['query'],top_k=10)

    return {'bm25_results': results}

def rrf_results_node(state:RagState)->dict:
    results = reciprocal_rank_fusion(dense_results=state['dense_results'],
                                     bm25_results=state['bm25_results'])

    return {'rrf_results':results}

def access_control_node(state:RagState)->dict:
    role = UserRole(state['role'])

    results = apply_ac(results=state['rrf_results'],role=role)
    return {'authorized_results': results}

def reranker_node(state:RagState)->dict:

    results = rerank_results(query=state['query'],results=state['authorized_results'],top_k=5)

    return {'reranked_results':results}

def relevance_node(state:RagState)->dict:
    result = filter_relevant_results(results=state['reranked_results'],threshold=0.0)

    return {'relevant_results':result}

def route_after_relevance(state:RagState)->dict:
    if state['relevant_results']:
        return "build_context"
    if state['route'] == "hybrid":
        return "build_context"
    
    return "no_context"

def no_context_node(state:RagState)->dict:
    return {'answer': 'I could not find sufficient relevent authorized information to answer this question'}


def rag_context_builder_node(state:RagState)->dict:
    result = build_context(results=state['relevant_results'])

    return {'rag_context': result}

def route_after_rag_context(state:RagState)->str:
    if state['route'] == "rag":
        return "rag_response_generator"
    if state['route'] == "hybrid":
        return "rag_ready"
    raise ValueError(f"Unexpected route after rag_context: {state['route']}")

def rag_response_generator_node(state:RagState)->dict:
    result = generate_answer(query=state['query'],context=state['rag_context'])

    return {'answer':result,
            "messages":[AIMessage(content=result)]}



#   SQL DATABASE SIDE NODES

def sql_query_generator_node(state:RagState)->dict:
    role = DBRole(state['role'])
    sql = generate_sql_query(state['query'],role=role)
    return {"sql_query": sql}

def sql_validator_node(state:RagState)->dict:
    role = DBRole(state['role'])
    val_sql= validate_sql(sql=state['sql_query'],role=role)
    return {"validated_sql": val_sql}

def sql_result_node(state:RagState)->list[dict]:
    role = DBRole(state["role"])
    result = execute_sql(sql=state['validated_sql'],role=role)
    return {"sql_result": result}

def sql_context_node(state:RagState)->str:
    context = sql_context_builder(sql_results=state['sql_result'])
    return {"sql_context": context}

def route_after_sql_context(state:RagState)->str:
    if state['route'] == "sql":
        return "sql_response_generator"
    if state['route'] == "hybrid":
        return "sql_ready"
    raise ValueError(f"Unexpected route after sql_context : {state['route']}")

def sql_response_generator_node(state:RagState)->str:
    response = sql_responce_generator(sql_context=state['sql_context'],query=state['query'])
    return {"answer":response,
            "messages":[AIMessage(content=response)]}

def hybrid_responce_generator_node(state:RagState)->str:
    response = hybrid_responce_generator(rag_context=state['rag_context'],
                                         sql_context=state['sql_context'],
                                         query=state['query'])
    return {"answer":response,
            "messages":[AIMessage(content=response)]}

def rag_ready(state:RagState):
    return {}

def sql_ready(state:RagState):
    return {}

def evidence_checker_node(state:RagState)->dict:
    response = check_hybrid_evidence(query=state['query'],rag_context=state.get("rag_context",""),
                                     sql_context=state.get("sql_context",""))
    return {"sufficient_evidence":response.suficient,
            "missing_information":response.missing_info,
            "next_step":response.next_action,
            "corrective_rag_query":response.rag_query,
            "corrective_sql_query":response.sql_query}

def route_after_evidence_checker_node(state:RagState)->dict:
    if state["sufficient_evidence"]:
        return "answer"
    retry_count = state.get("hybrid_retry_count")
    if retry_count >= 2:
        return "answer"
    return "corrective_retrieval"



def hybrid_corrective_reterieval_node(state:RagState)->dict:
    action = state["next_step"]
    updates = {}
    if action == "rag":
        rag_output = corrective_rag_pipeline(query=state.get("corrective_rag_query",""),role=state["role"])
        merged_result = merge_rag_results(old_context=state.get("relevant_results",[]),
                                            new_context=rag_output["result"])
        final_context = build_context(results=merged_result)
        return {"relevant_results":merged_result,
                "rag_context":final_context,
                "hybrid_retry_count": state.get("hybrid_retry_count",0)+1}
    elif action == "sql":
        sql_output = corrective_sql_pipeline(query=state.get("corrective_sql_query",""),role=state["role"])
        merged_context  = merge_sql_context(old_context=state.get("sql_context",""),
                                       new_context=sql_output["context"])
        return {"sql_context":merged_context,
               "hybrid_retry_count": state.get("hybrid_retry_count",0)+1}
    elif action == "both":
        sql_output = corrective_sql_pipeline(query=state.get("corrective_sql_query",""),role=state["role"])
        merged_context  = merge_sql_context(old_context=state.get("sql_context",""),
                                               new_context=sql_output["context"])
        rag_output = corrective_rag_pipeline(query=state.get("corrective_rag_query",""),role=state["role"])
      
        merged_result = merge_rag_results(old_context=state.get("relevant_results",[]),
                                                    new_context=rag_output["result"])
        final_context = build_context(results=merged_result)
        return {"sql_context":merged_context,
               "hybrid_retry_count": state.get("hybrid_retry_count",0)+1,
               "relevant_results":merged_result,
               "rag_context":final_context}
    else:
        raise ValueError(f"Invalid corrective retrival action: {action}")

    
        