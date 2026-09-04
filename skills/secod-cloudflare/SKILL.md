---
name: secod-cloudflare
description: Act as the Cloudflare account, zone and Developer Platform security router. It supersedes the former monolithic scope of secod-cloudflare-workers and routes every detected…
---

# SECOD Cloudflare

## Scope and applicability

Act as the Cloudflare account, zone and Developer Platform security router. It supersedes the
former monolithic scope of `secod-cloudflare-workers` and routes every detected Workers, Pages,
Queues, Workflows, Hyperdrive, Vectorize, Workers AI or AI Gateway profile below; Access,
Turnstile, WAF and Browser Rendering checks remain conditional on actual use. No product profile
replaces this common account, zone, API-token, domain or general app-security layer.

## Control requirements

Exact Cloudflare account, zone, project/script/service, environment, plan, user/service/API
token, account/zone role, custom domain/DNS/TLS, Wrangler/IaC/CI, Access application/policy,
Turnstile sitekey/secret, WAF/ruleset, binding, Logpush/analytics/alert and production/preview
inventory; human access uses least-privilege account/zone roles with MFA/SSO where available,
production owners and API-token owners are named/reviewed, no Global API Key or broad reusable
token where a scoped expiring API token, service token or Wrangler OAuth/federation path
suffices, and CI/deployment tokens cannot modify unrelated accounts, zones or production
resources; exact custom-domain/route/DNS ownership, TLS and origin/redirect configuration,
account/zone/environment separation, immutable IaC/release input and Wrangler secret-versus-
plaintext-variable distinction, with every secret/binding name, type, ID and environment target
validated before deployment and no development override/compatibility flag or production
credential accepted by preview; when Access protects an application, backend code validates the
Access JWT signature against the fixed Cloudflare JWKS source with pinned algorithm, expected
issuer/audience/time/subject/claims, bounded cache/unknown-`kid` refresh and rotation, never
trusts a decode-only token, header identity or token-provided key URL, and retains application
tenant/object/action authorization; when Turnstile is detected, server-side Siteverify checks
expected hostname/action, freshness and single use, and when WAF is detected, review exact
ruleset/rule order/action/logging/bypass/exception and production-preview parity without
claiming either product is mandatory for unrelated apps; account/zone audit logs, deployment
logs and application telemetry exclude secrets, bearer credentials, raw private bodies/prompts
and unnecessary PII, have retention/alert/incident ownership, and exact
Dashboard/API/CLI/source-status/last-modified/review-expiry evidence is retained; negative tests
for token/role/account/zone escalation, unowned domain/DNS/route or preview-production mix-up,
binding/secret leakage, Access JWT/header bypass, Turnstile/WAF bypass where used, disabled
logging and configuration drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare-workers`.

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
