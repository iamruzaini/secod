# Executable implementation fixtures: secod-identity-access

Run:

```text
python tests/insecure-fixtures/secod-identity-access/run_fixtures.py
```

The fixture contrasts request-controlled tenant/role decisions with verified-session identity,
server-loaded ownership, tenant-admin authorization, cross-tenant denial, and unauthenticated
denial. It uses an in-memory store only. It is not a scanner or proof of deployed authorization.
