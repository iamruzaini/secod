---
name: secod-observability-response
description: Review and verify actionable, redacted security evidence plus tested containment, revocation, failure detection, recovery and restoration procedures. Apply when audit logging, log redaction, security alerting, incident runbooks, API-key revocation visibility, backup restore drills or webhook/queue/provider failure monitoring are present or claimed; package presence alone is Candidate.
---

# Observability & Response Security

## Mission

Produce actionable, redacted security evidence and confirm tested containment, revocation,
failure detection, recovery and restoration procedures exist for the reviewed repository.

Repository-only review cannot prove that production logs are actually emitted and retained,
that alerts actually fire on real incidents, that runbook steps work against live tenants, or
that a backup restores successfully in the provider environment. Those require runtime,
Dashboard/API, drill or human-supplied evidence. A failed checker or incomplete test never
counts as success.

`secod-ship-check` owns final launch readiness. This skill supplies findings only.

## Scope and ownership

Owned controls:

- Structured security audit events for login, access denial, privilege/admin changes,
  sensitive reads, payments and webhooks.
- Redaction of passwords, tokens, headers, bodies, prompts and PII from logs, errors and
  evidence exports; log access restriction and retention decisions.
- API-key lifecycle visibility: creation, use, scope/role change, anomaly, rotation and
  revocation.
- Alerts for fail-closed security-control failures, provider outages, retry exhaustion,
  disabled webhook endpoints and reconciliation drift.
- Incident runbooks with explicit breach-to-containment mapping for affected credentials,
  sessions, refresh-token families, share links, API keys, provider keys and tenant access;
  tested revocation, rotation, customer notification and recovery steps.
- Evidence preservation during an incident.
- Partial-operation recovery drills and backup restore tests.

Excluded controls (route to owner):

| Excluded | Owner |
| --- | --- |
| Fail-closed authorization design, bounded retry, cancellation, deterministic cleanup, partial-write rollback design | `secod-failure-safety` |
| Rate limits, quotas, spend ceilings, idempotency-key mechanics | `secod-abuse-limits` |
| Session/token issuance, storage and revocation mechanism design | `secod-identity-access` |
| Webhook signature/freshness/replay validation at the input boundary | `secod-inputs-apis`; payment-webhook specifics in `secod-payments-billing` |
| Backup encryption and data retention/deletion lifecycle policy | `secod-crypto-data-protection` |
| Secret storage, rotation mechanics and configuration separation | `secod-secrets-config` |
| Provider-specific log/alert/dashboard capabilities | Triggered framework/provider adapter |

This skill verifies detection, alerting, response evidence and drills for those mechanisms; it
does not re-review the mechanisms themselves.

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

Conditional routes (only when signals exist):

- `secod-payments-billing` — detected payment flows require payment-event audit and
  reconciliation-drift alerting evidence there as well.
- `secod-ai-api-integrations` — detected AI integrations add prompt/output logging rules owned
  there; this skill still owns redaction verification of whatever is logged.
- Triggered framework/provider adapter (e.g. `secod-vercel-platform`, `secod-cloudflare`,
  `secod-supabase`) — owns platform log drains, dashboards and provider-native alert limits.

## Required inputs

Repository inputs: source, middleware/logging code, error handlers, job/queue consumers,
webhook handlers, CI definitions, infrastructure-as-code, test suites, docs/runbooks.

Version/environment inputs: runtime and framework versions, per-environment (development,
preview, staging, production) logging/alerting configuration.

Provider/Dashboard inputs (commonly unavailable from repository alone — label as such):

- Log sink/drain configuration, retention periods and access controls in the deployed platform.
- Alert rule definitions, recipients and delivery-channel tests.
- Provider-side API-key inventory, last-used timestamps and audit-log availability.
- Backup schedule, snapshot retention and restore capability.
- On-call/notification routing and past incident records.

Human-supplied evidence: drill reports, restore-test outputs, notification templates,
approval for any destructive verification.

When external artifacts are supplied, read `references/external-evidence.md`, then run
`python skills/secod-observability-response/scripts/validate_evidence_bundle.py <manifest.json>`
from `secod/`. Bundle validation checks provenance fields, file hashes and required artifact
classes only. Inspect artifact contents before assigning any control status; a complete bundle
does not itself prove a control passed.

## Applicability and discovery

