def build_context(results:list[dict])->str:

    if not results:
        return ""

    context = []

    for i , result in enumerate(results,start=1):

        metadata = result["metadata"]

        context.append(
            f"""
[SOURCE_{i}]
File Name : {metadata.get("file_name")}
Sections : {metadata.get("section")}
Page Number : {metadata.get("page_number")}

{metadata.get("chunk_text","")}""".strip()
        )

    return "\n\n".join(context)
