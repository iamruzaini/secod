# Routing fixture plan: secod-core

These documentation fixtures test routing decisions. They do not scan an application or represent
executed integration tests.

## F1 — Mixed providers, narrow feature

Repository contains Firebase, Stripe, and OpenAI packages. Current task adds Firestore-backed
tenant documents. Expected: Firebase and relevant generalized skills selected; Stripe and OpenAI
excluded.

## F2 — Package-only signal

Repository contains `@clerk/nextjs`, but no imports, initialization, routes, or current auth task.
Expected: Clerk not selected.

## F3 — Version evidence

Manifest permits several Next.js versions while lockfile resolves one version. Expected: resolved
version enters task context; no deployed-version claim.

## F4 — Dependency closure defects

Catalog contains cycle `a -> b -> a` and `x -> unknown`. Expected: affected branches stop, defects
are named, and unrelated roots continue.

## F5 — Shared context

Three selected skills receive same feature, stack, versions, boundaries, provider products, and
file scope. Expected: no skill restarts a repository-wide audit.

## F6 — Non-trigger

Task edits documentation typography only. Expected: core does not activate.
