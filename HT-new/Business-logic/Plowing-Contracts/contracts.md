# Contracts

## Contract Types

| No. | Contract type |
| ---: | --- |
| 1 | Hybrid with in-app payment |
| 2 | Fixed Price with in-app payment |
| 3 | Clip Card with in-app payment |
| 4 | Plowing Contract without in-app payment |
| 5 | Common Road with in-app payment |

## Purpose

This file is the central overview of contract types currently mentioned in HT-Brain. It explains what each contract is for, how it is used, and which business and migration rules are confirmed.

The detailed rules below were collected mainly from:

- `HT-new/Business-logic/Plowing-Contracts/discution-with-axon.md`
- `HT-new/Business-logic/Plowing-Contracts/cotract-clipcard-plowing-area-commonroad.md`
- `HT-new/Business-logic/Plowing-Contracts/plowing-improvements.md`
- `HT-new/Business-logic/Plowing-Contracts/contract-migration-data-flow.md`
- `HT-new/Business-logic/Plowing-Contracts/contract-area-use-cases.md`
- `HT-new/Business-logic/Plowing-Contracts/payment-module-migration.md`
- `HT-new/CabinOwner/workflows.md`
- `HT-new/Friio-app-Brain/friio-app-overview.md`

## Contract List

### Contract and payment type

| No. | Contract | Payment type |
| ---: | --- | --- |
| 1 | Clip Card | In-app |
| 2 | Common Road | In-app |
| 3 | Hybrid | In-app |
| 4 | Fixed Price | In-app |
| 5 | Plowing Contract | Outside the app |

### What each contract is used for

| Contract | Main use |
| --- | --- |
| Clip Card | Clip-based plowing with separate clip activation or refill operations. |
| Common Road | Plowing of a shared road, separate from a cabin's private contract. |
| Hybrid | Monthly-payment and special price-category/price-area plowing cases. |
| Fixed Price | Cabins covered by a service area but located outside all price areas. |
| Plowing Contract | Normal/private plowing where payment is handled outside the application. |

### Documentation status

| Contract | Status |
| --- | --- |
| Clip Card | Business and migration rules documented. |
| Common Road | Business and migration rules documented. |
| Hybrid | Migration classification documented; pricing rules need clarification. |
| Fixed Price | Area-based migration rule documented; pricing rules need clarification. |
| Plowing Contract | Area and migration rules documented; payment workflow needs clarification. |

Important: the notes explicitly confirm the technical contract types `ClipCardContract`, `CommonRoadContract`, and `PlowingContract`. The extractor code confirms how Hybrid and Fixed Price candidates are selected, but does not show whether they are separate database contract types, product variants, or pricing models in the target system.

## 1. Clip Card With In-App Payment

### Description and use

Clip Card is used when plowing is handled through clips. The contract can be assigned to a `PlowingArea`, including a `PlowingArea` located inside a larger `WorkingArea`.

The notes distinguish between the contract purchase and clip activity:

| Operation | `ReferenceType` | `ReferenceId` |
|---|---|---|
| Clip Card contract itself | `CONTRACT` | `Contract.Id` |
| Clip activation or refill | `CLIP` | `ClipPrice.Id` |

Do not use `Contract.Id` for an order item whose `ReferenceType` is `CLIP`.

### Example use

- A cabin is inside a `PlowingArea`.
- The area has a `ClipCardContract`.
- The system uses that contract because `PlowingArea` is checked before `WorkingArea`.
- A clip activation or refill points to `ClipPrice.Id`.

### Product visibility

The cabin-owner application should eventually show clear Clip Card information and usage history. The exact customer-facing fields are still an open question.

## 2. Common Road With In-App Payment

### Description and use

Common Road is used for plowing a road shared by multiple cabins or customers. It is separate from the private plowing contract for an individual cabin.

One area can have:

- one private contract; and
- one common road contract.

The common road contract should be shown separately from the private contract in customer and administrative overviews.

### Supported areas

A `CommonRoadContract` can use these area types through `ContractArea`:

| Area type | Supported |
|---|---|
| `PlowingArea` | Yes |
| `WorkingArea` | Yes |
| `AdditionalArea` | No |

### Migration flow

1. Create `CommonRoadContract`.
2. Add the related `PlowingArea` or `WorkingArea` to `ContractArea`.
3. Create `Order`.
4. Create `OrderItem`.
5. Create `CabinContract`.
6. Create `Transaction`.

The contract order item uses:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

Example common-road fields mentioned in the migration discussion:

```text
PayOutside = 0
Provider = NETS
```

