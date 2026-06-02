# AI Instructions

This Brain folder stores project memory for `E:\utv\Migration-DQT`.

When working on `Migration-DQT`, read these files first:

1. `overview.md`
2. `data_models.md`
3. `workflows.md`
4. `testing.md`
5. `open_questions.md`

Then inspect the repository source code before making changes.

## Repository

```text
E:\utv\Migration-DQT
```

## Main Purpose

`Migration-DQT` is an independent data quality testing repository for validating migration output.

Current priority:

- Compare old Broyte users from DuckDB with new/staging Broyte users.
- Validate user email and phone data.

## Important Rules

- Keep DQT independent from migration execution.
- DQT should use read-only Azure SQL connections.
- Do not store secrets in code or Brain docs.
- Keep SQL mappings configurable in JSON files.
- Use CSV reports because they are easy to inspect manually.
- Prefer Broyte-specific staging table `polaris.br_users` for Broyte user checks.
- Treat `polaris.Users` as the general auth/user table, not the primary Broyte migration comparison table.

## Update This Brain Folder

Update this folder when changing:

- DQT checks
- source/staging table mappings
- data model assumptions
- Azure staging table names
- local snapshot behavior
- commands or test workflows
- known issues and open questions

