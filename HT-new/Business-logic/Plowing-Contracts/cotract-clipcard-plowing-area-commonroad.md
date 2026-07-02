# Contract Migration Notes: ClipCard, Plowing, CommonRoad and Areas

## Purpose

This document summarizes the main clarification points about migrating different contract types, especially `CommonRoadContract`, `PlowingContract`, and `ClipCardContract`.

It explains how `OrderItem.ReferenceId`, `ReferenceType`, `ContractArea`, `PlowingArea`, and `WorkingArea` should be used during migration.

---

# 1. OrderItem ReferenceId

For `OrderItem.ReferenceId`, the value depends on the `OrderItem.ReferenceType`.

| ReferenceType | ReferenceId should be |
| ------------- | --------------------- |
| `CONTRACT`    | `Contract.Id`         |
| `CLIP`        | `ClipPrice.Id`        |

## Important rule

For normal contract-related order items:

```sql
ReferenceType = 'CONTRACT'
ReferenceId = Contract.Id
```

For clip-related order items:

```sql
ReferenceType = 'CLIP'
ReferenceId = ClipPrice.Id
```

## Important clarification

For `CLIP` OrderItems, do **not** use `Contract.Id`.

Use:

```sql
ReferenceId = ClipPrice.Id
```

`Contract.Id` is only correct when the `ReferenceType` is `CONTRACT`.

---

# 2. Same Area Used for Different Contract Types

The same area can be assigned to:

```text
1 private contract
+
1 common road contract
```

This means the same area can be used for both:

```text
PlowingContract
+
CommonRoadContract
```

## Supported area types in ContractArea

Only these area types are supported in `ContractArea`:

| Area type        | Supported in ContractArea |
| ---------------- | ------------------------- |
| `PlowingArea`    | Yes                       |
| `WorkingArea`    | Yes                       |
| `AdditionalArea` | No                        |

## Main rule

```text
ContractArea supports PlowingArea and WorkingArea.
ContractArea does not support AdditionalArea.
```

---

# 3. Requirements for CommonRoadContract

The migration approach for `CommonRoadContract` is correct.

The expected flow is:

```text
Create CommonRoadContract
→ Add related area to ContractArea
→ Create Order
→ Create OrderItem
→ Create CabinContract
→ Create Transaction
```

This is similar to the normal `PlowingContract` flow, but details should be adjusted for the common road case.

## Example common road details

```text
PayOutside = 0
Provider = NETS
```

## Area rule

Areas of the same type should not overlap.

Company plowing areas can be placed inside a `WorkingArea`.

---

# 4. Using WorkingArea in ContractArea

Using `WorkingArea` directly in `ContractArea` is supported.

The system checks contracts for a cabin in this order:

```text
1. Check by PlowingArea
2. If no contract is found, check by WorkingArea
```

This means that if cabins are inside a `WorkingArea`, contracts can still be valid when that `WorkingArea` is saved in `ContractArea`.

## Important rule

You do not always need to create a separate `PlowingArea` if the cabins are already inside a valid `WorkingArea`.

However, creating a separate `PlowingArea` can still be better when you need clearer separation.

---

# 5. Mixed Contract Types Inside the Same WorkingArea

Mixed contract types inside the same `WorkingArea` are supported.

Example:

```text
WorkingArea
├── PlowingArea
│   └── Cabin A uses ClipCardContract
└── Cabin B outside PlowingArea uses PlowingContract from WorkingArea
```

The system logic is:

```text
Cabin inside PlowingArea
→ Use contract assigned to PlowingArea

Cabin not inside PlowingArea but inside WorkingArea
→ Use contract assigned to WorkingArea
```

So cabins inside the same `WorkingArea` can use different contract types without conflict.

## Best practice

Even though this is supported, it is better to create a separate `PlowingArea` inside the `WorkingArea` and assign the needed contract to that area when possible.

This gives better separation and makes the migration easier to understand and maintain.

---

# 6. ClipCard Contract Rules

For ClipCard, both `CONTRACT` and `CLIP` can be relevant depending on the order item.

## Contract-based ClipCard order item

Use this when the order item is related to the contract itself:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

## Clip-based order item

