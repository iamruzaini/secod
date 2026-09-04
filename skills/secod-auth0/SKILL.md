---
name: secod-auth0
description: Satisfy secod-auth-provider-integrations and every applicable secod-identity-access requirement. Apply when @auth0/*, auth0, auth0-react, auth0-spa-js, express-oauth2-jwt-bearer,…
---

# SECOD Auth0

## Scope and applicability

Satisfy `secod-auth-provider-integrations` and every applicable `secod-identity-access`
requirement. Apply when `@auth0/*`, `auth0`, `auth0-react`, `auth0-spa-js`, `express-oauth2-jwt-
bearer`, an Auth0 tenant/custom domain, `AUTH0_*`/framework public Auth0 configuration,
Universal Login, Auth0 Actions, Auth0 Organizations, Auth0 Management API, Auth0 Log Streams,
SSO/SCIM or M2M clients are detected. Auth0 establishes identity; all application authorization,
tenant, ownership and high-impact-action decisions remain backend-enforced.

## Control requirements

Exact Auth0 tenant, region, custom domain, application/API identifiers, application type,
enabled connections, grant types, signing algorithm, tenant/Dashboard administrators, SDK
versions and staging/production inventory; Universal Login for new browser login integrations
unless a documented exception requires another maintained flow, and Authorization Code + PKCE
with high-entropy, single-use, short-lived `state`/nonce/code verifier for applicable
applications; no implicit, Resource Owner Password or legacy Rules/Hooks flow without an
explicit, current Auth0-supported exception and compensating review; exact production Allowed
Callback URLs, Allowed Logout URLs, Application Login URI, Allowed Web Origins and CORS origins,
with no broad wildcards, localhost, request-derived return URL or unowned custom subdomain;
exact custom-domain/tenant-domain consistency in redirects, issuer, cookies and Actions; server-
side API authentication uses custom-API access tokens only—not ID tokens, `/userinfo` tokens or
Auth0 Management API tokens—with a fixed expected Auth0 issuer, custom API audience/identifier,
pinned allowed algorithm (RS256 unless a documented, carefully scoped alternative is justified),
signature, `exp`, `iat`, `nbf` where present, `azp`/client and required `scope`/permission
checks; use a fixed configured JWKS/discovery origin, robust key cache, bounded refresh on
unknown `kid`, signing-key rotation, no `decode()`-only acceptance and no attacker-controlled
issuer/JWKS/algorithm/audience; secure application session cookie and SDK session configuration,
with HttpOnly/Secure/SameSite/domain/path policy, session idle and absolute expiry, fixed
login/logout return destinations, SSO/federated logout behavior, session/device revocation and
sensitive-action reauthentication; refresh tokens stored only in secure server-side or HttpOnly
cookie contexts, Refresh Token Rotation enabled where used, a minimal justified overlap/leeway
period, absolute and inactivity expiration, reuse-detection/family-revocation incident response,
atomic replacement and concurrency/retry behavior, with no tokens in local storage, URLs, logs
or browser-to-browser RPC; MFA/step-up policy for privileged actions, phishing-resistant factor
preference where applicable, enrollment/factor-change/recovery and session invalidation
evidence; explicit Auth0 Attack Protection decision and production response settings for Bot
Detection, Suspicious IP Throttling, Brute-force Protection and Breached Password Detection—not
monitoring-only defaults without accepted risk; Actions inventory by trigger, order, version and
environment, with pinned/maintained dependencies, timeout/retry/error behavior, least-privilege
Action Secrets rather than code or logs, no secrets/PII/unencrypted data in URLs or logs, HTTPS
and allowlisted outbound destinations, validation of untrusted event/request data,
`api.access.deny()`/fail-closed behavior for required checks, and production deployment/rollback
evidence; Action redirects must allowlist their destination and validate return state, never put
sensitive data in `api.redirect.encodeToken` because it is signed rather than encrypted, and
account for SSO, silent authentication, refresh exchanges and other flows that may bypass
interactive login; minimal collision-resistant custom claims under a controlled non-Auth0
namespace, no sensitive/private user data or authorization decisions delegated solely to
custom/browser claims, and only exact data needed for the token’s intended resource; when
Organizations, enterprise SSO, SCIM or role/permission features are enabled, immutable Auth0
subject/organization/membership mapping, backend tenant/owner/RBAC checks for every
resource/action, no email-domain or browser-claim tenancy grant, membership/role/deprovisioning
lifecycle reconciliation and production test evidence; Auth0 Management API tokens and M2M
Client Credentials remain server-side, use only the intended Management API or custom API
audience, narrow endpoint/API permissions and client grants, shortest suitable lifetime,
quota/rate-limit handling, secret/key rotation and no client delivery—Management API access
tokens cannot be revoked once issued; Auth0 tenant, Actions and dashboard access use least
privilege, MFA, owner/admin separation, audit history and periodic review; if Log Streams are
enabled, select only necessary event categories, mask PII rather than treat non-cryptographic
obfuscation as encryption, protect the destination, monitor at-least-once duplicate delivery,
retry/pause health and retention/replay, and reconcile security events; exact Auth0 plan,
region, enabled feature maturity, Dashboard configuration, direct-source version or last-
modified evidence, reviewed date and review expiry; negative tests for ID/opaque/Management
token misuse, issuer/audience/algorithm/JWKS confusion and unknown-`kid` flooding, missing
scopes, callback/logout/web-origin/CORS/open-redirect abuse, custom-domain mismatch,
cookie/session fixation and failed logout, refresh replay/reuse/expiry, MFA/step-up bypass,
Action secret/log/redirect/bypass and rollback defects, custom-claim collisions/data leakage,
cross-organization access, M2M/Management API over-scope, attack-protection monitoring-only
configuration, and Log Stream duplicate/pause/PII leakage.

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
