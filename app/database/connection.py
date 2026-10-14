import os
from functools import lru_cache
from enum import Enum

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine

load_dotenv()


class DBRole(str, Enum):
    """Mirrors the two Postgres roles created in rgd_tech_schema.sql /
    roles_and_grants.sql (rag_support, rag_admin). The engine used for a
    query is chosen by the caller's resolved app role — this is what makes
    the database-level GRANTs actually load-bearing, rather than the ACL
    filter being the only enforcement point."""
    SUPPORT = "support"
    ADMIN = "admin"


def _build_database_url(user_env: str, password_env: str) -> str:
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    user = os.getenv(user_env)
    password = os.getenv(password_env)

    missing = [
        name for name, val in [
            ("POSTGRES_HOST", host), ("POSTGRES_PORT", port),
            ("POSTGRES_DB", db), (user_env, user), (password_env, password),
        ] if not val
    ]
    if missing:
        raise RuntimeError(
            f"Missing required env vars for DB connection: {', '.join(missing)}"
        )

    # RDS enforces SSL depending on the parameter group; sslmode=require is
    # a safe default that works whether or not it's actually mandatory.
    sslmode = os.getenv("POSTGRES_SSLMODE", "require")
    return URL.create(drivername="postgresql+psycopg",
                      username=user,
                      password=password,
                      host=host,
                      port=int(port),
                      database=db,
                      query={"sslmode":sslmode}
                      )
    #(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    #f"?sslmode={sslmode}")



@lru_cache(maxsize=2)
def get_engine(role: DBRole) -> Engine:
    """Returns a cached engine for the given role. Cached so we don't
    rebuild a connection pool per request — each role gets exactly one
    pool for the process lifetime."""
    if role == DBRole.SUPPORT:
        url = _build_database_url("POSTGRES_SUPPORT_USER", "POSTGRES_SUPPORT_PASSWORD")
    else:
        url = _build_database_url("POSTGRES_ADMIN_USER", "POSTGRES_ADMIN_PASSWORD")

    return create_engine(
        url,
        pool_pre_ping=True,   # RDS silently drops idle connections; this
                               # avoids handing out a dead connection
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800,    # recycle before RDS's own idle timeout hits
    )


# Convenience accessors — prefer get_engine(role) in new code so the role
# is always explicit at the call site.
def get_support_engine() -> Engine:
    return get_engine(DBRole.SUPPORT)


def get_admin_engine() -> Engine:
    return get_engine(DBRole.ADMIN)
