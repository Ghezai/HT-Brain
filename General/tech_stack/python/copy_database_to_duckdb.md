# Database Tables To DuckDB Snapshot

Use this guide when a Python project needs to copy cloud or local database tables into a local DuckDB file for testing, reporting, or data quality checks.

This pattern is useful because you can connect to the source database once, save the data locally, and run repeated checks without using the network or source database every time.

## Example Goal

Copy:

```text
Azure SQL: polaris.br_users
```

Into:

```text
Local DuckDB: db_stag.duckdb
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
  db_stag.duckdb
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
  "target_duckdb_path": "db_stag.duckdb",
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

## Snapshot All Configured Tables

Run:

```bash
python scripts/export_staging_to_duckdb.py --replace
```

`--replace` means:

- drop the local snapshot table if it already exists
- recreate it
- insert fresh cloud rows

If the config has several table objects, this command refreshes every configured table.

## Snapshot Selected Tables

For scripts that support table selection, add `--tables` and list one or more source or target table names:

```bash
python scripts/import_mysql_to_duckdb.py --replace --tables nx_person_objects
```

Several selected tables:

```bash
python scripts/import_mysql_to_duckdb.py --replace --tables nx_users nx_persons nx_person_objects
```

Selection behavior:

- without `--tables`, copy every table in the config
- with `--tables`, copy only the selected tables
- `--replace` only drops and recreates the selected target tables
- unselected DuckDB tables are left untouched
- table names should match either `source_name` or `target_name` from the config

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
  "target_duckdb_path": "db_stag.duckdb",
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
python -c "import duckdb; conn = duckdb.connect('db_stag.duckdb', read_only=True); print(conn.execute('SELECT table_name FROM information_schema.tables ORDER BY table_name').fetchall()); conn.close()"
```

Count rows:

```bash
python -c "import duckdb; conn = duckdb.connect('db_stag.duckdb', read_only=True); print(conn.execute('SELECT COUNT(*) FROM polaris_br_users').fetchone()[0]); conn.close()"
```

Show sample rows:

```bash
python -c "import duckdb; conn = duckdb.connect('db_stag.duckdb', read_only=True); print(conn.execute('SELECT * FROM polaris_br_users LIMIT 10').fetchall()); conn.close()"
```

## Important Notes

- The local DuckDB table is created automatically by the snapshot script.
- You do not need to manually create the table first.
- Store local snapshot files in `.gitignore`.
- Use read-only cloud connections when possible.
- Use local DuckDB snapshots for repeated tests to reduce network usage.
- Keep table definitions in the JSON config and choose what to run with CLI arguments.
- For large tables, use a stable batch column such as `id` when the script supports batching.

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
DuckDB: db_stag.duckdb
Local table: polaris_br_users
```

Result from latest run:

```text
Copied 243 rows from polaris.br_users to db_stag.duckdb:polaris_br_users
```

## Nixus MySQL Example From Migration-DQT

Project:

```text
E:\utv\Migration-DQT
```

Full refresh command:

```bash
./.venv/Scripts/python.exe scripts/import_mysql_to_duckdb.py --config config/nixus_snapshot_tables.json --replace
```

Selected table refresh:

```bash
./.venv/Scripts/python.exe scripts/import_mysql_to_duckdb.py --config config/nixus_snapshot_tables.json --replace --tables nx_person_objects
```

Several selected tables:

```bash
./.venv/Scripts/python.exe scripts/import_mysql_to_duckdb.py --config config/nixus_snapshot_tables.json --replace --tables nx_users nx_persons nx_person_objects
```

Current Nixus target DuckDB:

```text
DSOT-nixus.duckdb
```

Current configured target tables:

```text
nx_users
nx_persons
nx_providers
nx_cabins
nx_cabin_addresses
nx_person_objects
```
