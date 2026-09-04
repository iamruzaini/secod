# Executable secod-secrets-config fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-secrets-config/run_fixtures.py
```

Runner uses Python standard library only, makes no network calls, changes no repository or
provider state, and emits JSON. Exit `0` means all maintained fixture expectations were
reproduced. It does not prove reviewed application, deployed environment, provider, rotation,
revocation, push-protection, cache-purge, or fork/clone state.

Cases cover redacted source/log detection, bearer leakage, excess privilege, template parity,
plaintext/client-exposed secrets, environment conflicts, rotation evidence, revocation paths,
production bypasses, revoke-first history response, default credentials, unauthorized probes,
and a clean repository case. Synthetic markers are not usable credentials. Expected results
live in `tests/expected-results/secod-secrets-config.md`.
