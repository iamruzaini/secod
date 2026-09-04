---
name: secod-payments-billing
description: Provider-neutral payments/billing security baseline. Review server-resolved pricing, provider-authoritative entitlements, webhook authenticity/replay defense, idempotency, atomic mapping, ledger/reconciliation invariants, credential isolation for any checkout, subscription, invoice, payment webhook, refund, dispute or chargeback flow. Package presence alone is Candidate.
---

# Payments Billing Security

## Mission

Own the correctness of payment, subscription, entitlement, refund and dispute state:
the server treats verified provider state as authoritative and stays correct under duplicate,
delayed, out-of-order, retried and partially failed operations.

Repository-only review cannot prove deployed webhook endpoints are reachable with current
signing secrets, that provider Dashboard/API state matches repository claims, or that live/test
environments match what variables suggest. Those require provider-side evidence.

`secod-ship-check` owns final launch readiness. This skill never issues a launch verdict.

## Scope and ownership

Owned controls: server-resolved pricing and entitlement decisions, provider-hosted checkout
selection, outbound-write idempotency and session expiration, API/webhook version pinning,
webhook authenticity and replay defense including the capability matrix, delivery processing and
reconciliation, atomic customer-to-user/tenant/entitlement mapping, ledger invariants and
lifecycle correction (cancellation, expiration, renewal failure, refund, dispute, chargeback),
restricted server-only credentials, test/live separation, periodic reconciliation.

Excluded controls and owners:

- Rate limits, quota bypass, coupon/checkout-initiation abuse, cost ceilings — `secod-abuse-limits`
- General fail-closed behavior, partial-write rollback patterns outside billing state, retry/cancellation propagation — `secod-failure-safety`
- Audit events for payments/webhooks, redaction, alerting on disabled endpoints — `secod-observability-response`
- Secret storage hygiene and variable leakage — `secod-secrets-config`
- Webhook route transport hardening (authn on routes, SSRF, body limits) — `secod-inputs-apis`
- Per-provider envelope specifics, SDK lifecycle details, provider Dashboard settings — `secod-stripe`, `secod-polar`, `secod-lemonsqueezy`, `secod-dodo-payments`, `secod-whop`

Direct dependencies (copy from `secod/catalog.json`): `secod-core`.

Conditional routes (real routes only):

| Signal | Route |
| --- | --- |
| Stripe package/config/webhooks | `secod-stripe` |
| Polar package/config/webhooks | `secod-polar` |
| Lemon Squeezy package/config/webhooks | `secod-lemonsqueezy` |
| Dodo Payments package/config/webhooks | `secod-dodo-payments` |
| Whop package/config/webhooks | `secod-whop` |

No other conditional routes. Absence of a detected-provider adapter is itself a finding.

## Required inputs

Repository inputs: payment SDK/package versions, checkout creation code, webhook handlers,
entitlement/access-grant code, database schema for orders/subscriptions/ledger/idempotency keys,
environment-variable names, CI/deployment definitions, tests.

Commonly unavailable repository-only (request explicitly; absence is `Not verified`, never pass):

- Deployed environment inventory per stage (development/preview/staging/production)
- Provider Dashboard/API state: webhook endpoint status, signing-secret rotation dates, API version pinned, enabled events, test/live mode
- Live-mode credential separation evidence
- Reconciliation job schedules and last-run results
- Human confirmation of intended products/prices and entitlement policy

## Applicability and discovery

Group signals:

- **Package/SDK**: `stripe`, `@dodopayments/*`, `@polar-sh/*`, `lemonsqueezy`, `@whop/*` or generic payment packages in manifests/lockfiles.
- **Environment variables**: `*_SECRET_KEY`, `*_API_KEY`, `*_WEBHOOK_SECRET`, `DODO_PAYMENTS_*`, `STRIPE_*`, `POLAR_*`, `LEMONSQUEEZY_*`, `WHOP_*` names.
- **Routes/webhooks**: checkout/session creation routes, `POST` handlers consuming raw bodies at webhook paths, success/cancel/return URLs, customer-portal routes.
- **Configuration**: product/price IDs in config or DB, adapter capability matrices, deduplication tables/migrations, reconciliation jobs/cron.
- **Deployment/provider evidence**: cron/queue definitions for reconciliation, separate staging/live deployments, provider dashboard screenshots or Management/API exports supplied by the operator.

