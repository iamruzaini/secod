# Expected result: secod-failure-safety

Fixture runner executes nine deterministic cases and exits nonzero on expectation drift. Expected
unsafe cases reproduce findings for exception disclosure, identity-provider fail-open, partial
mutation, blind retry/replay, missing breaker, orphaned cleanup and cross-tenant degraded cache.
Clean case reproduces secure behavior. Missing-evidence case remains `Not verified`.

Fixture success proves only maintained harness behavior. Production degraded-state behavior,
distributed breaker consistency and outage readiness remain `Not verified` until artifacts listed
in `skills/secod-failure-safety/references/external-evidence.md` are supplied. Overall launch
readiness remains exclusively owned by `secod-ship-check`.
