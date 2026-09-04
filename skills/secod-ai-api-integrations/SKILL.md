---
name: secod-ai-api-integrations
description: Review developer-owned AI API, SDK, RAG, chat, streaming and realtime integrations for server-side key handling, usage/spend limits, model/provider allowlists, prompt-injection defense, tenant-scoped retrieval/context/cache, retention/deletion, output validation, moderation, fallback parity and batch/webhook authenticity. Apply when an LLM SDK (`openai`, `@anthropic-ai/sdk`, `@google/genai`, `ai`), chat/completion proxy route, embedding/vector-store call, SSE/streaming AI endpoint, realtime session, or provider webhook is detected. Package presence alone is Candidate.
---

# AI API Integrations Security

## Mission

Secure the application's developer-owned AI API paths so that long-lived provider credentials
never reach clients, every proxied request is authenticated and bounded, tenancy decisions stay
outside model control, and model output cannot grant data, payment or admin access.

Repository-only review cannot prove provider Dashboard settings, deployed retention/training
configuration, production traffic behavior or provider-side deletion completion. This skill
secures developer-owned integrations only; users' agents, MCP servers and client-agent permissions
are out of scope. `secod-ship-check` owns final launch readiness.

## Scope and ownership

Owned controls: `PROVISIONAL-AI-01` through `PROVISIONAL-AI-11` below.

Excluded controls and their owners:

- General authentication/session mechanics: `secod-identity-access`.
- Secret storage mechanics and environment hygiene: `secod-secrets-config`.
- Generic input validation, request signing, non-AI webhooks: `secod-inputs-apis`.
- Rate-limit infrastructure, quota stores and retry/backoff depth: `secod-abuse-limits`;
  this skill verifies the AI-specific subset inside its controls.
- Log infrastructure, alert delivery, incident response: `secod-observability-response`.
- Partial-operation rollback and degraded-state patterns: `secod-failure-safety`.
- Payment/consequential entitlement flows touched by AI features: `secod-payments-billing`.
- Provider-native project/key/plan specifics: matching provider skill (`secod-openai`,
  `secod-anthropic`, `secod-google-genai`, `secod-xai-grok`, `secod-vercel-ai`,
  `secod-cloudflare-workers-ai`, `secod-cloudflare-ai-gateway`, `secod-cloudflare-vectorize`).

Direct dependencies (copied exactly from `secod/catalog.json`): `secod-core`.

Conditional routes (only when the named feature is detected):

- Detected provider SDK/integration: the matching provider skill above.
- Vector database/index specifics beyond RAG flow logic: the owning platform skill.
- AI generation spend/token limits at infrastructure level: `secod-abuse-limits`.

## Required inputs

Repository-supplied:

- AI route/handler code: proxy endpoints, streaming handlers, embeddings/RAG pipelines,
  batch/background jobs, webhook receivers, client-facing AI UI code.
- Model/provider configuration: allowlists, snapshot/version strings, fallback chains,
  moderation settings, cache key construction, retention calls.
- Tests and CI covering prompt-injection, improper-output, cross-tenant retrieval and
  limit-exhaustion cases.
- Deployment definitions separating development, preview, staging and production.

Commonly unavailable repository-only inputs (label as such when absent):

- Provider Dashboard/API evidence: retention, training opt-out, zero-data-retention eligibility,
  telemetry, region, spend ceilings, project/key scoping.
- Proof of provider-side completion of file/vector-store deletions.
- Human confirmation of approved data-handling policy and fallback acceptance.

## Applicability and discovery

Inventory each environment separately. Conflicting or shared environment signals are
`Not verified`. Official AI-provider/SDK reference discovery uses `llms.txt` and, where
published, `llms-full.txt`; security-critical conclusions must be verified against directly
linked official documentation, never the index alone.

Signal groups:

- Package/SDK: `openai`, `@anthropic-ai/sdk`, `@google/genai`, `groq-sdk`, `mistral`,
  `cohere`, `ai` / `@ai-sdk/*`, LangChain/LlamaIndex, vector-store client packages,
  provider webhook verifier libraries.
- Environment variables: `OPENAI_API_KEY` and equivalents, base URLs, gateway IDs,
  model defaults, spend caps.
