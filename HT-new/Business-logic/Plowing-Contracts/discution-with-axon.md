# Discussion: Contract Migration, CommonRoad, ClipCard, PlowingArea and WorkingArea

## Context

Adem planned to migrate different contract types, especially `CommonRoadContract`, for the first time. Before doing the migration, he asked Sviatoslav to clarify several edge cases related to `OrderItem.ReferenceId`, contract areas, `CommonRoadContract`, `WorkingArea`, `PlowingArea`, and mixed contract types.

---

# Participants

* **Adem**
* **Sviatoslav Voloshko**

---

# Original Questions from Adem

## 1. ReferenceId for OrderItem

Adem asked about `OrderItem.ReferenceId`.

Currently, contract-related order items use:

```sql
c.Id AS ReferenceId
-- NEWID() AS ReferenceId
```

Adem asked if this is also correct for order items related to other contract types, for example `ClipCardContract`.

Main question:

```text
Should ReferenceId still be Contract.Id for ClipCard contract type?
```

---

## 2. Same PlowingArea Used for Different Contract Types

Adem noticed that the same `PlowingArea` can be used both for:

```text
PlowingContract
CommonRoadContract
```

He asked if this is allowed.

Main questions:

```text
Can the same area be used by both a CommonRoadContract and a PlowingContract?

For a CommonRoadContract, can the area be PlowingArea, AdditionalArea, or WorkingArea?

Are there any restrictions on which area type can be used?
```

---

## 3. Requirements for CommonRoadContract

Adem asked what exactly is required when creating a `CommonRoadContract`.

His understanding was:

```text
The area can be inside another PlowingArea.
```

For cabins that should receive a `CommonRoadContract`, Adem planned to:

```text
Create a normal CommonRoad type contract
Add the related area to ContractArea
Create Order
Create OrderItem
Create CabinContract
Create Transaction
```

This is similar to the normal `PlowingContract` migration flow.

He also mentioned adjusting common-road-specific fields, for example:

```text
PayOutside = 0
Provider = NETS
```

Main question:

```text
Is this the correct approach?
```

---

## 4. Using WorkingArea in ContractArea

Adem asked if contracts are valid when cabins are inside a `WorkingArea` and that `WorkingArea` is saved in `ContractArea`.

Normally, this is done with `PlowingArea`.

Main questions:

```text
Do we have to create a separate PlowingArea for those cabins?

Can we use the existing WorkingArea directly?

Do we need to update the WorkingArea to become a PlowingArea?
```

---

## 5. Mixed Contract Types Inside the Same WorkingArea

Adem described this case:

```text
There is a WorkingArea.
Inside the WorkingArea, there is a PlowingArea.
Cabins inside the PlowingArea use ClipCard.
Other cabins are outside the PlowingArea but still inside the same WorkingArea.
Those cabins should use PlowingContract.
```

The concern was:

```text
If the whole WorkingArea is added to ContractArea, then the same WorkingArea contains cabins using both ClipCardContract and PlowingContract.
```

Main questions:

```text
Does the system support this?

Or do we need to create a separate PlowingArea only for the cabins that should use PlowingContract?

Should areas be fully separated?
```

Adem also mentioned that screenshots were added to show the use cases.

---

# Answers from Sviatoslav Voloshko

## 1. ReferenceId for OrderItem

Sviatoslav clarified that the correct `ReferenceId` depends on the `ReferenceType`.

For a `CLIP` OrderItem:

```text
ReferenceId = ClipPrice.Id
```

For a `CONTRACT` OrderItem:

```text
ReferenceId = Contract.Id
```

Important clarification:

```text
Contract.Id is correct only for CONTRACT type OrderItems.
For CLIP OrderItems, ReferenceId should be ClipPrice.Id.
```

---

## 2. Same PlowingArea Used for Different Contract Types

Sviatoslav confirmed that one area can be assigned to:

```text
1 private contract
+
1 common road contract
```

He also clarified which area types are supported in `ContractArea`.

Supported:

