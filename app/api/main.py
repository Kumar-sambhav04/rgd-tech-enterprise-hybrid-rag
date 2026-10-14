from typing import Literal
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level= logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

logger = logging.getLogger(__name__)

from app.graph.rgd_assistant_executor import run_rgd_assistant

app = FastAPI(title= "RGD Tech Enterprise Assistant API",
              version= "1.0.0")

class ChatRequest(BaseModel):
    query:str
    role: Literal["support","admin"]
    thread_id:str

class Source(BaseModel):
    source_id:str
    chunk_id:str
    file_name:str | None = None
    section:str | None = None
    page_number:int | None = None

class ChatResponse(BaseModel):
    answer:str
    route: str | None = None
    sources: list[Source]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):
    try:
        result = run_rgd_assistant(query=request.query,
                               role=request.role,
                               thread_id=request.thread_id)
        return result
    except Exception as e:

        logger.exception("Error while processing the chat request.")
        raise HTTPException(status_code=500,detail= "Unable to process the request at this time.") from e