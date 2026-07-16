import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
DEV_DB_PATH = BASE_DIR / "dev.db"


def _use_turso():
    return bool(os.getenv("TURSO_DATABASE_URL"))


def get_connection():
    if _use_turso():
        import libsql_experimental as libsql

        conn = libsql.connect(
            database=os.getenv("TURSO_DATABASE_URL"),
            auth_token=os.getenv("TURSO_AUTH_TOKEN"),
        )
        return conn, "turso"

    conn = sqlite3.connect(DEV_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn, "sqlite"


def init_db():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn, kind = get_connection()
    try:
        if kind == "sqlite":
            conn.executescript(schema)
        else:
            for stmt in filter(str.strip, schema.split(";")):
                conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def query(sql, params=(), fetch=None):
    conn, kind = get_connection()
    try:
        cur = conn.execute(sql, params)
        if fetch == "one":
            row = cur.fetchone()
            result = _row_to_dict(row, cur, kind)
        elif fetch == "all":
            result = [_row_to_dict(r, cur, kind) for r in cur.fetchall()]
        else:
            result = None
        conn.commit()
        return result
    finally:
        conn.close()


def _row_to_dict(row, cur, kind):
    if row is None:
        return None
    if kind == "sqlite":
        return dict(row)
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))
