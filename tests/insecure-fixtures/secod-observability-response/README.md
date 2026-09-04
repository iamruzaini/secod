# Executable observability-response fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-observability-response/run_fixtures.py
```

Runner uses Python standard library only, makes no network calls and emits JSON. Exit `0` means
all maintained fixture expectations were reproduced. It does not prove reviewed application or
production behavior.

Cases cover structured audit events, nested redaction bypass, revoked-key replay, alert routes
without delivery, delivered alert capture, silent sink failure, unexercised runbooks, backup
schedules without restore artifacts, repository-only evidence limits and evidence-bundle intake.
Expected results live in `tests/expected-results/secod-observability-response.md`.
