# Executable implementation fixtures: secod-inputs-apis

Run:

```text
python tests/insecure-fixtures/secod-inputs-apis/run_fixtures.py
```

The fixture exercises SSRF allowlisting plus DNS-result checks, raw-body HMAC verification,
payload validation, and argument-safe command construction. It uses deterministic callbacks and
does not make network or shell calls. It is not a scanner or proof of deployed behavior.
