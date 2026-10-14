from app.database.sql_validator import validate_sql
from app.database.connection import DBRole


from app.database.connection import DBRole
from app.database.sql_validator import validate_sql


# 1. Valid query
print("TEST 1")

sql = validate_sql(
    "SELECT order_status FROM rgd.orders WHERE order_id = 'O1012'",
    DBRole.SUPPORT
)

print("Passed:")
print(sql)


# 2. DELETE should fail
print("\nTEST 2")

try:
    validate_sql(
        "DELETE FROM rgd.orders WHERE order_id = 'O1012'",
        DBRole.SUPPORT
    )

except ValueError as e:
    print("Blocked correctly:")
    print(e)


# 3. Admin-only table should fail for support
print("\nTEST 3")

try:
    validate_sql(
        "SELECT * FROM rgd.employees",
        DBRole.SUPPORT
    )

except ValueError as e:
    print("Blocked correctly:")
    print(e)

"""
# 1. Should pass
validate_sql(
    "SELECT order_status FROM rgd.orders WHERE order_id = 'O1012'",
    DBRole.SUPPORT
)

# 2. Should fail: write operation
validate_sql(
    "DELETE FROM rgd.orders WHERE order_id = 'O1012'",
    DBRole.SUPPORT
)

# 3. Should fail: support user accessing admin-only table
validate_sql(
    "SELECT * FROM rgd.employees",
    DBRole.SUPPORT
)"""
