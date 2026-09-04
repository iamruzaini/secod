---
name: secod-abuse-limits
description: Review rate limits, quotas, idempotency, race-condition safety, bounded retries, sensitive business-flow abuse controls, export/rendering resource caps and cost ceilings at user and tenant scope. Apply when login/signup/password-reset, checkout/refund/coupon/free-trial, invitation/email/SMS sending, AI generation, export or browser-rendering jobs, webhook or queue consumers, or rate-limiter/idempotency libraries are present. Package presence alone is Candidate.
---

# Abuse Limits Security

## Mission

Bound resource consumption and prevent replay, duplication, race conditions, retry storms and
business-logic abuse at user and tenant scope, so one principal cannot exhaust compute, money,
third-party quota or business inventory.

Repository-only review cannot prove deployed enforcement, distributed rate-limit store
consistency, provider/Dashboard settings, or real production behavior under load.
`secod-ship-check` owns final launch readiness; this skill never issues it alone.

## Scope and ownership

Owned controls: request-level and business-level abuse limits (`PROVISIONAL-ABUSE-01` through
`PROVISIONAL-ABUSE-08` below).

Excluded controls and their owners:

- Process/container CPU/memory sandboxing, worker pool sizing: `secod-runtime-execution`,
  `secod-container-runtime`.
- General failure handling, partial-mutation rollback, degraded states, deterministic cleanup:
  `secod-failure-safety`; this skill verifies only the abuse-facing subset inside its controls.
- Webhook signature/authenticity verification: `secod-inputs-apis`; payment webhook correctness:
  `secod-payments-billing`.
- Authentication and authorization decisions themselves: `secod-identity-access`.
- Alert delivery/monitoring infrastructure: `secod-observability-response`.
- Provider-native quota/plan configuration: the matching provider skill (`secod-stripe`,
  `secod-openai`, `secod-cloudflare-workers`, and so on).

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

Conditional routes (only when the named feature is detected):

- Incoming payment webhooks or refunds: `secod-payments-billing`.
- AI generation spend or token limits: `secod-ai-api-integrations`.
- Outbound email/SMS sending abuse: `secod-email-messaging`.
- Queue/workflow infrastructure specifics: the owning platform skill.

## Required inputs

Repository-supplied:

- Application code and middleware wiring for limiters, idempotency stores, queues, retries.
- Route/handler inventory for auth, recovery, checkout, coupons, invitations, exports, AI calls,
  webhook receivers.
- Tests and CI runs covering duplicate, replayed, concurrent and burst requests.
- Deployment definitions showing development, preview, staging and production separately.

Commonly unavailable repository-only inputs (label as such when absent):

- Provider Dashboard/API evidence: edge/WAF rate-limit rules, plan quotas, spend alerts.
- Production evidence of distributed limiter consistency across instances and regions.
- Human confirmation of third-party spending ceilings and alert recipients.

When any item is needed, read and apply `references/external-evidence.md`. Validate a supplied
bundle with `scripts/validate_evidence_bundle.py`; validator checks intake structure and hashes,
not security or control passage.

## Applicability and discovery

Inventory each environment separately. Conflicting or shared environment configuration is
`Not verified`.

Signal groups:

- Package/SDK: rate-limiter middleware, idempotency-key helpers, queue/job libraries,
  headless-browser or rendering packages, AI SDKs.
- Environment variables: limiter backend URLs, quota values, retry/backoff settings, spend caps.
- Routes/webhooks: `/login`, `/signup`, `/password-reset`, OTP/magic-link senders, coupon
  redemption, checkout, refund, export/download, AI generation, webhook receiver paths.
- Configuration: middleware order, reverse-proxy/WAF rule files, queue worker concurrency.
- Deployment/provider evidence: edge rules, usage plans, billing alerts, autoscaling bounds.

Classification:

- `Candidate`: package installed, example variable, dormant file or weak signal only.
- `Likely`: repository code/config implements the control; deployed/provider state unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API or
  other provider evidence.

## Review workflow

Steps 1 and 2 are parallelizable; later steps depend on them.

1. Inventory environments and trust boundaries: every public mutating endpoint, webhook receiver,
   queue consumer, export/rendering job and paid third-party call path, per environment.
2. Correlate active features and flows: map each sensitive flow to caller identities, cost
   drivers and current limits.
3. Verify applicable controls below against repository evidence first, then deployment and
   provider evidence.
4. Validate supplied external-evidence bundle structure, then inspect each retained artifact and
   correlate it to the reviewed deployment.
5. Run safe negative tests locally or in an authorized non-production environment only.
6. Classify evidence and route findings per status rules and the ownership table.

## Control requirements

The catalog defines no stable control IDs for this skill yet; IDs below use
`PROVISIONAL-<provider>-<number>` and catalog approval is required before promotion.

