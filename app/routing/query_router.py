from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class route_decision(BaseModel):
    route: Literal["rag","sql","hybrid"]

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",temperature=0)
router_llm = llm.with_structured_output(route_decision)

def route_query(query:str)->str:
    prompt = f"""
You are a query router for RGD Tech enterprice assistant.
Classify user question into exactly one route.

rag:
Use When the answer of the user question come from policies, procedures, product documentation,
support documentation, warranty, shipping, return, refunds, rules, and other unstructured documents.

sql:
Use when the answer of the users question requires structured business records such as:
customers information, order, payments, shhipment, refund records, return, inventory, employees, 
and other database records.

hybrid:
Use when the answer requires BOTH, structured business information AND policy / documents information

EXamples:
Question: What is RGD Tech refund policy?
route: rag

Question: What is status of order O1012?
route: sql

Question: Has refund RF005 has been processed?
route: sql

Question: Order O1012 was dilivered 20 days ago. Can it still be returned?
route: hybrid

Question: Is customers C004 returned laptop eligible for a refund ?
route: hybrid
.


USERS_QUESTION: 
{query}
""" 
    responce = router_llm.invoke(prompt)

    return responce.route
