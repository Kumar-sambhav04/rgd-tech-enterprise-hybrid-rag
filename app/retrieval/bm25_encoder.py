from pathlib import Path

from pinecone_text.sparse import BM25Encoder

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BM25_DIR = BASE_DIR / "data" / "BM25"
BM25_PARAMS_FILE = BM25_DIR/"bm25_params.json"

def fit_bm25(text:list[str])-> BM25Encoder:
    """Fit BM25 using whole chunk corpous"""

    bm25 = BM25Encoder()
    bm25.fit(text)

    BM25_DIR.mkdir(parents=True, exist_ok= True)

    bm25.dump(str(BM25_PARAMS_FILE))

    return bm25

def load_bm25()->BM25Encoder:
    """Load previously fitted BM25 paramaters
    will be used at query time or retrival time"""

    if not BM25_PARAMS_FILE:
        raise FileNotFoundError(f"BM25 parameter file not  found: {BM25_PARAMS_FILE}")

    bm25 = BM25Encoder()
    bm25= bm25.load(str(BM25_PARAMS_FILE))

    return bm25

def encode_query(query:str)->dict:
    ## Encode using previously fitted bm25 parameters 
    bm25 = load_bm25()
    sparse_vector = bm25.encode_queries(query)

    # encode_queries and encode_documents is function of BM25Encoder
    return sparse_vector

# 