---
name: secod-failure-safety
description: Review fail-closed behavior, partial-mutation rollback, retry classification, circuit breakers, timeout/cancellation propagation, deterministic cleanup, safe degraded states and redacted error responses so security and data correctness survive dependency, storage, network and provider failures. Apply to all server-side applications; concrete triggers include global exception handlers, transaction wrappers, retry/backoff helpers, circuit-breaker libraries, queue/job workers and outbound provider calls. Package presence alone is Candidate.
---

# Failure Safety Security

## Mission

Preserve security posture and data correctness when dependencies, storage, networks or providers
fail: authentication and authorization deny by default under dependency failure, partial mutations
roll back or reconcile, retries stay safe, resources clean up deterministically, and error output
never discloses internals.

Repository-only review cannot prove production failure behavior, real degraded-state outcomes,
provider outage conduct, or that fault-injection results hold in deployed environments.
`secod-ship-check` owns final launch readiness; this skill never issues it alone.

## Scope and ownership

Owned controls: catalog-approved general failure-handling controls (`SECOD-FAIL-01` through
`SECOD-FAIL-10` below).

Excluded controls and their owners:

- API-boundary inventory, request/response bounding, webhook authenticity/freshness/replay fields:
  `secod-inputs-apis`; this skill verifies deep failure semantics of the same paths.
- Payment/entitlement state-machine correctness, provider reconciliation specifics:
  `secod-payments-billing`; this skill verifies the general rollback/degraded pattern around those
  mutations.
- Abuse-facing subset: rate-limit fail-open behavior, retry storms, quota bypass under failure:
  `secod-abuse-limits`.
- Alerting on fail-closed failures, provider outages, retry exhaustion, disabled webhook endpoints;
  log redaction plumbing; recovery drills and backup restore tests: `secod-observability-response`.
- Command/template execution boundaries and their sandboxing: `secod-runtime-execution`.
- Upload/export/rendering limits themselves: `secod-data-files` (this skill owns cancellation,
  timeout propagation and deterministic cleanup patterns for long jobs).
- Authentication/authorization decision logic itself: `secod-identity-access`.
- Provider-native resilience settings (connection pools, managed queues, DLQs): owning provider
  skill.

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

Conditional routes (only when the named feature is detected):

- Payment, refund or entitlement mutations: `secod-payments-billing`.
- Webhook receivers: `secod-inputs-apis` (authenticity) plus the platform queue/DLQ owner skill.
- AI provider calls or fallback paths: `secod-ai-api-integrations`.
- Export/rendering jobs and temporary file lifecycle: `secod-data-files`.
- Storage/database provider specifics: the owning provider skill.

## Required inputs

Repository-supplied:

- Global exception/middleware wiring, error-rendering code, transaction wrappers, retry/backoff
  helpers, circuit-breaker configuration, queue/job consumer code, cleanup paths (`finally`,
  `defer`, shutdown hooks).
- Route/handler inventory marking every flow that mutates database, payment or entitlement state or
  calls a third-party provider.
- Tests and CI runs covering storage, provider and network failure injection, duplicate delivery
  and cancellation.
- Deployment definitions separating development, preview, staging and production.

Commonly unavailable repository-only inputs (label as such when absent):

- Production evidence of degraded-state behavior and breaker trips.
- Tested provider-outage runbooks and reconciliation results.
- Dashboard/API evidence for managed retry schedules, DLQ retention or connection-pool limits.

Request these artifacts using `references/external-evidence.md`. A template or runbook draft is
not executed evidence; retain `Not verified` until dated production captures and drill results are
supplied.

## Applicability and discovery

Apply to every server-side application. Inventory each environment separately; conflicting or
shared environment signals are `Not verified`.

Signal groups:

- Package/SDK: global error handlers, transaction libraries, retry/backoff helpers
  (`p-retry`, `tenacity`, `resilience4j`, Polly-class), circuit-breaker packages, queue/job
  frameworks.
- Environment variables: DB/provider URLs, pool sizes, timeouts, retry counts, breaker thresholds,
  degraded-mode flags.
- Routes/webhooks: mutating endpoints, webhook receivers, job/queue consumers, health/readiness
  probes.
- Configuration: middleware order, transaction isolation settings, timeout maps, graceful-shutdown
  settings.
- Deployment/provider evidence: readiness/liveness behavior, autoscaling on failure, managed
  service outage notices.

Classification:

- `Candidate`: handler or library installed, example variable, dormant file or weak signal only.
- `Likely`: repository code/config implements the control; deployed/runtime behavior unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API or
  other provider evidence.

