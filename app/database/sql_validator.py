# i have generated this code through AI
import sqlglot
from sqlglot import exp

from app.database.connection import DBRole
from app.database.schema_context import get_allowed_tables


FORBIDDEN_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
    exp.Merge,
)


def validate_sql(
    sql: str,
    role: DBRole
) -> dict:
    """
    Validate generated SQL before execution.

    Returns the SQL if valid.
    Raises ValueError if unsafe or unauthorized.
    """

    # -------------------------
    # Parse SQL
    # -------------------------

    try:
        statements = sqlglot.parse(
            sql,
            read="postgres"
        )

    except Exception as exc:
        raise ValueError(
            f"Invalid SQL syntax: {exc}"
        )


    # -------------------------
    # Only one statement
    # -------------------------

    if len(statements) != 1:
        raise ValueError(
            "Only one SQL statement is allowed."
        )


    statement = statements[0]


    # -------------------------
    # Must be a query
    # -------------------------

    if not isinstance(statement, exp.Query):
        raise ValueError(
            "Only read-only SELECT queries are allowed."
        )


    # -------------------------
    # Block dangerous operations
    # -------------------------

    for forbidden_type in FORBIDDEN_EXPRESSIONS:

        if statement.find(forbidden_type):
            raise ValueError(
                f"Forbidden SQL operation: "
                f"{forbidden_type.__name__}"
            )


    # -------------------------
    # Check authorized tables
    # -------------------------

    allowed_tables = get_allowed_tables(role)


    # CTE names are temporary query names,
    # not real database tables.
    cte_names = {
        cte.alias_or_name
        for cte in statement.find_all(exp.CTE)
    }


    for table in statement.find_all(exp.Table):

        table_name = table.name
        schema_name = table.db

        # Allow references to CTEs
        if table_name in cte_names:
            continue

        # Only our rgd schema is allowed
        if schema_name and schema_name != "rgd":
            raise ValueError(
                f"Unauthorized schema: {schema_name}"
            )

        # Table must be authorized for role
        if table_name not in allowed_tables:
            raise ValueError(
                f"Unauthorized table: {table_name}"
            )


    return sql