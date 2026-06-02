# Migration-Broyte Overview

## Purpose

The `Migration-Broyte` project prepares and validates Broyte migration data locally.

Repository:

```text
E:\utv\Migration-Broyte
```

Main local database:

```text
E:\utv\Migration-Broyte\broyte.duckdb
```

## What The Project Does

- Fetches data from Broyte APIs.
- Stores source and prepared data in DuckDB.
- Runs SQL migrations to create and update tables.
- Imports historical CSV and JSONL data.
- Merges and cleans migration data.
- Runs local validation tests.
- Exports prepared data to CSV.
- Prepares data for Azure/HT staging transfer.

## Main Folders

```text
migrations/
scripts/api-to-duckdb/
scripts/data-to-duckdb/
scripts/duckdb-to-csv/
scripts/duckdb-to-ht_stg_db/
scripts/reporting/
test/
Documents/
```

## Important Tables

Current important DuckDB tables include:

- `br_users`
- `br_organizations`
- `br_cabins`
- `br_cabins_with_address`
- `br_cabin_users`
- `br_areas`
- `br_customer_presences`
- `br_plowing_history`
- `br_admin_api`
- `br_driver_admin`
- `br_drivers`
- `br_order_histories_api`

## Current Activity Notes

Important work and changes are documented in:

```text
Brain/Migration-Broyte/activity/
```

Current activity note:

```text
activity/country_data_cleanup_summary.md
```

This records the cleanup where missing `br_users.Country` values were filled from `CountryCode`.

## Related Brain Folders

```text
Brain/Migration-Broyte
Brain/Migration-DQT
Brain/Broyte.no
Brain/General
```

## Related Project

`Migration-DQT` is the separate data quality testing project.

Repository:

```text
E:\utv\Migration-DQT
```

It compares the prepared migration data in `broyte.duckdb` against staging data.
