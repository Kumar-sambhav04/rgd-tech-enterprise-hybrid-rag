

def sql_context_builder(sql_results:list[dict])->str:
    if not sql_results:
        return "No matching database results we found."

    rows = []

    for i, row in enumerate(sql_results,start=1):
        rows.append(f"Row_{i} : {row}")

    return "\n".join(rows)

