# Trigger case: secod-supabase

## Should trigger

```text
Create tenant projects in Supabase with browser reads, server administration, and private Storage.
```

Expected: design RLS with the schema, keep elevated keys server-only, scope Storage policies, use
user-scoped clients where possible, and add SQL/policy tests.

## Should not trigger

```text
Create tenant documents in Firestore with no Supabase dependency or configuration.
```

Expected: Supabase excluded.
