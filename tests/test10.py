from app.database.sql_generator import generate_sql_query
from app.database.connection import DBRole

responce = generate_sql_query(
    query="What is the status of order O1012?",
    role=DBRole.SUPPORT
)
print(responce)