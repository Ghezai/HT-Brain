# Changelog

## 2026-06-02

- Added Brain documentation for `Migration-DQT`.
- Documented active user email/phone DQT.
- Documented source/staging mapping:
  - `br_users.UserId` -> `polaris.br_users.UserId`
  - `br_users.Email` -> `polaris.br_users.Email`
  - `br_users.PhoneNumber` -> `polaris.br_users.PhoneNumber`
- Documented open question about snapshot config still using `polaris.Users`.
- Updated source DuckDB path from `Migration/test.duckdb` to `Migration/broyte.duckdb`.
