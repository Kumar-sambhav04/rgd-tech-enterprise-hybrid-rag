from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from datetime import date


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",temperature=0)
current_date = date.today().isoformat()
def hybrid_responce_generator(rag_context:str,sql_context:str,query)->str:

    prompt = f"""
You are RGD Tech Enterprise assistant
Answer the users question using both 
1. The structures database results.
2. and policy / document context

Rules:
1. Use database results for specific business facts such as order status, delivery date, 
   payment status, return status, refund status, customer information, or product information.
2. Use document context for policies, rules, eligibility, procedures, and guidelines.
3. Do not invent information.
4. Cite policy/document claims using the provided source labels such as [SOURCE_1].
5. Do not invent source labels.
6. If the available information is insufficient, say so clearly.
7. Keep the answer clear and concise.

DATABASE_RESULT: {sql_context}

DOCUMENT_CONTEXT : {rag_context}

Todays Date : {current_date}

USERS_QUESTION : {query}
"""
    response = llm.invoke(prompt)
    return response.text
