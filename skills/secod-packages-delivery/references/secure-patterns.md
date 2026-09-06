# Secure packages and delivery: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Dependency choice is justified by maintenance, provenance, permissions, and actual need.
- Builds use reviewed lockfiles and immutable inputs where supported.
- CI and releases use least privilege, protected secrets, traceable artifacts, and tested rollback.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Adding abandoned or unnecessary packages for trivial functionality.
- Executing unreviewed install scripts or floating CI action tags.
- Publishing from developer machines with broad long-lived tokens.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
