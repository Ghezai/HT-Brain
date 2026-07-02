# Contract Area Use Cases

## Purpose

This note explains the `WorkingArea` and `PlowingArea` examples from the contract migration discussion. It converts the screenshots into explicit lookup results that can be checked during migration.

## Confirmed Lookup Rule

For each cabin, the system checks:

1. `PlowingArea` contract.
2. If no applicable contract is found, `WorkingArea` contract.

This is a priority/fallback rule. It allows a specific contract inside a smaller area and a different fallback contract across a broader area.

## Use Case 1: PlowingArea Inside WorkingArea

```text
WorkingArea: PlowingContract fallback
|
|-- PlowingArea: ClipCardContract
|   |-- Cabin A -> Clip Card
|   |-- Cabin B -> Clip Card
|   |-- Cabin C -> Clip Card
|   `-- Cabin D -> Clip Card
|
|-- Cabin X -> Plowing Contract from WorkingArea
|-- Cabin Y -> Plowing Contract from WorkingArea
|-- Cabin Z -> Plowing Contract from WorkingArea
`-- Cabin W -> Plowing Contract from WorkingArea
```

### Result

| Cabin location | First matching area | Contract used |
| --- | --- | --- |
| Inside the nested `PlowingArea` | `PlowingArea` | Clip Card |
| Inside `WorkingArea`, outside `PlowingArea` | `WorkingArea` fallback | Plowing Contract |

Cabins X, Y, Z, and W do not each require their own `PlowingArea` when the existing `WorkingArea` has the correct Plowing Contract.

A separate `PlowingArea` may still be created when clearer operational or migration separation is needed. It is a best-practice option, not a general validity requirement.

## Use Case 2: WorkingArea and PlowingArea Overlap

```text
WorkingArea only        Overlap: both areas        PlowingArea only
Cabin A                 Cabin C                    Cabin E
Cabin B                 Cabin D                    Cabin F
```

Assume:

- `WorkingArea` has a Plowing Contract.
- `PlowingArea` has a Clip Card contract.

### Result

| Cabin position | Area lookup | Contract used |
| --- | --- | --- |
| WorkingArea only | No PlowingArea match, then WorkingArea | Plowing Contract |
| Inside both areas | PlowingArea checked first | Clip Card |
| PlowingArea only | PlowingArea | Clip Card |
| Outside both areas | No match from these areas | No contract from this setup |

Different contract types in the overlap are supported because the lookup order resolves which one applies.

## Common Road on an Area

One area may have:

```text
1 private contract
+
1 common road contract
```

This means a `PlowingArea` or `WorkingArea` can participate in both private plowing and common-road coverage.

Common Road does not replace the private-contract lookup described above. It is a separate common-road contract dimension.

## Supported Area Types

| Area type | Can be used in `ContractArea`? |
| --- | --- |
| `PlowingArea` | Yes |
| `WorkingArea` | Yes |
| `AdditionalArea` | No |

## Overlap Rules

- `PlowingArea` and `WorkingArea` can overlap or be nested because they are different types.
- Areas of the same type should not overlap.
- A `PlowingArea` inside another `PlowingArea` was not confirmed by the discussion and should be avoided unless the platform team approves it.
- Prefer separate, clearly scoped `PlowingArea` records when they make contract ownership and migration easier to understand.

## Common Road Migration Checklist

For cabins receiving `CommonRoadContract`:

1. Create `CommonRoadContract`.
2. Connect the related `PlowingArea` or `WorkingArea` through `ContractArea`.
3. Create `Order`.
4. Create `OrderItem`.
5. Create `CabinContract`.
6. Create `Transaction`.

The contract order item uses:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

Example fields from the discussion:

```text
PayOutside = 0
Provider = NETS
```

These values should still be verified against the target schema and payment configuration for the migration environment.

## Clip Card OrderItem Reminder

| Order item purpose | `ReferenceType` | `ReferenceId` |
| --- | --- | --- |
| Clip Card contract itself | `CONTRACT` | `Contract.Id` |
| Clip activation or refill | `CLIP` | `ClipPrice.Id` |

## Source

- `discution-with-axon.md`: original questions and confirmed answers from Sviatoslav Voloshko.
- The two supplied screenshots: nested-area and overlapping-area contract examples.
