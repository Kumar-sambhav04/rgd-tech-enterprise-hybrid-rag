from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import date
from typing import Literal,Optional


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",temperature=0)

class EvidenceDecision(BaseModel):
    suficient: bool
    missing_info:Optional[str] = None
    next_action: Literal["answer","rag","sql","both"]
    rag_query:Optional[str] = None
    sql_query:Optional[str] = None

structured_llm = llm.with_structured_output(EvidenceDecision)

def check_hybrid_evidence(query:str,rag_context:str,sql_context:str)->EvidenceDecision:
    current_date = date.today().isoformat()

    prompt = f"""
You are the Evidence sufficency checker for the RGD Tech enterprise assistant.
Your job is not to answer the user's question.
Your job is to determine that wether the current retrived Structured and Unstructured document
are sufficient for anothoer model to answer the user's question completely or it needs more information.

Current Date: {current_date}
Users_question: {query}
Policy / Document Evidence: {rag_context}
Structured Database Evidence: {sql_context}

Rules:
1. Mark the evidence as sufficient only when the available evidance contains the facts and
policies requires to answer the question
2. Do not assume or invent missing facts.
3. If the information is missing from company policies/documents, set the next_action = "rag"
4. If the information is missing from structured company records, set the next_action = "sql"
5. If the both type of information is missing, set the next_action = "both"
6. If the evidence is sufficient set:
    sufficient = "true"
    next_action = "answer"
    rag_query = null
    sql_squey = null
7. If additional document,policy/ Rag-retrieval is required, create a precise standalone reterieval
query using facts already dictovered and what need to be reterieve more, and set this new query to rag_query .
8. If additional SQL reterieval is required create a precise natural language sql request query describing
exactly what structured information must be reterieved, and set this new query to sql_query.
9. Do not reterieve the information which is already given in the evidence.
10. Keep the corrective query focused only for the missng eidence.

"""

    return structured_llm.invoke(prompt)
