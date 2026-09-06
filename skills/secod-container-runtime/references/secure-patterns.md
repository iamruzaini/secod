# Secure container implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Images contain only required runtime content and use immutable provenance where supported.
- Workloads run non-root with minimal capabilities, writable paths, and network access.
- Build and runtime secrets never become image layers or environment disclosures.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Running as root, privileged mode, host namespaces, or broad volume mounts by default.
- Copying repository secrets or build credentials into image layers.
- Using mutable tags as only production artifact identity.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
