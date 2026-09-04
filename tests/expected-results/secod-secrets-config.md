# Expected result: secod-secrets-config

Fixture runner executes fourteen deterministic cases and exits nonzero on expectation drift.
Unsafe cases reproduce redacted findings for credential-like source/log content, bearer exposure,
overprivileged runtime roles, template gaps, plaintext or client-exposed secrets, environment
identity conflicts, missing revocation paths, production bypasses, misordered history cleanup and
default credentials. Missing rotation evidence and an unauthorized deployed default-credential
probe remain `Not verified`; the probe is never performed. Clean repository case has no finding.

Fixture output never contains synthetic matched credential values. Success proves maintained
harness behavior only. Deployed values, provider secret stores, rotation/revocation completion,
push protection, cache/ref purges, runtime flags and fork/clone state remain `Not verified` until
current authorized evidence is supplied. Output sets `production_evidence: false` and leaves
readiness unissued. Overall launch readiness remains exclusively owned by `secod-ship-check`.
