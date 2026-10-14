from app.retrieval.dense_retriever import dense_retriever
from app.retrieval.bm25_retriever import bm25_retriever
from app.retrieval.rrf import reciprocal_rank_fusion
from app.authorization.access_control import (apply_ac,UserRole)

query = "What are the internal employee compensation guidelines?"


print("\n==============================")
print("DENSE RETRIEVAL")
print("==============================\n")

dense_results = dense_retriever(
    query=query,
    top_k=5
)


for result in dense_results:

    metadata = result["metadata"]

    print(f"Rank       : {result['rank']}")
    print(f"ID         : {result['id']}")
    print(f"Score      : {result['score']}")
    print(f"File       : {metadata.get('file_name')}")
    print(f"Section    : {metadata.get('section')}")
    print(f"Access     : {metadata.get('access_level')}")
    print(f"Text       : {metadata.get('chunk_text')}")
    print("-" * 70)


print("\n==============================")
print("BM25 RETRIEVAL")
print("==============================\n")

bm25_results = bm25_retriever(
    query=query,
    top_k=5
)


for result in bm25_results:

    metadata = result["metadata"]

    print(f"Rank       : {result['rank']}")
    print(f"ID         : {result['id']}")
    print(f"Score      : {result['score']}")
    print(f"File       : {metadata.get('file_name')}")
    print(f"Section    : {metadata.get('section')}")
    print(f"Access     : {metadata.get('access_level')}")
    print(f"Text       : {metadata.get('chunk_text')}")
    print("-" * 70)


##________________________________________________________


fused_results = reciprocal_rank_fusion(
    dense_results=dense_results,
    bm25_results=bm25_results
)


print("\n==============================")
print("RRF FUSION")
print("==============================\n")


for result in fused_results:

    metadata = result["metadata"]

    print(f"Rank       : {result['rank']}")
    print(f"ID         : {result['id']}")
    print(f"RRF Score  : {result['rrf_score']}")
    print(f"Sources    : {result['sources']}")
    print(f"File       : {metadata.get('file_name')}")
    print(f"Section    : {metadata.get('section')}")
    print(f"Access     : {metadata.get('access_level')}")
    print(f"Text       : {metadata.get('chunk_text')}")
    print("-" * 70)

    #------------------------------------------------------------
print("="*70)
print("SUPPORT RESULTS ONLY")

support_results = apply_ac(fused_results,UserRole.SUPPORT)

for result in support_results:

    metadata = result["metadata"]

    print(f"Rank       : {result['rank']}")
    print(f"ID         : {result['id']}")
    print(f"RRF Score  : {result['rrf_score']}")
    print(f"Sources    : {result['sources']}")
    print(f"File       : {metadata.get('file_name')}")
    print(f"Section    : {metadata.get('section')}")
    print(f"Access     : {metadata.get('access_level')}")
    print(f"Text       : {metadata.get('chunk_text')}")
    print("-" * 70)


print("="*70)
print("SUPPORT RESULTS ONLY")

authorized_results = apply_ac(fused_results,UserRole.ADMIN)
for result in authorized_results:

    metadata = result["metadata"]

    print(f"Rank       : {result['rank']}")
    print(f"ID         : {result['id']}")
    print(f"RRF Score  : {result['rrf_score']}")
    print(f"Sources    : {result['sources']}")
    print(f"File       : {metadata.get('file_name')}")
    print(f"Section    : {metadata.get('section')}")
    print(f"Access     : {metadata.get('access_level')}")
    print(f"Text       : {metadata.get('chunk_text')}")
    print("-" * 70)

from app.retrieval.reranker import rerank_results


relevant_results = rerank_results(
    query=query,
    results=authorized_results,
    top_k=5)

print("\n" + "=" * 70)
print("RERANKED RESULTS")
print("=" * 70)

for result in relevant_results:

    metadata = result["metadata"]

    print(f"Rank          : {result['rank']}")
    print(f"Previous Rank : {result['rrf_rank']}")
    print(f"ID            : {result['id']}")
    print(f"RRF Score     : {result['rrf_score']}")
    print(f"Rerank Score  : {result['rerank_score']}")
    print(f"File          : {metadata.get('file_name')}")
    print(f"Section       : {metadata.get('section')}")
    print(f"Access        : {metadata.get('access_level')}")
    print(f"Text          : {metadata.get('chunk_text')}")
    print("-" * 70)

from app.rag.context_builder import build_context
from app.rag.generator import generate_answer


context = build_context(relevant_results)

answer = generate_answer(
    query=query,
    context=context
)

print("\n==============================")
print("GENERATED ANSWER")
print("==============================\n")

print(answer)