# Testing

## Main Test Command

```bash
python run_dqt.py --config config/user_email_phone.json
```

This runs the current user email/phone DQT.

## What It Compares

Source:

```text
Migration/broyte.duckdb: br_users
```

Staging:

```text
Azure SQL: polaris.br_users
```

## Reports

Summary:

```text
reports/user_email_phone_summary.csv
```

Issues:

```text
reports/user_email_phone_issues.csv
```

## Exit Code Behavior

`run_dqt.py` returns non-zero when there are critical or high issues.

This means a DQT run can fail even when the code works correctly, because data quality issues were found.

## Python Compile Check

After Python edits:

```bash
python -m compileall dqt scripts run_dqt.py list_table_columns.py
```

## Useful Debug Commands

List columns:

```bash
python list_table_columns.py polaris.br_users
```

Count rows:

```bash
python -c "from dotenv import load_dotenv; load_dotenv('.env'); from dqt.connections.azure_staging_connection import connect; conn = connect(read_only=True); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM polaris.br_users'); print(cur.fetchone()[0]); conn.close()"
```

Show sample rows:

```bash
python -c "from dotenv import load_dotenv; load_dotenv('.env'); from dqt.connections.azure_staging_connection import connect; conn = connect(read_only=True); cur = conn.cursor(); cur.execute('SELECT TOP 10 * FROM polaris.br_users'); columns = [c[0] for c in cur.description]; print(columns); [print(tuple(row)) for row in cur.fetchall()]; conn.close()"
```
