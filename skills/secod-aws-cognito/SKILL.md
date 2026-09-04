---
name: secod-aws-cognito
description: Satisfy secod-aws-web, secod-identity-access and secod-auth-provider-integrations. Apply when Amazon Cognito User Pools, Identity Pools, managed login/hosted UI, app clients,…
---

# SECOD AWS Cognito

## Scope and applicability

Satisfy `secod-aws-web`, `secod-identity-access` and `secod-auth-provider-integrations`. Apply
when Amazon Cognito User Pools, Identity Pools, managed login/hosted UI, app clients, resource
servers, Cognito authorizers, Lambda triggers, federation/SAML/OIDC, MFA, threat protection or
Cognito JWTs are detected. Cognito establishes identity; application tenant, ownership and high-
impact authorization remain backend enforced.

## Control requirements

Exact user/identity pool, Region, domain, app client, app-client type, secret, OAuth grant,
callback/logout URL, scope/resource server, identity provider, federation/attribute mapping,
Lambda trigger, MFA/recovery, threat-protection/WAF, token/session/revocation, group and
environment inventory; public clients have no client secret, confidential/M2M server clients
keep their secret server-side in managed storage and rotate it, public browser/mobile code never
contains AWS credentials or administrative Cognito permissions, and every callback/logout URL is
exact HTTPS in production with no broad wildcard, request-derived redirect or unowned preview
domain; Authorization Code plus PKCE/state/nonce for browser/public clients, minimum
grant/scope/attribute access, fixed issuer/JWKS/RS256/expected token use/client or
audience/expiry/not-before/subject/scope verification at every backend, JWKS cache/key-rotation
behavior, no decode-only trust, no ID token as an API authorization token, refresh-token/session
storage and revocation/logout controls, and no token in URL, local storage, logs or client-to-
client RPC; separate user-pool/app-client configuration and no broad user-pool administrative
IAM role, exact user-pool-to-identity-pool role mapping and unauthenticated identity decision,
least-privilege temporary AWS credentials and role conditions, immutable subject/tenant mapping,
backend object authorization and resistance to group/custom-claim/account-linking escalation;
self-registration, password/MFA/recovery, user-existence-error, rate-limit, WAF and threat-
protection decisions with audit-only rollout followed by explicit enforcement/accepted-risk
evidence, user-event/audit-log access/retention and alerting, and Lambda trigger least
privilege, input validation, timeout/error/fail-closed behavior; negative tests for app-client
secret or AWS-credential delivery, callback/open-redirect/PKCE/state/nonce abuse,
token/JWKS/issuer/audience/scope/algorithm confusion, token revocation/logout failure, identity-
pool role escalation, tenant/attribute/group confusion, anonymous identity or self-signup abuse,
MFA/threat-protection monitoring-only configuration, and trigger privilege escalation.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-aws-web`, `secod-identity-access`, `secod-auth-provider-integrations`.

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
