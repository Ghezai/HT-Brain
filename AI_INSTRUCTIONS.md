# AI Brain Guide

## Purpose

The `Brain` folder is shared knowledge storage for AI-assisted work across the `E:\utv` workspace.

Each repository or business area under `E:\utv` should have a matching folder inside `Brain`. The files in that folder document important information that AI agents and developers need when working on that project.

The goal is to avoid rediscovering the same context every time.

## Folder Mapping

Example:

```text
E:\utv\Migration-Broyte
E:\utv\Brain\Migration-Broyte

E:\utv\Migration-DQT
E:\utv\Brain\Migration-DQT

E:\utv\NSS-orderapp
E:\utv\Brain\NSS-orderapp
```

If a project has a business/domain name that is different from the repository name, create a separate folder for the domain too.

Example:

```text
E:\utv\Brain\Broyte.no
E:\utv\Brain\HT-new
```

## What To Store

Create small `.md` files for important project knowledge.

Recommended files:

```text
Brain/<project>/
  overview.md
  tech_stack.md
  data_models.md
  business_logic.md
  workflows.md
  integrations.md
  testing.md
  deployment.md
  open_questions.md
  changelog.md
```

Use only the files that are useful for that project.

## File Responsibilities

`overview.md`

- What the project does
- Main users or business purpose
- Important related repositories

`tech_stack.md`

- Programming languages
- Frameworks
- Database engines
- Package managers
- Runtime versions
- Important tools

`data_models.md`

- Important tables
- Important fields
- Primary keys
- Foreign keys
- Source-to-target mappings
- Known naming differences between systems

`business_logic.md`

- Rules the system must follow
- Ownership rules
- Permission rules
- Validation rules
- Domain-specific exceptions

`workflows.md`

- Common developer workflows
- Migration flows
- Import/export flows
- Data quality flows
- User or admin workflows

`integrations.md`

- APIs
- Cloud services
- Databases
- Authentication providers
- External systems

`testing.md`

- How to run tests
- What each test covers
- Required test data
- Known test limitations

`deployment.md`

- Deployment process
- Environments
- Required environment variables
- Release notes

`open_questions.md`

- Unknowns
- Decisions waiting for confirmation
- Data issues that need business review

`changelog.md`

- Important project changes
- Schema changes
- Business rule changes
- Migration/DQT updates

## Update Rule

When a repository changes in a way that affects future AI work, update the matching `Brain` folder.

Update `Brain` when changing:

- data models
- table mappings
- business rules
- important commands
- tech stack
- workflow steps
- database connections
- API integrations
- deployment steps
- testing strategy
- known issues

Do not update `Brain` for tiny implementation details that are already obvious in code.

## Writing Style

Keep files short and practical.

Use:

- clear headings
- bullet lists
- exact table names
- exact command examples
- exact file paths when useful

Avoid:

- long explanations
- secrets or passwords
- duplicated code
- outdated assumptions

## Security Rule

Never store secrets in `Brain`.

Do not write:

- passwords
- API keys
- database connection passwords
- private tokens
- personal credentials

It is okay to document environment variable names.

Example:

```env
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

## Data Model Example

```markdown
# Data Models

## br_users

Source: `Migration/broyte.duckdb`

Primary key:

- `UserId`

Important fields:

- `Email`
- `PhoneNumber`
- `ConnectedCompanies`

Maps to staging:

- `br_users.UserId` -> `polaris.br_users.UserId`
- `br_users.Email` -> `polaris.br_users.Email`
- `br_users.PhoneNumber` -> `polaris.br_users.PhoneNumber`
```

## Workflow Example

```markdown
# Workflows

## User Email/Phone DQT

Repository:

- `E:\utv\Migration-DQT`

Command:

```bash
python run_dqt.py --config config/user_email_phone.json
```

Reports:

- `reports/user_email_phone_summary.csv`
- `reports/user_email_phone_issues.csv`
```

## AI Usage Instructions

When an AI agent starts work on a project:

1. Read the matching `Brain/<project>/` folder first.
2. Read the repository files next.
3. Use `Brain` context as guidance, not as a replacement for code.
4. If code and `Brain` disagree, verify from the code and update `Brain`.
5. After important changes, update the relevant `Brain` `.md` files.

## Recommended First Files

For each existing folder, start with:

```text
overview.md
tech_stack.md
data_models.md
workflows.md
open_questions.md
```

Add the rest only when needed.
