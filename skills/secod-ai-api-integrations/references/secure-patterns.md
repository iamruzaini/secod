# Secure AI feature implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Model input and output remain untrusted across every application boundary.
- Retrieval, memory, files, and tools preserve caller and tenant authorization.
- Consequential effects require deterministic server policy and appropriate confirmation.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Letting model text or tool arguments directly select privileged effects.
- Retrieving across tenants or placing secrets in prompts.
- Assuming system prompts, schema mode, or model alignment is authorization.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.

## Short-lived client tokens

Load exact provider recipe before implementing realtime or browser/mobile client tokens. Confirm
token minting authority, scope, audience, expiry, replay constraints, and session limits from a
direct official page. Keep long-lived credentials server-side and prevent clients from broadening
scope or tool authority.
