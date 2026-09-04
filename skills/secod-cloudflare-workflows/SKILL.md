---
name: secod-cloudflare-workflows
description: Satisfy secod-cloudflare, secod-inputs-apis, secod-abuse-limits and secod-observability-response. Apply when Workflows definitions/bindings, step.do, retries, waits/events,…
---

# SECOD Cloudflare Workflows

## Scope and applicability

Satisfy `secod-cloudflare`, `secod-inputs-apis`, `secod-abuse-limits` and `secod-observability-
response`. Apply when Workflows definitions/bindings, `step.do`, retries, waits/events, rollback
handlers, schedules, Queue/Worker/HTTP triggers or Workflow instance APIs are detected. Durable
execution does not make input valid, side effects authorized or retries safe.

## Control requirements

Exact Workflow definition/binding/script/environment, trigger/caller, instance ID/event payload,
step name/retry/backoff/timeout, wait-event type/timeout, rollback/compensation, schedule,
retention, status/log/metrics, queue/service binding and production/preview inventory; only
named trusted Worker/service bindings or separately authenticated/authorized HTTP paths can
create, inspect, restart, terminate or send events to an instance, instance ID and event type
cannot grant cross-tenant access, all create/send-event payloads are
schema/tenant/object/signature checked before persistence, and TypeScript types are not mistaken
for runtime validation; every external effect is inside a deterministic granular `step.do`, uses
idempotency key/provider retrieval/reconciliation, has explicit retry
classification/backoff/timeout and `NonRetryableError` behavior, stores no secret or unnecessary
private data in step return/event/state, and registers plus tests compensating rollback where
partial payment, entitlement, deletion or external write must be reversed; top-level state is
derived from durable step return values, no security-relevant state relies on memory or mutable
incoming event, deterministic step names/control flow prevent accidental replay, wait events
have exact type/timeout/authentication and a safe timeout/cancellation path, and
successful/error instance retention/deletion/export follows data classification; schedules,
Queue triggers and child workflows have bounded concurrency, duplicate/cancel/restart semantics,
observability and operator recovery, while every Workflow binding and target is isolated across
production/preview; negative tests for untrusted trigger/instance/event access,
payload/schema/tenant validation failure, side effect outside step, step
retry/rollback/restart/duplicate/cancel defects, stale secret/state retention, wait-event
timeout/replay and cross-environment binding.

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
