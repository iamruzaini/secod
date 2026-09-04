---
name: secod-polar
description: Satisfy every secod-payments-billing requirement; bind checkout and customer state to the authenticated application user and grant entitlements only from verified provider state.
---

# SECOD Polar

## Scope and applicability

Satisfy every `secod-payments-billing` requirement; bind checkout and customer state to the
authenticated application user and grant entitlements only from verified provider state.

## Control requirements

Scope-limited server credentials; organization access token versus customer-session token
boundary; test/production separation; server-created checkout with `embed_origin`; customer and
tenant mapping; treat checkout `confirmed` as not equivalent to paid; verified Standard Webhooks
encoding requirements, raw body, `webhook-signature`, `webhook-timestamp` and `webhook-id`;
timestamp tolerance and persistent delivery-ID deduplication; rapid asynchronous acknowledgement
and queued processing; no-redirect delivery handling; idempotent delayed/out-of-order/retry
handling; rate-limit response handling; disabled-endpoint alerting and delivery-disablement
monitoring; subscription and benefit/entitlement events; refund/cancellation handling; no
browser-result entitlement grants; reconciliation.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-payments-billing`.

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
