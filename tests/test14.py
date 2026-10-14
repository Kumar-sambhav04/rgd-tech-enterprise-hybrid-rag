from app.graph.workflow import build_rag_graph


graph = build_rag_graph()


tests = [
    {
        "name": "RAG",
        "query": "What are the conditions for receiving a refund?",
        "role": "support"
    },
    {
        "name": "SQL",
        "query": "What is the status of order O1012?",
        "role": "support"
    },
    {
        "name": "HYBRID",
        "query": "Order O1012 has been delivered. Based on RGD Tech policy, can it still be returned?",
        "role": "support"
    }
]


for test in tests:

    print("\n" + "=" * 70)
    print(test["name"])
    print("=" * 70)

    result = graph.invoke({
        "query": test["query"],
        "role": test["role"]
    })

    print("Route :", result.get("route"))
    print("Answer:")
    print(result.get("answer"))
    print(result.get("validated_sql"))
    print(result.get("sql_context"))