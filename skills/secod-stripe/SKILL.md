---
name: secod-stripe
description: Satisfy every secod-payments-billing requirement; treat verified Stripe state as authoritative and keep secret or restricted keys server-side with test/live isolation.
---

# SECOD Stripe

## Scope and applicability

Satisfy every `secod-payments-billing` requirement; treat verified Stripe state as authoritative
and keep secret or restricted keys server-side with test/live isolation.

## Control requirements

Publishable/secret/restricted key boundaries; restricted-key/IP controls; key leak response;
Checkout and PaymentIntent lifecycle, including PaymentIntent reuse rules and 3DS/SCA; outbound
POST idempotency keys; server-resolved price and customer metadata; Connect account and
authorization boundaries where used, including Connect OAuth state/redirect/code handling;
customer-portal authorization; raw-body `Stripe-Signature` verification with signed timestamp
tolerance plus Event object ID/type validation; persistent Event ID deduplication and
idempotency; asynchronous acknowledgement with fast `2xx` before complex work; only subscribing
to necessary events; webhook API-version pinning and API/event version evidence; subscription,
renewal, cancellation, refund, dispute and chargeback entitlement correction; reconciliation.

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
