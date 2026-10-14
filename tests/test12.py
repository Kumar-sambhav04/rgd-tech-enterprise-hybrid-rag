from app.database.connection import DBRole

from app.database.sql_generator import generate_sql_query
from app.database.sql_validator import validate_sql
from app.database.sql_executor import execute_sql

query = "What is the status of order O1012"
role = DBRole.SUPPORT

sql = generate_sql_query(query=query,role=role)

print("\n Generated SQL Query Successfully:")
print(sql)

validated_sql = validate_sql(sql=sql,role=role)

print("SQL query validated successfully")
print(validated_sql)

result = execute_sql(sql=validated_sql,role=role)

print("\nSQL Result:")
print(result)

