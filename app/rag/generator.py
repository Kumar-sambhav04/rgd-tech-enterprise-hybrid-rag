from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from datetime import date



load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",temperature=0)

current_date = date.today().isoformat()

def generate_answer(query:str,context:str)->str:

    if not context:
        return ("I could not find sufficient relevent authorized information to answer this question")
    
    prompt = f"""You are the RGD Tech enterprise assistant
    Answer the users question using Only the provided context.
    Rules:
    1. Do not use the information outside the provided context.
    2. Every factual statement must include at least one supporting source label such as [SOURCE_1].
    3. Use ONLY the source labels that appear in the context.
    4. If the context does not have enough information to answer the question say tat sufficient information is not available.
    5. Cite the supporting source using the Source Lable exactly as provided, for example [SOURCE_1].
    6. If multiple sources support a statement, cite them like: [SOURCE_1] [SOURCE_2]
    7. Do not invent citations.
    8. Keep the answer clean and consise
    Example: Refund eligibility depends on the product category and applicabl return window. [SOURCE_1]


    Context : 
    {context}

    Todays Date : {current_date}

    User Question :
    {query}
    """

    responce = llm.invoke([HumanMessage(content=context)])

    return responce.text

