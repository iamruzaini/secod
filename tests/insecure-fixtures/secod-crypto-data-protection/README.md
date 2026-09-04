# Crypto-data-protection fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-crypto-data-protection/run_fixtures.py
```

Runner uses Python standard library only, makes no network calls, and validates synthetic external
evidence bundles. Exit `0` means evidence-intake expectations were reproduced; it does not prove
reviewed application or production behavior.

Executable cases cover complete evidence, missing provider deletion proof, stale restore-test
evidence, hash mismatch, unsafe paths, and control/kind mismatch. Documentation-only unsafe cases
remain: insecure randomness, weak password hashes, ECB, committed all-purpose keys, unclassified
PII, pre-consent analytics, and deletion propagation without a durable ledger.
