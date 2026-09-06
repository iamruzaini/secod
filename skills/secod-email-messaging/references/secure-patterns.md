# Secure email and messaging implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Tokens and codes are random, short-lived, single-use, purpose-bound, and recipient-bound.
- Responses resist account enumeration and abuse while preserving usable recovery.
- Message content and links do not expose secrets or accept open redirects.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Reusable or long-lived OTPs and magic links.
- Embedding sensitive data in URLs, templates, analytics, or provider metadata.
- Allowing caller-controlled recipients, redirect URLs, or templates without policy.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
