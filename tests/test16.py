import json

with open("data/chunk_preview.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    if (
        chunk["document_id"] == "DOC002"
        and "Return Windows" in chunk["section"]
    ):
        print("ID:", chunk["id"])
        print("SECTION:", chunk["section"])
        print("TEXT:")
        print(chunk["chunk_text"])