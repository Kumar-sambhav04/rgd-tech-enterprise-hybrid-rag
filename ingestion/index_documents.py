import json
from pathlib import Path

from app.retrieval.dense_encoder import embed_chunk
from app.retrieval.bm25_encoder import load_bm25
from app.retrieval.pinecone_client import dense_index, bm25_index

BASE_DIR = Path(__file__).resolve().parent.parent
CHUNK_FILE = BASE_DIR/ "data"/ "chunk_preview.json"

EMBEDDING_DIR = BASE_DIR/ "data"/ "embedding"
DENSE_CACHE_FILE = EMBEDDING_DIR/ "dense_vector.json"

PINECONE_BATCH_SIZE = 20

def load_chunks()-> list[dict]:
    return json.loads(CHUNK_FILE.read_text(encoding="utf-8"))

def get_dense_vector(chunks:list[dict])-> list[list[float]]:
    """This function load cached dense vectors if they exist, Otherwise it create 
     them and store them locally, so if the upserting process fails we dont have to
      do the embedding adain """
    
    if  DENSE_CACHE_FILE.exists():
        print("Loading cached dense embedding")
        cached = json.loads(DENSE_CACHE_FILE.read_text(encoding="utf-8"))
        ## Check if the cached dense vectos is of the same current chunks 
        cached_id = [item["id"] for item in cached]
        chunks_id = [chunk["id"] for chunk in chunks]

        if cached_id != chunks_id:
            raise RuntimeError("The cached dense embedding does not match the current chunk set")
        return [el["vector"] for el in cached]

    print("Generating dense Embedding")
    texts = [text["chunk_text"] for text in chunks]

    vectors = embed_chunk(text=texts)
    if len(vectors)!= len(chunks):
        raise RuntimeError("The number vectors does not match the number of chunks")

    EMBEDDING_DIR.mkdir(parents=True,exist_ok=True)

    cache = [{"id": chunk["id"],"vector":vector} for chunk,vector in zip(chunks,vectors)]

    DENSE_CACHE_FILE.write_text(json.dumps(cache),encoding="utf-8")

    print(f"Dense Vector cached at {DENSE_CACHE_FILE}")
    return vectors

def build_metadata(chunk:dict)->dict:
    return {
        "document_id": chunk["document_id"],
        "file_name":chunk["file_name"],
        "version":chunk["version"],
        "chunk_number":chunk["chunk_number"],
        "page_number":chunk["page_number"],
        "section":chunk["section"],
        "access_level":chunk["access_level"],
        "chunk_text":chunk["chunk_text"]
    } # this can be used by both index because metadata will be same for every chunk

def build_dense_records(chunks:list[dict], dense_vector:list[list[float]])->list[dict]:
    records = []

    for chunk,vector in zip(chunks,dense_vector):
        records.append({
            "id":chunk["id"],
            "values": vector,
            "metadata": build_metadata(chunk)
            })
    return records

def build_bm25_record(chunks:list[dict])->list[dict]:

    bm25 = load_bm25()
    texts = [text["chunk_text"] for text in chunks]

    sparse_vectors = (bm25.encode_documents(texts))

    if len(sparse_vectors) != len(chunks):
        raise RuntimeError("Total number of sparse vector doesnot match the total num of chunks")

    records = []
    for chunk,sparse_vector in zip(chunks,sparse_vectors):
        records.append({
            "id":chunk["id"],
            "sparse_values":{"indices":sparse_vector["indices"],
                             "values":sparse_vector["values"]},
            "metadata":build_metadata(chunk)
        })
    return records

def upsert_records(index, records:list[dict], lable:str):
    total = len(records)

    for els in range(0,total,PINECONE_BATCH_SIZE):
        batch = records[els:els+PINECONE_BATCH_SIZE]

        response = index.upsert(vectors= batch)

        print(f"{lable} {els}to {els+PINECONE_BATCH_SIZE} upserted")

        print(response)

    
def main():

    print("RGD Tech Pinecone Ingestion")

    # _______ Load Chunk _______

    chunks = load_chunks()
    print(f"Chunk loded {len(chunks)}")

    #_______Dense Encodein_______

    dense_vector = get_dense_vector(chunks=chunks)
    print(f"Dense vector {len(dense_vector)}")

    #______Dense Record_________

    dense_record = build_dense_records(chunks=chunks,dense_vector=dense_vector)

    # ________BM25 Record_________

    bm25_record = build_bm25_record(chunks=chunks)
    print(f"BM25 vector {len(bm25_record)}") 
    # BM25 sparse vector is build in this function and its parameter file s alreadu created

    if not len(chunks) == len(dense_record) == len(bm25_record):
        raise RuntimeError("Record count doesnot match")
    print("Record Validation Successful")
    print(f"Chunks : {len(chunks)}")
    print(f"Dense vector : {len(dense_record)}")
    print(f"Sparse vector : {len(bm25_record)}")

    print("Upsertine Dense Records ... ")

    upsert_records(dense_index,dense_record,"Dense Vector")

    print("Upserting BM25 Records ...")

    upsert_records(bm25_index,bm25_record,"BM25")

    print("\n___Injection Complet___\n")

if __name__ == "__main__":
    main()

