# Production evidence and outage-drill contract

Use this contract when repository evidence cannot establish deployed failure behavior. Blank
templates, screenshots without resource identity, and unexecuted runbooks are not evidence.

## Required production artifacts

For each environment and critical dependency, request:

- resource/service identity, environment, region, deployment version and capture time;
- redacted breaker configuration and timestamped open, trial and closed transitions;
- request counts proving calls stopped reaching the dependency while breaker was open;
- degraded-mode captures for authenticated, unauthorized and cross-tenant requests;
- retry/DLQ/pool configuration exported from the provider Dashboard or Management API;
- outage-drill result with operator, approver, start/end time, observations and follow-up owner.

Evidence must be current, internally consistent and tied to reviewed deployment. Record stale,
partial, inaccessible or contradictory artifacts as `Not verified`.

## Distributed breaker consistency check

Test every production topology class in an authorized non-production environment first:

1. Identify instance, region and shared-state scope for each breaker.
2. Sustain dependency failures until configured threshold.
3. Capture dependency call count per instance and aggregate call count.
4. Confirm all instances fast-fail within one configured observation window.
5. Confirm only bounded trial calls occur during recovery and authorization still fails closed.
6. Repeat during scale-out or instance replacement; record divergence and maximum added calls.

Per-instance breakers may pass local trip behavior but remain `Recommended hardening` when
aggregate pileup is possible. Claim `Passed with evidence` only when topology-matched captures
show bounded aggregate calls.

## Provider-outage drill

Preconditions: named incident commander, authorized non-production target, rollback owner,
dependency-specific stop conditions, dashboards open and no real user/payment mutations.

1. Record healthy baseline and deployment identity.
2. Inject timeout, connection refusal and provider error separately.
3. Verify authorization denies, mutations roll back or reconcile, retries stay bounded, breaker
   opens, cancellation stops child work, cleanup completes and outward errors remain redacted.
4. Verify degraded responses remain tenant-scoped and privileged writes stay disabled.
5. Restore dependency, observe bounded trial traffic, reconcile durable intermediates and confirm
   normal service only after invariants hold.
6. Save redacted logs, metrics, traces, result, deviations, follow-up owner and due date.

Abort immediately on real-user impact, cross-tenant disclosure, unbounded traffic, uncontrolled
cost, irreversible mutation or loss of observability. Preserve evidence and route incident work to
`secod-observability-response`; route launch verdict to `secod-ship-check`.
