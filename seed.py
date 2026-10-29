import random

from faker import Faker

from db import DB_NAME, get_connection

NUMBER_USERS = 10
NUMBER_TASKS = 30
USERS_WITHOUT_TASKS = 2  # кілька користувачів лишаємо без завдань для запитів
STATUSES = [("new",), ("in progress",), ("completed",)]


def generate_users(fake: Faker, count: int) -> list[tuple[str, str]]:
    return [(fake.name(), fake.unique.email()) for _ in range(count)]


def generate_tasks(
    fake: Faker, count: int, status_ids: list[int], user_ids: list[int]
) -> list[tuple[str, str | None, int, int]]:
    tasks = []
    for _ in range(count):
        # приблизно кожне п'яте завдання без опису
        description = fake.paragraph(nb_sentences=2) if random.random() > 0.2 else None
        title = fake.sentence(nb_words=4).rstrip(".")
        tasks.append((title, description, random.choice(status_ids), random.choice(user_ids)))
    return tasks


def seed(db_name: str = DB_NAME) -> None:
    fake = Faker()
    with get_connection(db_name) as conn:
        cur = conn.cursor()

        cur.executemany("INSERT INTO status (name) VALUES (?)", STATUSES)
        cur.executemany(
            "INSERT INTO users (fullname, email) VALUES (?, ?)",
            generate_users(fake, NUMBER_USERS),
        )

        status_ids = [row[0] for row in cur.execute("SELECT id FROM status").fetchall()]
        user_ids = [row[0] for row in cur.execute("SELECT id FROM users").fetchall()]
        users_with_tasks = user_ids[:-USERS_WITHOUT_TASKS]

        cur.executemany(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
            generate_tasks(fake, NUMBER_TASKS, status_ids, users_with_tasks),
        )


if __name__ == "__main__":
    seed()
    print("Database seeded with random data")