## Review workflow

Steps 1 and 2 are parallelizable; later steps depend on them.

1. Inventory environments and trust boundaries: every mutating flow, external dependency, queue
   consumer and scheduled job, per environment.
2. Correlate active features and flows: map each flow to its failure surface (DB, storage,
   network, provider) and current failure handling.
3. Verify applicable controls below against repository evidence first, then deployment and
   runtime evidence.
4. Run safe negative tests locally or in an authorized non-production environment only
   (fault injection, duplicate delivery, mid-operation cancellation).
5. Classify evidence and route findings per status rules and the ownership table.

## Control requirements

Stable IDs below are approved in `secod/catalog.json`. Treat catalog entry as authority; do not
rename, reuse or infer additional IDs in reports.

### `SECOD-FAIL-01` — Centralized global exception handling

**Applicability:** Every server-side entry point (HTTP routes, Server Actions, queue consumers,
scheduled jobs, websocket handlers). Protected property: defined, auditable behavior for any
uncaught exceptional condition (OWASP A10:2025).

**Inspect and verify:** One centralized/global exception path registered for each runtime
(entry-point middleware, framework error boundary, worker `process`/`unhandledRejection`
handlers); per-site catches handle locally where meaningful; no silent catch-all that swallows
errors without logging and rejection; unhandled conditions crash or isolate rather than continue
in unknown state.

**Unsafe evidence:** No global handler; empty `catch {}`; catch-and-continue on authorization or
payment steps; duplicated divergent error-handling logic per route.

**Required negative test:** Trigger an unexpected exception in a non-production route or job;
expect the global path to log safely, return a generic response, and leave no half-applied state.

**Passing / Not verified:** Pass requires global-handler evidence plus one demonstrated
exception-path test. Absent, incomplete or failed tests are `Not verified`.

**Related skill routing:** API-boundary bounding: `secod-inputs-apis`; alerting on repeated
exceptions: `secod-observability-response`.

### `SECOD-FAIL-02` — Fail-closed authentication and authorization dependencies

**Applicability:** Every request path whose identity or permission check depends on another
system (identity-provider SDK, session store, policy engine, cache-backed auth lookup, JWKS
fetch). Protected property: denial by default when the dependency is unavailable or errors.

**Inspect and verify:** Error/timeout branches of every authn/authz call default to deny;
JWKS/key-store fetch failure rejects rather than trusts stale-unbounded caches; session-store
outage denies instead of treating requests as anonymous-but-allowed into privileged flows;
feature-flag/config service failure cannot enable access.

**Unsafe evidence:** Middleware catches IdP errors and proceeds; cache miss treated as
authenticated; policy engine unreachable yields allow; health checks mark failing instance ready
while it serves privileged traffic.

**Required negative test:** Block or fault the identity/policy dependency in a non-production
environment; expect every dependent privileged request denied with a generic error.

**Passing / Not verified:** Pass requires deny-on-error branch evidence plus one dependency-failure
test. Package-only presence or inferred branch behavior is `Not verified`.

**Related skill routing:** Authn/authz decision correctness: `secod-identity-access`;
provider-specific token validation: matching provider adapter skill.

### `SECOD-FAIL-03` — Rollback of partial database/payment/entitlement mutations

