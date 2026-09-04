# Expected result: secod-abuse-limits

`run_fixtures.py` exits `0` and emits JSON with `tests_run: 25`, `expected_tests: 25`,
`coverage_complete: true`, `failures: 0`, `errors: 0`,
`expectations_reproduced: true`, ABUSE-01 through ABUSE-08 in `controls_exercised`, and false
provider/production evidence flags. `release_handoff` contains all control statuses, blockers,
requested external evidence and exclusive `secod-ship-check` verdict ownership.

Expected unsafe behavior reproduces missing and instance-local limits, account enumeration,
duplicate effects, concurrent double redemption, session-key quota bypass, orphan child work and
bounded-queue shedding. Missing deployed-store, provider-spend or production evidence remains
`Not verified`.

Fixture success proves maintained harness behavior only. Runner emits `readiness_verdict:
not_issued` and routes verdict ownership to `secod-ship-check`.
