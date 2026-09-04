---
name: secod-threat-model
description: Establish assets, actors, trust boundaries, tenant boundaries, attacker goals, abuse cases, failure states and high-impact flows before a launch verdict. Triggers include any repository or design review request, new privileged/payment/AI feature, multi-tenant data model changes, new third-party integration, and any pre-launch assessment; absence of a prior model makes every downstream control unscoped.
---

# SECOD Threat Model Security

## Mission

Produce a written threat model covering assets, actors, trust boundaries, tenant boundaries,
attacker goals, abuse cases, failure states, and high-impact flows — grounded in the
application inventory produced by `secod-core` — so that every downstream SECOD skill knows
what it is protecting and against whom.

Repository-only review cannot prove deployed topology, provider-side trust behavior, real
attacker reachability, or that mitigations work in production. It produces the model and the
mitigation/residual-risk register with named owners. `secod-ship-check` owns final launch
readiness; this skill never issues it.

## Scope and ownership

Owned controls: asset/actor/privileged-action inventory; data-class inventory; complete
attack-surface enumeration including public/internal/deprecated/shadow/debug surfaces;
trust-boundary and data-flow modeling across browser, backend, build, CI/CD, deployment,
preview, production; tenant-boundary modeling; STRIDE-based abuse-case generation; third-party,
payment, and AI flow modeling including AI fallback/cache/embedding paths; failure-state,
degraded-mode, and recovery modeling; high-cost operation identification; deployment-assumption
documentation; mitigation/residual-risk register with routed owners.

Excluded controls (owned elsewhere): control-level verification of authentication, injection,
SSRF, uploads, payments, AI isolation, secrets, CI integrity (`secod-identity-access`,
`secod-inputs-apis`, `secod-runtime-execution`, `secod-data-files`, `secod-payments-billing`
plus adapters, `secod-ai-api-integrations` plus adapters, `secod-secrets-config`,
`secod-packages-delivery`, and family routers); monitoring/alerting implementation
(`secod-observability-response`); rate-limit implementation (`secod-abuse-limits`);
launch verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: none. This skill consumes the `secod-core` inventory and routes each
identified risk to its owning control skill; it has no conditional adapters of its own.

## Required inputs

From repository: the `secod-core` applicability inventory (signals by class and environment);
routes, webhooks, queue/cron workers; database schemas/migrations/policies; environment
configuration names; CI/CD and IaC definitions; existing design docs or ADRs if present.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
actual production topology and network reachability; preview/staging URL exposure; provider-side
data flows beyond documented APIs; organizational actors (who can deploy, who holds admin);
incident-history knowledge; business impact tolerances; third-party contractual data-handling
terms.

Human-supplied evidence: authorized architecture diagrams, deployment topology, data-class
confirmations, acceptable-risk decisions signed by an owner.

## Applicability and discovery

Always applicable: every review requires a current threat model before control verdicts are
finalized downstream.

Signal groups consumed (produced by `secod-core`; classify any newly observed signal here):

- Package/SDK: providers and integrations that define trust edges.
- Environment variables: names revealing additional environments, tenants, or provider tiers.
- Routes/webhooks: public surface, admin/internal surfaces, callback endpoints.
- Configuration: multi-tenant flags, environment separation, debug/test surfaces, IaC topology.
- Deployment/provider evidence: preview URLs, generated hosts, dashboard-derived topology.

Classification follows `secod-core` semantics:

- `Candidate`: inferred edge or actor without corroboration.
- `Likely`: modeled edge supported by code/config but unverified in deployment.
- `Active`: edge corroborated by deployed, runtime, Dashboard, Management API, or provider
  evidence.

