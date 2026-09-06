# Cryptography and protected-data implementation: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Use maintained cryptographic libraries and purpose-specific primitives; never invent cryptography.
- Keys remain separate from ciphertext and have rotation and recovery paths.
- Protected data is minimized across storage, logs, backups, caches, and deletion.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Custom encryption, hardcoded keys, static nonces, or reversible password storage.
- Using plain hashes for passwords or unauthenticated encryption for protected records.
- Claiming encryption solves authorization, retention, or exposure in application memory.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
