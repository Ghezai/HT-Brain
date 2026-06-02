# Tech Stack

## Language

- Python

## Python Packages

Defined in `requirements.txt`:

```text
duckdb
pyodbc
python-dotenv
```

## Databases

Old/source:

- DuckDB
- Default path: `../Migration/broyte.duckdb`

New/staging:

- Azure SQL / SQL Server
- Connected through `pyodbc`
- Uses SQL Server ODBC driver

Local staging snapshot:

- DuckDB
- Default path: `data/ht-staging.duckdb`

## Config

Environment:

```text
.env
.env.example
```

DQT check config:

```text
config/user_email_phone.json
```

Azure snapshot config:

```text
config/staging_snapshot_tables.json
```

## Security

Do not commit `.env`.

Required env names:

```env
DUCKDB_PATH=
HT_STAGING_DUCKDB_PATH=
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_ENCRYPT=
DB_TRUST_SERVER_CERTIFICATE=
DB_LOGIN_TIMEOUT=
```
