# Country Data Cleanup Summary

## Overview

We updated the `broyte.main.br_users` table to fill missing or empty values in the `Country` column based on the telephone `CountryCode`.

This was done because some users had a `CountryCode` value such as `+47`, `+46`, or `+45`, but the `Country` column was empty.

## Table Updated

```text
broyte.main.br_users
```

## Column Updated

```text
Country
```

## Source Column Used

```text
CountryCode
```

## Update Rule

Only rows where `Country` was `NULL` or empty were updated.

Existing country values were not changed.

```sql
WHERE Country IS NULL OR TRIM(Country) = ''
```

## Rows Updated

```text
1301 rows
```

## Execution Time

```text
0.02 seconds
```

## Country Code Mapping Used

| CountryCode | Country |
|---|---|
| +47 | Norway |
| +46 | Sweden |
| +45 | Denmark |
| +358 | Finland |
| +354 | Iceland |
| +31 | Netherlands |
| +353 | Ireland |
| +39 | Italy |
| +44 | United Kingdom |
| +49 | Germany |
| +84 | Vietnam |

## SQL Query Used

```sql
UPDATE broyte.main.br_users
SET Country =
    CASE CountryCode
        WHEN '+47' THEN 'Norway'
        WHEN '+46' THEN 'Sweden'
        WHEN '+45' THEN 'Denmark'
        WHEN '+358' THEN 'Finland'
        WHEN '+354' THEN 'Iceland'
        WHEN '+31' THEN 'Netherlands'
        WHEN '+353' THEN 'Ireland'
        WHEN '+39' THEN 'Italy'
        WHEN '+44' THEN 'United Kingdom'
        WHEN '+49' THEN 'Germany'
        WHEN '+84' THEN 'Vietnam'
        ELSE Country
    END
WHERE (Country IS NULL OR TRIM(Country) = '')
  AND CountryCode IN (
      '+47', '+46', '+45', '+358', '+354',
      '+31', '+353', '+39', '+44', '+49', '+84'
  );
```

## Result

The user country data was cleaned by automatically filling missing countries from telephone country codes.

Example:

| CountryCode | Before | After |
|---|---|---|
| +47 | empty | Norway |
| +46 | empty | Sweden |
| +45 | empty | Denmark |
| +44 | empty | United Kingdom |
| +49 | empty | Germany |

## Recommended Verification Query

Use this query to check the result grouped by `CountryCode` and `Country`:

```sql
SELECT
    CountryCode,
    Country,
    COUNT(*) AS TotalUsers
FROM broyte.main.br_users
GROUP BY CountryCode, Country
ORDER BY CountryCode, Country;
```

## Notes

- The original issue happened because the query first used `Contry`, but the correct column name in the table is `Country`.
- After correcting the column name, the update worked successfully.
- Total updated rows: `1301`.
