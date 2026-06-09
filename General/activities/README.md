# Activities

This folder stores general weekly activity logs across projects.

Use it to record important work done during the week, especially work that affects more than one repository or should be remembered by AI later.

## What To Log

- project updates
- database changes
- data cleanup
- data quality checks
- bug fixes
- workflow changes
- important commands used
- decisions made
- open questions

## Naming

Use one file per week:

```text
DD-to-DD-MM-YYYY_W<week-number>.md
```

Example:

```text
01-to-07-06-2026_W23.md
```

## Weekly Header

Start each weekly file with the date range and week number in one row:

```markdown
# Activities | 08 June 2026 to 14 June 2026 | Week 24
```

## Entry Format

```markdown
## <Weekday> <Day> <Month> <Year>

### <Project Or Area>

**Activity**

- ...

**Details**

- ...

**Files Changed**

- `path/to/file`

**Commands**

```bash
command here
```

**Result**

- ...

**Follow-Up**

- ...
```

Example:

```markdown
## Tuesday 02 June 2026

### Migration-DQT

**Activity**

- Created local Azure staging snapshot flow and imported Broyte users.

**Files Changed**

- `Migration-DQT/config/staging_snapshot_tables.json`
- `Migration-DQT/scripts/export_staging_to_duckdb.py`

**Commands**

```bash
python scripts/export_staging_to_duckdb.py --replace
```

**Result**

- Copied `243` rows from `polaris.br_users` into local DuckDB table `polaris_br_users`.

**Follow-Up**

- Use the local snapshot for DQT comparisons.
```

Do not store secrets, passwords, API keys, or private tokens.