Maintain separate models for development, preview, staging, and production. A boundary present
in one environment but not another is recorded per environment. Conflicting or shared
environment signals keep affected model elements `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries using the `secod-core` inventory; draw or record
   every boundary crossing (browser↔backend, backend↔provider, build↔deploy, prod↔preview/
   staging, tenant↔tenant). Parallelizable per environment once inventories exist.
2. Correlate active features and flows into the model: assets, actors, privileged actions, data
   classes, entry/exit points. Parallelizable after step 1 completes for that environment.
3. Verify applicable controls below: completeness of surfaces, abuse coverage, failure coverage,
   cost coverage, assumption documentation, register quality.
4. Run safe negative tests: completeness probes against fixtures and the live inventory
   (read-only reasoning; no provider interaction).
5. Classify evidence, emit findings, route each identified risk to its owner skill, hand the
   residual-risk register to `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-threat-model-N` and require catalog approval before promotion.

Threat identification method: apply STRIDE per element at each trust boundary (Spoofing→authN,
Tampering→integrity, Repudiation→accounting, Information Disclosure→confidentiality, Denial of
Service→availability, Elevation of Privilege→authZ), supplemented by LINDDUN-style privacy
questions where personal data crosses boundaries. Anchor abuse-case priorities on OWASP
Top 10:2025 categories — note SSRF now inside A01 Broken Access Control, supply-chain failures
elevated to A03, and failing-open/logical-error classes under new A10 Mishandling of Exceptional
Conditions.

### `PROVISIONAL-threat-model-1` — Assets, actors, and privileged actions

**Applicability:** Every application. Protects against mis-scoped reviews that protect nothing
real.

**Inspect and verify:** Enumerate user roles and admin/operator roles; enumerate data classes
(Public / Internal / Confidential / Regulated / Credentials-and-verifiers) mapped to actual
stores found in inventory; list every privileged action (role change, export, refund, deletion,
key rotation, tenant creation) with its route/worker and required privilege. Cite
schema/route/code evidence for each.

**Unsafe evidence:** "Admin" defined only by hidden UI; data classes asserted without store
evidence; undocumented export contents treated as non-sensitive.

**Required negative test:** Fixture with an undocumented admin export must classify contents
`Unknown`, force conservative handling, and block downstream scoping until resolved.

**Passing / Not verified:** Pass requires every role, data class, and privileged action cited
to inventory evidence. Unclassified data or unknown actors keep affected elements `Not
verified`.

**Related skill routing:** Data-class confirmation depth → `secod-crypto-data-protection`;
privileged-action enforcement checks → `secod-identity-access`.

### `PROVISIONAL-threat-model-2` — Complete attack-surface enumeration

**Applicability:** Every application. Protects against unmodeled entry points.

**Inspect and verify:** From the `secod-core` inventory, enumerate all API hosts/routes/versions
including public, internal, deprecated, shadow, and debug surfaces; background jobs, queues,
scheduled work with their credential scopes and data flows; email/SMS/magic-link/OTP/invitation/
account-recovery flows; file upload/export and browser-rendering entry points; realtime and
webhook endpoints. Every enumerated surface needs an environment tag.

**Unsafe evidence:** Debug/test/shadow endpoints omitted because "not production"; recovery
flows absent from the model; queue consumers modeled without credential scope.

**Required negative test:** Inventory containing a debug/mock route must appear in the model's
surface list and be flagged for ownership routing (`secod-inputs-apis`), not silently dropped.

**Passing / Not verified:** Pass requires surface list reconciled 1:1 against the core
inventory with zero unmatched entries. Unmatched or conflicting entries keep the affected
surfaces `Not verified`.

**Related skill routing:** Surface-level validation → `secod-inputs-apis`;
`secod-runtime-execution` for execution surfaces; hosting/cloud routers for worker surfaces.

### `PROVISIONAL-threat-model-3` — Trust boundaries and data-flow model

**Applicability:** Every application. Protects against threats that cross unexamined edges.

**Inspect and verify:** Record every boundary: browser↔backend, backend↔third-party, backend↔
database/storage, build↔CI/CD↔deploy, production↔preview/staging, tenant↔tenant, human admin↔
production. For each crossing record protocol, authentication/capability mechanism, data classes
transferred, and failure behavior. Tenant boundary must state where tenant context originates
and where it is verified.

**Unsafe evidence:** Boundary drawn without an enforcement point; tenant context accepted from
the browser with no server verification noted; preview treated as inside the production trust
boundary.

**Required negative test:** Multi-tenant fixture must show each tenant-boundary crossing with a
named server-side verification point; a missing one is `Fix before launch` for the model.

**Passing / Not verified:** Pass requires all boundaries recorded with enforcement points and
data classes. Deployment topology without supplied evidence keeps those edges `Likely` at best.

**Related skill routing:** Enforcement verification → `secod-identity-access` (authN/authZ/
tenant), `secod-supabase`/family routers for provider-enforced boundaries,
`secod-web-app-security` for browser edge.

### `PROVISIONAL-threat-model-4` — Abuse cases and misuse cases

**Applicability:** Every modeled surface. Protects against controls built for the happy path.

**Inspect and verify:** For each high-impact flow (auth, recovery, payment, entitlement, export,
AI generation, invitation), generate STRIDE abuse cases including: cross-tenant access attempts,
ID manipulation, replay/reuse, enumeration, privilege escalation via parameter tampering, quota
bypass through multiple accounts, business-logic sequence abuse (skip steps, repeat steps,
negative values, unusual orderings). Prioritize by impact × likelihood; anchor on OWASP
Top 10:2025 A01/A07/A10 patterns. Record each abuse case with expected secure outcome.

**Unsafe evidence:** Abuse list generic boilerplate not tied to actual flows; payment flows
modeled without duplicate/out-of-order/refund cases; AI flows modeled without prompt-injection
and output-abuse cases.

**Required negative test:** Checkout flow fixture must yield at minimum: replay, out-of-order,
price-tampering, cross-tenant purchase, and refund-abuse cases with expected server behaviors;
missing categories are model defects.

**Passing / Not verified:** Pass requires abuse cases per high-impact flow covering all six
STRIDE categories or documented justification why a category cannot apply. Untestable
assumptions keep the case `Not verified`.

**Related skill routing:** Case execution → `secod-abuse-limits` (rate/idempotency),
`secod-payments-billing` + adapters, `secod-ai-api-integrations`, `secod-identity-access`.

### `PROVISIONAL-threat-model-5` — Failure states, degraded modes, and recovery

**Applicability:** Every dependency, provider, transaction, and revocation path in the model.
Protects against fail-open and unrecoverable partial states.

**Inspect and verify:** For each external dependency/provider and each multi-step operation:
define behavior under timeout, outage, partial completion, retry, cancellation, duplicate
delivery (webhooks/queues); define session/token/revocation propagation after password reset,
factor change, role change, compromise; define degraded modes and their reduced guarantees;
document recovery paths and who executes them. Explicitly evaluate fail-open risk at every
security check (OWASP Top 10:2025 A10). Never invent provider retry schedules or delivery
guarantees — mark unknown provider behavior as an assumption to verify against provider docs.

**Unsafe evidence:** "Provider is reliable" as mitigation; no rollback defined for
payment/entitlement mutations; revocation modeled as instant global without evidence.

**Required negative test:** Payment webhook flow fixture must specify duplicate-delivery and
out-of-order handling plus partial-failure rollback before the model passes; absence is a model
defect routed to `secod-payments-billing`.

**Passing / Not verified:** Pass requires every modeled dependency and privileged mutation to
have explicit timeout/outage/partial/duplicate behavior plus recovery owner. Unverified provider
behavior stays `Not verified` with the exact documentation needed.

**Related skill routing:** Implementation checks → `secod-failure-safety`,
`secod-inputs-apis` (webhook authenticity/freshness/dedup), `secod-observability-response`
(recovery drills, backup restore), `secod-identity-access` (revocation propagation).

### `PROVISIONAL-threat-model-6` — Third-party, payment, and AI flow modeling

**Applicability:** Any third-party integration, payment provider, or AI API usage detected in
inventory. Protects against unmodelled external trust and data exposure.

**Inspect and verify:** For each third party: purpose, data sent/received with classes, auth
direction, webhook paths, failure behavior, contractual/retention assumptions. Payment flows:
checkout, entitlement grant, refund/dispute/chargeback paths, idempotency, reconciliation. AI
flows: provider/model fallback chains, what reaches prompts (secrets? other-tenant data?), cached
prompts/responses, embeddings and vector-store contents and their tenant scoping, tool/function
calling reach, retention/training settings as modeling assumptions requiring provider-doc
verification.

**Unsafe evidence:** Fallback providers assumed to satisfy the same data policy; vector store
modeled without tenant-scoped metadata strategy; "AI provider handles security" assumption.

**Required negative test:** RAG feature fixture must produce a flow record showing tenant filter
point before retrieval and fallback-provider policy comparison; missing either blocks the model.

**Passing / Not verified:** Pass requires flow records per active integration with data classes
and trust decisions cited. Provider retention/region/fallback-policy facts are `Not verified`
until confirmed against current official provider documentation.

**Related skill routing:** `secod-ai-api-integrations` + model adapters, `secod-vercel-ai`,
Cloudflare AI adapters; `secod-payments-billing` + payment adapters; `secod-email-messaging`;
`secod-crypto-data-protection` (retention/deletion lifecycle).

### `PROVISIONAL-threat-model-7` — High-cost operations and spend abuse

**Applicability:** Any metered/expensive operation: AI generation, exports, rendering, email/SMS
at volume, queue fan-out, third-party API calls. Protects against financial-exhaustion attacks.

**Inspect and verify:** Enumerate operations with per-call cost or volume amplification; identify
who can trigger them, what caps exist, what happens when caps fail; model abuse via many accounts,
retries, oversized inputs. Route cap implementation to `secod-abuse-limits`; this control owns
identification and attacker-perspective completeness.

**Unsafe evidence:** Cost ceilings asserted without any enforcing code/config signal; free-tier
signup modeled without multi-account abuse case.

**Required negative test:** AI-generation endpoint fixture must appear in the cost model with
trigger actor, amplification factor estimate, and routed cap owner; omission is a model defect.

**Passing / Not verified:** Pass requires every inventory-detected expensive operation present
in the cost model with routed owner. Actual ceiling effectiveness is owned downstream and stays
out of scope here.

**Related skill routing:** `secod-abuse-limits`, `secod-ai-api-integrations`, payment adapters
(spend alerts).

### `PROVISIONAL-threat-model-8` — Assumptions, mitigations, and residual-risk register

**Applicability:** Every model element. Protects against silent acceptance of unproven safety.

**Inspect and verify:** Produce a register listing: deployment assumptions (topology, environment
separation, plan/tier) each tagged repository-evidenced vs supplied-evidence vs unverified; each
identified threat mapped to a mitigation with owning skill and status; residual risks explicitly
accepted with named accepter and review date; provider-behavior assumptions flagged for official-
documentation confirmation. The register feeds `secod-ship-check`.

**Unsafe evidence:** Residual risks without owners; assumptions marked safe because "default";
mitigations referencing controls no skill owns.

**Required negative test:** Fixture with one accepted-risk entry lacking an accepter name must
fail register validation (`Not verified` for that entry).

**Passing / Not verified:** Pass requires zero unmapped high-impact threats, zero ownerless
residual risks, and every unverified assumption listed with the evidence needed.

**Related skill routing:** `secod-ship-check` consumes the register; all control skills own
their mitigation entries.

## Exceptional and failure conditions

- `secod-core` inventory unavailable, incomplete, or malformed: threat model proceeds only for
  inventoried scope; everything else `Not verified`; never guess surfaces.
- Model built from stale inventory: re-run applicability; stale models cannot pass
  PROVISIONAL-threat-model-2.
- Conflicting environment evidence: model element recorded per conflicting source, classified
  `Conflicting`, affected threats `Not verified`.
- Provider documentation inaccessible or contradictory during flow modeling: record assumption
  as unverified in the register; do not resolve by inference.
- Partial review interruption: retain completed model sections with scope markers; unfinished
  sections block the register from passing.
- A failed checker or incomplete test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: none.

If `secod-core` is missing, unresolved, malformed, or fails: mark every control `Not verified`,
name `secod-core` as the missing owner, never reconstruct inventories from prose, never issue
launch readiness. Risks identified during modeling route to the owning skills named per control;
unroutable risks go to `secod-ship-check` as blockers.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: complete reconciled surface enumeration; boundaries with enforcement
  points; STRIDE coverage per high-impact flow; failure/recovery records per dependency;
  cost model complete; register with zero unmapped high-impact threats and zero ownerless
  residual risks.
- `Fix before launch`: missing surface reconciliation, missing tenant-boundary enforcement
  points, missing payment/AI abuse categories, ownerless critical residual risks.
- `Recommended hardening`: justified STRIDE-category exclusions worth revisiting; low-impact
  assumptions unverified.
- `Not verified`: unverified deployment topology, unconfirmed provider behavior, unresolved
  conflicts, missing supplied evidence, interrupted model sections.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (assets/actors/boundaries/surfaces by environment);
test results; requested external evidence (topology confirmations, provider-doc verifications,
risk-acceptance sign-offs, by owner); `Not verified` items with next verification step; launch
blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-threat-model/README.md` | Documentation-only plan | All controls |
| Undocumented admin export | Documentation-only case | -1 (unknown data class) |
| Debug/mock route omitted from model | Documentation-only case | -2 (surface reconciliation) |
| Multi-tenant edge without server verification point | Documentation-only case | -3 |
| Checkout without duplicate/refund abuse cases | Documentation-only case | -4 |
| Webhook flow without partial-failure rollback | Documentation-only case | -5 |
| RAG flow without pre-retrieval tenant filter | Documentation-only case | -6 |
| AI endpoint absent from cost model | Documentation-only case | -7 |
| Accepted risk without named accepter | Documentation-only case | -8 |

No executable commands exist for these fixtures; reasoning-based verification only. Never claim
Markdown fixture plans executed as code. Never run destructive, production-changing,
user-creating, payment-creating, refunding, key-rotating, dashboard-changing, or
account-changing tests without explicit authorization.

## References

- [`references/sources.md`](sources.md) — source register: OWASP Top 10:2025, OWASP Threat
  Modeling Cheat Sheet (four-question framework, STRIDE), LINDDUN privacy framework reference.
