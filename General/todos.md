# Todos

## 2026 Year Focus
This year has two main work targets.
### Target 1: Migration DQT and Auto Data Validation
### Target 2: New Unified App Auto Testing


### Target 1: Migration DQT and Auto Data Validation

Build a data quality testing process for migration data.

We have unified staging and production databases with migrated data from:

- Friio
- Nixus
- Broyte.no

The goal is to test if the data matches correctly between:

- Source/local databases
- Migration data
- Unified staging database
- Unified production database

Main focus:

- Copy important source data into local DuckDB snapshots.
- Compare migrated data with local/source data.
- Check users, cabins, providers, contracts, areas, orders, and payments.
- Find missing, duplicated, invalid, or incorrectly mapped data.
- Document all repeatable test commands and results.

### Target 2: New Unified App Auto Testing

Get the new unified application running locally and test the most important user and operation flows.

The app areas include:

- Cabin owner web
- Mobile app
- Backoffice web
- API

Main focus:

- Run the new app locally.
- Test login and access for different roles.
- Test important cabin owner, backoffice, and operational flows.
- Use API tests for backend behavior.
- Use UI tests, possibly Playwright, for main frontend flows.
- Document setup, test commands, issues, and results.

---

## Target 1: Migration DQT and Data Validation

### Nixus DuckDB Snapshot

- [x] Get data from Nixus to local MySQL.
- [x] Test that local MySQL connection works from `Migration-DQT`.
- [x] Create local DuckDB for Nixus data: `nixus.duckdb`.
- [x] Import Nixus MySQL data into local `nixus.duckdb`.
  - Use `Migration-DQT/scripts/import_mysql_to_duckdb.py`.
  - Use `Migration-DQT/config/nixus_snapshot_tables.json`.
  - Run with `--replace` when a fresh snapshot is needed.
- [x] Verify imported DuckDB tables.
  - Check that `nx_users`, `nx_persons`, `nx_providers`, `nx_cabins`, and `nx_cabin_addresses` exist.
  - Check row counts against the MySQL source tables.
  - Open `nixus.duckdb` in DBeaver for manual inspection.
- [x] Add Broyte DuckDB snapshot to Migration-DQT frontend viewer.
  - Connect `broyte.duckdb` to the Flask DuckDB viewer.
  - Verify Broyte tables can be listed from DuckDB.
- [x] Create Migration-DQT instruction file for important commands.
  - Add Flask run command.
  - Add DuckDB snapshot commands.
  - Add MySQL connection check command.
  - Add package install/update commands.
- [x] Document new PC clone setup for `ht-migration-dqt`.
  - Create `.venv`.
  - Install packages from `requirements.txt`.
  - Create `.env` from `.env.example`.
  - Use Git Bash path format: `./.venv/Scripts/python.exe`.
- [x] Document OneDrive workflow for local DuckDB snapshots.
  - Download `DSOT-broyte.duckdb`, `DSOT-nixus.duckdb`, and `DSOT-stag.duckdb` from Nixus Microsoft Cloud OneDrive after cloning on a new PC.
  - Keep the files in the `ht-migration-dqt` repository root.
  - Upload refreshed `.duckdb` files back to OneDrive after local database updates.

### Migration Data Quality Checks

- [ ] Tomorrow priority: create first DQT check for Nixus users.
  - Check email format.
  - Check phone format.
  - Check missing email and phone.
  - Check duplicate emails.
  - Check users are linked to persons correctly.
- [ ] Create first Nixus data quality checks.
  - Start with user data.
  - Check email, phone, required fields, duplicates, and invalid values.
  - Compare Nixus local DuckDB data with unified staging or production data where needed.
- [ ] Add checks for Broyte.no migrated data.
  - Validate users.
  - Validate cabins.
  - Validate providers.
  - Validate contracts and plowing-related data.
- [ ] Add checks for Friio migrated data.
  - Identify important source tables.
  - Create local snapshot if needed.
  - Compare important records with unified database data.
- [ ] Compare migration data across environments.
  - Local/source data vs staging.
  - Staging vs production.
  - Migration tables vs final unified app tables.

### Migration DQT Documentation

- [x] Document the Nixus snapshot workflow.
  - Add commands to `Migration-DQT/TEST_COMMANDS.md`.
  - Add important notes to `HT-Brain` or project brain docs.
- [x] Document new clone setup and DuckDB snapshot sharing workflow.
  - Add setup notes to `ht-migration-dqt/README.md`.
  - Add setup notes to `ht-migration-dqt/INSTRUCTIONS.md`.
  - Note that `.duckdb` snapshots are stored in OneDrive, not Git.
- [ ] Document how to run each data quality test.
- [ ] Document known data mapping rules.
- [ ] Document known issues and open questions from migration testing.

---

## Target 2: New Unified App Local Testing

### Local App Setup

- [ ] Get the new unified application running locally.
- [ ] Document required repositories, services, databases, and environment files.
- [ ] Document local run commands for each app area.
- [ ] Confirm local API can connect to the correct local/staging database.

### Web and App Access Testing

- [ ] Investigate why my super admin account can log in to cabin owner web but cannot log in to backoffice web.
  - Check with people/team.
  - Check account permissions and roles.
  - Check correct environment URL.
  - Check authentication configuration.
  - Check app/API errors during login.
- [ ] Test cabin owner web login and main flows.
- [ ] Test backoffice web login and main admin flows.
- [ ] Test mobile app login and main flows.

### API Testing

- [ ] Identify important API endpoints for cabin owner, app, and backoffice flows.
- [ ] Create API test examples for login, cabins, contracts, services, orders, and payments.
- [ ] Document API test commands and expected results.
- [ ] Add API issues and investigation notes to `HT-Brain`.

### UI Testing

- [ ] Decide where Playwright tests should live.
- [ ] Create first Playwright tests for the most important flows.
  - Cabin owner login.
  - Backoffice login.
  - View cabin data.
  - View contracts/services.
  - Main operational flow for plowing if available.
- [ ] Document how to run Playwright tests locally.
- [ ] Track UI bugs and missing functionality found during testing.
