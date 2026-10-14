from typing_extensions import TypedDict, Required,NotRequired,Annotated,Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class RagState(TypedDict):
    # input
    raw_query: Required[str]
    
    role: Required[str]
    query: NotRequired[str]

    messages: NotRequired[Annotated[list[BaseMessage],add_messages]]

    # retrieval
    dense_results:NotRequired[list[dict]]
    bm25_results: NotRequired[list[dict]]

    # fused resulte
    rrf_results:NotRequired[list[dict]]
    # alc filtration
    authorized_results:NotRequired[list[dict]]

    #reranked results
    reranked_results:NotRequired[list[dict]]
    # relevent results
    relevant_results:NotRequired[list[dict]]

    # generation
    rag_context : NotRequired[str]
    answer:NotRequired[str]

    #citation
    valid_citation: NotRequired[bool]

    # PostgresSQL database state
    sql_query: NotRequired[str]
    validated_sql: NotRequired[str]
    sql_result: NotRequired[list[dict]]
    sql_context: NotRequired[str]

    
    route: NotRequired[str]

    # hybrid query re reterival
    sufficient_evidence: NotRequired[bool]
    missing_information: NotRequired[str]
    next_step: NotRequired[Literal["rag","sql","both","answer"]]
    corrective_rag_query:NotRequired[str]
    corrective_sql_query:NotRequired[str]
    hybrid_retry_count:NotRequired[int]
    