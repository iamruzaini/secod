# Executable critical-behavior fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-critical-behaviors/run_fixtures.py
```

Runner uses Python standard library only and makes no network calls. It exercises intentionally
insecure and guarded in-memory sample behaviors for broken tenant authorization, missing
server-side authorization, exposed secrets, weak webhook verification, payment replay,
unrestricted file upload, public storage, command injection, SSRF, missing rate limits, retry
storms, sensitive logs, unsafe AI tool execution, and cross-tenant vector retrieval.

Exit `0` means all fourteen named expectations reproduced. Output explicitly keeps production
evidence false and readiness unissued. These fixtures test SECOD guidance contracts; they do not
prove that an inspected application, deployed service, provider dashboard, or production runtime
is secure.
