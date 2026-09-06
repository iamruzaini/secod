# Expected result: secod-supabase

The agent enables RLS and writes explicit tenant/member policies, preserves caller identity for
ordinary requests, confines secret/service authority to trusted server paths, and tests owner,
member, cross-tenant, unauthenticated, Storage, and elevated-operation cases. Missing schema or JWT
claim context is resolved before emitting policy SQL.
