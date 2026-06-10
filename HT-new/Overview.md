# HT New App Knowledge Overview

## Purpose

The `HT-new` folder is the knowledge base for the new unified HT application.

This folder should collect important information about the new app that is being built from multiple existing apps and systems. The goal is to make it easy for developers, testers, product people, and AI assistants to understand how the new app should work.

Use this folder for notes about:

- App functionality and business rules
- Plowing process
- Contracts
- Areas
- Clip cards
- Common road logic
- Migration questions and decisions
- Business ideas and future improvements
- App workflows and user behavior
- Important discussions with team members or external partners

## Current Main Area: Plowing

The first knowledge area in this folder is `Plowing`.

Plowing notes describe how the new app should handle contract and area logic related to cabins, providers, plowing areas, working areas, common roads, and clip cards.

Current Plowing notes include:

- `Plowing/cotract-clipcard-plowing-area-commonroad.md`
  - Summary of contract migration rules.
  - Explains how `OrderItem.ReferenceId` and `ReferenceType` should work.
  - Covers `ContractArea`, `PlowingArea`, `WorkingArea`, `CommonRoadContract`, `PlowingContract`, and `ClipCardContract`.
  - Includes migration checklist and practical examples.

- `Plowing/discution-with-axon.md`
  - Notes from discussion with Axon/Sviatoslav.
  - Clarifies business and technical rules for contract migration.
  - Documents answers about common road contracts, mixed contract types, and area lookup logic.

## Important Plowing Rules

- `CONTRACT` order items should use `Contract.Id` as `ReferenceId`.
- `CLIP` order items should use `ClipPrice.Id` as `ReferenceId`.
- `ContractArea` supports `PlowingArea` and `WorkingArea`.
- `ContractArea` does not support `AdditionalArea`.
- The system checks cabin contracts by `PlowingArea` first, then falls back to `WorkingArea`.
- Mixed contract types inside the same `WorkingArea` are supported.
- Best practice is to create a separate `PlowingArea` when clearer separation is needed.

## Knowledge Areas

Current folders:

- `Plowing`
  - Plowing process, contract migration, area logic, clip card rules, and common road rules.
- `CabinOwner`
  - Cabin owner web workflows, login behavior, visible data, contracts, orders, and support flow.
- `Backoffice`
  - Backoffice access, roles, permissions, admin workflows, and login issues.
- `BusinessIdeas`
  - Future ideas and improvements for plowing, operations, user experience, and reporting.
- `Discussions`
  - Meeting notes, provider discussions, team clarifications, decisions, and follow-up tasks.

## How To Use This Folder

When adding new knowledge, create a clear markdown file in the correct topic folder.

Good examples:

- `Plowing/contract-rules.md`
- `Plowing/area-rules.md`
- `CabinOwner/workflows.md`
- `Backoffice/user-access.md`
- `BusinessIdeas/plowing-improvements.md`
- `Discussions/meeting-with-provider.md`

Each note should include:

- Short purpose
- Context
- Main rules or decisions
- Examples if needed
- Open questions or follow-up tasks

## Goal

The goal of `HT-new` is to keep important knowledge in one place so future app development, migration, testing, and business decisions are easier to understand and continue.
