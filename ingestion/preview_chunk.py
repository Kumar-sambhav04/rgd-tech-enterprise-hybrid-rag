from pathlib import Path
import json
from sqlalchemy import text

from app.database.connection import get_admin_engine
from ingestion.pdf_loader import load_pdf_pages
from ingestion.chunker import chunk_documents

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR/ "data" / "documents"
OUTPUT_FILE = BASE_DIR / "data"/ "chunk_preview.json"

def get_active_db_document():
    """Reade details metadata from postgres SQL"""

    engine = get_admin_engine()

    query = text("""
        SELECT document_id,filename, version ,access_level from rgd.documents
          WHERE status = 'active' ORDER BY document_id
    """)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    return rows

def main():
    documents = get_active_db_document()
    all_chunks = []

    print("\n========RGD Tech chunk preview========\n")

    for doc in documents:
        document_id = doc["document_id"]
        filename = doc["filename"]
        version = doc["version"]
        access_level = doc["access_level"]

        pdf_path = DOCUMENTS_DIR/ filename

        if not pdf_path.exists():
            print(f"Missing PDF |"
                  f"{document_id} | {filename}")
            continue

        pages = load_pdf_pages(pdf_path=pdf_path)

        chunks = chunk_documents(
            document_id= document_id,
            file_name=filename,
            version=version,
            access_level=access_level,
            pages= pages
        )
        all_chunks.extend(chunks)

        print(f"{document_id} |"
              f"{filename} |"
              f"Pages= {len(pages)} |"
              f"Chunks= {len(chunks)}"
              f"{access_level}"
        )

    OUTPUT_FILE.write_text(json.dumps(all_chunks,
                         indent=2,ensure_ascii=False), encoding= "utf-8")

    print("\n"+ "="*50)

    print(f"Document Found = {len(documents)}")
    print(f"Toral Chunks = {len(all_chunks)}")
    print(f"Preview file = {OUTPUT_FILE}")

if __name__ == "__main__":
    main()