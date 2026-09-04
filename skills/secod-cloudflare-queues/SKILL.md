---
name: secod-cloudflare-queues
description: Satisfy secod-cloudflare, secod-inputs-apis, secod-abuse-limits and secod-observability-response. Apply when Queues producers/consumers, queue bindings, HTTP pull consumers,…
---

# SECOD Cloudflare Queues

## Scope and applicability

Satisfy `secod-cloudflare`, `secod-inputs-apis`, `secod-abuse-limits` and `secod-observability-
response`. Apply when Queues producers/consumers, queue bindings, HTTP pull consumers,
batch/retry/delay settings, dead-letter queues or queue-triggered Workers are detected. Queue
delivery is untrusted, delayed and duplicated; it never authorizes a state change.

## Control requirements

Exact queue/DLQ, producer/consumer script or HTTP pull client, account/environment/binding,
message schema/classification, producer/consumer API token, batch size/timeout, retry/delay,
retention, consumer concurrency, visibility timeout/lease, DLQ/redrive, alert/owner and
production/preview inventory; distinct producer/consumer bindings and minimum API tokens are
scoped to named queues, HTTP pull credentials with required read/write authority remain server-
only and are rotated, no client/browser holds a queue token or lease, and queue/DLQ/environment
names cannot be selected by untrusted input; validate
producer/source/type/schema/version/tenant/object authority and external signature before a side
effect, persist an idempotency/event key, account for batch redelivery and at-least-once/out-of-
order delivery, explicitly acknowledge safely completed messages and retry only safe/idempotent
work, and bound message size, batch, visibility, retry, delay, retention, concurrency, cost and
cancellation; each failure path has an intentional DLQ and active consumer/operator playbook
because messages at retry limit are deleted without a DLQ and unconsumed DLQ messages have
limited retention, redrive revalidates and reauthorizes instead of blindly replaying, and
monitoring alerts on backlog, retry, DLQ, token and consumer failure; negative tests for
unauthorized producer/consumer/pull-token access, forged or cross-tenant message,
duplicate/reordered/replayed batch, partial-ack failure, retry/DLQ deletion or unmonitored
retention loss, unbounded concurrency/cost and preview-production queue drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare`, `secod-inputs-apis`, `secod-abuse-limits`, `secod-observability-response`.

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
