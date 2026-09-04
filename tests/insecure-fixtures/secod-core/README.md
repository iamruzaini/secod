# Insecure fixture plan: secod-core

Minimal reproducible unsafe cases for routing/classification controls. Documentation-only plan;
no executable code is maintained in this repository.

## F1 — Manifest-only provider signal

`package.json` contains `@clerk/nextjs`; no imports, no `clerkMiddleware`, no `CLERK_*` names,
no webhook route. Expected classification: `Candidate`. Failure mode under test: reporting
Clerk as active or secure from package presence alone.

## F2 — Environment version conflict

Lockfile resolves `next@15.x`; supplied production build artifact reports `next@14.x`.
Expected classification: `Conflicting`, routed to `secod-nextjs`, launch coverage blocked until
reconciled.

## F3 — Closure defects

Dependency graph contains cycle `a -> b -> a` and edge `x -> unknown-slug`. Expected: both
branches terminate with named reports, unrelated branches continue, affected controls
`Not verified`, launch verdict prohibited.

## F4 — Missing-evidence case

Search over one workspace root times out mid-enumeration. Expected: mechanism failure recorded,
searched scope stated, partial evidence retained, inventory completeness `Not verified`, next
verification step named. Never `Passed with evidence`.

## F5 — Undocumented sensitive export

Admin endpoint `/admin/export` streams a database dump; contents not documented anywhere.
Expected: flow classified `Unknown`, routed to `secod-crypto-data-protection` review, launch
readiness prevented until authorized evidence reclassifies it.
