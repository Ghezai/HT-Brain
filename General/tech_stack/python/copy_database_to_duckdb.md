# Cloud Table To DuckDB Snapshot

Use this guide when a Python project needs to copy one cloud or local database table into a local DuckDB file for testing, reporting, or data quality checks.

This pattern is useful because you can connect to the cloud or local db once, save the data locally, and run repeated checks without using the network every time.

## Example Goal

Copy:

```text
Azure SQL: polaris.br_users
```

Into:

```text
Local DuckDB: stag.duckdb
Table: polaris_br_users
```

## Recommended Files

```text
my-project/
  .env
  requirements.txt
  config/
    staging_snapshot_tables.json
  scripts/
    export_staging_to_duckdb.py
  dqt/
    connections/
      azure_staging_connection.py
  stag.duckdb
```

## Requirements

```txt
duckdb
pyodbc
python-dotenv
```

Install:

```bash
python -m pip install -r requirements.txt
```

## Environment Variables

`.env.example`:

```env
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=1433
DB_ENCRYPT=yes
DB_TRUST_SERVER_CERTIFICATE=no
DB_LOGIN_TIMEOUT=30
```

Do not commit `.env`.

## Snapshot Config

Create:

```text
config/staging_snapshot_tables.json
```

Example:

```json
{
  "target_duckdb_path": "stag.duckdb",
  "tables": [
    {
      "source_name": "polaris.br_users",
      "target_name": "polaris_br_users",
      "query": "SELECT * FROM polaris.br_users"
    }
  ]
}
```

Meaning:

- `target_duckdb_path`: local DuckDB file to store cloud data
- `source_name`: cloud table name for documentation/logging
- `target_name`: local DuckDB table name
- `query`: SQL query to run against the cloud database

## Snapshot One Table

Run:

```bash
python scripts/export_staging_to_duckdb.py --replace
```

`--replace` means:

- drop the local snapshot table if it already exists
- recreate it
- insert fresh cloud rows

## Snapshot Selected Columns

Instead of `SELECT *`, use selected columns:

```json
{
  "source_name": "polaris.br_users",
  "target_name": "polaris_br_users",
  "query": "SELECT UserId, Email, PhoneNumber FROM polaris.br_users"
}
```

Then run:

```bash
python scripts/export_staging_to_duckdb.py --replace
```

## Snapshot Multiple Tables

Add more objects to the `tables` list:

```json
{
  "target_duckdb_path": "stag.duckdb",
  "tables": [
    {
      "source_name": "polaris.br_users",
      "target_name": "polaris_br_users",
      "query": "SELECT * FROM polaris.br_users"
    },
    {
      "source_name": "polaris.br_cabins",
      "target_name": "polaris_br_cabins",
      "query": "SELECT * FROM polaris.br_cabins"
    }
  ]
}
```

Run:

```bash
python scripts/export_staging_to_duckdb.py --replace
```

## Verify Local Snapshot

List tables:

```bash
python -c "import duckdb; conn = duckdb.connect('stag.duckdb', read_only=True); print(conn.execute('SELECT table_name FROM information_schema.tables ORDER BY table_name').fetchall()); conn.close()"
```

Count rows:

```bash
python -c "import duckdb; conn = duckdb.connect('stag.duckdb', read_only=True); print(conn.execute('SELECT COUNT(*) FROM polaris_br_users').fetchone()[0]); conn.close()"
```

Show sample rows:

```bash
python -c "import duckdb; conn = duckdb.connect('stag.duckdb', read_only=True); print(conn.execute('SELECT * FROM polaris_br_users LIMIT 10').fetchall()); conn.close()"
```

## Important Notes

- The local DuckDB table is created automatically by the snapshot script.
- You do not need to manually create the table first.
- Store local snapshot files in `.gitignore`.
- Use read-only cloud connections when possible.
- Use local DuckDB snapshots for repeated tests to reduce network usage.

## Example From Migration-DQT

Project:

```text
E:\utv\Migration-DQT
```

Command:

```bash
python scripts/export_staging_to_duckdb.py --replace
```

Current config copies:

```text
Azure SQL: polaris.br_users
DuckDB: stag.duckdb
Local table: polaris_br_users
```

Result from latest run:

```text
Copied 243 rows from polaris.br_users to stag.duckdb:polaris_br_users
```
