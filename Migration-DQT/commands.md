# Commands

The full repository command reference is in:

```text
Migration-DQT/TEST_COMMANDS.md
Migration-DQT/AZURE_DB_COMMANDS.md
```

Most important commands:

## Activate Venv

Git Bash:

```bash
source .venv/Scripts/activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run DQT

```bash
python run_dqt.py --config config/user_email_phone.json
```

## List Columns

```bash
python list_table_columns.py polaris.br_users
```

## Snapshot Azure To DuckDB

```bash
python scripts/export_staging_to_duckdb.py --replace
```

