# Threat-aware feature design: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Every sensitive flow has named actors, assets, entry points, trust boundaries, and abuse cases.
- Security requirements become implementation decisions and tests, not a standalone report.
- Scope stays limited to the feature being built unless broader modeling is requested.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Starting implementation without locating trust and tenant boundaries.
- Producing a generic threat report disconnected from code changes.
- Treating STRIDE labels as evidence that risks were mitigated.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
