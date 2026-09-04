---
name: secod-better-auth
description: Satisfy secod-auth-provider-integrations and every applicable secod-identity-access requirement. Apply when better-auth, betterAuth(), Better Auth route handlers such as…
---

# SECOD Better Auth

## Scope and applicability

Satisfy `secod-auth-provider-integrations` and every applicable `secod-identity-access`
requirement. Apply when `better-auth`, `betterAuth()`, Better Auth route handlers such as
`/api/auth/*`, `BETTER_AUTH_SECRET`/`BETTER_AUTH_*`, Better Auth plugins, or Better Auth
session/account tables are detected. Better Auth establishes identity; all application
authorization remains backend-enforced.

## Control requirements

Explicit production `baseURL`/`BETTER_AUTH_URL`, canonical host and base path; exact
`trustedOrigins` and `allowedHosts` with no broad production wildcards; exact OAuth/SSO callback
and redirect destinations; prohibit `advanced.disableCSRFCheck`, `advanced.disableOriginCheck`,
`account.skipStateCookieCheck`, request-derived production base URLs, and unsafe custom
redirect/callback validation; secure cookie attributes and names, narrowly scoped cross-
subdomain cookie domain, and production `useSecureCookies`; reverse-proxy, IP-header and
`trustedProxies` evidence showing clients cannot spoof rate-limit/session IPs and the origin is
reachable only through trusted proxies; server-only, high-entropy `BETTER_AUTH_SECRET` plus
`secrets`/`BETTER_AUTH_SECRETS` versioned rotation and decryption-retirement plan; explicit
session expiry, `updateAge`, freshness, cookie-cache and secondary-storage strategy,
device/session listing, per-session/all-session revocation and sensitive-action
reauthentication; OAuth Authorization Code + PKCE/state/nonce, bounded state lifetime, exact
provider callbacks and minimum scopes; if a custom `verifyIdToken` callback is used,
independently verify signature, issuer, audience and expiry; OAuth access/refresh tokens are
server-only and encrypted before database storage with managed key rotation because Better Auth
does not encrypt them by default; conservative account-linking policy with explicit trusted
providers, verified provider identity and recent authentication—do not rely on default automatic
verified-email/cross-provider linking; complete enabled-plugin inventory and per-plugin
route/control review for Admin, Organization, SSO/SAML/OIDC, SCIM, API Key, Passkey, 2FA, Magic
Link, Email OTP, One-Time Token, Bearer/JWT, OAuth/OIDC Provider, Device Authorization,
Anonymous, Phone and Username; Admin roles, impersonation, ban and user-management actions have
server-side authorization, audit evidence and step-up protection; Organization
membership/role/permission and organization-creation policy are backend-enforced; SSO/OIDC
discovery and SCIM bearer endpoints use fixed trusted configuration, least privilege, rotation,
organization scope, event reconciliation and deprovisioning; API keys are scoped,
expiry/revocation/audit controlled and never exposed after initial presentation; Magic Link, OTP
and One-Time Token use expiry, single-use, rate limits and safe exact callbacks; passkeys
satisfy the shared WebAuthn contract; production endpoint rate limits, durable shared storage in
serverless/multi-instance deployments, per-route rules and explicit limits for server-side
`auth.api` calls because those bypass Better Auth's built-in client-request limiter; secure
`scrypt` password hashing or an approved custom KDF with hash-migration evidence,
verification/recovery/email-enumeration policy and password-reset/account-deletion controls;
exact Better Auth, plugin and adapter versions plus migration, downgrade and
development/production evidence; negative tests for malicious origin/callback/state/PKCE/ID-
token validation, CSRF-disablement, proxy-IP spoofing, cookie-domain leakage, session
expiry/revocation, unencrypted OAuth tokens, automatic account takeover linking, cross-tenant
organization/admin/API-key/SCIM/SSO privilege escalation, rate-limit bypass and stale database
schema.

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