Classification:

- `Candidate`: package present, example variable name, dormant file, weak signal only.
- `Likely`: real code/configuration exists; deployed or provider state unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API or provider evidence (e.g., received webhook logs, provider event history).

Inventory development, preview, staging and production separately. Conflicting or shared
environment signals (one key set across stages, shared webhook endpoint, live secret in preview)
are `Not verified` and a finding.

## Review workflow

Ordered steps:

1. Inventory environments and trust boundaries: which stages exist, which keys/webhook endpoints each uses, where browser trust ends.
2. Correlate active features and flows: checkout, subscription lifecycle, webhooks, refunds/disputes, entitlement grants, portal access.
3. Verify applicable controls below.
4. Run safe negative tests (fixtures/local only).
5. Classify evidence and route findings to excluded-control owners and provider adapters.

Steps 1–2 are parallelizable across flows (independent evidence, no state changes). Steps 3–5
depend on 1–2 outputs.

## Control requirements

Catalog defines no stable control IDs for this skill; `PROVISIONAL-PB-*` used pending catalog
approval.

### `PROVISIONAL-PB-1` — Server-resolved price and entitlement

**Applicability:** Any checkout creation or entitlement check. Protects against client-controlled amount, currency, product, quantity, discount or tenant.

**Inspect and verify:** Checkout/session creation code resolves product, price, currency, quantity, discount, tenant from server-held config or DB by stable ID — never from request body, query params, localStorage or client-posted amounts. Entitlement checks derive from internal records, not client claims. Trace one flow end to end.

**Unsafe evidence:** Amount/product/price accepted from client input; discount codes applied client-side; tenant ID taken from client without authorization check.

**Required negative test:** Submit a checkout/entitlement request with tampered price/product/tenant fields; expect server ignores or rejects them. Local/unit-testable.

**Passing / Not verified:** Passed with evidence requires the full server-resolution path plus the tamper test. Missing resolution path, untestable flow, or client-influenced fields is `Not verified` minimum; client-trusted amounts is `Do not ship`.

**Related skill routing:** Authorization of who may buy — `secod-web-app-security`; abuse volume — `secod-abuse-limits`.

### `PROVISIONAL-PB-2` — Provider-hosted checkout; no raw card handling

**Applicability:** Any card/payment-data entry. Protects PCI scope and card data exposure.

**Inspect and verify:** Payment collection uses provider-hosted checkout, approved embedded components or SDK elements. No PAN/CVC collection, custom card forms posting to provider APIs, or card data touching app servers/logs unless a documented intentional compliance decision exists (then route to `secod-crypto-data-protection` and flag scope).

**Unsafe evidence:** Card fields rendered by the app; card data in server logs, DB rows or analytics; homegrown card form.

**Required negative test:** Search codebase and log-emitting paths for PAN-pattern capture (`rg -i "card.?number|pan|cvc|cvv"` over source and logging calls); confirm no collection path exists.

**Passing / Not verified:** Passed with evidence requires hosted/approved component usage confirmed in code. Raw handling without compliance decision is `Do not ship`.

**Related skill routing:** Intentional raw handling — `secod-crypto-data-protection`; provider-specific component rules — provider adapter skill.

### `PROVISIONAL-PB-3` — Outbound write idempotency and session expiration

**Applicability:** Every outbound payment-API write (checkout create, refund create, subscription update). Protects against duplicate charges/refunds on retry or double-submit.

**Inspect and verify:** Outbound writes carry a provider idempotency key where the provider supports one, derived deterministically from business intent (order/cart/action ID), not random per attempt. Checkout sessions have expiration set or provider default documented; post-expiry completion path defined (expired session cannot be paid into an active grant without revalidation).

**Unsafe evidence:** Writes without idempotency key where provider supports it; non-deterministic keys; unbounded-lived sessions completed without state recheck.

**Required negative test:** Replay the same logical write twice (unit/integration with stubbed provider); expect single effective mutation.

**Passing / Not verified:** Passed with evidence requires deterministic keys on all writes plus replay test. Provider does not support idempotency keys: require documented compensating strategy instead — unsupported claim is `Not verified`.

**Related skill routing:** Retry/backoff classification — `secod-failure-safety`; provider support specifics — provider adapter skill.

### `PROVISIONAL-PB-4` — API and webhook version pinning

