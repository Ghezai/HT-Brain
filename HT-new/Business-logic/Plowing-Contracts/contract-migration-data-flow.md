# Contract Migration Data Flow

## Purpose

This note documents how `data_migration_2025_new/full_import_sqlazure` identifies cabins and prepares data for the five target contract options.

It describes the extractor behavior. It does not replace the target-system import specification.

## Main Classification Rules

| Source condition | Migration handling |
| --- | --- |
| Cabin inside a `price_area` for a Clip Card provider | Export for Clip Card migration and usage transfer. |
| Cabin inside a monthly-payment `price_area` | Export through the separate monthly/Hybrid workflow. |
| Cabin linked to a `price_category` | Export through the monthly workflow and treat as a Hybrid candidate. |
| Cabin outside every `price_area` but inside a `service_area` | Candidate for Fixed Price. |

Common Road and Plowing Contract without in-app payment are not selected by these extractor conditions. They are governed by separate business and target migration rules.

## Area Selection

### Price areas

Cabins inside price areas are found with the existing geometry rule:

```sql
ST_CONTAINS(price_areas.area, object_addresses.position)
```

The related `price_area` must also be migrated as a contract area because the target system needs the area to calculate and handle Clip Card or Hybrid contracts.

### Service areas

All `service_areas` are also migrated as contract areas.

The migration accepts that a cabin can be inside both a `price_area` and a `service_area`. In that case, the price-area Clip Card/Hybrid logic takes precedence.

Fixed Price candidates are cabins that:

1. are not inside any `price_area`; and
2. are inside a `service_area`.

This avoids creating manual exception areas during migration.

### Price categories

Price-category objects are not found with price-area geometry. They are selected through:

```text
provider_objects.price_category_id
```

Newly drawn price-category areas are intended to become contract areas in the target system. Their cabins are Hybrid candidates and are processed with monthly-payment cases.

## General Legacy Contract Export

Source file:

```text
NSS-Hyttetjenester/data_migration_2025_new/full_import_sqlazure/data_extractors/extract_contracts.php
```

Behavior:

- selects all columns from `contracts` for configured provider IDs;
- does not filter by active status, validity dates, or service period;
- writes `ht_contracts_<MIGR_DATE>.csv`; and
- requires a fresh production database dump before generating migration CSV files.

The source `contracts` table includes fields such as provider, cabin/object, service period, name, validity dates, total price, active status, and contract template ID.

Legacy template constants found in `shared_utils/common.php`:

| ID | Template |
| ---: | --- |
| 1 | Winter services (`Vintertjenester`) |
| 2 | Summer services (`Sommertjenester`) |
| 10 | Road plowing constant exists, but it is not included in the active template list. |

These legacy templates are not the same thing as the five target UI contract labels. Target contract selection also depends on areas, provider configuration, and payment data.

## Supporting Area Exports

The migration also exports the source structures used for classification and target contract areas:

| Source data | CSV output |
| --- | --- |
| `price_areas` | `ht_price_areas_<MIGR_DATE>.csv` |
| `price_categories` | `ht_price_categories_<MIGR_DATE>.csv` |
| `service_areas` | `ht_service_areas_<MIGR_DATE>.csv` |

These datasets preserve the source area/category records. The cabin classification exports then connect objects to the relevant price area or price category.

## Clip Card Usage Export

Source file:

```text
NSS-Hyttetjenester/data_migration_2025_new/full_import_sqlazure/data_extractors/export_clippcard_payment_price_area_objects.php
```

Output:

```text
payment_module/ht_clipcard_usage_<MIGR_DATE>.csv
```

Flow:

1. Read configured Clip Card providers.
2. Find each provider's latest service period by `periode_from` descending.
3. Read the provider's price areas.
4. Find cabins inside each price area.
5. Find all contracts for each cabin in the latest service period.
6. Calculate Clip Card usage for each contract.
7. Export one row per contract when multiple contracts exist.

Normal usage fields:

| Field | Meaning |
| --- | --- |
| `bought` | Prepaid clip count. |
| `delivered` | Used/delivered count. |
| `remained` | `bought - delivered`. |
| `extra_delivery` | Deliveries beyond the prepaid handling. |

The export also records provider, price area, cabin/object, contract, service period, and whether a current-period contract exists.

### Missing current-period contract

If no contract exists in the latest service period:

- find the latest historical contract for the same provider and cabin;
- export its contract and service-period identifiers only as a reference;
- keep `has_contract = 0`; and
- set all clip values to zero.

If the cabin has no contract in any service period for that provider, the row is skipped.

Important limitation: the current-period contract query does not filter on active status or validity dates.

## Monthly Payment and Hybrid Export

Source files:

```text
NSS-Hyttetjenester/data_migration_2025_new/full_import_sqlazure/data_extractors/export_monthly_all_objects.php
NSS-Hyttetjenester/data_migration_2025_new/full_import_sqlazure/data_extractors/extract_provider_objects.php
```

Output:

```text
payment_module/ht_monthly_payment_price_area_category_objects_<MIGR_DATE>.csv
```

Two source types are supported:

| `source_type` | How cabins are selected |
| --- | --- |
| `price_area` | Cabin address is inside active price-area geometry. |
| `price_category` | Cabin is linked through `provider_objects.price_category_id`. |

The exporter:

- uses configured monthly-payment providers;
- finds the latest service period for each provider;
- emits one unique row per provider and cabin;
- includes price-area or price-category identifiers and names;
- records whether contracts exist in the latest service period;
- stores the first contract ID plus all contract IDs as a comma-separated value; and
- does not calculate Clip Card usage.

The contract lookup in this export does not check active status or validity dates.

## Known Migration Decisions and Limitations

- Area overlap is accepted for migration and reviewed later if it causes target-system problems.
- Monthly-payment and price-category cases are intentionally separated from the general area flow.
- Provider cohorts are configured directly in the extractor scripts.
- The extractor scripts prepare CSV data; they do not fully document target contract creation, pricing, renewal, cancellation, or refund rules.
- A fresh source database dump and correct `MIGR_DATE`/`TARGET_FOLDER` values are required before export.

## Source Code References

- `full_import_sqlazure/data_extractors/export_clippcard_payment_price_area_objects.php`
- `full_import_sqlazure/data_extractors/export_monthly_all_objects.php`
- `full_import_sqlazure/data_extractors/extract_provider_objects.php`
- `full_import_sqlazure/data_extractors/extract_contracts.php`
- `full_import_sqlazure/data_extractors/extract_price_areas.php`
- `full_import_sqlazure/data_extractors/extract_price_categories.php`
- `full_import_sqlazure/data_extractors/extract_service_areas.php`
- `full_import_sqlazure/shared_utils/common.php`
