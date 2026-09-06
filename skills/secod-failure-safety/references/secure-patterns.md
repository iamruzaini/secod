# Failure-safe application implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Authentication and authorization failures deny access; they never fall open.
- Partial operations preserve or restore business invariants.
- Retries are classified, bounded, idempotent, and observable.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Catching all exceptions and continuing with privileged behavior.
- Retrying non-idempotent writes blindly or forever.
- Returning success before durable state or compensation is established.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
