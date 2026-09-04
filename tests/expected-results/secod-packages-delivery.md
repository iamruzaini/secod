# Expected result: secod-packages-delivery

`run_fixtures.py` exits `0` and emits JSON with `tests_run: 8`, `failures: 0`, `errors: 0`,
`expectations_reproduced: true`, `controls_exercised` containing
`PROVISIONAL-packages-1` through `PROVISIONAL-packages-12`, `source_records: 8`,
`source_register_validated: true`, and dashboard, registry and production evidence set to
`false`.

Expected findings from unsafe cases:

- Missing lockfile, supported-version policy, registry/script policy, minimal permissions,
  hermetic inputs, production gate, immutable artifact, enforced attestation verification or
  rollback path is `Fix before launch` for its mapped control.
- Privileged PR-head checkout with credentials and a signing key committed to the repository are
  `Do not ship`.
- A short Action SHA with an independent digest check is `Recommended hardening`.
- A missing repository artifact, failed/skipped negative test, absent required provider export,
  pending source or expired source is `Not verified`, never `Passed with evidence`.
- Missing dashboard/registry evidence specifically leaves controls -2, -3, -4, -7, -8, -9, -10
  and -11 `Not verified` in the synthetic review matrix.
- Tag-pinned Actions, `latest` production artifacts, privileged untrusted checkout and
  `verify ... || true` are reproduced as unsafe static patterns.

The complete synthetic case returns `Passed with evidence` for matrix coverage only. Local fixture
success never becomes a pass for an inspected repository or production system and never issues a
launch verdict.
