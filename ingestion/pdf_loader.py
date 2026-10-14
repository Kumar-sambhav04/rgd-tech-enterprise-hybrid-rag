from pathlib import Path


import pymupdf4llm
def load_pdf_pages(pdf_path:Path)-> list[dict]:
    pages = pymupdf4llm.to_markdown(str(pdf_path),
                                    page_chunks=True,
                                    use_ocr=False,
                                    show_progress=False)

    extracted_pages = []

    for page in pages:
        text = page.get("text","").strip()

        metadata = page.get("metadata",{})

        page_number = metadata.get("page_number") or metadata.get("page")

        extracted_pages.append({
            "page_number":page_number,
            "text":text
        })
    return extracted_pages

    


#from langchain_community.document_loaders import PyPDFLoader

#def load_pdf_pages(pdf_path: Path)-> list[dict]:
#   loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

#    pages = []

#    for doc in documents:
#        text = doc.page_content.strip()

#        if not text:
#            continue

#        page_number = doc.metadata.get("page",0) + 1

#        pages.append({
#            "page_number":page_number,
#            "text":text
#        })
#    return pages
