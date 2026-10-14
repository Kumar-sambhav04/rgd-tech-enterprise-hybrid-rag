from app.database.connection import get_support_engine, get_admin_engine
from sqlalchemy import text

with get_support_engine().connect() as conn:
    conn.execute(text("SET search_path TO rgd"))
    try:
        conn.execute(text("SELECT * FROM employees LIMIT 1"))
        print("FAIL: support saw employees")
    except Exception:
        conn.rollback()
        conn.execute(text("SET search_path TO rgd"))
        print("OK: support denied on employees")

    result = conn.execute(text("SELECT count(*) FROM orders"))
    print("OK: support sees", result.scalar(), "orders")

with get_admin_engine().connect() as conn:
    conn.execute(text("SET search_path TO rgd"))
    result = conn.execute(text("SELECT count(*) FROM employees"))
    print("OK: admin sees", result.scalar(), "employees")