Group discovery signals:

- **Package/SDK:** logging libraries (`pino`, `winston`, `structlog`, OpenTelemetry),
  error trackers (`Sentry`), audit-log libraries, alerting/monitoring SDKs, backup tooling.
- **Environment variables:** log-level, log-drain/alert webhook URLs, `SENTRY_*`/`OTEL_*`
  variables, backup/restore credentials, on-call integration variables.
- **Routes/webhooks:** auth handlers, admin actions, payment/webhook endpoints, queue/job
  consumers, health-check endpoints.
- **Configuration:** logger setup/redaction filters, error-handler middleware, alert-rule
  config files, IaC for log sinks/alarms/budgets, runbook docs, `SECURITY.md`.
- **Deployment/provider evidence:** platform log drains, dashboard alert settings, provider
  audit-log features, backup schedules (only with Dashboard/API/human evidence).

Classification:

- `Candidate`: package installed, example variable referenced, dormant config file or weak
  signal only.
- `Likely`: logging/alerting/backup code or configuration exists but deployed or provider
  state is unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API
  or provider evidence (drain configured, alert delivered, restore executed).

Inventory audit events, alerts, backups and runbooks separately for development, preview,
staging and production. Conflicting or shared signals across environments (same sink, same
alert route, shared backup target without isolation) are `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries: which environments emit which events to which
   sinks, who can read them, what crosses environment boundaries.
2. Correlate active features and flows: map detected auth, admin, sensitive-read, payment and
   webhook flows to required audit events and alerts. Parallelizable with step 1 (read-only).
3. Verify applicable controls below. Steps are independent per control; parallelize only
   across read-only inspections.
4. Run safe negative tests (see each control and Negative fixtures section).
5. Classify evidence, mark gaps `Not verified`, route findings, and hand overall readiness to
   `secod-ship-check`.

For every security-critical conclusion about a provider/framework feature, discover through
the official `llms.txt` index (and `llms-full.txt` where published), then verify against the
directly linked official documentation page. Discovery snapshots never substitute for direct
source verification; record sources in `references/sources.md`.

## Control requirements

Stable control IDs below are approved in `secod/catalog.json`.

### `SECOD-OBS-01` — Structured security audit events

**Applicability:** Any server handling login, access denial, privilege/admin change,
sensitive-data reads, payments or webhooks. Protected property: ability to reconstruct who did
what, to what, when, with what outcome for security-relevant actions.

**Inspect and verify:** Locate event-emission points for each flow (auth handlers, guards/middleware
denials, role/scope changes, sensitive record access, payment state changes, webhook receipts).
Confirm each event carries actor, action, target, timestamp, outcome and a correlation/request ID;
confirm structured output (JSON/key-value, not free-text interpolation); confirm events survive
async boundaries where applicable. Secure decision: every listed flow emits a complete event to a
persistent sink reachable by operators.

**Unsafe evidence:** Missing events for any listed flow; events missing actor/target/outcome;
free-text-only logs; events written only to console in production; no correlation ID.

**Required negative test:** In a local/dev harness, perform an unauthorized access attempt or
admin change and confirm a denial/privilege-change event with actor, target and outcome is
emitted and queryable in the sink.

**Passing / Not verified:** Passed with evidence requires emitted-event inspection (code path
plus dev-harness output) AND production-sink evidence (dashboard export, retained sample with
secrets redacted, or operator confirmation). Missing production-sink evidence, dev-only
verification, or unverifiable retention is `Not verified`.

**Related skill routing:** Payment event semantics to `secod-payments-billing`; AI prompt/output
logging rules to `secod-ai-api-integrations`; platform drain configuration to triggered adapter.

### `SECOD-OBS-02` — Redaction and log-data minimization

**Applicability:** Every log, error report, trace and evidence export that can carry request
bodies, headers, prompts, model output or user fields. Protected property: no passwords, tokens,
session identifiers, authorization headers, raw bodies, prompts or unnecessary PII in logs,
error payloads or exported evidence.

**Inspect and verify:** Inspect logger serializers/redaction filters, exception-handler
middleware, error-tracker scrubbing config, and every explicit log call near auth, payment and
AI paths. Grep for logging of `Authorization`, `cookie`, `password`, `token`, `secret`,
request body dumps and prompt/response bodies. Confirm URL sanitization where tokens appear in
query strings. Secure decision: deny-by-default field filtering (allowlist, not blocklist where
feasible), verified against actual emitted output, not just configuration intent.

**Unsafe evidence:** Raw header/body/prompt logging; blocklist-only filters demonstrably bypassed
by nested or renamed fields; error tracker receiving full request context; secrets in trace IDs
or URLs; no retention/access decision recorded.

**Required negative test:** Submit a request containing marker values in password/token/header
fields through the dev harness; confirm markers never appear in emitted log/error-tracker output.
Search existing retained logs/fixtures for historical leaks using markers, not real secrets.

**Passing / Not verified:** Passed with evidence requires filter inspection AND emitted-output
marker test AND a documented retention/access decision. Filter config without output proof, or
unscannable historical logs, is `Not verified`.

**Related skill routing:** Secret exposure remediation to `secod-secrets-config`; AI-context
retention decisions to `secod-ai-api-integrations`.

### `SECOD-OBS-03` — API-key lifecycle visibility

**Applicability:** Applications issuing application-scoped API keys/tokens to users or tenants,
and applications consuming provider keys. Protected property: creation, use, scope/role change,
anomaly, rotation and revocation of keys are visible and actionable.

**Inspect and verify:** For issued keys: inspect issuance/rotation/revocation endpoints for audit
events (`SECOD-OBS-01`), key-prefix/last-used tracking, and anomaly hooks feeding
`SECOD-OBS-04` alerts. For
provider keys: confirm how unexpected use or scope drift would be noticed (provider audit logs,
usage alerts, periodic reconciliation). Secure decision: revocation takes effect on the enforcement
path within one request lifetime, and its effect is observable.

**Unsafe evidence:** Keys created/deleted with no event; revocation relying on periodic cache
expiry nobody measured; no way to list active keys per tenant; provider-key anomalies have no
detection path.

**Required negative test:** Dev harness: issue a key, revoke it, replay it against the enforcing
endpoint and confirm rejection; confirm both events (creation, revoked-use denial) are logged.
Do not rotate or revoke real production keys without explicit authorization.

**Passing / Not verified:** Passed with evidence requires replay-after-revocation test output
plus lifecycle-event evidence. Enforcement-path timing claims without measurement are
`Not verified`.

**Related skill routing:** Revocation mechanism design to `secod-identity-access`; secret
storage/rotation mechanics to `secod-secrets-config`.

### `SECOD-OBS-04` — Security alerting for control failures

**Applicability:** Any deployment with fail-closed security checks, external providers, retries
or webhooks. Protected property: operators learn about fail-closed security-control failures,
provider outages, retry exhaustion, disabled webhook endpoints and reconciliation drift before
or as users do.

**Inspect and verify:** Inventory alarm definitions (IaC or Dashboard evidence): dependency
failure triggering fail-closed denials, provider outage/error-rate alarms, dead-letter/
retry-exhaustion alarms, webhook endpoint auto-disablement alerts, reconciliation-job drift
alerts. Confirm each has a recipient, severity and delivery channel; confirm at least one
delivered test or historical firing exists. Never assume a provider's default notifications cover
these; require named evidence.

**Unsafe evidence:** Alarms defined but with no recipient/route; only generic error-rate
dashboards; silent DLQ growth; disabled-endpoint emails going to an unmonitored address;
alerts only in staging.

**Required negative test:** In dev/test, trigger one monitored condition (e.g. forced dependency
failure or retry exhaustion in a sandbox consumer) and capture the alert delivery. Do not disable
production webhook endpoints to test.

**Passing / Not verified:** Passed with evidence requires alarm-definition review AND one captured
delivery (test or historical) per critical alert class. Definitions without delivery evidence are
`Not verified`.

**Related skill routing:** Spend/quota ceilings to `secod-abuse-limits`; platform-native alarm
limits to triggered adapter; fail-closed design correctness to `secod-failure-safety`.

### `SECOD-OBS-05` — Incident runbooks and breach-to-containment mapping

**Applicability:** Any production deployment holding credentials, sessions, share links, API
keys, provider keys or tenant data. Protected property: a documented, tested path from detected
breach signal to containment for every affected capability class.

**Inspect and verify:** Require a runbook (repo doc or linked internal doc reference) mapping each
breach class — compromised password, stolen session cookie, refresh-token family reuse, leaked
share link, leaked application API key, leaked provider key, tenant takeover — to concrete
containment steps: what to revoke, in which system, in what order, with what verification. Confirm
revocation/rotation steps match actual mechanisms found in the code/provider (`SECOD-OBS-03`);
confirm
customer-notification step exists with template and trigger threshold. Confirm at least tabletop-
level execution evidence.

**Unsafe evidence:** No runbook; runbook naming systems/mechanisms absent from the repository or
provider; steps requiring undocumented provider abilities; no notification path; runbook never
exercised even as tabletop.

**Required negative test:** Tabletop walk-through of one breach class (e.g. leaked session):
follow the runbook against a dev/staging tenant and record each step that fails or cannot be
verified. Document gaps as findings. Do not execute containment against production.

**Passing / Not verified:** Passed with evidence requires runbook coverage of all applicable
breach classes AND a completed exercise (tabletop minimum) with dated results. Untested runbooks
are `Not verified`.

**Related skill routing:** Session/share-link/refresh-token revocation design to
`secod-identity-access`; provider-key rotation mechanics to `secod-secrets-config` and triggered
adapter.

### `SECOD-OBS-06` — Evidence preservation

**Applicability:** Any environment where an incident could require post-hoc analysis. Protected
property: relevant logs, audit events and configurations remain retrievable, integrity-protected
and access-controlled after an incident begins.

**Inspect and verify:** Check retention periods meet or exceed detection-plus-investigation
horizon; check immutability/write-protection of the security log sink where the platform supports
it; check access control on log stores; check export procedure exists and was exercised. Confirm
redaction (`SECOD-OBS-02`) applies to preserved evidence too.

**Unsafe evidence:** Retention shorter than plausible investigation window; mutable log storage
writable by the application identity itself; no export path; evidence access unrestricted.

**Required negative test:** Attempt (in dev or with authorization) to delete/alter a preserved
event via application credentials; confirm prevention. Export one redacted sample and confirm
completeness of actor/action/target/time/outcome fields.

**Passing / Not verified:** Passed with evidence requires retention/immutability/access evidence
from the deployed store AND an exercised export. Repository claims without store evidence are
`Not verified`.

**Related skill routing:** Data-retention policy ownership to `secod-crypto-data-protection`;
store configuration to triggered adapter.

### `SECOD-OBS-07` — Recovery drills for partial operations and backup restore

**Applicability:** Any deployment with durable writes or backups. Protected property: partial
multi-step operations can be reconciled after failure, and backups restore into working service
with proven RPO/RTO.

**Inspect and verify:** Inspect reconciliation logic for multi-step operations (payment + grant,
write + fan-out, provision + bill) and its alerting hookup (`SECOD-OBS-04`). Inspect backup schedule,
protection and restore procedure; require evidence of an executed restore (drill report,
timestamped output) rather than schedule existence. Confirm restored environments reject stale
credentials/secrets appropriately.

**Unsafe evidence:** Backups scheduled but never restored; restore target never validated for
service correctness; partial-operation recovery handled by manual ad-hoc SQL with no procedure;
reconciliation drift undetected.

**Required negative test:** Execute (or obtain dated artifacts of) a restore into an isolated
target and verify data plus service behavior; simulate one interrupted multi-step operation in
dev and confirm the reconciliation path completes or alerts.

**Passing / Not verified:** Passed with evidence requires executed-restore artifact AND observed
partial-operation recovery. Schedule-only evidence is `Not verified`. Restore drills touching real
provider projects require explicit prior authorization.

**Related skill routing:** Partial-write rollback design and bounded retry to
`secod-failure-safety`; backup encryption/retention to `secod-crypto-data-protection`;
provider-managed backup/PITR specifics to triggered adapter.

## Exceptional and failure conditions

Fail-closed requirements for observability/response machinery itself:

- **Logging/alerting dependency failure:** emission or alert-delivery failure must not silently
  drop security events; require bounded local buffering or a visible failure signal. Silent
  swallow-and-continue is unsafe evidence for `SECOD-OBS-01`/`SECOD-OBS-04`.
- **Partial operations:** if event write succeeds but business operation fails (or vice versa),
  the discrepancy must be detectable; tie to `SECOD-OBS-07` reconciliation.
- **Retry and cancellation:** audit-event and alert deliveries classify retries explicitly,
  bound attempts, and never duplicate events into false incident signals without deduplication.
- **Session/token revocation under degraded logging:** revocation must not depend on the logging
  subsystem being healthy; containment works while evidence may be degraded — record this mode
  in runbooks (`SECOD-OBS-05`).
- **Webhook duplicates, replays, redeliveries and failures:** the monitoring layer counts and
  alerts on them (`SECOD-OBS-04`); authenticity validation stays with `secod-inputs-apis` /
  `secod-payments-billing`. Never invent provider retry schedules, redelivery guarantees or
  endpoint-disable thresholds — require provider-source evidence for any such claim.

A failed checker, unreachable sink, or incomplete drill never counts as success; affected
controls are `Not verified`.

## Dependency and routing rules

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

If a dependency or conditional route is missing, unresolved, malformed or incomplete:

- Mark every affected control `Not verified`.
- Name the missing owner/evidence in the finding.
- Never invent replacement dependencies or substitutes.
- Never issue launch readiness; that verdict belongs to `secod-ship-check`.

## Evidence and status rules

Statuses used only: `Do not ship`, `Fix before launch`, `Recommended hardening`,
`Passed with evidence`, `Not verified`.

Thresholds for this skill:

- `Do not ship`: missing redaction of secrets/tokens in logs (`SECOD-OBS-02`) on any production
  path, no audit events at all for authentication/payment flows (`SECOD-OBS-01`), or revocation
  provably non-functional (`SECOD-OBS-03`).
- `Fix before launch`: applicable control lacks required production/drill evidence but has sound
  implementation; alerting classes with no delivery evidence; untested runbook.
- `Recommended hardening`: improvement beyond stated requirement (e.g., allowlist redaction
  upgrade, additional breach-class coverage).
- `Passed with evidence`: full combined evidence per control.
- `Not verified`: missing, stale, conflicting, inaccessible, unsupported or failed evidence,
  including package-presence-only claims, snapshot-only documentation, and inferred dashboard
  settings.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported
or failed evidence.

## Required output

One finding per applicable control with fields:
`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (per environment: events, sinks, alerts, backups, runbooks, drills).
- Test results (executed vs documentation-only).
- Requested external evidence (dashboard exports, drill artifacts, provider audit samples).
- `Not verified` items with exact missing-evidence reason.
- Potential launch-impact findings handed to `secod-ship-check`; never issue a blocker or
  launch-readiness verdict here.

