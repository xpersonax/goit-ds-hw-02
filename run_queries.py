from db import BASE_DIR, DB_NAME, get_connection


def read_queries(path: str = "queries.sql") -> list[tuple[str, str]]:
    """Split queries.sql into (title, sql) pairs; title is the comment above a query."""
    text = (BASE_DIR / path).read_text(encoding="utf-8")
    queries = []
    for chunk in text.split(";"):
        lines = [line for line in chunk.strip().splitlines() if line.strip()]
        title = next((l[2:].strip() for l in lines if l.startswith("--")), "")
        sql = "\n".join(l for l in lines if not l.startswith("--")).strip()
        if sql:
            queries.append((title, sql))
    return queries


def run_queries(db_name: str = DB_NAME) -> None:
    """Run all queries in order; data changes are rolled back at the end."""
    with get_connection(db_name) as conn:
        cur = conn.cursor()
        for title, sql in read_queries():
            print(f"\n=== {title}")
            cur.execute(sql)
            if cur.description:  # SELECT
                for row in cur.fetchall():
                    print(row)
            else:  # INSERT / UPDATE / DELETE
                print(f"rows affected: {cur.rowcount}")
        conn.rollback()  # щоб демонстраційні запити не змінили дані


if __name__ == "__main__":
    run_queries()
