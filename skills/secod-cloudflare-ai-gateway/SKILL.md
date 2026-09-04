---
name: secod-cloudflare-ai-gateway
description: Satisfy secod-cloudflare, secod-ai-api-integrations, secod-secrets-config, secod-abuse-limits and secod-observability-response. Apply when AI Gateway endpoints/bindings, BYOK…
---

# SECOD Cloudflare AI Gateway

## Scope and applicability

Satisfy `secod-cloudflare`, `secod-ai-api-integrations`, `secod-secrets-config`, `secod-abuse-
limits` and `secod-observability-response`. Apply when AI Gateway endpoints/bindings, BYOK
provider credentials, gateway IDs/tokens, caching, logging, DLP/guardrails, rate limits, spend
limits, dynamic routing/fallbacks or custom Access-protected gateway domains are detected.

## Control requirements

Exact account/gateway ID/binding/domain, gateway/API token and permissions, provider/BYOK
credential, model/route/fallback, authentication, Access policy, logging/payload
collection/retention, cache/default/custom cache key/TTL, DLP/guardrail, rate/spend limit,
metadata, billing and production/preview inventory; gateways require authentication, application
calls use a Worker binding or server-only least-privilege token, no browser/client receives
Cloudflare or provider credential, and account-scoped AI Gateway `Run` permissions are not
treated as per-gateway isolation—separate accounts or a Worker-side binding are used where
tenant/gateway isolation requires it; named gateways are explicitly provisioned rather than
accidentally accepting an auto-created default whose logging is on and rate limiting is off,
BYOK keys are least scoped/rotated and provider/model routes/fallbacks meet the same
data/region/retention policy; logging and payload collection are configured for data sensitivity
because request/response bodies can be stored by default, per-request log/cache/metadata headers
are server controlled, sensitive prompts/private output/secrets are excluded or payload logging
disabled, retention/export/deletion/incident evidence exists, and DLP/guardrail outcomes are
monitored without treating them as application authorization; cache behavior is explicit for
each data class, personalized/private/tenant-scoped responses never share a custom cache key or
cache entry across principals, cache TTL/skip overrides and fallback/retry/timeouts are bounded,
and rate/spend/concurrency controls limit abuse/cost; custom domains behind Access have exact
policy and application-level user/tenant authorization, while any `cf.user_id`/metadata is
validated in the app context rather than replacing local authorization; negative tests for
unauthenticated/default-gateway or account-token overreach, client/BYOK credential exposure,
cross-gateway/tenant cache or route leak, payload-log/DLP/export disclosure, custom-
header/cache-key/metadata spoofing, rate/spend/fallback abuse, Access custom-domain bypass and
production-preview gateway/configuration drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare`, `secod-ai-api-integrations`, `secod-secrets-config`, `secod-abuse-limits`, `secod-observability-response`.

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
