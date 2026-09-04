# Executable failure-safety fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-failure-safety/run_fixtures.py
```

Runner uses Python standard library only, writes no files, makes no network calls and emits JSON.
Exit `0` means all nine fixture expectations were reproduced. It does not prove reviewed
application or production safety.

Cases: clean secure behavior, exception detail leak, IdP-timeout fail-open, interrupted multi-step
mutation, blind retry plus webhook replay, absent circuit breaker, orphaned cleanup, cross-tenant
degraded cache and missing production evidence. Expected statuses live in
`tests/expected-results/secod-failure-safety.md`.
