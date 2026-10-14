from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)


def format_history(messages: list[BaseMessage]) -> str:
    history = []
    for message in messages:
        if message.type == "human":
            role = "User"
        elif message.type == "ai":
            role = "Assistant"
        else:
            role = message.type
        history.append(f"{role}: {message.content}")
    return "\n".join(history)


def resolve_query(raw_query:str,message_history:list[BaseMessage])->str:

    if not message_history:
        return raw_query
    
    history_text = format_history(messages=message_history)
    
    prompt = f"""
    You are RGD Tech enterprise query resolver assistant.
    You have to rewrite the follow-up questions into standalone question.

    Use the conversation history only to resolve refrences such as:
    it, this order, that product, this refund, they, that product etc.

    Do not add any facts that are not the part of the conversation.

    CONVERSATION_HISTORY: 
    {history_text}

    Current user Question: 
    {raw_query}

    Return only the standalone rewritten question.
    """

    response = llm.invoke(prompt)

    return response.text.strip()






    