These are examples from the discussion and should be checked against the target schema before migration.

## 3. Hybrid With In-App Payment

### Description and use

The migration extractor treats Hybrid as a special case connected to monthly payment and area-based pricing.

Confirmed source-selection rules:

- objects inside `price_category` areas receive Hybrid contracts;
- `price_category` cases are handled with monthly-payment cases;
- some monthly-payment providers select cabins by `price_area` geometry;
- other monthly-payment providers select cabins through `provider_objects.price_category_id`;
- both source types are exported with the same object and contract-reference columns; and
- the monthly/Hybrid export does not calculate Clip Card usage.

The monthly export includes one row per unique object per provider. It records the source type, area/category identifiers, latest service period, whether a contract exists, and all contract IDs found for that period.

### What it is used for

Hybrid is used for special monthly-payment plowing arrangements, especially price-category-based areas. The code establishes which cabins are candidates, but does not explain the complete price calculation, renewal, or customer payment behavior.

### Remaining uncertainty

- What features are combined by the Hybrid model.
- Whether all monthly-payment objects become Hybrid contracts.
- How price and usage are calculated.
- Which target `OrderItem.ReferenceType` values are created.
- Whether Hybrid is a contract type or a product/pricing variant.

## 4. Fixed Price With In-App Payment

### Description and use

The migration decision identifies Fixed Price candidates geographically:

- migrate all `service_areas` as contract areas;
- check whether the cabin is inside a `price_area` using `ST_CONTAINS(price_areas.area, object_addresses.position)`;
- cabins inside a `price_area` are handled by Clip Card or Hybrid logic; and
- cabins outside every `price_area`, but inside a `service_area`, can receive Fixed Price contracts.

This avoids creating manual exception areas for the smaller number of cabins covered by a service area but not by its overlapping price area.

### What it is used for

It is used for in-app paid plowing where service-area coverage exists without a more specific price-area contract.

### Remaining uncertainty

- Whether the fixed price covers a season, year, order, or another period.
- Whether usage is unlimited or restricted.
- Renewal, cancellation, and refund rules.
- The exact target contract creation flow and target database value.

## 5. Plowing Contract Without In-App Payment

### Description and use

This is the normal/private plowing contract where payment is handled outside the application. It connects the cabin to the applicable plowing service through an area.

A normal plowing contract order item uses:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

The existing notes confirm the contract and area behavior, but do not document the external invoicing or settlement process.

### Example use

- A cabin is outside a specific `PlowingArea` but inside a `WorkingArea`.
- The `WorkingArea` has a `PlowingContract`.
- No more specific `PlowingArea` contract is found.
- The system falls back to the `WorkingArea` contract.

## Contract Candidate Classification During Migration

The old system does not store the five UI contract labels directly in the exported `contracts` rows. The migration combines legacy contracts, provider configuration, payment data, and geographic/category membership to decide the target contract behavior.

| Source condition | Target contract candidate |
| --- | --- |
| Cabin inside a `price_area` for a Clip Card provider | Clip Card |
| Cabin in a monthly-payment `price_area` case | Hybrid or special monthly-payment handling |
| Cabin linked through `provider_objects.price_category_id` | Hybrid |
| Cabin outside all `price_areas` but inside a `service_area` | Fixed Price |

The extractor explicitly accepts overlap between `price_area` and `service_area`. The more specific price-area Clip Card/Hybrid logic is applied first; service-area Fixed Price logic is for cabins outside price areas.

Monthly payment and price-category cases are intentionally exported through a separate workflow instead of being mixed into the general area export.

Common Road and Plowing Contract without in-app payment are not classified by these area/payment extractor rules. Their behavior comes from the separate contract discussion and target migration design.

## Confirmed Answers From the Contract Discussion

| Question | Confirmed answer | Migration implication |
| --- | --- | --- |
| What should `OrderItem.ReferenceId` contain? | `CONTRACT` uses `Contract.Id`; `CLIP` uses `ClipPrice.Id`. | Never use `Contract.Id` for a clip activation/refill order item. |
| Can one area have private and common-road contracts? | Yes: one private contract plus one common-road contract. | Common Road can coexist with the area's private plowing contract. |
| Which area types can be saved in `ContractArea`? | `PlowingArea` and `WorkingArea` are supported; `AdditionalArea` is not. | Do not migrate an `AdditionalArea` as a contract area. |
| Can `WorkingArea` be used directly? | Yes. | A separate `PlowingArea` is not required for every cabin. |
| Which area contract wins? | Check `PlowingArea` first, then fall back to `WorkingArea`. | A specific Clip Card area can override the broader Working Area contract. |
| Can mixed contract types exist in one `WorkingArea`? | Yes. | Cabins in the nested/overlapping `PlowingArea` can use Clip Card while other cabins use the Working Area's Plowing Contract. |
| Is the proposed Common Road creation flow correct? | Yes. | Create contract, `ContractArea`, order, order item, `CabinContract`, and transaction. |

