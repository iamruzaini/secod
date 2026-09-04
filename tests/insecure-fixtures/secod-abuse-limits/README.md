# Executable abuse-limits fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-abuse-limits/run_fixtures.py
```

Runner uses Python standard library only, writes auto-cleaned temporary fixture files, retains no
files, makes no network calls and emits JSON.
Exit `0` means all twenty-five named fixture expectations ran normally. Runner fails on missing,
unexpected, skipped or expected-failure cases. It does not prove an inspected
application, deployed limiter store, provider spend controls or production behavior is secure.

Cases cover ABUSE-01 through ABUSE-08: shared and instance-local limiting, missing limiter,
uniform recovery responses, idempotent and duplicate effects, concurrent redemption, bounded
retry, identity-rotation quota bypass, export caps, cancellation, queue shedding, missing external
evidence and explicit `secod-ship-check` handoff.

Seventeen intake cases verify every control across two deployments plus per-deployment shared-store
evidence, collision-safe result identity and refusal for missing, stale, future, malformed,
unknown-control, missing capture identity, over-age evidence, non-finite spend, insufficient
shared-store probes, cross-environment-incomplete or weak provider-spend evidence.
Every refusal preserves
`secod-ship-check` ownership. Structural completeness never proves artifact content or control
passage.

Treat runner JSON as one local test artifact inside a full skill report. Runner does not replace
per-control findings, applicability inventory or deployment/provider evidence review.
