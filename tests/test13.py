from app.routing.query_router import route_query


queries = [
    "What is the refund policy?",
    "What is the status of order O1012?",
    "Order O1012 was delivered 20 days ago. Can it still be returned?"
]


for query in queries:

    route = route_query(query)

    print("\nQuery:", query)
    print("Route:", route)