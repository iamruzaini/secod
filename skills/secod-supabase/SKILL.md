---
name: secod-supabase
description: Treat RLS, least-privilege Postgres roles and server-side authorization as mandatory for tenant data; never expose or misuse service_role/secret authority. Apply to every detected…
---

# SECOD Supabase

## Scope and applicability

Treat RLS, least-privilege Postgres roles and server-side authorization as mandatory for tenant
data; never expose or misuse `service_role`/secret authority. Apply to every detected Supabase
project and route `secod-supabase-auth` as a required dependency whenever Supabase Auth, JWT
signing keys, OAuth, OTP/email, MFA, CAPTCHA or Auth rate-limit signals exist.

## Control requirements

Exact project ref, organization, region, plan, custom domain, exposed schemas, enabled
Data/GraphQL/Realtime/Storage/Edge Function/Database Webhook/Queue features and
development/preview/production inventory; publishable/legacy `anon` key versus server-only
secret/`service_role` boundaries, with no RLS-bypass key in browser, mobile, public builds,
logs, CI output or untrusted routes; RLS enabled on every exposed table, view, function and
Storage object path with positive and negative tenant/owner/admin tests, least-privilege
`GRANT`/`REVOKE` role review, column-level security for sensitive fields, and secure handling of
`security_definer` functions and views (`security_invoker = true` where a view must obey RLS);
explicit Security Advisor review and resolution/accepted-risk evidence for RLS-disabled or
permissive policies, exposed views/materialized views/functions, sensitive columns, GraphQL
schema exposure and public queues; Storage bucket/object ownership and access policies, public-
bucket decision, signed URL scope/expiry/revocation, upload/download content and size limits,
and bucket/object tenant-isolation tests; Edge Function JWT verification, per-function
authorization, secret isolation, restricted outbound access and webhook validation; Realtime
feature and publication inventory, RLS policies on `realtime.messages`, `private: true` channels
where authorization is required, topic/action/tenant tests, JWT refresh/expiry behavior and
Realtime limits; Data API/GraphQL exposure review, API schema allowlist and Data API disablement
when the application only uses trusted server/database access; SSL Enforcement, database Network
Restrictions and PrivateLink/private-network evidence where available, with connection-string
and pooler access review; organization MFA enforcement, least-privilege organization/project
roles, multiple owners, audit/access review and production/preview separation; Vault encrypted-
secret use and `vault.decrypted_secrets` privilege review, with no database secret in
migrations, source or exposed configuration; migrations, branching/preview database,
replication/publication and release/rollback evidence; database backup retention, backup
encryption/access, PITR/RPO decision and restore test; Postgres connection logging,
security/audit evidence and alerting; when Supabase Auth is detected, exact `secod-supabase-
auth` evidence for JWT signing-key rotation, redirect allowlists, OTP lifetime/entropy, CAPTCHA,
Auth rate limits, custom SMTP/link-tracking safety, session/MFA and Auth configuration; source
URL/status or version/last-modified evidence, reviewed date and review expiry; negative tests
for secret/service-role exposure, RLS/role/column/view/function/GraphQL/queue bypass, cross-
tenant Storage/Realtime/Edge Function access, public API exposure, network/SSL misconfiguration,
Vault-secret disclosure, migration/branch/environment drift and failed backup restoration.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-supabase-auth`.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
