---
name: secod-workos
description: Satisfy secod-auth-provider-integrations and every applicable secod-identity-access requirement. Apply when @workos-inc/*, WorkOS/AuthKit SDKs, WORKOS_API_KEY, WORKOS_CLIENT_ID,…
---

# SECOD Workos

## Scope and applicability

Satisfy `secod-auth-provider-integrations` and every applicable `secod-identity-access`
requirement. Apply when `@workos-inc/*`, WorkOS/AuthKit SDKs, `WORKOS_API_KEY`,
`WORKOS_CLIENT_ID`, AuthKit, SSO, Directory Sync, SCIM, RBAC, Audit Logs, API Keys, API Gateway,
WorkOS Actions or WorkOS webhooks are detected. WorkOS establishes identity; every application
authorization, tenant, ownership and high-risk-action decision remains backend-enforced.

## Control requirements

Explicit Hosted AuthKit UI versus custom Authentication API/SSO flow decision, with an exact
application/client ID, canonical custom/hosted authentication domain, environment, endpoint and
SDK inventory; server-only WorkOS API keys, WorkOS signing/action/webhook secrets and per-
environment client IDs, with least privilege, rotation, source control exclusion and strict
staging/production isolation—never mix API keys, Client IDs, organizations, connections, users,
webhook endpoints or secrets across environments; backend validation of every AuthKit access JWT
using only the fixed client-specific WorkOS signing JWKS and a pinned allowed algorithm,
signature, expected issuer (including the configured custom AuthKit domain), expected
audience/client ID, `exp`, `iat`, `nbf` where present, `sub`, `sid`, token type and required
organization/role/permission claims; JWKS cache, bounded unknown-`kid` refresh, key rotation and
failure behavior that never accepts token-provided issuer, JWKS URL, algorithm or tenant; secure
sealed session-cookie configuration, high-entropy versioned cookie-sealing secret and
rotation/retirement plan, HttpOnly/Secure/SameSite/domain/path policy, no browser-readable
access or refresh tokens, and no credentials in URLs, logs or client RPC; WorkOS Dashboard
evidence for maximum session length, short access-token duration, inactivity timeout,
session/device visibility, sensitive-action reauthentication, per-session and all-session
revocation, and logout that deletes the application session and calls the WorkOS logout
endpoint; refresh tokens stored only server-side or in secure HttpOnly cookies, treated as
single-use/rotated, atomically replaced on every successful refresh, with WorkOS session-
resilience/replay-grace and concurrent-refresh failure handling explicitly tested; exact
production authorization callback, redirect, sign-in and sign-out URL allowlists, no broad
production wildcards or request-derived destinations, Authorization Code + PKCE/state/nonce
where the selected API flow uses them, and tested SP-initiated plus IdP-initiated SSO including
IdP error, RelayState and unexpected connection behavior; custom AuthKit domain configured
before enabling production passkeys, passkey hosted-UI limitation, progressive-
enrollment/recovery/deletion policy and the shared WebAuthn contract; organization
selection/switching only through verified membership, immutable WorkOS
subject/organization/membership mapping, backend tenant/owner/RBAC/permission checks at each
resource and action, minimal JWT-template/role claims (including the browser cookie size limit),
and no authorization solely from a browser claim, email domain or UI selection; inventory and
test Organization Policies, JIT/directory provisioning, SSO and SCIM/Directory Sync
deprovisioning, group/role changes and membership reactivation, durable event cursor/ID storage,
stale-event timestamps, idempotent upserts and reconciliation with the Events API or
authoritative WorkOS API before local access is granted, changed or revoked; raw-body WorkOS
Actions and webhook verification before parsing or acting, using the provider SDK or equivalent
`WorkOS-Signature` timestamp plus HMAC-SHA256 check with a bounded freshness tolerance and
constant-time comparison, fixed per-environment secret, persistent event/delivery-ID
deduplication, queued processing after fast `2xx`, duplicate/delayed/out-of-order/retry and
disablement recovery, event-type/object/context validation, fail-closed action verdicts, and
correctly signed WorkOS Action responses; MFA policy evidence that explicitly accounts for the
documented fact that AuthKit MFA does not apply to SSO users, with organization/IdP MFA policy
or an accepted residual risk; Audit Log/event evidence for privileged identity, membership,
role, session and configuration changes; if AuthKit API Keys or API Gateway is enabled, least-
privilege user/organization key permission policy, one-time secret presentation, validation with
WorkOS plus local tenant/permission authorization, revocation/rotation, and per-request gateway-
assertion signature/issuer/audience/expiry validation; exact WorkOS product, SDK/API versions,
custom-domain/Dashboard settings, plan/feature maturity, region where relevant, direct-source
version or last-modified evidence, reviewed date and review expiry; negative tests for
token/JWKS/issuer/audience confusion, custom-domain issuer mismatch, session/refresh replay or
race, cookie disclosure, callback/RelayState/redirect abuse, staging-production cross-wiring,
cross-tenant organization or role escalation, missed/stale/deprovisioning events,
forged/replayed/out-of-order Actions/webhooks, Action allow-on-error, SSO-without-MFA, and
passkey custom-domain migration failure.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-auth-provider-integrations`, `secod-identity-access`.

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
