from app.graph.workflow import build_rag_graph

graph = build_rag_graph()

result = graph.invoke({
    "query": "What are the conditions for receiving a refund?",
    "role": "support"
})

print("\nFINAL ANSWER\n")
print(result["answer"])