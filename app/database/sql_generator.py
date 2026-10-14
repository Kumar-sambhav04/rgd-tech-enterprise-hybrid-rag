from langchain_google_genai import ChatGoogleGenerativeAI

from app.database.schema_context import get_schema_context
from app.database.connection import DBRole
from dotenv import load_dotenv

load_dotenv

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",
    temperature=0)

def generate_sql_query(query:str,role:DBRole)->str:

    schema_context = get_schema_context(role=role)

    prompt = f"""
You are a PostgreSQL SQL generator for RGD Tech database.
Generate read only PostgreQL query that answers the user's question,
Rules:
1. Use only the tables and columns exactly as scown in schema context bellow.
2. Use schema name "rgd" explicitly for every table.
3. Generate only SELECT or WITh queries
4. Never generate INSERT , UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, or  REVOKE even if the question requires something like this.
5. Do not invent table or columns.
6. Use join when needed.
7.  Return only SQL query.
8. Do not include markdown code fences.
9. Do not include explainations.

For questions that require applying a policy or rule to a specific
customer/order/product/return/refund, retrieve ALL structured facts
that may be necessary to evaluate that policy.

For example, return-eligibility questions may require:
- order ID
- product name/category
- actual delivery date
- order status
- return information

Use the necessary JOINs rather than retrieving only one obvious field.

DATABASE SCHEMA : {schema_context}
USER QUESTION : {query}
"""
    responce = llm.invoke(prompt)

    sql = responce.text.strip()

    return sql
