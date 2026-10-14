"""
One-time database bootstrap: runs schema -> seed -> roles, in order,
using the RDS MASTER user.

This is intentionally NOT part of app/database/connection.py. connection.py
is runtime code the app imports on every request; it should only ever be
able to construct rag_support / rag_admin connections. This script uses a
different, more privileged credential (the RDS master user) and is meant
to be run manually, once, from the command line — never imported by the
app itself.

Usage:
    python data/database_scripts/init_db.py

Requires these additional vars in .env (on top of the ones connection.py
already uses):
    POSTGRES_MASTER_USER
    POSTGRES_MASTER_PASSWORD

Safe to re-run only against a fresh database — schema.sql uses plain
CREATE TABLE (no IF NOT EXISTS) and roles.sql uses DROP ROLE IF EXISTS /
CREATE ROLE, so re-running after the first successful run will fail on
"table already exists". If you need to reset, drop and recreate the
`rgd` schema first (see the reset() function at the bottom).
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = Path(__file__).parent
FILES_IN_ORDER = [
    SCRIPT_DIR / "rgd_tech_schema.sql",
    SCRIPT_DIR / "rgd_tech_seed.sql",
    SCRIPT_DIR / "rgd_tech_roles.sql",
]


def _master_connection_string() -> str:
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_MASTER_USER")
    password = os.getenv("POSTGRES_MASTER_PASSWORD")
    sslmode = os.getenv("POSTGRES_SSLMODE", "require")

    missing = [n for n, v in [
        ("POSTGRES_HOST", host), ("POSTGRES_PORT", port), ("POSTGRES_DB", db),
        ("POSTGRES_MASTER_USER", user), ("POSTGRES_MASTER_PASSWORD", password),
    ] if not v]
    if missing:
        print(f"Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return f"host={host} port={port} dbname={db} user={user} password={password} sslmode={sslmode}"


def run_sql_file(conn: psycopg.Connection, path: Path) -> None:
    print(f"\n--- Running {path.name} ---")
    sql = path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print(f"--- {path.name} completed ---")


def main() -> None:
    conn_str = _master_connection_string()
    print("Connecting to RDS as master user...")

    with psycopg.connect(conn_str) as conn:
        for path in FILES_IN_ORDER:
            if not path.exists():
                print(f"ERROR: expected file not found: {path}", file=sys.stderr)
                sys.exit(1)
            try:
                run_sql_file(conn, path)
            except Exception as e:
                conn.rollback()
                print(f"\nFAILED on {path.name}: {e}", file=sys.stderr)
                print(
                    "Stopped — fix the error above before re-running. "
                    "Files already applied before the failure are still "
                    "committed (each file commits independently).",
                    file=sys.stderr,
                )
                sys.exit(1)

    print("\nAll three files applied successfully: schema -> seed -> roles.")


def reset() -> None:
    """Drops the rgd schema (and the two roles) entirely, so init can be
    re-run from a clean slate. Run explicitly with:
        python -c "from data.database_scripts.init_db import reset; reset()"
    Not called automatically — this is destructive."""
    conn_str = _master_connection_string()
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS rgd CASCADE;")
            cur.execute("DROP ROLE IF EXISTS rag_support;")
            cur.execute("DROP ROLE IF EXISTS rag_admin;")
        conn.commit()
    print("Schema and roles dropped. Re-run init_db.py to rebuild from scratch.")


if __name__ == "__main__":
    main()