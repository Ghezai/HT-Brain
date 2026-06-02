# DuckDB In Python Projects

Use this guide when adding DuckDB to a new Python project.

DuckDB is useful when a project needs a simple local database file for migration, reporting, data testing, imports, exports, or local snapshots.

## Recommended Project Structure

```text
my-python-project/
  db.py
  main.py
  requirements.txt
  data/
    app.duckdb
```

## Install DuckDB

Add to `requirements.txt`:

```txt
duckdb
```

Install:

```bash
python -m pip install -r requirements.txt
```

If using a virtual environment:

Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Create `db.py`

Use `Path(__file__)` so the database path works no matter where the command is run from.

```python
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "app.duckdb"


def connect(read_only: bool = False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH), read_only=read_only)
```

## Use DuckDB In `main.py`

```python
from db import connect


def main():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                name VARCHAR,
                email VARCHAR
            )
        """)

        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            [1, "Ghezai", "ghezai@example.com"]
        )

        rows = conn.execute("SELECT * FROM users").fetchall()
        print(rows)


if __name__ == "__main__":
    main()
```

Run:

```bash
python main.py
```

## Read-Only Usage

Use read-only mode for data quality tests, reporting, and validation scripts.

```python
from db import connect


with connect(read_only=True) as conn:
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    print(count)
```

## Why Not Use Only A String Path

Avoid this:

```python
DB_PATH = "data/app.duckdb"
```

It only works reliably when Python is run from the project root.

Prefer this:

```python
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "app.duckdb"
```

This makes the database path relative to `db.py`.

## Environment Variable Option

For projects where the database path can change, use `.env`.

Install:

```txt
python-dotenv
duckdb
```

`.env.example`:

```env
DUCKDB_PATH=data/app.duckdb
```

`db.py`:

```python
import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def get_db_path() -> Path:
    value = os.getenv("DUCKDB_PATH", "data/app.duckdb")
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def connect(read_only: bool = False):
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path), read_only=read_only)
```

## Useful SQL Examples

Create table:

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        name VARCHAR,
        email VARCHAR
    )
""")
```

Insert one row:

```python
conn.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    [1, "Ghezai", "ghezai@example.com"]
)
```

Query rows:

```python
rows = conn.execute("SELECT * FROM users").fetchall()
```

Count rows:

```python
count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
```

Export table to CSV:

```python
conn.execute("COPY users TO 'data/users.csv' (HEADER, DELIMITER ',')")
```

Import CSV:

```python
conn.execute("""
    CREATE TABLE users_from_csv AS
    SELECT * FROM read_csv_auto('data/users.csv')
""")
```

## Open DuckDB In DBeaver

DBeaver can open `.duckdb` files.

Steps:

1. Open DBeaver.
2. Click `New Database Connection`.
3. Search for `DuckDB`.
4. Select `DuckDB`.
5. If DBeaver asks to install the DuckDB driver, install it.
6. In the database/file path field, choose the `.duckdb` file.

Example file:

```text
E:\utv\my-python-project\data\app.duckdb
```

7. Click `Test Connection`.
8. Click `Finish`.

After connecting, open the database tree and inspect tables.

## Important DBeaver Note

Do not write to the same DuckDB file from Python and DBeaver at the same time.

Safe workflow:

1. Close Python scripts that use the DuckDB file.
2. Open the `.duckdb` file in DBeaver.
3. Inspect data.
4. Close/disconnect DBeaver before running write scripts again.

## Common Problems

Problem:

```text
Database file does not exist
```

Fix:

- Make sure the path is correct.
- Run the Python script once to create the file.

Problem:

```text
Cannot open database in read-only mode
```

Fix:

- The file must already exist before opening read-only.

Problem:

```text
Database is locked
```

Fix:

- Close DBeaver or stop the Python process using the file.

## Recommended Git Ignore

Usually do not commit local DuckDB data files.

`.gitignore`:

```gitignore
data/*.duckdb
data/*.duckdb.wal
```

Keep only:

```text
data/.gitkeep
```

if you want Git to track the folder.
