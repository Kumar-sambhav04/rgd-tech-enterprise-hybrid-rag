import time

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    output_dimensionality=768,
    vertexai=False
)

def embed_chunk(text:list[str],batch_size:int=20)->list[list[float]]:
    all_vectors = []

    for el in range(0,len(text),batch_size):
        batch = text[el:el + batch_size]  # each batch will be updated

        print(
            f"Embedding Chunks"
            f"{el+1} to {el +len(batch)}")

        vectors = embeddings.embed_documents(batch)

        all_vectors.extend(vectors)

        if el + batch_size < len(text):
            time.sleep(20)
    return all_vectors

def embed_query(query:str)-> list[float]:
    """Generate embeddings for user query"""
    return embeddings.embed_query(query)

