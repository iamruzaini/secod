# Secure data and file handling: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Every object operation is authorized against trusted ownership and tenant state.
- Accepted content, size, count, processing, and storage scope are bounded.
- Files use generated identifiers and remain non-executable and private by default.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Trusting filename extensions, MIME headers, or client-generated storage paths.
- Serving uploads from an executable origin or public bucket by default.
- Extracting archives or processing media without size and expansion limits.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