### `PROVISIONAL-ABUSE-01` — Per-principal rate limits and quotas

**Applicability:** Every endpoint whose repeated invocation costs compute, money or trust: auth,
recovery, OTP, checkout, search, export, AI. Protected property: finite resource budgets per IP,
user and tenant.

**Inspect and verify:** Limiter middleware/config and its backing store. Limits keyed per
IP/user/tenant as appropriate, enforced server-side before expensive work, present in every
deployed environment, backed by a shared store when multiple instances serve traffic. Page-size,
array-length, batch-count caps on list/batch endpoints.

**Unsafe evidence:** No limiter; in-memory store behind multiple instances; limiter registered
after the expensive handler; client-controlled key material (trusting client-set forwarded
headers).

**Required negative test:** Burst one endpoint past its threshold; expect `429` (or documented
equivalent) without the protected side effect executing.

**Passing / Not verified:** Pass requires server-side enforcement plus passing negative test per
environment class. Missing shared-store consistency proof or absent/failed tests are `Not verified`.

**Related skill routing:** Edge/WAF-layer limits: owning platform skill.

### `PROVISIONAL-ABUSE-02` — Credential-stuffing and login-flow defenses

**Applicability:** Login, signup, token refresh, password recovery, OTP verification. Protected
property: account-takeover resistance via interaction-frequency limits.

**Inspect and verify:** Throttling or progressive delay on failed attempts; counters keyed to
both account and source; lockout or step-up per OWASP guidance; uniform responses that do not
enumerate accounts; recovery/OTP senders covered by ABUSE-01.

**Unsafe evidence:** Unlimited attempts; recovery flow exempt from limiting; distinguishable
responses for existing versus unknown accounts.

**Required negative test:** Repeated failed logins then repeated reset requests for one test
account; expect throttling/block and identical recovery responses for known versus unknown
accounts.

**Passing / Not verified:** Pass requires throttling evidence plus the test. Auth-library
presence alone is `Not verified`.

**Related skill routing:** Auth depth: `secod-identity-access`.

### `PROVISIONAL-ABUSE-03` — Idempotency, deduplication and replay safety

**Applicability:** Every state-changing or money-moving operation reachable twice: payments,
refunds, webhooks, queue consumers, submissions, retries after timeout. Protected property:
at-most-once effect where business requires it.

**Inspect and verify:** Persisted event/request identifier checked inside the same transaction as
the side effect; unique constraints backing idempotency keys; webhook handlers safe under
redelivery; queue consumers tolerate at-least-once delivery; idempotency keys server-generated or
validated for tenant binding.

**Unsafe evidence:** External effects recorded after execution instead of atomically; dedupe
store separate from mutation transaction; client-supplied ID accepted without scope check; no
dedup path at all.

**Required negative test:** Deliver the same signed webhook/event or repeat an
idempotency-keyed request twice; expect exactly one persisted side effect and identical second
response.

**Passing / Not verified:** Pass requires code-path evidence plus the duplicate-delivery test.
Missing signature verification does not fail this control but routes to `secod-inputs-apis`.

**Related skill routing:** Payment webhooks: `secod-payments-billing`; input authenticity:
`secod-inputs-apis`.

### `PROVISIONAL-ABUSE-04` — Race-condition safety on concurrent mutations

**Applicability:** Flows where simultaneous requests create duplicate or invalid outcomes:
inventory reservation, credit/balance spend, coupon redemption, trial creation, seat claims.
Protected property: cardinality and state-machine integrity under concurrency.

**Inspect and verify:** Transactions, row locks, atomic compare-and-swap updates or database
unique constraints guard check-then-act sequences; checks and decrements atomic; server
revalidates price, credits and eligibility rather than trusting client-computed values.

**Unsafe evidence:** Read-modify-write without locking or uniqueness constraint; price, discount
or credit amount accepted from client payload; parallel-request probe creates duplicates or
negative balances.

**Required negative test:** Issue N concurrent redemption/reservation requests for a quantity-1
resource; expect exactly one success and consistent final state.

**Passing / Not verified:** Pass requires atomicity mechanism in code plus the concurrency-test
result. Absent or flaky tests are `Not verified`.

**Related skill routing:** Flow modeling: `secod-threat-model`; payment pricing:
`secod-payments-billing`.

### `PROVISIONAL-ABUSE-05` — Bounded retries, backoff and circuit breaking

**Applicability:** Every outbound call or job with retry logic: HTTP clients, queues, workers,
scheduled jobs. Protected property: no retry amplification against own system or providers.

**Inspect and verify:** Retry classification so only safe transient failures (timeouts, connection
resets, documented retryable statuses such as `429` and `5xx`) retry; exponential backoff with
jitter; explicit maximum attempt count; circuit breaker or bulkhead where a failing dependency can
accumulate work; `Retry-After` honored when a provider sends it.