Route overall launch readiness to `secod-ship-check`; this skill never issues it.

## Negative fixtures and tests

Map fixtures to controls:

| Fixture case | Controls |
| --- | --- |
| Clean: complete structured events, redaction filters, alert routes, runbook, restore artifact | `SECOD-OBS-01`..`SECOD-OBS-07` positive path |
| Insecure: raw token/password logged via body dump; nested-field blocklist bypass | `SECOD-OBS-02` |
| Missing-evidence: alert rules defined with no delivery evidence; backup schedule without restore artifact | `SECOD-OBS-04`, `SECOD-OBS-07` |
| Failure/replay: revoked-key replay accepted; duplicated webhook inflating alert counts without dedup; silent log-sink failure | `SECOD-OBS-03`, `SECOD-OBS-04`, `SECOD-OBS-01` |

Run `python tests/insecure-fixtures/secod-observability-response/run_fixtures.py` from `secod/`.
Runner uses Python standard library only, makes no network calls and emits machine-readable JSON.
Fixture success proves maintained harness behavior only. Production sink, delivered production
alerts, live runbook execution and provider restore remain `Not verified` until current artifacts
meeting `references/external-evidence.md` are supplied and inspected.

Never run destructive, production-changing, user-creating, payment-creating, refunding,
key-rotating, dashboard-changing or account-changing tests without explicit authorization.

## References

- [Source register](references/sources.md) — retained security-critical sources with review dates/expiry.
- [External evidence contract](references/external-evidence.md) — artifact manifest and provenance rules.
- Trigger case: `../../tests/trigger-cases/secod-observability-response.md`
- Insecure fixture plan: `../../tests/insecure-fixtures/secod-observability-response/README.md`
- Expected result: `../../tests/expected-results/secod-observability-response.md`

Keep direct URLs, long matrices, version notes and plan/region assumptions in `references/sources.md`,
not here.
