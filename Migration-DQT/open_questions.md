# Open Questions

## Snapshot Table Target

Current active DQT compares against:

```text
polaris.br_users
```

Current snapshot config copies:

```text
polaris.Users -> polaris_Users
```

Need to decide whether `config/staging_snapshot_tables.json` should instead copy:

```text
polaris.br_users -> polaris_br_users
```

For Broyte user DQT, `polaris.br_users` is likely the correct snapshot table.

## Local-To-Local DQT

The repo has a helper for local staging DuckDB:

```text
dqt/connections/staging_duckdb_connection.py
```

But `run_dqt.py` currently reads staging directly from Azure SQL.

Need to decide when to add a mode that compares:

```text
Migration/broyte.duckdb
data/ht-staging.duckdb
```

instead of connecting to Azure for every DQT run.

## Staging Schema Confirmation

Confirm final table names for Broyte migration DQT:

- `polaris.br_users`
- other future Broyte tables

Confirm whether `polaris.Users` is only auth/general user data.

## Future Checks

Potential next DQT checks:

- user active status
- connected companies
- cabin-user relationship
- company ownership
- missing/extra cabins
- duplicate keys
- required fields
