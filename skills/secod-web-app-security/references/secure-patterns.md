# Secure browser-facing implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Untrusted content never becomes executable markup or script.
- State-changing requests require server authorization and appropriate CSRF/origin protection.
- Browser controls complement server enforcement; they never replace it.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Rendering unsanitized HTML or constructing script from untrusted strings.
- Trusting CORS, hidden UI, or SameSite alone as authorization.
- Putting credentials or sensitive durable state in browser-accessible storage.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
