# Safe runtime execution: implementation playbook

## Apply during coding

1. Locate untrusted input, trusted policy source, protected effect, persistent state, and failure boundary.
2. Preserve these invariants:

- Untrusted data never selects executable code, command names, or shell syntax.
- Process arguments use structured APIs and strict allowlists.
- Execution runs with bounded resources and least privilege.

3. Use repository's existing language/framework abstractions. Load provider adapter before writing exact SDK calls.
4. Reject unsafe shortcuts:

- Passing concatenated strings to a shell.
- Using denylist escaping as primary command-injection defense.
- Evaluating templates, expressions, or code from untrusted data.

5. Add successful and rejected-path tests for each relevant authorization, tenant, boundary, duplicate, concurrency, retry, and dependency-failure case.

## Missing context

Inspect manifests, lockfiles, schemas, routes, configuration names, and existing tests. If external setting is inaccessible, implement repository-owned work and provide exact provider verification step. Do not convert missing access into scanner verdict.
