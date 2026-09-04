---
name: secod-supabase-auth
description: Satisfy secod-identity-access, secod-auth-provider-integrations and secod-supabase; always route with secod-supabase, which remains the owner for database, Storage, Realtime and…
---

# SECOD Supabase Auth

## Scope and applicability

Satisfy `secod-identity-access`, `secod-auth-provider-integrations` and `secod-supabase`; always
route with `secod-supabase`, which remains the owner for database, Storage, Realtime and Edge
Function RLS/data controls. Apply when `supabase.auth.*`, `@supabase/supabase-js`,
`@supabase/ssr`, GoTrue/Auth configuration, Auth Hooks, MFA, OAuth/social login, SSO, third-
party Auth, `SUPABASE_*` credentials or Supabase JWT signing-key configuration is detected.
Supabase Auth establishes identity; all application authorization and tenant/owner boundaries
remain backend and RLS enforced.

## Control requirements

Exact Supabase organization/project/reference, region, plan, custom domain, Auth
provider/connection, SMTP, OAuth/SSO, MFA, captcha, rate-limit, redirect, session, Auth Hook and
signing-key inventory with development/preview/production separation; strict publishable
(`sb_publishable_...`) versus secret (`sb_secret_...`) and legacy `anon` versus `service_role`
authority boundaries, no secret or service-role credential in browser/mobile/desktop/public
build, logs, CI output or untrusted server route, and no secret-key/RLS-bypass call until the
developer-controlled backend has authenticated and authorized the user, tenant and resource;
asymmetric JWT signing keys (prefer the current Supabase signing-key system over the legacy
shared JWT secret/HS256), fixed project JWKS verification or `supabase.auth.getClaims()`/a
vetted JWT verifier, pinned expected issuer, algorithm, `kid`, expiry, subject, role, session
and required claims, bounded cache/unknown-`kid` refresh and key-revocation behavior; tested
migration from the legacy JWT secret, including dependent API keys/Edge Functions, cache
propagation, staged rotation, legacy-key revocation and incident cache-bust plan; explicit Auth
Dashboard evidence for session maximum lifetime, inactivity timeout, access-token lifetime and
single-session-per-user policy—because the defaults permit indefinite, multi-device sessions—and
refresh-token reuse detection kept enabled with its retry/reuse interval, serial refresh
handling and whole-session revocation response; sensitive actions validate the current
authenticated session and, where immediate logout/revocation is required, validate
`session_id`/server session state rather than treating a still-unexpired JWT as proof; correct
PKCE for SSR/server flows, single-use authorization-code exchange and secure `@supabase/ssr`
cookie adapter behavior on every response, with HttpOnly/Secure/SameSite/domain/path policy
appropriate to the server-only architecture, no hand-rolled unsafe token persistence, no
access/refresh tokens in URLs/logs, and no server authorization decision from unverified
`getSession()` cookie data; exact Site URL, email-template origin and redirect allowlist with
narrowly bounded local and preview patterns only, no broad production wildcard, open redirect or
unowned preview/custom domain; fixed OAuth/provider callback configuration, minimum scopes,
provider-token handling and refresh policy, with provider tokens/refresh tokens sent to a
trusted server before any use outside the completing browser because Supabase does not store
them; email/password/magic-link/OTP/recovery/invite/identity-linking configuration, password
strength and breached-password policy, reauthentication/current-password requirement for
password change, single-use/expiry and anti-prefetch email confirmation design, server-side
redirect verification, security notification emails, custom SMTP limits and no token, user
metadata or sensitive state disclosure in templates; CAPTCHA/Turnstile or hCaptcha configuration
and server verification where detected, realistic Auth rate limits for email, OTP, password
reset, verification, refresh, MFA and anonymous sign-in, and trusted-proxy evidence before
enabling `Sb-Forwarded-For` with a secret key; MFA enrollment, challenge, recovery, factor
removal and reauthentication controls plus server, API and restrictive RLS enforcement of `aal2`
for sensitive operations—MFA UI or an `aal` browser claim alone is insufficient; Auth Hook
inventory for Send Email/SMS, Custom Access Token, Password/MFA verification and enabled
HTTP/Postgres hooks, raw-body Standard Webhooks signature/timestamp verification and schema
checks for HTTP hooks, outbound destination/timeout/error handling, fail-closed business
decisions, migration/version evidence, and no insecure `SECURITY DEFINER`: grant only the
minimum `supabase_auth_admin` execution/schema access and revoke `anon`, `authenticated` and
`public` access; custom access-token hooks preserve all required claims, add only minimal non-
sensitive claims and never let mutable `user_metadata`, client claims or an untrusted role
bypass backend/RLS authorization; when SAML SSO, social OAuth, identity linking, third-party
Auth or external JWTs are enabled, fixed issuer/discovery/JWKS and audience/claim mapping,
asymmetric-key and key-rotation requirements, immutable local subject/tenant mapping, account-
linking takeover resistance, backend/RLS tenant checks, deprovisioning/reconciliation and any
companion provider adapter (such as `secod-clerk`, `secod-auth0` or `secod-workos`) routed as a
required dependency; Supabase Auth audit-log storage, retention and access policy, project
Security Advisor findings and sensitive authentication-event alert/review evidence; exact
Supabase SDK/GoTrue/configuration versions, source URL/status/version or last-modified evidence,
reviewed date and review expiry; negative tests for browser secret/service-role exposure and RLS
bypass, legacy-secret/HS256/JWKS/issuer/claim confusion and stale key cache, session
timeout/single-session/logout/refresh-token replay, SSR cookie/code-exchange/getSession trust
defects, callback/email/template/OTP abuse, OAuth token leakage, CAPTCHA/rate-limit/proxy-header
bypass, AAL2/MFA/RLS bypass, forged Hook payloads, Hook privilege escalation or `SECURITY
DEFINER`, custom-claim escalation, third-party JWT/tenant mismatch, and
development/preview/production configuration drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-identity-access`, `secod-auth-provider-integrations`, `secod-supabase`.

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