**Applicability:** Any provider API/webhook consumption. Protects against silent breaking changes altering verification or event semantics.

**Inspect and verify:** API version pinned explicitly (header/config/SDK constraint); webhook handler pins or validates the provider's event/API version field where the provider supplies one. An upgrade/migration path exists (documented test or staged rollout plan); upgrades are deliberate, not implicit.

**Unsafe evidence:** Unpinned floating version; handler ignores version field where provided; no migration consideration.

**Required negative test:** Feed the handler an event carrying an unexpected/unrecognized version (fixture); expect explicit rejection or flagged branch, not silent default processing.

**Passing / Not verified:** Passed with evidence requires pin visible in code/config plus unexpected-version rejection. Cannot confirm provider supplies version semantics without adapter/source evidence: `Not verified`.

**Related skill routing:** Version facts and current values — provider adapter skill.

### `PROVISIONAL-PB-5` — No entitlement from client-reported paid state

**Applicability:** Success pages, redirect/callback handlers, client polls. Protects against free access.

**Inspect and verify:** Access granted only after verified webhook processing or authoritative provider-side retrieval (server API call confirming paid state) tied to internal order. Redirect targets, callback params, client-posted session/status/`paid=true` values never grant anything; success page is presentation only. Confirm no code path writes entitlement from client-controlled identifiers without provider verification.

**Unsafe evidence:** Entitlement insert in success-route handler from URL params; client can name session/checkout ID and receive access without server verification.

**Required negative test:** Call the success/callback route directly with fabricated-but-plausible identifiers; expect no grant (and ideally a server-side lookup that fails closed).

**Passing / Not verified:** Passed with evidence requires verified-webhook-or-retrieval gate proven for every grant path. Any client-trusted grant path is `Do not ship`.

**Related skill routing:** Route authn/authz mechanics — `secod-inputs-apis`; provider retrieval APIs — provider adapter skill.

### `PROVISIONAL-PB-6` — Webhook authenticity, freshness and replay defense (capability matrix)

**Applicability:** Every payment webhook endpoint. Protects against forged, replayed and stale events driving state changes.

**Inspect and verify:** Handler reads the raw body before parsing and verifies every authenticity/replay field the provider actually supplies: signature, timestamp/freshness tolerance, delivery/event ID, event type, account/context, API version. Constant-time signature comparison. Maintain a capability matrix per integrated provider listing exactly which fields its contract provides. When signed timestamp or unique delivery ID absent: require the adapter's documented compensating control — stable deduplication key derived from authoritative event/resource fields, persisted payload replay ledger, provider-side retrieval before acting, reconciliation strategy. Never demand a field the contract lacks and never invent one.

**Unsafe evidence:** Parsed-body verification, missing signature check, no timestamp tolerance where supported, no persistent deduplication, matrix absent or contradicts provider contract.

**Required negative test:** Fixture webhook with invalid signature, stale timestamp (where supported), and duplicated delivery ID: expect rejection/dedup respectively. All local, read-only.

**Passing / Not verified:** Passed with evidence requires raw-body verification matching the provider's actual field set (matrix-backed) plus all three negative cases. Matrix entries without primary-source backing are `Not verified`.

**Related skill routing:** Envelope/header exactness — provider adapter skill; transport-level route protection — `secod-inputs-apis`.

### `PROVISIONAL-PB-7` — Delivery processing, monitoring and missed-event reconciliation

**Applicability:** Webhook endpoints and their processing pipeline. Protects against lost, disabled or unprocessed deliveries leaving state wrong.

**Inspect and verify:** Handler verifies, enqueues or processes durably, then acknowledges fast; complex work not inline before ack. Duplicate, delayed, out-of-order and retried events handled idempotently (persistent event-ID/dedup-key store checked before effects). Delivery failure and disabled-endpoint detection exists (provider alerting, polling, or reconciliation job); a reconciliation path recovers missed events from provider state. Do not assume specific provider retry counts or schedules — only what the adapter's sourced contract documents.

**Unsafe evidence:** Inline heavy work before ack, ack-before-persist, memory-only dedup, no disabled-endpoint awareness, no reconciliation.

**Required negative test:** Deliver the same event twice and out-of-order variants (fixtures/stubs); expect identical end state and correct ordering handling.

