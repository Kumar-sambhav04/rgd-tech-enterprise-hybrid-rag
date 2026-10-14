from app.database.sql_generator import generate_sql_query
from app.database.sql_validator import validate_sql
from app.database.sql_executor import execute_sql
from app.database.sql_context_builder import sql_context_builder

def corrective_sql_pipeline(query:str,role:str)->dict:
    sql_query = generate_sql_query(query=query,role=role)
    validated_query = validate_sql(sql=sql_query,role=role)
    sql_output = execute_sql(sql=validated_query,role=role)
    context = sql_context_builder(sql_results=sql_output)

    return {
        "sql_query": validated_query,
        "result": sql_output,
        "context":context
    }

def merge_sql_context(old_context:str,new_context:str)->str:
    return "\n\n".join(context for context in [old_context,new_context] if context)