- Routes/webhooks: `/api/chat`, `/completions`, `/embeddings`, SSE/WebSocket stream
  endpoints, upload-to-context paths, provider webhook receiver paths, batch status routes.
- Configuration: model allowlist tables, middleware ordering around AI routes, cache key
  builders, moderation/filter settings, RAG ingestion pipelines.
- Deployment/provider evidence: gateway bindings, project/region config, billing alerts.

Classification:

- `Candidate`: package installed, example variable, dormant file or weak signal only.
- `Likely`: repository code/config implements the control; deployed/provider state unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API
  or other provider evidence.

## Review workflow

Steps 1 and 2 are parallelizable; later steps depend on them.

1. Inventory environments and trust boundaries: every AI-touching route, job, webhook and
   client surface, per environment.
2. Correlate active features and flows: chat, streaming, realtime, RAG, embeddings, batch,
   function/tool calling, image/file generation, provider webhooks.
3. Verify applicable controls below against repository evidence first, then deployment and
   provider/Dashboard evidence.
4. Run safe negative tests locally or in an authorized non-production environment only.
5. Classify evidence and route findings per status rules and the ownership table.

## Review-time external evidence gates

Read and apply `references/review-evidence.md` whenever provider/Dashboard evidence is required or
a short-lived client-token mechanism is detected. Its evidence mappings and provider-specific
token gate are mandatory. Missing or wrong-scope evidence keeps only mapped controls `Not
verified`; never make blanket cross-provider claims.

## Control requirements

The catalog defines no stable control IDs for this skill yet; IDs below use
`PROVISIONAL-<provider>-<number>` and catalog approval is required before promotion.

### `PROVISIONAL-AI-01` — Server-side credentials and authenticated proxying

**Applicability:** Every path where the browser/app client reaches a model provider. Protected
property: long-lived provider keys and provider-account authority stay server-side.

**Inspect and verify:** Provider keys referenced only in server runtime (no `NEXT_PUBLIC_*`,
browser bundles, mobile configs or repo-committed values); client requests hit an app endpoint
that authenticates the user first (`secod-core`/auth middleware) before forwarding; any official
short-lived client-token mechanism (for example ephemeral realtime tokens) passes the review-time
provider-specific gate above.

**Unsafe evidence:** Provider key shipped to client; unauthenticated proxy route; long-lived key
inlined where an officially documented short-lived token should be; key chosen or supplied by
client input.

**Required negative test:** Request the AI endpoint without a valid session; expect rejection
before any provider call. Inspect client bundle for key material; expect none.

**Passing / Not verified:** Pass requires server-only key evidence plus passing unauthenticated-
request test per environment class. A detected short-lived client-token path also requires current
provider-specific documentation and matching implementation/configuration evidence. Key
rotation/scoping depth routes to provider skills; Dashboard-only proof is requested external
evidence, otherwise `Not verified`.

**Related skill routing:** Key storage/scoping details: `secod-secrets-config`, provider skill.

### `PROVISIONAL-AI-02` — Per-user, tenant and spend limits on AI consumption

**Applicability:** Every model call whose cost scales with user input. Protected property:
per-user, tenant, model, request, token, file, stream, retry and monthly-spend budgets against
abuse and runaway cost.

**Inspect and verify:** Server-enforced counters/ceilings per user, tenant and aggregate account;
token limits (`max_tokens`) set by server policy, not client payload; file/upload size and count
caps feeding context; stream duration/chunk bounds; bounded retries (see ABUSE depth);
monthly-spend ceiling or alert configured; concurrency caps on expensive generation.

**Unsafe evidence:** Client-controlled token/file/stream parameters passed through to provider;
no per-principal ceiling; unlimited retries; cost visible only via manual dashboard checks.

**Required negative test:** Submit oversized input or repeated requests past a configured cap;
expect server rejection (`429` or documented equivalent) before provider spend accrues.

**Passing / Not verified:** Pass requires server-side bound evidence plus the negative test.
Provider-side spend-ceiling evidence commonly unavailable repository-only: request the exact
Dashboard/API artifact listed in the external-evidence gate; absent or non-matching evidence keeps
AI-02 `Not verified`. Limiter store consistency: `secod-abuse-limits`.

