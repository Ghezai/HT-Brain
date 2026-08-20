# Friio Repo — Code Quality Review of Recent Changes (2026-08-18)

## Purpose

Code quality review of the most recent merged changes in the `Friio` monorepo, covering commits `c31388a3^..HEAD` (2026-08-14 to 2026-08-18). Requested to check the quality of what shipped across the plow-backoffice, webshop, and Platform.Maps backend in that window.

## Context

Commit range reviewed spans four feature areas:

- **Users page redesign** (plow-backoffice) — Keino Valstad
- **Clip history** added to customer webshop and backoffice — Adem Erbas
- **Map layer group renaming** (Platform.Maps backend + backoffice UI) — Keino Valstad
- **Map layers UI design fixes** + docs (`AGENTS.md`, `ARCHITECTURE.md`) — Alban Sejdiu

Review was run as a high-effort multi-angle pass (7 finder agents: line-by-line diff, removed-behavior audit, cross-file tracing, reuse/duplication, simplification, efficiency, altitude/bandaid-fix hunting), then the top findings were verified directly against source before reporting.

## Findings

### Critical / Security

- **Auth middleware disabled in Development environment** — `src/platform/src/API/Platform.API/Program.cs:177`
  `app.UseAuthentication()` / `app.UseAuthorization()` are now wrapped in `if (!app.Environment.IsDevelopment())`. Any deployment running with `ASPNETCORE_ENVIRONMENT=Development` (shared dev/staging box, misconfigured container env var) serves every API endpoint — including user management and map-layer admin writes — with zero auth/authz enforcement.

- **Debug logs leak user/financial data in production** — `src/webshop/application/src/routes/.../contracts/$contractId/details/index.tsx:21` (and `api/plowing-agreements/index.ts`, `api/contracts/index.ts`, `api/orders/index.ts`, `lib/auth/auth-loader.ts`, `contract-details.tsx`)
  Leftover `console.log('[FLOW-N ...]')` statements log `userId`, `cabinId`, `contractId`, and plowing-agreement clip balances on every server-side loader run — leaking per-user identifiers and financial data into production logs, and adding noise/wasted allocation on a hot page.

### Correctness

- **Users page silently truncates to 500 rows, drops pagination** — `src/plow-backoffice/app/routes/__index/users.tsx:98`
  The loader now hardcodes `page: 1, size: 500, roles: []` and ignores the URL's actual search/filter/sort params, doing everything client-side over only the first 500 rows (`showPagination={false}`). Any org with more than 500 platform users will have rows silently missing, with no error or indication.

- **Clip-history pagination total ignores season filter** — `src/plow-backoffice/.../clips-history.tsx:70`
  Rows are filtered client-side to the active contract's season per page, but `CabinDetailsPaginationWrapper` still uses the server's unfiltered `history.total`. A cabin with clip history spanning multiple seasons can land on a page that looks empty ("no history found", pager hidden) even though other pages have data.

- **Resend-invite shown without edit permission** — `src/plow-backoffice/app/routes/__index/users.tsx:330`
  Visibility changed from `canPlatformUserEdit` to the same role-priority check used for Delete, dropping the edit-permission gate. A delete-only admin now sees a clickable "Resend Invite" button that silently 403s server-side instead of being hidden.

- **`Promise.all` result destructured to wrong variable** — `src/webshop/.../contracts/$contractId/details/index.tsx:26`
  `const [contract, plowingAgreementsPreview] = await Promise.all([...])` — the array's second promise is actually `getContractPrices`, not `getPlowingAgreementsPreview` (the third element). Currently only feeds a debug log so it's latent, but a landmine for future logic reading `plowingAgreementsPreview.private`.

- **Notification fetch errors silently swallowed** — `src/webshop/application/src/api/notifications/index.ts:27`
  A new try/catch (tagged `[LOCAL DEBUG]`) swallows any error — network failure, 401, malformed response — and returns an empty result. Real outages/auth problems get masked as "no notifications."

- **Map-layer rename has a check-then-act race** — `src/platform/.../MapLayersRepository.cs:98` (plausible, not fully confirmed)
  `RenameMapLayerGroup` does a conflict check (`AnyAsync`) then a separate `ExecuteUpdateAsync` with no transaction/concurrency guard. Two concurrent renames could both pass the uniqueness check before either commits.

- **Rename modal closes before async result resolves** — `src/plow-backoffice/.../FriioMapLayersControl.tsx:470` (plausible)
  The modal closes immediately after firing the rename request, before the fetcher resolves. On failure, the typed new name is discarded and the user has to reopen and retype.

### Reuse / Simplification / Efficiency

- **Hardcoded Norwegian strings bypass i18n** — `FriioMapLayersControl.tsx:247` — group subtitle labels are inline Norwegian ternaries instead of using the `t(...)` mechanism used elsewhere in the same file.
- **Error-code parsing duplicated across 3 routes** — `renameMapLayerGroup.ts:55`, `putMapLayerArea.ts`, `deleteMapLayerArea.ts` all reimplement the same "split on `. Error: ` then JSON.parse" logic instead of a shared helper.
- **Optimistic update followed by unneeded full revalidate** — `map-editor.tsx:351` — success handlers patch local state manually and then call `revalidator.revalidate()` anyway, doubling network work (4 API calls) on every rename/edit.
- **Inconsistent error-routing pattern** — `ModuleExceptionHandler.cs:27` — new switch arms route by string-matching `ErrorCode` with `when` guards, a different pattern from the rest of the file/other modules which dispatch by exception type.

## Overall Assessment

Feature work itself (clip history, map layer renaming, users page redesign) is reasonably scoped, but this batch shows signs of shipping with debug scaffolding still in place and a couple of scope-reduction shortcuts (hardcoded pagination size, dropped permission check) that look unintentional rather than deliberate.

## Follow-up / Open Questions

- [ ] Confirm whether `ASPNETCORE_ENVIRONMENT=Development` is ever set on a shared/staging/prod-adjacent box — if so, the auth bypass needs an immediate fix.
- [ ] Strip all `[FLOW-N]` / `[LOCAL DEBUG]` console.log and silent-catch scaffolding before next release.
- [ ] Decide whether the users page should restore server-side pagination/filtering or if a deliberate "load all, filter client-side" approach is intended (and if so, raise or remove the 500-row cap).
- [ ] Verify with Keino/Adem whether the Resend-Invite permission change was intentional.
- [ ] Fix the `plowingAgreementsPreview`/`getContractPrices` destructuring mismatch before it's used for real logic.
