from sqlalchemy import inspect

from app.database.connection import (get_engine,DBRole)

SUPPORT_TABLES = {
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "returns",
    "refunds",
    "documents",
    "document_chunks"
}
ADMIN_TABLES = {
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "returns",
    "refunds",
    "warehouses",
    "inventory"
    "employees",
    "documents",
    "document_chunks"
}

def get_allowed_tables(role:DBRole)->set[str]:
    if role == DBRole.SUPPORT:
        return SUPPORT_TABLES
    if role == DBRole.ADMIN:
        return ADMIN_TABLES
    raise ValueError(f"Unsupported database role: {role}")


def get_schema_context(role:DBRole)->str:

    engine = get_engine(role)
    inspector = inspect(engine)

    allowed_tables = get_allowed_tables(role=role)

    schema_parts = []

    for table_name in sorted(allowed_tables):
        columns = inspector.get_columns(table_name=table_name,schema="rgd")

        columns_lines = []
        for column in columns:
            columns_lines.append(f"-{column['name']}: {column['type']}")

        table_schema = (
                f"Table: rgd.{table_name}\n"
                +"\n".join(columns_lines)
                )
        schema_parts.append(table_schema)

    return "\n\n".join(schema_parts)

