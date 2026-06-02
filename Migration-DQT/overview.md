# Overview

`Migration-DQT` contains independent data quality tests for migration validation.

The repo compares data from:

- old/source DuckDB database in `E:\utv\Migration\broyte.duckdb`
- new/staging Azure SQL database

Current first-version check:

- user email and phone comparison

## Related Repositories

```text
E:\utv\Migration
E:\utv\Migration-DQT
E:\utv\Brain\Migration-DQT
```

## Current DQT Scope

The active DQT check compares:

```text
Migration/broyte.duckdb: br_users
Azure SQL: polaris.br_users
```

Fields checked:

- `UserId`
- `Email`
- `PhoneNumber`

## Important Files

```text
run_dqt.py
config/user_email_phone.json
dqt/checks/user_email_phone.py
dqt/connections/azure_staging_connection.py
dqt/connections/duckdb_connection.py
dqt/reporting/csv_reports.py
TEST_COMMANDS.md
AZURE_DB_COMMANDS.md
```

## Reports

DQT reports are written to:

```text
reports/
```

Current report files:

```text
reports/user_email_phone_summary.csv
reports/user_email_phone_issues.csv
```