**Related skill routing:** Limit/quota infrastructure: `secod-abuse-limits`; provider plan
limits: provider skill.

### `PROVISIONAL-AI-03` — Server-owned model/provider allowlists and version governance

**Applicability:** Every place a provider, model, snapshot/version, tool set or generation
parameter can be selected. Protected property: clients cannot choose arbitrary providers/models,
unrestricted token limits, retention settings or provider credentials.

**Inspect and verify:** Explicit server-side allowlist mapping user intent to approved
provider/model; explicit model snapshot/version strings rather than floating aliases where the
provider supports pinning; deprecation monitoring and an upgrade-approval step recorded;
regression/evaluation evidence before model upgrades reach production; retention/generation
parameters decided server-side.

**Unsafe evidence:** Model/provider name accepted from client payload; unpinned aliases where
pinning is available and stability matters; silent auto-upgrade with no evaluation artifact;
retention flags client-selectable.

**Required negative test:** Request a disallowed or arbitrary model through the endpoint;
expect server rejection regardless of provider acceptance.

**Passing / Not verified:** Pass requires allowlist evidence plus the rejection test.
Deprecation/upgrade process without recorded approval artifacts is `Fix before launch` or
`Not verified` depending on evidence quality.

**Related skill routing:** Provider-specific model/version rules: provider skill.

### `PROVISIONAL-AI-04` — Untrusted inputs and outputs; no model-granted authority

**Applicability:** Prompts, user uploads, retrieved RAG documents, fetched webpages and all
model output. Protected property: consequential authorization never originates in model text.

**Inspect and verify:** Application treats all listed inputs as untrusted data, not instructions;
model output parsed/rendered as content only; any action, data grant, payment change or admin
capability triggered by output re-validated against the authenticated user's server-side
entitlements; application-owned prompt-injection test cases and improper-output test cases exist
and run in CI; system prompts do not contain secrets whose disclosure would be exploitable.

**Unsafe evidence:** Output fields such as `"role": "admin"` or `"grantAccess": true` consumed
without server re-validation; RAG/webpage text concatenated into instruction position with no
delimiting/escaping strategy or injection tests; tool/function execution driven solely by model
decision on privileged endpoints.

**Required negative test:** Inject an instruction via retrieved document or user input that
attempts a privileged action or data disclosure; expect no privilege change and no unrelated data
in response. Feed malformed/improper output; expect safe error, not workflow execution.

**Passing / Not verified:** Pass requires untrusted-treatment evidence plus both tests.
Moderation-layer presence alone does not satisfy this control.

**Related skill routing:** Authorization mechanics: `secod-identity-access`; payment grants:
`secod-payments-billing`.

### `PROVISIONAL-AI-05` — Tenant isolation in retrieval, context and caching

**Applicability:** RAG retrieval, context assembly, conversation history and any prompt/response/
cache keyed storage. Protected property: one principal never retrieves another tenant's context.

**Inspect and verify:** Tenant/owner filter applied before retrieval query and again before
returned context reaches the caller; prompt, response and semantic-cache keys include tenant/user
scope; model context contains no secrets and no unrelated-tenant data; similarity ranking never
used as authorization.

**Unsafe evidence:** Retrieval query without owner predicate; shared cache key across principals;
secrets or other tenants' records observable in assembled context or logged payloads.

**Required negative test:** Retrieve as tenant A with content ids/names belonging to tenant B;
expect empty result. Repeat identical prompt as two tenants sharing a cache; expect no cross-
principal cache hits.

**Passing / Not verified:** Pass requires filter-before-retrieval plus scoped-key evidence plus
both tests. Cross-tenant leakage reachable in any test is `Do not ship`.

**Related skill routing:** Vector index/binding specifics: owning platform skill (e.g.
`secod-cloudflare-vectorize`); data-layer authorization: `secod-identity-access`.

### `PROVISIONAL-AI-06` — Retention, deletion and data-handling policy match

**Applicability:** Uploaded files, embeddings, vector stores, RAG indexes, conversation history
and provider-held copies. Protected property: data lifecycle and provider settings match data
sensitivity.

