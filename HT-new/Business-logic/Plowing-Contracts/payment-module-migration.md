# Payment Module Migration

## Purpose

This note describes the payment-module datasets exported alongside plowing contracts. These files provide the orders, prices, invoices, products, transactions, services, and usage data required to reconstruct contract payment context in the target system.

## Main Payment Export

Source file:

```text
NSS-Hyttetjenester/data_migration_2025_new/full_import_sqlazure/data_extractors/export_all_payment_module.php
```

The script exports configured providers to:

```text
payment_module/ht_<table_name>_<MIGR_DATE>.csv
```

## Exported Datasets

| Source table | Migration purpose |
| --- | --- |
| `service_orders` | Payment-module service orders. |
| `service_order_lines` | Individual lines belonging to service orders. |
| `invoices` | Invoice records for the selected providers. |
| `service_products` | Products that can be purchased or connected to services. |
| `service_product_lines` | Lines belonging to service products. |
| `service_prices` | Prices used by service products/contracts. |
| `price_area_products` | Product assignment for price areas. |
| `price_category_products` | Product assignment for price categories. |
| `transaction_log` | Payment/transaction records. |
| `trans_log_lines` | Individual transaction-log lines. |
| `services` | Legacy services, including contract-linked usage values. |

Most tables are filtered directly by `provider_id`.

`service_product_lines` has no direct `provider_id`, so it is selected by joining to `service_products`:

```sql
service_product_lines.service_product_id = service_products.id
```

and filtering on `service_products.provider_id`.

## Contract and Service Relationship

Legacy services are connected to contracts through:

```text
services.contract_id
```

For Clip Card calculations, the migration uses the contract validity period and service data to determine:

| Value | Source/meaning |
| --- | --- |
| Bought | `services.prepaid_count` for the contract/service. |
| Delivered | Delivery records calculated for the contract and cabin. |
| Remaining | Bought minus delivered. |
| Extra delivery | Deliveries tracked beyond normal prepaid usage. |

The main Clip Card usage output is:

```text
payment_module/ht_clipcard_usage_<MIGR_DATE>.csv
```

It is generated separately from the generic payment-table export because it calculates usage per cabin and contract.

## Monthly Payment and Hybrid Context

Monthly-payment and price-category cabins are exported separately to:

```text
payment_module/ht_monthly_payment_price_area_category_objects_<MIGR_DATE>.csv
```

This file identifies the cabin, provider, source type, area/category, service period, and related legacy contracts. It does not calculate Clip Card usage.

This separation is intentional:

- Clip Card usage needs bought/delivered/remaining calculations.
- Monthly and Hybrid migration needs cabin-to-price-area/category classification.
- Generic payment exports preserve the underlying order, invoice, product, price, and transaction rows.

## Practical Data Set Grouping

| Topic | Relevant exports |
| --- | --- |
| Contract source | `ht_contracts_<MIGR_DATE>.csv` |
| Clip Card balance and usage | `ht_clipcard_usage_<MIGR_DATE>.csv` |
| Monthly/Hybrid cabin classification | `ht_monthly_payment_price_area_category_objects_<MIGR_DATE>.csv` |
| Products and prices | `ht_service_products_*`, `ht_service_product_lines_*`, `ht_service_prices_*` |
| Area/category product mapping | `ht_price_area_products_*`, `ht_price_category_products_*` |
| Orders and invoices | `ht_service_orders_*`, `ht_service_order_lines_*`, `ht_invoices_*` |
| Transactions | `ht_transaction_log_*`, `ht_trans_log_lines_*` |
| Contract-linked legacy services | `ht_services_*` |

## Operational Requirements

- Refresh the old Hyttetjenester production database dump before generating CSV files.
- Verify the configured provider cohort for the current migration group.
- Update `MIGR_DATE` and `TARGET_FOLDER` for the migration session.
- Compare CSV row counts with source query counts.
- Treat the generic payment export, Clip Card usage export, and monthly/Hybrid export as complementary datasets.

## Open Questions

1. Which exact target tables consume each CSV?
2. How are source transaction statuses mapped to target payment statuses?
3. How are duplicate or reversed transactions handled?
4. Which invoice and transaction records must be excluded or transformed?
5. How are monthly subscriptions renewed or terminated in the target system?
6. How are Clip Card balances reconciled after target import?

## Source Code References

- `full_import_sqlazure/data_extractors/export_all_payment_module.php`
- `full_import_sqlazure/data_extractors/export_clippcard_payment_price_area_objects.php`
- `full_import_sqlazure/data_extractors/export_monthly_all_objects.php`
- `full_import_sqlazure/data_extractors/extract_provider_objects.php`
- `full_import_sqlazure/data_extractors/extract_services.php`
