from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from datetime import date


load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-3.8-flash",temperature=0)
current_date = date.today().isoformat()


def sql_responce_generator(sql_context:str,query:str)->str:
    prompt = f"""
You are RGD Tech Enterprise assistant.
Answer the users questions using ONLY the database result provided bellow.
Rules:
1. Use only result provided in database result.
2. Do not invent missing values.
3. If no matching record is found in database result then clearly say so.
4. Give a consise and natural answer
5. Do not mention SQL or internal database implementation unless necessary.

DATABASE_RESULTS : {sql_context}
Todays Date : {current_date}

USERS_QUESTION : {query}
"""

    responce = llm.invoke(prompt)

    return responce.text