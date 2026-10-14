import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,chunk_overlap=150,separators=["\n\n","\n",". ",""]
)

HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$")

def clean_heading(heading:str)->str:

    heading = heading.strip()
    heading = heading.replace("**","") # removing markdown bold marker
    # removing number or any symbool from the heading
    heading = re.sub(r"^\d+(?:\.\d+)*\.?\s*","",heading)

    return heading.strip()

def extract_sections(pages:list[dict])-> list[dict]:

    sections = []

    current_section= "General"
    current_page = 1
    current_line = []

    def save_section():
        if not current_line:
            return
        text = "\n\n".join(current_line)
        if text:
            sections.append({
                "section_heading":current_section,
                "page_number":current_page,
                "text":text
            })

    for page in pages:

        page_number = page["page_number"]
        markdown = page["text"]

        for line in markdown.splitlines():
            line = line.strip()

            if not line:
                if current_line:
                    current_line.append("")
                continue
            
            heading_match = HEADING_PATTERN.match(line) # returns a match object or None, not string containing info about the match and the line

            if heading_match:
                save_section()  # hear this save the previous section 
                # and loop continue for next section
                raw_heading = heading_match.group(1)  # return a string heading by preforming the group(1) opration on match object 
                current_section = clean_heading(raw_heading)
                current_page = page_number
                current_line = []

            else:
                current_line.append(line)

    save_section()
    return sections

def chunk_documents(
        document_id:str,
        file_name:str,
        version:str,
        access_level:str,
        pages:list[dict] ) -> list[dict]:  # here pages is list of dict because the pymupdf4llm returns pages having their page number and text that's why each page is a dictionary

    sections = extract_sections(pages=pages)

    final_chunk = []
    chunk_number = 1

    for section in sections:
        section_name = section["section_heading"] # from def save_section
        page_number = section["page_number"]
        section_text = section["text"]

        pieces = text_splitter.split_text(section_text)

        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            chunk_id = (
                f"{document_id}-"
                f"v{version}-"
                f"chunk-{chunk_number:03d}")
            chunk_text = (
                f"{section_name}\n\n{piece}"
                if section_name != "General"
                else piece )

            final_chunk.append({
                "id" : chunk_id,
                "document_id" : document_id,
                "document_title"
                "file_name" : file_name,
                "version": version,
                "chunk_number":chunk_number,
                "page_number": page_number,
                "section":section_name,
                "access_level":access_level,
                "chunk_text": chunk_text
                })
            chunk_number += 1
    return final_chunk

            

    
            

        
            


