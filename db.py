import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = str(BASE_DIR / "tasks.db")


@contextmanager
def get_connection(db_name: str = DB_NAME) -> Iterator[sqlite3.Connection]:
    """Connection to SQLite: commit on success, rollback on error."""
    conn = sqlite3.connect(db_name)
    # SQLite не перевіряє зовнішні ключі за замовчуванням, без цього
    # каскадне видалення (ON DELETE CASCADE) не спрацює
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()