**Applicability:** Every multi-step mutation spanning rows, tables, services or providers
(order + payment + entitlement, user + profile + invitation, debit + credit). Protected property:
all-or-nothing semantics or recoverable reconciliation; never a durable half-applied state
(OWASP A10:2025 scenario #3).

**Inspect and verify:** Transactions wrap related writes at one consistency boundary; cross-service
or cross-provider steps use compensating actions or a recoverable outbox/saga pattern with a named
reconciliation owner; rollback executes before returning errors to clients; interrupted jobs resume
idempotently or restart cleanly; payment/entitlement mapping rolls back or reconciles after partial
failure.

**Unsafe evidence:** Sequential awaits across services with no compensation; catch blocks that keep
earlier writes; entitlement granted before provider confirmation with no reversal path; no
ledger/reconciliation trail for cross-system mutations.

**Required negative test:** Inject a failure between mutation steps in a non-production run; expect
full rollback or a recorded, recoverable intermediate state — never silently committed halves.

**Passing / Not verified:** Pass requires transaction/compensation design evidence plus one
mid-operation failure test. Billing-state-specific invariants route to `secod-payments-billing`;
their absence here does not pass this control but is routed.

**Related skill routing:** Billing state machines and reconciliation: `secod-payments-billing`;
audit trail of reversals: `secod-observability-response`.

### `SECOD-FAIL-04` — Safe retry classification

**Applicability:** Every outbound call and job step that can be retried (DB queries, provider APIs,
webhook deliveries, queue messages). Protected property: only safe transient failures retried,
bounded attempts, no duplicated side effects.

**Inspect and verify:** Retry classification distinguishes transient/idempotent-safe failures from
non-retryable ones (validation, auth, business rejections); retried operations are idempotent
(idempotency keys, upserts, conditional writes) or guarded by deduplication; bounded maximum
attempts with backoff and jitter; retries propagate or record context, never loop unbounded inside
request handling.

**Unsafe evidence:** Retrying non-idempotent money or provisioning writes blind; infinite or
unconfigured attempt counts; retrying `4xx` validation/auth failures; identical retries without
dedup keys.

**Required negative test:** Force a transient failure then a permanent failure for one operation;
expect bounded retry of the first and immediate classified stop for the second, with no duplicated
side effect.

**Passing / Not verified:** Pass requires classification plus idempotency evidence and one retry
test. Storm/abuse-facing limits stay owned by `secod-abuse-limits`; absence there does not pass
this control but is routed.

**Related skill routing:** Bounded backoff/jitter abuse view: `secod-abuse-limits`; webhook
provider-capability matrices: `secod-inputs-apis`, `secod-payments-billing`.

### `SECOD-FAIL-05` — Circuit breakers on failing dependencies

**Applicability:** Dependencies whose repeated failure degrades the application or burns cost
(provider APIs, DB, email/SMS, AI, storage). Protected property: fast-fail isolation instead of
per-request pileup against a dead dependency.

**Inspect and verify:** Breaker or bulkhead exists on identified critical dependencies with defined
open/trial thresholds; open state returns deliberate degraded responses rather than hanging; state
transitions logged/alertable; breaker scope matches deployment topology (per-instance breakers
behind many instances still admit aggregate pileups — note this).

**Unsafe evidence:** No breaker on any critical path; breaker that fails open into allowing
privileged operations; thresholds so high they never trip.

**Required negative test:** Drive a dependency to sustained failure in a non-production run; expect
the breaker to open within configured thresholds and subsequent calls to fail fast without hitting
the dependency.

**Passing / Not verified:** Pass requires configuration plus one trip demonstration. Distributed
breaker-consistency evidence commonly unavailable repository-only; record as requested external
evidence.

**Related skill routing:** Load-shedding/quota interplay: `secod-abuse-limits`; alerting on open
breakers: `secod-observability-response`.

### `SECOD-FAIL-06` — Timeout and cancellation propagation

**Applicability:** Every inbound request, background job and outbound call. Protected property:
bounded execution; cancellation reaches child work, transactions and third-party calls.

**Inspect and verify:** Explicit timeouts on outbound HTTP/DB/queue calls; per-stage job deadlines;
cancellation contexts propagate to spawned tasks and downstream calls so aborted work stops billing
and writing; server shutdown drains or cancels in-flight work deliberately.

**Unsafe evidence:** Default-infinite client timeouts; parent cancelled while orphan children
continue; detached promises/fire-and-forget writes surviving cancellation; no shutdown hook.

**Required negative test:** Cancel one long request/job mid-flight in a non-production run; expect
child work, held transactions and third-party calls to terminate within the timeout budget and no
further side effects afterward.

**Passing / Not verified:** Pass requires timeout-map evidence plus one cancellation test. Orphaned
resource cleanup depth is SECOD-FAIL-07.

**Related skill routing:** Job/resource caps: `secod-data-files`, `secod-abuse-limits`; process-level
execution bounds: `secod-runtime-execution`.

### `SECOD-FAIL-07` — Deterministic cleanup

**Applicability:** Temporary files, rendering sessions, DB connections/transactions, locks,
uploaded staging objects, allocated workers. Protected property: fixed cleanup outcome on success,
failure, timeout and cancellation alike (OWASP A10:2025 scenario #1).

**Inspect and verify:** Cleanup tied to scoped release constructs (`finally`, `defer`, context
managers) not only happy paths; temp artifacts carry expiry/TTL; locks and reservations auto-release
on holder death; repeated failure leaves no accumulating residue; cleanup itself idempotent.

**Unsafe evidence:** Resource acquisition without guaranteed release; cleanup only on success path;
staging buckets filling with abandoned uploads; leaked locks blocking future operations.

**Required negative test:** Abort a flow holding a resource mid-operation; expect the resource
released or expired deterministically with no accumulation across repeats.

**Passing / Not verified:** Pass requires scoped-release evidence plus one abort test. Storage
retention/deletion policy depth: `secod-crypto-data-protection`.

**Related skill routing:** Upload/staging expiry: `secod-data-files`; backup hygiene:
`secod-crypto-data-protection`.

### `SECOD-FAIL-08` — Safe degraded states

**Applicability:** Every feature with a defined reduced-capacity mode (read-only mode, cached
responses, disabled integrations, maintenance pages). Protected property: degradation never widens
authorization, exposes stale privileged data, or enables unsafe writes.

**Inspect and verify:** Each degradation path documented with what remains allowed; degraded
responses still enforce full authorization and tenant filtering; cached fallback data checked
against sensitivity (no privileged data served to unauthorized callers); degraded flags cannot be
flipped by untrusted input; recovery path defined.

**Unsafe evidence:** Undefined behavior when a dependency dies (crash loop or ad-hoc improvisation);
degraded cache serving cross-tenant data; read-only mode accepting privileged writes; kill-switch
controllable via client input.

**Required negative test:** Force one dependency down in a non-production environment; exercise a
privileged and a cross-tenant request in degraded mode; expect both still correctly authorized and
scoped.

**Passing / Not verified:** Pass requires defined degraded behavior plus one exercised degraded
test. Monitoring of degraded periods: `secod-observability-response`.

**Related skill routing:** Cache privacy: `secod-web-app-security`; threat-model degraded-mode
inventory: `secod-threat-model`.

### `SECOD-FAIL-09` — Redacted error responses

**Applicability:** Every error surfaced to clients, browsers, logs-boundary consumers or job
results. Protected property: no stack traces, SQL, internal hosts, secrets, tokens or PII in
outward error output (OWASP A10:2025 scenario #2; CWE-209).

**Inspect and verify:** Client-facing errors generic with correlation IDs; verbose detail goes to
server logs only after redaction; debug/verbose error modes disabled in production builds;
framework debug pages off; upstream provider errors wrapped, not proxied verbatim; error templates
free of reflection of unsanitized input.

**Unsafe evidence:** Stack traces or query text returned to clients; raw provider error bodies
forwarded; `DEBUG=true` in production; error messages echoing user input unencoded (also XSS risk).

**Required negative test:** Trigger representative errors (invalid input, forced DB error, forced
provider error) against a deployed or local production-mode build while signed out; expect generic
messages, no internal detail.

**Passing / Not verified:** Pass requires production-mode redaction evidence plus triggered-error
results. Log-side redaction plumbing: `secod-observability-response`.

**Related skill routing:** Debug-surface exposure: `secod-inputs-apis`; reflected-input encoding:
`secod-web-app-security`.

### `SECOD-FAIL-10` — Failure-mode tests for storage, provider and network

**Applicability:** Every application with external dependencies (all server-side apps). Protected
property: repeatable proof that controls SECOD-FAIL-01 through SECOD-FAIL-09 hold under storage,
provider and network
failure, including webhook duplicate/replay/redelivery handling.

**Inspect and verify:** Test suite or CI stage injects storage failure, provider timeout/error and
network partition/delay; webhook receivers tested against duplicate, replayed, out-of-order and
failed deliveries; assertions cover deny-by-default, rollback, bounded retries, cleanup and
redaction; tests run in CI on relevant changes and are versioned with the code.

**Unsafe evidence:** No fault-injection coverage; tests exist but never run in CI; assertions only
check happy-path status codes; fixture plans claimed executed without execution.

**Required negative test:** Execute the maintained insecure fixture cases (below) or equivalent
fault-injection suite; expect each control's expected secure result.

**Passing / Not verified:** Pass requires executed tests covering all three failure classes plus
webhook duplication where receivers exist. Missing, skipped or failed runs are `Not verified` — a
failed checker or incomplete test never counts as success.

**Related skill routing:** Duplicate/replay field-level verification: `secod-inputs-apis`;
payment-event idempotency: `secod-payments-billing`; alert routing on failure:
`secod-observability-response`.

## Exceptional and failure conditions

Fail-closed behavior required where applicable:

- Timeouts and dependency failure: authn/authz dependencies deny (SECOD-FAIL-02); outbound calls
  bounded (SECOD-FAIL-06); breakers isolate sustained failure (SECOD-FAIL-05).
- Partial operations, cleanup, rollback, reconciliation: SECOD-FAIL-03 plus SECOD-FAIL-07; unrecoverable
  intermediates must be detectable and routable to a reconciliation owner.
- Retry and cancellation: classified and bounded (SECOD-FAIL-04); cancellation propagates
  (SECOD-FAIL-06);
  redelivery revalidates rather than blindly replaying state changes.
- Session/token revocation: revocation must remain effective during degraded operation — a failed
  session store or cache must not resurrect revoked sessions or tokens.
- Webhook duplicate, replay, redelivery and failure: dedup/idempotency must survive all four;
  receiver failure acknowledges only after verified durable handling, per provider capability.

Never invent provider retry schedules, delivery guarantees, expiry periods or plan capabilities —
verify against the owning provider skill's sources or record `Not verified`. A failed checker or
incomplete test never counts as success.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

Conditional routes: payment/refund/entitlement mutations to `secod-payments-billing`; webhook
authenticity to `secod-inputs-apis` plus the platform queue/DLQ owner; AI provider failure paths to
`secod-ai-api-integrations`; export/rendering job cleanup to `secod-data-files`; storage provider
resilience specifics to the owning provider skill.

If a dependency or applicable route is missing, unresolved, malformed or incomplete: mark affected
controls `Not verified`, name the missing owner/evidence, never invent replacement dependencies,
never issue launch readiness.

## Evidence and status rules

Valid statuses only:

- `Do not ship`: exploitable failure posture reachable pre-auth or with normal traffic — authz
  dependency fails open (SECOD-FAIL-02), partial payment/entitlement mutation persists
  (SECOD-FAIL-03), or internals/secrets exposed in errors (SECOD-FAIL-09).
- `Fix before launch`: control designed but unproven under failure — no fault-injection coverage
  (SECOD-FAIL-10), unbounded retries on money/provisioning writes, missing cancellation propagation with
  side effects.
- `Recommended hardening`: single-layer protection where defense in depth warranted, undocumented
  degraded states, per-instance-only breakers behind many instances.
- `Passed with evidence`: control implemented, required negative test executed in a production-mode
  or non-production environment, evidence current and non-contradictory.
- `Not verified`: package-only presence, inferred behavior, inaccessible/stale/contradictory
  sources, incomplete, skipped or failed tests.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported or
failed evidence.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`, `verification`,
`limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (flows x environments x failure classes, Candidate/Likely/Active)
- Test results including negative tests
- Requested external evidence (production/deployed behavior, provider settings)
- `Not verified` items
- Launch blockers

Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

Fixture mapping (see `tests/insecure-fixtures/secod-failure-safety/README.md`,
`tests/trigger-cases/secod-failure-safety.md`, `tests/expected-results/secod-failure-safety.md`):

| Fixture case | Controls exercised | Executable? |
| --- | --- | --- |
| Clean app: all secure primitives combined | SECOD-FAIL-01..10 pass paths | Python fixture |
| Catch-all swallowing exceptions; stack trace returned to client | SECOD-FAIL-01, -09 | Python fixture |
| Authorization middleware proceeding on identity-provider timeout | SECOD-FAIL-02 | Python fixture |
| Multi-step mutation interrupted mid-way with no rollback | SECOD-FAIL-03, -10 | Python fixture |
| Blind retry duplicating a non-idempotent write; replayed webhook event | SECOD-FAIL-04, -10 | Python fixture |
| Dead dependency hammered per-request, no breaker | SECOD-FAIL-05 | Python fixture |
| Cancelled job leaving orphaned resources | SECOD-FAIL-06, -07 | Python fixture |
| Degraded cache serving cross-tenant data | SECOD-FAIL-08 | Python fixture |
| Missing runtime/deployment evidence | All | Python fixture |

Run `python tests/insecure-fixtures/secod-failure-safety/run_fixtures.py` from `secod/`. Passing
means fixture expectations reproduced; it is not application or production evidence. Safe probes
may run against a local build or explicitly authorized non-production environment only. Never run
destructive or account-changing tests without explicit authorization.

## Verification commands

From `secod/`, run `python tests/insecure-fixtures/secod-failure-safety/run_fixtures.py` and
`python scripts/validate_skills.py`. Preserve runner JSON with review evidence. CI repeats fixture
runner in `.github/workflows/test-fixtures.yml`.

## References

- Source register: `references/sources.md`.
- External evidence contract and outage drill: `references/external-evidence.md`.
- Trigger case: `../../tests/trigger-cases/secod-failure-safety.md`; expected result:
  `../../tests/expected-results/secod-failure-safety.md`; fixture plan:
  `../../tests/insecure-fixtures/secod-failure-safety/README.md`.
- Keep direct URLs, version notes and plan/region assumptions in `references/sources.md`.
