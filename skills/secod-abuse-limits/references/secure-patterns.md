# Abuse-resistant feature implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Limits apply at relevant IP, user, tenant, resource, and global scopes.
- Duplicate, concurrent, delayed, and replayed requests preserve business invariants.
- Backoff, queue bounds, and budgets prevent failures from amplifying load.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Single global limit where per-identity or per-tenant abuse matters.
- Retrying every failure without jitter, attempt bounds, or idempotency.
- Check-then-write logic without atomic enforcement.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
