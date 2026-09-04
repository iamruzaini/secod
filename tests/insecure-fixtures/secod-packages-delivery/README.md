# Executable packages-delivery fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-packages-delivery/run_fixtures.py
```

The runner uses the Python standard library, reads the committed source register, writes no
files, makes no network calls and emits JSON. Exit `0` means all fixture expectations were
reproduced. It does not prove that an inspected repository, GitHub organization, registry,
artifact, deployment dashboard or production environment is secure.

Cases exercise all 12 provisional controls: a complete synthetic evidence bundle; one explicit
unsafe issue per control; missing repository, negative-test, dashboard and registry evidence;
pending and expired primary sources; mutable Action and artifact references; privileged
`pull_request_target` checkout; and fail-open attestation verification.

The source-register test requires exactly PKG-S1 through PKG-S8, direct HTTPS URLs, `Reviewed`
status, unexpired review deadlines and a recorded SHA-256 fingerprint. Source freshness supports
review claims only. Real control status still requires the repository and external evidence named
by the skill contract.
