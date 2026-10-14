from app.database.connection import DBRole,get_engine
from sqlalchemy import text

def execute_sql(sql:str,role:DBRole)->list[dict]:
    """Execute validated SQL query using role specific PostgreSQL connection"""

    engine = get_engine(role)

    with engine.connect() as connection:
        result = connection.execute(text(sql))

        rows = result.mappings().all()

    return [dict(row) for row in rows]