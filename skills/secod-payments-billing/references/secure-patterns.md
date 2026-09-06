# Correct payment and entitlement implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Server-owned product, price, currency, customer, tenant, and entitlement state is authoritative.
- Entitlements change only from authenticated provider state and idempotent transitions.
- Duplicate, delayed, and out-of-order events converge through reconciliation.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Trusting browser prices, customer IDs, payment success, or redirect parameters.
- Granting entitlement before verified provider state.
- Assuming webhook delivery is unique, ordered, or immediate.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