**Passing / Not verified:** Passed with evidence requires durable processing, persistent idempotency, and a named reconciliation mechanism. Inability to confirm provider retry/disabled-endpoint behavior leaves those sub-checks `Not verified`, not passed.

**Related skill routing:** Queue/worker durability — `secod-failure-safety`; alerting on disabled endpoints — `secod-observability-response`; provider retry facts — provider adapter skill.

### `PROVISIONAL-PB-8` — Atomic mapping to user, tenant and entitlement

**Applicability:** Verified-event processing that creates or updates customer/subscription-to-user/tenant/entitlement links. Protects against orphaned payments and unmapped access.

**Inspect and verify:** Mapping written atomically (single transaction or equivalent): verified event plus resolved internal identity plus entitlement change commit together or not at all. Partial failure yields rollback, durable pending state, or recoverable reconciliation record — never payment-without-access or access-without-payment left silent. Identity resolution uses authenticated linkage (email/customer-id lookup with collision policy), not attacker-controllable values alone.

**Unsafe evidence:** Multi-step non-transactional writes without recovery record; entitlement derived solely from an email claim inside webhook payload without collision/account-linking policy; swallowed mapping errors.

**Required negative test:** Inject failure between steps (stubbed DB/queue throw); expect rollback or recoverable pending state, consistent final state after retry.

**Passing / Not verified:** Passed with evidence requires atomicity mechanism plus injected-failure test. Untestable path is `Not verified`; silent inconsistency path is `Fix before launch` or `Do not ship` by impact.

**Related skill routing:** Account-linking/email-identity policy — `secod-auth-provider-integrations`; transactional failure taxonomy — `secod-failure-safety`.

### `PROVISIONAL-PB-9` — Ledger invariants and lifecycle correction

**Applicability:** Payment, refund, dispute, entitlement state stores. Protects auditability and revocation correctness.

**Inspect and verify:** State transitions recorded append-only (immutable event/ledger rows; corrections as new entries, not destructive updates). Cancellation, expiration, renewal failure, refund, dispute and chargeback each have an explicit handler that corrects entitlement access; revoked access takes effect for active sessions within the application's stated window. Periodic provider-state reconciliation compares internal vs provider records and repairs drift.

**Unsafe evidence:** Mutable overwrite of financial records; missing dispute/chargeback handler; refunds processed without entitlement correction; no reconciliation.

**Required negative test:** Apply refund/cancel/dispute fixtures; expect entitlement revoked/downgraded and append-only history preserved (no prior rows mutated).

**Passing / Not verified:** Passed with evidence requires lifecycle coverage for every enabled provider feature plus reconciliation evidence. Feature enabled but no handler is `Fix before launch`.

**Related skill routing:** Session-revocation propagation speed — `secod-identity-access`; audit event content — `secod-observability-response`.

### `PROVISIONAL-PB-10` — Restricted server-only credentials; test/live separation

**Applicability:** All provider credentials. Protects against key theft, live-data corruption, cross-stage bleed.

**Inspect and verify:** Secret/restricted keys appear only server-side (no client bundle, repo, logs, browser-exposed variables); least-scoped/restricted keys used where provider offers them; test and live credentials strictly separated per stage; no live secret in development/preview. Periodic review/rotation evidence requested from operator.

**Unsafe evidence:** Secret key in `NEXT_PUBLIC_*`/client code, committed files or logs; same live key across stages; publishable key used for privileged calls.

**Required negative test:** Scan client-entry bundles and repo history surface (`rg` over client dirs for key prefixes per provider adapter); confirm absent. Read-only.

**Passing / Not verified:** Passed with evidence requires server-only placement plus stage separation. Live key client-exposed is `Do not ship`. Rotation/Dashboard state unverifiable from repo: `Not verified` sub-item.

**Related skill routing:** Secret storage and scanning — `secod-secrets-config`; per-provider key models and leak response — provider adapter skill.

## Exceptional and failure conditions

Fail-closed requirements for target-reachable flows:

- **Timeouts/dependency failure**: provider unreachable during verification or retrieval — deny the state change, keep durable pending/retry record; never default to granting.
- **Partial operations**: checkout completed but mapping/entitlement write fails — rollback or durable pending state plus reconciliation; alert rather than silent inconsistency.
- **Retry/cancellation**: retries classified by the adapter contract; cancellation mid-flow leaves no half-applied entitlement; expired sessions cannot complete into grants without revalidation.
- **Revocation**: refund/dispute/cancellation revoke access even while sessions remain valid, within the application's stated propagation window.
- **Webhook duplicates/replay/redelivery/failure**: idempotent processing per `PROVISIONAL-PB-6/7`; unknown event types rejected safely; handler errors retried by provider without corrupting state.

