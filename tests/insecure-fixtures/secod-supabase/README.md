# Executable implementation fixtures: secod-supabase

Run:

```text
python tests/insecure-fixtures/secod-supabase/run_fixtures.py
```

The fixture models missing RLS, tenant-scoped row access, private Storage objects, service-role
credential boundaries, and server-owned row updates. It uses in-memory data and does not contact a
Supabase project; deployed RLS, Storage policies, and secrets remain external configuration.
