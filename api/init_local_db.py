"""
Create a local PostgreSQL database (if needed) and then create ORM tables.

Usage:
    python -m api.init_local_db
"""
import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from dotenv import load_dotenv

load_dotenv()

from setup_db import (
    Base,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    SQLALCHEMY_DATABASE_URL,
    engine,
)

import models
# from . import film_model  # noqa: F401  Ensures Film model is registered on Base.metadata.


def _quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _validate_env() -> None:
    missing = []
    print(POSTGRES_DB)
    print(POSTGRES_PASSWORD)

    if not POSTGRES_DB:
        missing.append("POSTGRES_DB")
    if not POSTGRES_USER:
        missing.append("POSTGRES_USER")
    if not POSTGRES_PASSWORD:
        missing.append("POSTGRES_PASSWORD")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


def _create_database_if_missing() -> None:
    target_url = make_url(SQLALCHEMY_DATABASE_URL)
    database_name = target_url.database

    if not database_name:
        raise RuntimeError("Database name is missing in SQLALCHEMY_DATABASE_URL.")

    if not re.match(r"^[A-Za-z0-9_]+$", database_name):
        raise RuntimeError(
            "POSTGRES_DB contains invalid characters. "
            "Use letters, numbers, and underscores only."
        )

    admin_url = target_url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)

    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": database_name},
            ).scalar()

            if exists:
                print(f"Database '{database_name}' already exists.")
            else:
                conn.execute(text(f"CREATE DATABASE {_quote_ident(database_name)}"))
                print(f"Database '{database_name}' created.")
    finally:
        admin_engine.dispose()


def main() -> None:
    print(os.getenv("JIMMY"))
    print(os.getenv("POSTGRES_USER"))
    _validate_env()
    _create_database_if_missing()
    Base.metadata.create_all(bind=engine)
    print("Tables created (or already existed).")


if __name__ == "__main__":
    main()
