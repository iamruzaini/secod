---
name: secod-dodo-payments
description: Satisfy every secod-payments-billing requirement; verify and deduplicate every event and maintain correct entitlement state across retries, renewal failures, refunds and disputes.
---

# SECOD Dodo Payments

## Scope and applicability

Satisfy every `secod-payments-billing` requirement; verify and deduplicate every event and
maintain correct entitlement state across retries, renewal failures, refunds and disputes.

## Control requirements

Server-only credentials; test/live separation; signing-secret rotation; Standard Webhooks raw-
body signature and timestamp verification with a freshness window; prohibit test-only unsafe
verification helpers in production; persistent `webhook-id` deduplication; event-type
validation; quick acknowledgement and queued processing; delayed, retry and out-of-order
behavior; API request idempotency where supported; customer/subscription mapping; credit and
usage entitlement state; license and dunning events; renewals, refunds, disputes and
cancellations; reconciliation.

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
