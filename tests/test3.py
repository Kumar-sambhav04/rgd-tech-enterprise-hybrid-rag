from pathlib import Path

from ingestion.pdf_loader import load_pdf_pages
from ingestion.chunker import chunk_documents


pdf_path = Path("data/documents/refund_policy_2026.pdf")

pages = load_pdf_pages(pdf_path)

chunks = chunk_documents(
    document_id="DOC001",
    file_name="refund_policy_2026.pdf",
    version="2026.1",
    access_level="support",
    pages=pages,
)


print(f"\nTotal chunks: {len(chunks)}")


for chunk in chunks:

    print("\n" + "=" * 80)

    print("ID:", chunk["id"])
    print("Page:", chunk["page_number"])
    print("Section:", chunk["section"])
    print("Characters:", len(chunk["chunk_text"]))
    print("Access:", chunk["access_level"])

    print("\nTEXT:\n")
    print(chunk["chunk_text"])