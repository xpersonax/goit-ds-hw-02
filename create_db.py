from db import BASE_DIR, DB_NAME, get_connection


def create_db(db_name: str = DB_NAME) -> None:
    """Create all tables from schema.sql (existing tables are recreated)."""
    sql = (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
    with get_connection(db_name) as conn:
        conn.executescript(sql)


if __name__ == "__main__":
    create_db()
    print(f"Database created: {DB_NAME}")
