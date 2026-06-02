# Business Logic

## User Contact Validation

The current DQT check validates user contact data after migration.

Comparison is by:

```text
user_id
```

Current source/staging key:

```text
br_users.UserId -> polaris.br_users.UserId
```

## Email Rules

Normalization:

- trim whitespace
- lowercase the email

Validation:

- missing source email is a `Medium` issue
- invalid source email is a `Medium` issue
- missing staging email is a `High` issue
- invalid staging email is a `High` issue
- source/staging email mismatch is a `High` issue

## Phone Rules

Normalization:

- trim whitespace
- remove non-digit characters
- preserve leading `+` if present

Validation:

- missing source phone is a `Medium` issue
- missing staging phone is a `High` issue
- source/staging phone mismatch is a `High` issue

## User Presence Rules

- User missing in staging is `Critical`.
- Extra user in staging is `Medium`.

## Current Issue Types

```text
missing_in_staging
extra_in_staging
missing_source_email
invalid_source_email
missing_staging_email
invalid_staging_email
email_mismatch
missing_source_phone
missing_staging_phone
phone_mismatch
```