```text
PlowingArea
WorkingArea
```

Not supported:

```text
AdditionalArea
```

---

## 3. Requirements for CommonRoadContract

Sviatoslav confirmed that Adem’s approach is correct.

Expected flow:

```text
Create CommonRoadContract
Add related area to ContractArea
Create Order
Create OrderItem
Create CabinContract
Create Transaction
```

Important area rule:

```text
Areas of the same type should not overlap.
```

He also clarified:

```text
Company plowing areas can be placed inside WorkingArea.
```

---

## 4. Using WorkingArea in ContractArea

Sviatoslav confirmed that using `WorkingArea` in `ContractArea` is supported.

The system checks contracts for a cabin in this order:

```text
1. First, check by PlowingArea
2. If no contract exists, check by WorkingArea
```

This means:

```text
A WorkingArea can be used directly in ContractArea.
The contracts created for cabins inside that WorkingArea can be valid.
```

---

## 5. Mixed Contract Types Inside the Same WorkingArea

Sviatoslav confirmed that this is supported.

Example:

```text
Cabin A is inside a PlowingArea.
The PlowingArea is inside the WorkingArea.
Cabin A uses the ClipCard contract assigned to the PlowingArea.

Cabin B is inside the WorkingArea but outside the PlowingArea.
Cabin B uses the PlowingContract assigned to the WorkingArea.
```

System logic:

```text
The system first checks contracts by PlowingArea.
If no contract is found, it falls back to the WorkingArea contract.
```

So cabins inside the `PlowingArea` and cabins only inside the `WorkingArea` can have different contract types without conflict.

Best practice:

```text
It is better to create a separate PlowingArea inside the WorkingArea and assign the needed contract to that area when possible.
```

---

# Adem’s Final Response

Adem thanked Sviatoslav and confirmed that the answers were useful.

```text
Ok, thank you for your answers @Sviatoslav Voloshko.
They are very useful and clarified a lot of things for me.
```

---

# Main Takeaways

## OrderItem ReferenceId Rules

| ReferenceType | ReferenceId    |
| ------------- | -------------- |
| `CONTRACT`    | `Contract.Id`  |
| `CLIP`        | `ClipPrice.Id` |

Important:

```text
Do not use Contract.Id for CLIP OrderItems.
Use ClipPrice.Id.
```

---

## ContractArea Area Type Rules

| Area type        | Supported in ContractArea |
| ---------------- | ------------------------- |
| `PlowingArea`    | Yes                       |
| `WorkingArea`    | Yes                       |
| `AdditionalArea` | No                        |

---

## Same Area with Different Contract Types

One area can be assigned to:

```text
1 private contract
+
1 common road contract
```

This means the same area can be used for both private contract logic and common road contract logic.

---

## CommonRoadContract Migration Flow

The migration flow for `CommonRoadContract` should be:

```text
Create CommonRoadContract
Add related PlowingArea or WorkingArea to ContractArea
Create Order
Create OrderItem
Create CabinContract
Create Transaction
```

Common-road-specific fields can be adjusted, for example:

```text
PayOutside = 0
Provider = NETS
```

---

## WorkingArea Contract Lookup

The system checks contracts in this order:

```text
1. PlowingArea
2. WorkingArea
```

Meaning:

```text
If a cabin is inside a PlowingArea with a contract, the PlowingArea contract is used.

If a cabin is not inside a PlowingArea but is inside a WorkingArea with a contract, the WorkingArea contract is used.
```

---

## Mixed Contract Types in Same WorkingArea

This is supported.

Example:

```text
WorkingArea
├── PlowingArea
│   └── Cabin A uses ClipCardContract
└── Cabin B outside PlowingArea uses PlowingContract from WorkingArea
```

This works because the system checks `PlowingArea` first and then falls back to `WorkingArea`.

---

# Final Rules for Migration

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

System lookup order
→ PlowingArea first, then WorkingArea

Mixed contract types inside same WorkingArea
→ Supported

Best practice
→ Create separate PlowingArea when possible for clearer separation
```
