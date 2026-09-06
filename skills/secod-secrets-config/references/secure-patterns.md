# Secure secrets and configuration: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Privileged credentials never enter source, client bundles, URLs, logs, prompts, or responses.
- Each environment and workload uses scoped credentials with rotation and revocation paths.
- Production starts only with validated secure configuration; no silent insecure fallback.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Prefixing a secret as public/client configuration.
- Committing example values that are usable credentials.
- Falling back to default keys, permissive origins, or disabled verification.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
