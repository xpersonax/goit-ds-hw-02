# goit-ds-hw-02

Task management database (SQLite): users, task statuses and tasks.

## Run

```bash
pip install -r requirements.txt
python create_db.py     # creates tasks.db from schema.sql
python seed.py          # fills tables with random data (Faker)
python run_queries.py   # runs all queries from queries.sql
```

## Files

- `schema.sql` - tables, UNIQUE constraints, foreign keys, cascade delete of tasks
- `db.py` - connection helper (enables `PRAGMA foreign_keys = ON`)
- `create_db.py` - creates the database
- `seed.py` - random data with Faker
- `queries.sql` - the 14 required SQL queries
- `run_queries.py` - executes `queries.sql` and prints results
