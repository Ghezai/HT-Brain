# Integrations

## Old Source DuckDB

Repository:

```text
E:\utv\Migration
```

Default database:

```text
E:\utv\Migration\broyte.duckdb
```

Environment variable:

```env
DUCKDB_PATH=../Migration/broyte.duckdb
```

Connection helper:

```text
Migration-DQT/dqt/connections/duckdb_connection.py
```

## Azure SQL Staging

Connection helper:

```text
Migration-DQT/dqt/connections/azure_staging_connection.py
```

Required environment variables:

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

Supported ODBC drivers are checked in this order:

```text
ODBC Driver 18 for SQL Server
ODBC Driver 17 for SQL Server
SQL Server Native Client 11.0
SQL Server
```

The helper uses `ApplicationIntent=ReadOnly` when `read_only=True`.

## Local Staging Snapshot

Default local snapshot:

```text
Migration-DQT/data/ht-staging.duckdb
```

Environment variable:

```env
HT_STAGING_DUCKDB_PATH=data/ht-staging.duckdb
```

Snapshot script:

```text
Migration-DQT/scripts/export_staging_to_duckdb.py
```
