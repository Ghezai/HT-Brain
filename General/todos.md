# Todos

## Migration DQT

- [x] Get data from Nixus to local
- [x] Test if local db is up to date vs prod db
- [ ] Create DuckDB for Nixus db
- [ ] Import Nixus MySQL data into local `nixus.duckdb`
  - Use `Migration-DQT/scripts/import_mysql_to_duckdb.py`
  - Use `Migration-DQT/config/nixus_snapshot_tables.json`
  - Run with `--replace` when a fresh snapshot is needed
- [ ] Verify imported DuckDB tables
  - Check that `nx_users`, `nx_persons`, `nx_providers`, `nx_cabins`, and `nx_cabin_addresses` exist
  - Check row counts against the MySQL source tables
  - Open `nixus.duckdb` in DBeaver for manual inspection
- [ ] Create first Nixus data quality checks
  - Start with user data
  - Check email, phone, required fields, duplicates, and invalid values
  - Compare Nixus local DuckDB data with Broyte/staging data where needed
- [ ] Document the Nixus snapshot workflow
  - Add commands to `Migration-DQT/TEST_COMMANDS.md`
  - Add important notes to `HT-Brain` or project brain docs

## Web/App Testing

- [ ] Investigate why my super admin acc can log in to cabin owner web but cannot log in to backoffice web.
  - Check with people 
