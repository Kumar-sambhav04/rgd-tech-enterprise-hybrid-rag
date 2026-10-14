import os 

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
DENSE_INDEX_NAME= os.getenv("PINECONE_DENSE_INDEX")
BM25_INDEX_NAME= os.getenv("PINECONE_BM25_INDEX")

if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE API KEY is missing")
if not DENSE_INDEX_NAME:
    raise RuntimeError("DENSE_INDEX_NAME is missing")
if not BM25_INDEX_NAME:
    raise RuntimeError("BM25_INDEX_NAME is missing")

pc = Pinecone(api_key=PINECONE_API_KEY)

dense_index = pc.Index(DENSE_INDEX_NAME)
bm25_index = pc.Index(BM25_INDEX_NAME)



