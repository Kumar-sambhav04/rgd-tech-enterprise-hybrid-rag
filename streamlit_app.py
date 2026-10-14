import streamlit as st
import uuid
import requests
from dotenv import load_dotenv
import os


load_dotenv()

API_BASE_URL= os.getenv("API_BASE_URL","http://127.0.0.1:8000")

#from app.graph.rds_assistant_executor import run_rgd_assistant


st.set_page_config(
    page_title="RGD Tech Assistant",
    page_icon="🤖",
    layout="centered")

st.title("RGD Tech Enterprise Assistant")


def reset_chat():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_role" not in st.session_state:
    st.session_state.active_role = "support"


role = st.selectbox(
    "User Role",
    ["support", "admin"]
)


if role != st.session_state.active_role:
    st.session_state.active_role = role
    reset_chat()


if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()
# -------------------------
# Role
# -------------------------

#role = st.selectbox(
#    "User Role",
#    ["support", "admin"])


# -------------------------
# Existing messages
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:
                with st.expander("Context Sources"):
                    for source in sources:
                        st.markdown(
                            f"""
**{source["source_id"]}**  
File: `{source["file_name"]}`  
Section: {source["section"]}  
Page: {source["page_number"]}
"""
                        )


# -------------------------
# User input
# -------------------------

query = st.chat_input("Ask RGD Tech...")


if query:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)


    # Run assistant
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            try:


                response = requests.post(f"{API_BASE_URL}/chat",json={
                        "query": query,
                        "role": role,
                        "thread_id": st.session_state.thread_id},
                        timeout=120)

                response.raise_for_status()
                result = response.json()
                #result = run_rgd_assistant(
                #    query=query,
                #    role=role,
                #    thread_id=st.session_state.thread_id)
                answer = result["answer"]
                
                sources = result.get("sources", [])
            except requests.exceptions.Timeout:
                answer = ("The request take too long to complete. Plese try again later.")
                sources = []
            except requests.exceptions.ConnectionError:
                answer = ("The assistant service is Unavailable, Please try again shortly")
                sources = []
            except requests.exceptions.HTTPError:
                answer = ("The assistant encountered an error while processing your request")
                sources = []
            except Exception:
                answer = ("An unexpected error occured, please try again")
                sources = []

        st.markdown(answer)

        #answer = result["answer"]
        #st.markdown(answer)
        #sources = result.get("sources", [])

        if sources:
            with st.expander("Sources"):
                for source in sources:
                    st.markdown(
                f"""
                **{source["source_id"]}**  
                File: `{source["file_name"]}`  
                Section: {source["section"]}  
                Page: {source["page_number"]}
                """)
        #st.write("DEBUG SOURCES:")
        #st.write(sources)


    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })