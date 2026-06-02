# Data Models

## Old Source Users

Model file:

```text
Migration-DQT/models/old/br_users.sql
```

Source database:

```text
Migration/broyte.duckdb
```

Source table:

```text
br_users
```

Primary key:

```text
UserId
```

Important fields:

```text
UserId
FirstName
Email
PhoneNumber
CountryCode
Country
PostalCode
PostalPlace
Address
Language
Active
ConnectedCompanies
```

## Broyte Staging Users

Model file:

```text
Migration-DQT/models/staging/polaris.br_users.sql
```

Azure staging table:

```text
polaris.br_users
```

Primary comparison key:

```text
UserId
```

Important fields:

```text
UserId
Email
PhoneNumber
```

## General Polaris Users

Model file:

```text
Migration-DQT/models/staging/polaris.Users.sql
```

Azure staging table:

```text
polaris.Users
```

This table is the general auth/user table. It has columns such as:

```text
Id
FirstName
LastName
Mail
PrincipalId
PhoneNumber
ExternalId
CreatedAt
UpdatedAt
Confirmed
RemovedAt
ImportedFrom
TermsAccepted
Address
PostalCode
Country
City
```

For Broyte-specific DQT user checks, prefer:

```text
polaris.br_users
```

## Active User Email/Phone Mapping

Config:

```text
Migration-DQT/config/user_email_phone.json
```

Source query:

```sql
SELECT UserId AS user_id, Email AS email, PhoneNumber AS phone FROM br_users
```

Staging query:

```sql
SELECT UserId AS user_id, Email AS email, PhoneNumber AS phone FROM polaris.br_users
```

Required aliases:

```text
user_id
email
phone
```