Use this when the order item is related to clip activation or clip refill:

```text
ReferenceType = CLIP
ReferenceId = ClipPrice.Id
```

## Main ClipCard rule

```text
ClipCard contract itself → CONTRACT → Contract.Id
Clip activation/refill → CLIP → ClipPrice.Id
```

---

# 7. Plowing Contract Rules

For normal plowing contracts:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

The order item should point to the plowing contract.

Plowing contracts do not need a special reference type.

---

# 8. CommonRoad Contract Rules

For common road contracts:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

The area connected to the contract should be saved in `ContractArea`.

Supported area types:

```text
PlowingArea
WorkingArea
```

Not supported:

```text
AdditionalArea
```

---

# 9. System Contract Lookup Order

The system checks which contract applies to a cabin in this order:

```text
1. PlowingArea
2. WorkingArea
```

This means:

```text
If cabin is inside a PlowingArea with a contract
→ Use the PlowingArea contract

If cabin is not inside a PlowingArea but is inside a WorkingArea with a contract
→ Use the WorkingArea contract
```

---

# 10. Final Simple Rules

```text
CONTRACT OrderItem
→ ReferenceId = Contract.Id

CLIP OrderItem
→ ReferenceId = ClipPrice.Id

ContractArea supports
→ PlowingArea and WorkingArea

ContractArea does not support
→ AdditionalArea

Same area can be used for
→ 1 private contract + 1 common road contract

System contract lookup order
→ PlowingArea first, then WorkingArea

Mixed ClipCard and PlowingContract in same WorkingArea
→ Supported

Best practice
→ Prefer separate PlowingArea when possible
```

---

# 11. Migration Checklist

| Check                                    | Rule                                                        |
| ---------------------------------------- | ----------------------------------------------------------- |
| Normal contract order item               | Use `ReferenceType = CONTRACT`, `ReferenceId = Contract.Id` |
| Clip order item                          | Use `ReferenceType = CLIP`, `ReferenceId = ClipPrice.Id`    |
| ClipCard contract itself                 | Use `CONTRACT` with `Contract.Id`                           |
| Clip activation/refill                   | Use `CLIP` with `ClipPrice.Id`                              |
| PlowingContract                          | Use `CONTRACT` with `Contract.Id`                           |
| CommonRoadContract                       | Use `CONTRACT` with `Contract.Id`                           |
| CommonRoadContract area                  | Use `PlowingArea` or `WorkingArea`                          |
| AdditionalArea                           | Do not use in `ContractArea`                                |
| Overlapping areas                        | Avoid overlapping areas of the same type                    |
| WorkingArea fallback                     | Supported                                                   |
| Mixed contract types in same WorkingArea | Supported                                                   |
| Best practice                            | Prefer separate `PlowingArea` when possible                 |

---

# 12. Practical Migration Example

## Case 1: Cabin inside PlowingArea with ClipCardContract

```text
Cabin is inside PlowingArea
PlowingArea has ClipCardContract
System uses ClipCardContract
```

Order item for the contract:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

Order item for clip activation/refill:

```text
ReferenceType = CLIP
ReferenceId = ClipPrice.Id
```

---

## Case 2: Cabin outside PlowingArea but inside WorkingArea with PlowingContract

```text
Cabin is not inside PlowingArea
Cabin is inside WorkingArea
WorkingArea has PlowingContract
System uses PlowingContract
```

Order item:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

---

## Case 3: CommonRoadContract using PlowingArea or WorkingArea

```text
Create CommonRoadContract
Connect PlowingArea or WorkingArea in ContractArea
Create Order
Create OrderItem
Create CabinContract
Create Transaction
```

Order item:

```text
ReferenceType = CONTRACT
ReferenceId = Contract.Id
```

---

# 13. Key Conclusion

The migration logic is valid as long as the correct `ReferenceType`, `ReferenceId`, and area type are used.

The most important distinction is:

```text
CONTRACT → Contract.Id
CLIP → ClipPrice.Id
```

For areas:

```text
Use PlowingArea or WorkingArea in ContractArea.
Do not use AdditionalArea.
```

For contract lookup:

```text
The system checks PlowingArea first.
If no contract is found, it falls back to WorkingArea.
```