**Inspect and verify:** Application-side deletion removes source file, embedding, vector-store
record and index entry, tracked to completion with verification; provider-side retention,
training-use opt-out, region, zero-data-retention eligibility and telemetry settings identified
per used endpoint/feature from direct official documentation and matched to the data
classification; expiry policies set where offered.

**Unsafe evidence:** Source deleted while vectors persist indefinitely with no reconciliation;
provider training/retention state unknown for sensitive data; ZDR assumed without documented
eligibility evidence.

**Required negative test:** Delete one ingested document; expect retrieval to return nothing and
deletion pipeline to complete without orphaned vectors (or a tracked pending state).

**Passing / Not verified:** Pass requires application lifecycle evidence plus the deletion test.
Provider-side retention/training/ZDR/telemetry configuration and deletion completion require the
matching review-time artifacts listed in the external-evidence gate. Absent, inaccessible, stale,
wrong-scope or uncorrelated evidence keeps AI-06 `Not verified`. Never invent retention periods,
plan availability or ZDR guarantees.

**Related skill routing:** Provider retention specifics: provider skill; storage lifecycle:
`secod-data-files`.

### `PROVISIONAL-AI-07` — Streaming and structured-output validation

**Applicability:** Incremental streamed parts and structured/JSON/tool-call output. Protected
property: no unsafe content reaches browser or application workflow before validation.

**Inspect and verify:** Stream parts validated/sanitized per part and rendered safely (no raw
HTML/markdown execution, no direct `innerHTML`); accumulated stream reconciled against final
schema; structured output schema-validated before rendering, storing, querying or passing into
normal application workflows; tool-call arguments validated against expected shapes before
execution.

**Unsafe evidence:** Stream chunks written straight into DOM or trusted as workflow triggers;
JSON.parse without schema check; structured fields stored or queried after parse failure is only
logged.

**Required negative test:** Return malformed JSON and an over-long/malicious stream chunk from a
test harness or mock provider; expect validation failure handled safely, no partial unsafe
render, no workflow side effect.

**Passing / Not verified:** Pass requires schema/validation code-path evidence plus the
malformed-output test.

**Related skill routing:** XSS/rendering depth: `secod-web-app-security`; workflow safety:
`secod-runtime-execution`.

### `PROVISIONAL-AI-08` — Moderation, blocked output and abuse reporting

**Applicability:** User-facing generation surfaces subject to safety/moderation policy. Protected
property: consistent, fail-safe handling of flagged content and an abuse-reporting decision.

**Inspect and verify:** Documented moderation policy applied to inputs and/or outputs as
appropriate; blocked-output and provider safety errors produce defined user-facing responses, not
crashes or raw error leakage; abuse-reporting mechanism or explicit decision not to have one
recorded and approved.

**Unsafe evidence:** Safety-category exceptions unhandled (500s leaking internals); moderation
result trusted as authorization; no record of the abuse-reporting decision.

**Required negative test:** Trigger a blocked-content response in a controlled case; expect the
defined safe response and correct status, no internal detail exposure.

**Passing / Not verified:** Pass requires policy evidence plus the blocked-response test. Policy
adequacy judgment is recorded; absence of any policy is `Fix before launch` for user-facing
surfaces.

**Related skill routing:** Monitoring/reporting infrastructure: `secod-observability-response`.

### `PROVISIONAL-AI-09` — Provider fallback policy parity

**Applicability:** Any automatic or configured fallback/failover between providers, models,
regions or gateways. Protected property: no fallback silently weakens approved data-handling
terms.

**Inspect and verify:** Each fallback target's provider, model, region, retention, training,
telemetry and privacy terms compared against the same approved policy; fallback chain explicit in
configuration; fallback events observable; client cannot trigger or select fallback targets.

**Unsafe evidence:** Implicit provider-level fallback enabled without review; fallback target with
unknown retention/training posture; client-selected routing.

**Required negative test:** Force primary-provider failure in a test environment; expect fallback
only within the approved chain and a recorded fallback event.

**Passing / Not verified:** Pass requires explicit-chain evidence plus parity review of every
target using current official documentation plus matching account/environment evidence. Unknown
or wrong-scope terms on any target keep affected flows `Not verified`.

**Related skill routing:** Gateway/routing specifics: provider or gateway skill
(`secod-vercel-ai`, `secod-cloudflare-ai-gateway`).