Area clarification:

- A `PlowingArea` inside or overlapping a `WorkingArea` is supported because they are different area types.
- Areas of the same type should not overlap.
- The discussion does not confirm that one `PlowingArea` should be placed inside another `PlowingArea`; avoid that unless separately approved.
- Creating a separate `PlowingArea` is still preferred when it gives clearer contract separation, but it is not always required.

See `contract-area-use-cases.md` for the two diagram scenarios in a cabin-by-cabin format.

## Shared Contract and Area Rules

### Contract lookup order

The system determines a cabin's contract in this order:

1. Check for a contract assigned to the cabin's `PlowingArea`.
2. If none exists, check for a contract assigned to its `WorkingArea`.

This allows different contract types inside the same `WorkingArea`.

Example:

```text
WorkingArea
|- PlowingArea: Cabin A uses ClipCardContract
|- Outside PlowingArea: Cabin B uses PlowingContract from WorkingArea
```

### ContractArea rules

- `PlowingArea` is supported.
- `WorkingArea` is supported and can be used directly.
- `AdditionalArea` is not supported.
- Areas of the same type should not overlap.
- Company plowing areas can be placed inside a `WorkingArea`.
- Prefer a separate `PlowingArea` when possible because it makes contract separation clearer.

### OrderItem reference rules

| `ReferenceType` | Required `ReferenceId` |
|---|---|
| `CONTRACT` | `Contract.Id` |
| `CLIP` | `ClipPrice.Id` |

## How Contracts Are Used in the Applications

### Cabin-owner application

The customer-facing application supports viewing and managing contracts and plowing services. Contract information should help the cabin owner understand:

- which private plowing contract applies to the cabin;
- whether a separate common road contract exists;
- whether lookup came from `PlowingArea` or `WorkingArea`;
- Clip Card balance or usage history, when relevant;
- related orders, payments, and transaction history; and
- how to contact the provider or support.

The exact fields visible to cabin owners are not yet finalized.

### Backoffice application

Backoffice users manage products/contracts, cabins, customers, service areas, plowing agreements, orders, payments, settlements, and reporting. Useful contract administration views should include:

- common road and private contracts shown separately;
- warnings for inconsistent area or contract setup;
- cabins without a valid plowing contract;
- the area level used for contract lookup; and
- migrated contract data-quality problems.

These items are recorded as improvement ideas, not all as confirmed implemented features.

## Open Questions

1. Is Hybrid a database contract type or a pricing/product variant?
2. Do all monthly-payment candidates become Hybrid, or are additional rules applied during target import?
3. What services and pricing rules make a contract Hybrid?
4. What period and usage does Fixed Price cover?
5. How are renewals, cancellations, and refunds handled for in-app contracts?
6. How is external payment, invoicing, and settlement handled for `PlowingContract`?
7. Which contract details should cabin owners see?
8. Should cabin owners see both private and common road contracts?
9. Which contract data should only be visible to backoffice users?
10. What are the exact target database values for the five contract labels listed here?

## Source Notes

- `HT-new/Business-logic/Plowing-Contracts/discution-with-axon.md`: original questions and confirmed answers from the contract migration discussion.
- `HT-new/Business-logic/Plowing-Contracts/cotract-clipcard-plowing-area-commonroad.md`: consolidated migration, area, reference, and lookup rules.
- `HT-new/Business-logic/Plowing-Contracts/plowing-improvements.md`: proposed contract visibility and administration improvements.
- `HT-new/Business-logic/Plowing-Contracts/contract-migration-data-flow.md`: source-to-target candidate classification and CSV workflows.
- `HT-new/Business-logic/Plowing-Contracts/contract-area-use-cases.md`: nested and overlapping area examples from the discussion screenshots.
- `HT-new/Business-logic/Plowing-Contracts/payment-module-migration.md`: supporting payment-module datasets and contract relationships.
- `HT-new/CabinOwner/workflows.md`: cabin-owner contract and service visibility questions.
- `HT-new/Friio-app-Brain/friio-app-overview.md`: application responsibilities for contracts, payments, plowing, and backoffice management.
