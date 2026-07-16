import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
DB_PATH = BASE_DIR / "dev.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()


def query(sql, params=(), fetch=None):
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        if fetch == "one":
            row = cur.fetchone()
            result = dict(row) if row is not None else None
        elif fetch == "all":
            result = [dict(r) for r in cur.fetchall()]
        else:
            result = None
        conn.commit()
        return result
    finally:
        conn.close()
