# Executable implementation fixtures: secod-nextjs

Run:

```text
python tests/insecure-fixtures/secod-nextjs/run_fixtures.py
```

The fixture models a Server Action called directly outside the UI, server-only environment
secrets, and tenant/user-scoped cache keys. It proves authorization comes from verified session
state and public configuration is the only client-bound configuration. No Next.js app or deployed
environment is inspected.
