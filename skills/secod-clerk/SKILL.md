---
name: secod-clerk
description: Satisfy secod-auth-provider-integrations and every applicable secod-identity-access requirement. Apply when @clerk/*, clerk, clerkMiddleware, CLERK_* variables, Clerk webhook…
---

# SECOD Clerk

## Scope and applicability

Satisfy `secod-auth-provider-integrations` and every applicable `secod-identity-access`
requirement. Apply when `@clerk/*`, `clerk`, `clerkMiddleware`, `CLERK_*` variables, Clerk
webhook routes, Clerk Organizations, Clerk JWT templates or a Clerk instance/custom domain is
detected. Clerk establishes identity; all application authorization remains backend-enforced.

## Control requirements

Backend Clerk SDK `authenticateRequest()`/`verifyToken()` validation or manual verification only
against the application's fixed Clerk instance JWKS or Dashboard public key; expected JWT
algorithm, signature, issuer, expiry, not-before, subject, token type and
`azp`/`authorizedParties` validation; fixed, configured JWKS trust with `kid` cache/rotation and
one bounded refresh, never a token-provided key/discovery URL; trusted origin and
`authorizedParties` configuration for cross-origin requests; explicit publishable-key versus
server-only secret-key and Backend API key boundary; Dashboard evidence for inactivity timeout,
maximum lifetime, single- versus multi-session behavior, active-session/device management, sign-
out/revocation and unexpected-sign-in response; Clerk fixation protection and
reverification/step-up authentication for sensitive actions; backend authorization of the
immutable Clerk user ID, active organization, role and permission boundary, including pending-
organization state—never UI-only organization state, email domain, display name or stale
browser/custom claim; account for Clerk's per-tab active-organization behavior, so background
work uses the correct current organization token and the backend verifies tenant ownership;
custom JWT claims are minimized, contain no secrets or private sensitive data, respect Clerk
token/cookie size guidance and are not relied on when fresh server-side state is required; MFA,
device trust, bot protection, email/password/recovery and account-linking settings are
evidenced; Clerk/Svix webhook raw-body verification with Clerk's `verifyWebhook()`, supported
timestamp/freshness handling, event-ID deduplication, signed event-type allowlist, retry/replay
handling, durable event processing and reconciliation; exact supported Clerk SDK/configuration
version, instance, custom-domain and development/production separation; negative tests for
expired, malformed, wrong-algorithm, wrong-issuer, wrong-`azp`, unknown/rotated-`kid` and
pending-organization tokens; cross-tenant organization access and multi-tab context confusion;
session revocation and sensitive-action reverification; forged, replayed, duplicate, delayed and
out-of-order webhooks.

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