Never invent provider retry schedules or delivery guarantees. A failed checker, crashed
processor, or incomplete test never counts as success; affected controls stay `Not verified`.

## Dependency and routing rules

Direct dependency exactly as in `secod/catalog.json`: `secod-core`.

Conditional routes: the five payment adapters listed above, only on their detection signals.

If `secod-core` or the applicable provider adapter is missing, unresolved, malformed or incomplete:

- Mark affected controls `Not verified`.
- Name the missing owner/evidence in findings.
- Never invent replacement dependencies or adapters.
- Never issue launch readiness; overall readiness belongs to `secod-ship-check`.

## Evidence and status rules

Statuses only: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`, `Not verified`.

Thresholds:

- `Do not ship`: client-trusted amounts or grants (`PB-1/PB-5`), client-exposed live secret (`PB-10`), forgeable webhook acceptance (`PB-6`).
- `Fix before launch`: missing idempotency on money-moving writes, non-atomic mapping with silent inconsistency, enabled lifecycle feature without handler, missing reconciliation.
- `Recommended hardening`: weaknesses with compensating controls, e.g., tolerance slightly generous, manual reconciliation step.
- `Passed with evidence`: control procedure executed with concrete artifacts (code paths, test output, provider-state evidence).
- `Not verified`: required evidence missing, stale, contradictory, inaccessible, snapshot-only, unsupported — or the check failed/incomplete.

Package presence never passes a control. Inferred configuration never passes.

### Capability-matrix evidence contract

Emit one row per detected provider with: `provider`, `adapter`, `signature`, `signed_timestamp`,
`freshness_rule`, `delivery_or_event_id`, `event_type`, `account_context`, `api_version`,
`retry_behavior`, `disabled_endpoint_behavior`, `compensating_replay_controls`, `source_refs`,
`source_review_expiry`, and `status`.

Every provider capability value must cite a current `Reviewed` direct-primary row from the
applicable adapter's `references/sources.md`. A missing adapter, missing row, indirect or snapshot
source, expired review, or unsupported value makes the matrix row `Not verified`; list it as a
launch blocker for `secod-ship-check`. Baseline sources never prove provider-specific fields.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End report includes:

- Applicability inventory (per stage: signals found, classification Candidate/Likely/Active, capability-matrix rows)
- Test results (executed commands, expected vs actual)
- Requested external evidence (Dashboard/API/operator items)
- `Not verified` items with the exact next verification step
- Launch blockers list

Route overall launch readiness exclusively to `secod-ship-check`.

## Negative fixtures and tests

Executable fixture suite: `secod/tests/insecure-fixtures/secod-payments-billing/README.md`; trigger case:
`secod/tests/trigger-cases/secod-payments-billing.md`; expected result:
`secod/tests/expected-results/secod-payments-billing.md`.

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-payments-billing/run_fixtures.py
```

The standard-library-only runner exercises PB-1 through PB-10, including clean behavior, client
tampering, raw card collection, outbound replay, unexpected API version, client-reported paid state,
forged/stale/duplicate webhooks, delivery disorder, retry/disablement gaps, partial mapping failure,
lifecycle correction, credential separation, missing adapter sources and missing provider evidence.
It writes no files, makes no network calls and emits machine-readable JSON. Exit `0` means fixture
expectations were reproduced, not that an inspected application or production provider passed.

Never report a fixture as executed without runner output. Never run destructive,
production-changing, user-creating, payment-creating, refunding, key-rotating, dashboard-changing or
account-changing tests without explicit authorization.

## References

- `references/sources.md` — provider-neutral primary-source register and portable mappings
- `references/prd-traceability.md` — complete PRD §8.4, §14.2 and §14.3 mapping; read when checking control, fixture or release-gate coverage
- Provider envelope/key/version specifics: `secod/skills/secod-stripe/SKILL.md`, `secod-polar`, `secod-lemonsqueezy`, `secod-dodo-payments`, `secod-whop` and their `references/sources.md`