### `PROVISIONAL-AI-10` — Background jobs, batch runs and provider webhooks

**Applicability:** Asynchronous generations, batch submissions, provider webhooks/callbacks and
status/result retrieval endpoints. Protected property: only authentic provider events mutate
state; results stay tenant-bound and idempotent.

**Inspect and verify:** Webhook signature/authenticity verification using the exact scheme the
provider documents (verify against direct official docs; never invent required fields);
duplicate/replayed deliveries deduplicated idempotently; batch submission, status and result
retrieval enforce ownership (no IDOR across tenants); persisted request IDs correlate results to
tenant; failures leave recoverable pending state, not inconsistent grants.

**Unsafe evidence:** Webhook receiver trusting payload without signature verification; status/
result endpoints accepting unscoped IDs; duplicate delivery double-charging or double-granting.

**Required negative test:** Replay one captured-and-resigned-as-invalid delivery; expect
rejection. Fetch another tenant's batch result ID; expect denial. Deliver a valid event twice;
expect single effect.

**Passing / Not verified:** Pass requires verification-plus-idempotency evidence plus all three
tests. Signature-mechanics depth: `secod-inputs-apis`; payment-consequential events also route
to `secod-payments-billing`.

**Related skill routing:** Input authenticity: `secod-inputs-apis`; payments: `secod-payments-
billing`; partial-failure recovery: `secod-failure-safety`.

### `PROVISIONAL-AI-11` — Safe usage, cost and prompt logging

**Applicability:** All AI request/response, token-usage and cost logging. Protected property:
operational visibility without new sensitive-data exposure.

**Inspect and verify:** Logs record usage metadata (tokens, model, latency, cost) without raw
secrets, bearer tokens, sensitive prompt bodies or private generated output unless explicitly
approved and minimized; log retention defined; redaction applied consistently across app logs and
AI-provider/gateway log streams.

**Unsafe evidence:** Full prompt/response bodies logged by default; provider/gateway payload
logging enabled for sensitive tenants with unknown retention; secrets interpolated into log lines.

**Required negative test:** Run one controlled AI request; inspect resulting logs for secret or
sensitive-body material; expect none.

**Passing / Not verified:** Pass requires redaction evidence plus the log inspection. Log
infrastructure/alerts: `secod-observability-response`; provider/gateway telemetry and payload-log
settings require matching Dashboard/API evidence and route to the owning provider/gateway skill.

## Exceptional and failure conditions

Fail-closed behavior required where applicable:

- Provider timeout or dependency failure: deny or degrade deliberately; never fall back outside
  the approved chain (AI-09) or grant unvalidated output (AI-07).
- Partial operations: failed generation, interrupted ingestion or interrupted deletion leaves a
  durable pending/rollback state; cleanup and reconciliation depth routes to `secod-failure-
  safety`; this skill verifies no orphaned provider-held data contradicts AI-06.
- Retry and cancellation: bounded per `secod-abuse-limits`/AI-02; cancelled streams stop provider
  spend where the provider supports cancellation, verified against official documentation.
- Session/token revocation: revoked users lose access to in-flight and future AI requests and
  their conversation/cache scopes.
- Webhook duplicate, replay, redelivery and failure: AI-10 holds under all four; a failed
  checker or incomplete test never counts as success.

Never invent provider retry schedules, delivery guarantees, retention periods, expiry windows,
plan availability, region availability or ZDR coverage.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

Conditional routes: detected provider integration to its provider skill (`secod-openai`,
`secod-anthropic`, `secod-google-genai`, `secod-xai-grok`, `secod-vercel-ai`,
`secod-cloudflare-workers-ai`, `secod-cloudflare-ai-gateway`, `secod-cloudflare-vectorize`);
limit/quota infrastructure to `secod-abuse-limits`; webhook authenticity depth to
`secod-inputs-apis`; payment-consequential AI outcomes to `secod-payments-billing`.

If a dependency or applicable route is missing, unresolved, malformed or incomplete: mark
affected controls `Not verified`, name the missing owner/evidence, never invent replacement
dependencies, never issue launch readiness.

## Evidence and status rules

Valid statuses only:

- `Do not ship`: provider key exposed to clients or unauthenticated proxy reachable (AI-01);
  cross-tenant retrieval or cache leak (AI-05); model output grants privileges without
  re-validation (AI-04).
- `Fix before launch`: missing spend/token/file limits on reachable paid flows (AI-02); missing
  webhook signature verification or result IDOR (AI-10); no moderation policy on user-facing
  generation (AI-08); client-selectable models/retention (AI-03); unsafe stream/structured
  rendering (AI-07).
- `Recommended hardening`: missing fallback-parity review (AI-09), incomplete deletion
  verification (AI-06), verbose-but-redacted logging gaps (AI-11), missing evaluation artifacts
  for model upgrades.
- `Passed with evidence`: control implemented server-side in every deployed environment class
  and its required negative test passed with retained evidence.
- `Not verified`: package-only presence, inferred configuration, inaccessible/stale/
  contradictory/snapshot-only sources, unsupported provider claims, incomplete or failed tests.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported or
failed evidence.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`, `verification`,
`limitations`, `source_refs`, `routed_skills`.

End the report with:

- Applicability inventory (features x environments, Candidate/Likely/Active)
- Test results including negative tests. For every item record `artifact_type`,
  `execution_status` (`not_executed`, `passed`, `failed`, or `blocked`), command/probe, target
  environment, time and retained evidence. Markdown plans always use `not_executed`.
- Requested external evidence (Dashboard/provider items not obtainable repository-only)
- `Not verified` items, each with affected controls and exact next verification step
- Launch blockers
- A `release_handoff` object with `verdict_owner: secod-ship-check`,
  `readiness_verdict: not_issued`, control statuses, blockers and requested external evidence

Route overall launch readiness to `secod-ship-check`. `readiness_verdict: not_issued` is an
explicit ownership boundary, not an omitted result. These evidence rules introduce no new status
or automatic release-blocker class; report applicable control statuses and blockers without
converting `Not verified` into a readiness verdict.

## Negative fixtures and tests

Fixture mapping (see `tests/insecure-fixtures/secod-ai-api-integrations/README.md`,
`tests/trigger-cases/secod-ai-api-integrations.md`,
`tests/expected-results/secod-ai-api-integrations.md`):

| Fixture case | Controls exercised | Executable? |
| --- | --- | --- |
| Clean app: server-side keys, allowlist, scoped RAG, validated streams | AI-01..11 pass paths | Documentation-only |
| Client-visible provider key or unauthenticated proxy | AI-01 | Documentation-only |
| Unbounded tokens/spend, client-selected model | AI-02, AI-03 | Documentation-only |
| Prompt-injection-driven privilege or cross-tenant retrieval/cache leak | AI-04, AI-05 | Documentation-only |
| Orphaned provider data after deletion; unknown retention posture | AI-06 | Documentation-only |
| Unsafe stream render or unvalidated structured output | AI-07 | Documentation-only |
| Missing moderation handling; unsigned provider webhook; result IDOR | AI-08, AI-10 | Documentation-only |
| Unreviewed fallback target | AI-09 | Documentation-only |
| Sensitive prompts in logs | AI-11 | Documentation-only |
| Missing-evidence case (integration present, provider settings unknown) | All | Documentation-only |

All target fixtures are Markdown plans; none are executable code. Label each one
`artifact_type: documentation_only` and `execution_status: not_executed`. Reading, reviewing or
reasoning through a plan is not execution. Never claim a Markdown fixture passed, failed or ran.
Safe local probes (unauthenticated request, malformed-output injection against a mocked/local
provider) may run against a locally started app or an explicitly authorized non-production
environment only; report them separately from fixture plans with command, target, time and retained
output. Never run destructive, production-changing, user-creating, payment-creating, refunding,
key-rotating, dashboard-changing or account-changing tests without explicit authorization.

## References

- Source register: `references/sources.md`.
- Review-time provider/Dashboard and client-token gates: `references/review-evidence.md`.
- Trigger case: `../../tests/trigger-cases/secod-ai-api-integrations.md`; expected result:
  `../../tests/expected-results/secod-ai-api-integrations.md`; fixture plan:
  `../../tests/insecure-fixtures/secod-ai-api-integrations/README.md`.
- Keep direct URLs, version notes and plan/region assumptions in `references/sources.md`.