**Unsafe evidence:** Blanket retry of all failures including `4xx`; unbounded attempts; zero or
fixed tight backoff loops; retries on non-idempotent operations without ABUSE-03 keys.

**Required negative test:** Inject a persistent dependency failure; attempts stop at the
configured maximum, backoff grows, no duplicate side effect occurs.

**Passing / Not verified:** Pass requires configured bounds plus the failure-injection test.
Never invent provider retry schedules or guarantees; unsupported provider-retry claims are
`Not verified`.

**Related skill routing:** Failure-mode depth: `secod-failure-safety`.

### `PROVISIONAL-ABUSE-06` — Sensitive business-flow abuse and quota-bypass resistance

**Applicability:** Account creation, invitations, email/SMS sending, password recovery, coupon and
promotion redemption, inventory reservation, checkout initiation, refunds, free-trial creation, AI
generation and other expensive third-party operations. Protected property: business economics
against automated abuse.

**Inspect and verify:** Explicit per-identity ceilings (count and value per user/tenant/IP/device
where applicable); eligibility, price and entitlement decided server-side; trial/free-tier bounded
by stable person/instrument/tenant signals; quotas survive identity rotation (new accounts,
sessions, IPs, API keys, devices cannot reset them); anti-automation measures proportionate to
business risk (OWASP API6 layering).

**Unsafe evidence:** Flow with no ceiling; quota keyed only to session cookie or IP while signup
is free; refund or coupon amount trusted from client; trial gate removable by clearing cookies;
distributed quota inconsistent across regions, instances, queues and workers.

**Required negative test:** Exceed a flow cap through a second account/session for the same tenant
or person-signal; expect denial. Submit a client-supplied price/discount override; expect server
rejection.

**Passing / Not verified:** Pass requires documented ceilings plus bypass-attempt results.
Business-risk acceptance for weaker controls must be recorded by the owner; otherwise findings
stay at `Fix before launch` or lower.

**Related skill routing:** Flow modeling: `secod-threat-model`; sending abuse:
`secod-email-messaging`; AI spend: `secod-ai-api-integrations`.

### `PROVISIONAL-ABUSE-07` — Resource-capped exports, rendering and long jobs

**Applicability:** Data exports, report generation, PDF/browser rendering, crawling, batch jobs.
Protected property: worker memory, time and output size against oversized requests and runaway
jobs.

**Inspect and verify:** Explicit limits for request count, CPU/time, memory, input/output/body
size, page/item count, pending calls and concurrent jobs; timeout set per job stage with
cancellation propagating to child tasks and third-party calls; deterministic cleanup after abort;
degraded-mode behavior defined when limits trip.

**Unsafe evidence:** Unbounded export row counts or body sizes; renderer invoked with
client-supplied URLs/sizes and no cap; cancellation kills the parent but leaves orphan child work;
no cleanup path for aborted jobs.

**Required negative test:** Request an export/render above each configured cap; expect rejection
or truncation at the limit, job termination within timeout, cleanup completed, and no orphaned
work continuing to bill.

**Passing / Not verified:** Pass requires cap evidence plus timeout/cancellation test. Cleanup and
degraded-state depth routes to `secod-failure-safety`; absence there does not fail this control but
is routed.

**Related skill routing:** Process-level caps: `secod-runtime-execution`; failure depth:
`secod-failure-safety`.

### `PROVISIONAL-ABUSE-08` — Cost ceilings, concurrency bounds and alerts

**Applicability:** Payments, AI, email, exports, uploads and every paid third-party API. Protected
property: total spend and concurrent load stay inside approved budgets.

**Inspect and verify:** Configured spending ceilings or billing alerts per provider; queue/worker
concurrency, backpressure and queue-depth limits; backpressure rejects or sheds load deliberately
instead of silently queuing unbounded work; alert recipients defined; ceilings cover both
per-request and aggregate paths.

**Unsafe evidence:** No spend cap or alert on any paid integration; unlimited consumer
concurrency; producers able to enqueue unbounded jobs; cost visibility only via manual dashboard
checks.

**Required negative test:** Drive controlled load past a configured concurrency bound in a
non-production environment; expect deliberate shedding (`429`, enqueue rejection or documented
degraded response), never silent unbounded growth. Provider Dashboard settings are inspected only
with authorization; otherwise recorded as requested external evidence.

**Passing / Not verified:** Pass requires repository-side bounds plus one demonstrated shed
behavior; provider-side ceiling evidence is commonly unavailable and stays `Not verified` unless
supplied.

**Related skill routing:** Monitoring/alerting infrastructure: `secod-observability-response`;
provider plan limits: owning provider skill.

## Exceptional and failure conditions

Fail-closed behavior required where applicable:

- Limiter/dedupe store unavailable: sensitive flows deny by default or apply a documented
  compensating control; never silently allow. Record which flows fail open today as findings.
- Partial operations: rollback/reconciliation owned by `secod-failure-safety`; this skill verifies
  aborted abusive work leaves no half-applied side effect (ABUSE-07).
- Retry and cancellation: bounded per ABUSE-05; cancellation propagates per ABUSE-07.
- Session/token revocation: revoked identities must not retain quota grants or in-flight job
  authority; verify revocation invalidates limiter identity keys used for bypass-prone quotas.
- Webhook duplicate, replay, redelivery, failure: ABUSE-03 dedup must hold under all four;
  redelivery revalidates rather than blindly replaying state changes.

A failed checker or incomplete test never counts as success. Never invent provider retry
schedules, delivery guarantees, expiry periods or plan capabilities.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

Conditional routes: payment webhooks/refunds to `secod-payments-billing`; AI spend/token limits to
`secod-ai-api-integrations`; email/SMS sending to `secod-email-messaging`; platform quota specifics
to the owning provider skill.

If a dependency or applicable route is missing, unresolved, malformed or incomplete: mark affected
controls `Not verified`, name the missing owner/evidence, never invent replacement dependencies,
never issue launch readiness.

## Evidence and status rules

Valid statuses only:

- `Do not ship`: exploitable exhaustion or duplication reachable pre-auth or with a free account
  (no limiter on auth/recovery/paid flows; money-moving operation without idempotency or race
  protection; client-trusted pricing).
- `Fix before launch`: control exists but bypassable through identity rotation, environment drift,
  store inconsistency, or missing negative-test coverage for a sensitive flow.
- `Recommended hardening`: single-layer limits where business risk warrants defense in depth,
  missing cost alerts, missing degraded-mode documentation.
- `Passed with evidence`: enforced server-side in every deployed environment class, shared-store
  consistency evidenced where multi-instance, and the required negative test passed.
- `Not verified`: package-only presence, inferred configuration, inaccessible/stale/contradictory
  sources, incomplete tests, or failed checks.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported or
failed evidence.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`, `verification`,
`limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (flows x environments, Candidate/Likely/Active)
- Test results including negative tests. For every item record `artifact_type`,
  `execution_status` (`not_executed`, `passed`, `failed`, or `blocked`), command/probe, target
  environment, time and retained evidence.
- Requested external evidence (Dashboard/provider items not obtainable repository-only)
- `Not verified` items, each with affected controls and exact next verification step
- Launch blockers
- A `release_handoff` object with `verdict_owner: secod-ship-check`,
  `readiness_verdict: not_issued`, control statuses, blockers and requested external evidence

Route overall launch readiness to `secod-ship-check`. `readiness_verdict: not_issued` is an
explicit ownership boundary, not an omitted result. Never convert fixture success or structurally
complete evidence into a launch verdict.

## Negative fixtures and tests

Fixture mapping (see `tests/insecure-fixtures/secod-abuse-limits/README.md`,
`tests/trigger-cases/secod-abuse-limits.md`, `tests/expected-results/secod-abuse-limits.md`):

| Fixture case | Controls exercised | Executable? |
| --- | --- | --- |
| Clean layered limits, idempotency, atomic claim, caps and shedding | ABUSE-01..08 pass paths | Python fixture |
| Missing or instance-local limiter; recovery enumeration | ABUSE-01, ABUSE-02 | Python fixture |
| Duplicate effect and bounded retry | ABUSE-03, ABUSE-05 | Python fixture |
| Concurrent redemption race | ABUSE-04 | Python fixture |
| Session-key identity rotation | ABUSE-06 | Python fixture |
| Oversized job and orphan child work | ABUSE-07 | Python fixture |
| Queue shedding plus missing spend/deployment evidence | ABUSE-08 | Python fixture |

Run from `secod/`: `python tests/insecure-fixtures/secod-abuse-limits/run_fixtures.py`. Fixture
success proves synthetic harness behavior only, never reviewed application or production behavior.
Safe local probes may run against a locally started app or an explicitly authorized
non-production environment only. Never run destructive, production-changing, user-creating,
payment-creating, refunding, key-rotating, dashboard-changing or account-changing tests without
explicit authorization.

## References

- Source register: `references/sources.md`.
- External evidence intake: `references/external-evidence.md`; structural validator:
  `scripts/validate_evidence_bundle.py`.
- Trigger case: `../../tests/trigger-cases/secod-abuse-limits.md`; expected result:
  `../../tests/expected-results/secod-abuse-limits.md`; fixture plan:
  `../../tests/insecure-fixtures/secod-abuse-limits/README.md`.
- Keep direct URLs, version notes and plan/region assumptions in `references/sources.md`.
