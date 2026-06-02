# Workflows

Run commands from:

```text
E:\utv\Migration-DQT
```

## Setup

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

## Test Azure Connection

```bash
python -c "from dotenv import load_dotenv; load_dotenv('.env'); from dqt.connections.azure_staging_connection import connect; conn = connect(read_only=True); cur = conn.cursor(); cur.execute('SELECT 1 AS ok, DB_NAME() AS database_name'); print(cur.fetchone()); conn.close()"
```

## List Azure Tables

```bash
python -c "from dotenv import load_dotenv; load_dotenv('.env'); from dqt.connections.azure_staging_connection import connect; conn = connect(read_only=True); cur = conn.cursor(); cur.execute(\"SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_SCHEMA, TABLE_NAME\"); [print(f'{r.TABLE_SCHEMA}.{r.TABLE_NAME}') for r in cur.fetchall()]; conn.close()"
```

## List Columns

```bash
python list_table_columns.py polaris.br_users
```

```bash
python list_table_columns.py polaris.Users
```

## Run User Email/Phone DQT

```bash
python run_dqt.py --config config/user_email_phone.json
```

## Create Local Azure Snapshot

```bash
python scripts/export_staging_to_duckdb.py --replace
```

Default target:

```text
data/ht-staging.duckdb
```

Snapshot config:

```text
config/staging_snapshot_tables.json
```

## Compile Check

```bash
python -m compileall dqt scripts run_dqt.py list_table_columns.py
```

