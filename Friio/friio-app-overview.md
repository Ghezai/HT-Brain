# Friio App Overview

Friio is a multi-app monorepo for a cabin and plowing service platform.

## Main Pieces

- `README.md`: root setup notes for Postgres, Liquibase migrations, .NET restore, JWT keys, and Swagger.
- `src/webshop/application`: Remix/React customer-facing app for cabin owners. It handles sign-in and registration, Vipps auth and payment flows, cabins, stays, contracts, plowing history, payments, notifications, account settings, and user/cabin invitations.
- `src/plow-backoffice`: Remix/React admin/backoffice app for operators and partners. It covers users, customers, cabins, orders, payment requests, plowing agreements, settlements, campaigns, map editor, organization settings, statistics, and plowing actions.
- `src/platform/src/API/Platform.API`: .NET backend API. It wires modules for `organizations`, `plowing`, `products`, `maps`, `cabins`, `plowingMaps`, and `platform` security/users.
- `liquibase`: database migrations, with changesets for users, roles/scopes, organizations, cabins, contracts, plowing, payments, campaigns, settlements, and reporting views.
- `src/infrastructure`: Azure Bicep and PowerShell deployment assets for app services/container apps, SQL, ACR, monitoring, dashboards, VNet, and environment parameters.
- `src/pipelines`: Azure pipeline YAML for tests, builds, image publishing, infrastructure provisioning, maps deployment, and environment-specific releases.
- `src/libraries`: internal npm and NuGet packages for multi-organization behavior and app roles.

## Domain Summary

The product appears to manage cabin-related services, especially snow/plowing operations. Customers can register cabins, manage stays/presence, buy or manage contracts, pay through payment flows, and see plowing/order history.

Admins and operators can manage cabins, customers, organizations, service areas, plowing statuses, agreements, products/contracts, campaigns, payments, settlements, and reports.

## Local Run Notes

For webshop local development, `src/webshop/README.md` expects `friio.dev`, `mkcert`, Docker, Make, Azure CLI, and credentials in `application/.env`.

The webshop local setup runs:

- Remix app on HTTP `3018`
- Live reload on `3019`
- Caddy HTTPS proxy
- Mailcatcher web UI on `3022`
- Mailcatcher SMTP on `3021`
- Redis on `3023`

The backend exposes Swagger/OpenAPI when enabled. The root README notes this URL:

```text
http://localhost:5187/swagger/index.html?urls.primaryName=V2
```

