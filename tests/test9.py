from app.database.schema_context import (
    get_schema_context,
)

from app.database.connection import DBRole


schema = get_schema_context(
    DBRole.SUPPORT
)

print(schema)