---
name: secod-supabase
description: >-
  Help coding agents implement Supabase database, Row Level Security, Storage,
  Realtime, Edge Functions, API keys, and server/client boundaries securely.
  Use when current feature uses Supabase SDKs, config, migrations, or products.
license: Apache-2.0
compatibility: "Requires Supabase; inspect current SDK, key model, schema, and migration tooling."
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Supabase implementation

## Purpose

Build Supabase features with RLS-backed tenant isolation, correct publishable/secret key boundaries,
safe Storage policies, server authorization, reproducible migrations, and negative tests.

## When to use

Use for Supabase database, Auth integration, Storage, Realtime, Edge Functions, SDK clients,
`supabase/config.toml`, or migrations. Add `secod-supabase-auth` when Auth behavior changes.

## Context to inspect

Resolve SDK/tool versions, schemas/tables/views/functions, exposed schemas, grants, RLS policies,
JWT/tenant claims, browser/server clients, key types, Storage buckets/paths, migrations, and tests.

## Secure defaults

- Browser/mobile receives publishable key only; RLS remains authorization boundary.
- Secret or legacy `service_role` key stays in trusted backend and never substitutes for user policy.
- Enable RLS and explicit grants/policies for every exposed table, view, and Storage object flow.
- Derive tenant/user identity from verified session/JWT context, not request fields.
- Keep grants and policies in reviewed migrations and test allowed plus denied paths.

## Implementation workflow

1. Map caller, key type, Postgres role, table/view/function, tenant, and Storage path.
2. Add grants and RLS policies in same migration.
3. Use user-scoped client where RLS should apply; use privileged client only behind explicit authorization.
4. Add database/policy tests and cross-tenant negative cases.
5. Document deployment, key rotation, and environment separation.

## Implementation recipes

- [`references/rls-key-boundaries.md`](references/rls-key-boundaries.md) — tenant RLS, key placement,
  privileged server path, Storage access, and tests.

## Unsafe patterns to avoid

- Exposing secret/`service_role` keys.
- Disabling RLS because API route is authenticated.
- Trusting client tenant IDs inside privileged queries.
- Protecting tables while exposing bypassing views/functions or broad Storage listing.

## Tests to add

Test owner/member success, anonymous denial, cross-tenant denial, forbidden writes, view/function
behavior, Storage list/read/write/delete policies, and privileged endpoint authorization.

## Provider and deployment steps

Name migrations to apply, keys to configure by type, environment/project target, and verification
commands. Never claim dashboard or deployed policy was inspected without access.

## Official sources

Use [`references/sources.md`](references/sources.md); use Supabase `llms.txt` only to discover direct pages.

## Completion handoff

State policies, grants, key boundaries, privileged operations, tests run, and exact deployment action.
Do not certify project security.
