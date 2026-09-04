---
name: secod-core
description: Inventory the application, classify every framework/provider/integration signal as Candidate/Likely/Active, compute the complete transitive skill dependency closure from the live catalog, route every applicable baseline skill and conditional adapter, and generate the Security Plan; routing is never proof that a control passed. Triggers include any repository review request, package.json/lockfile/next.config/wrangler/dockerfile/IaC detection, auth or payment or AI SDK imports, provider environment-variable names, webhook routes, queue/cron workers, and CI/deployment configuration; package presence alone is Candidate.
---

# SECOD Core Security

## Mission

Build the authoritative application inventory, compute the transitive skill dependency closure
against the live catalog, route every applicable baseline skill and conditional adapter, and
produce the Security Plan that downstream skills execute against.

Repository-only review cannot prove deployed behavior, provider-side configuration, dashboard
settings, active traffic, or any control outcome. It establishes attack-surface candidates and
routing only. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: safe repository discovery; signal classification (`Candidate`, `Likely`,
`Active`, `Conflicting`, `Unknown`) scoped by environment; framework, deployment, identity,
messaging, job, data, API, browser, integration, shell/subprocess/template-engine, cloud,
payment, and AI signal detection; dependency-closure validation including cycle and
unknown-slug handling; missing-skill detection; Security Plan generation; `secod-ship-check`
routing; provider reference discovery through official `llms.txt`/`llms-full.txt` indexes.

Excluded controls (owned elsewhere): credential/session/token validation and authorization
(`secod-identity-access`); injection, SSRF, webhook authenticity, GraphQL/WebSocket boundaries
(`secod-inputs-apis`); command/argument/template/code-injection defenses
(`secod-runtime-execution`); secret values, rotation, history rewriting, default credentials
(`secod-secrets-config`); XSS/CSP/CORS/cookies/browser storage (`secod-web-app-security`);
upload/storage content controls (`secod-data-files`); rate limits/idempotency/replay
(`secod-abuse-limits`); crypto choices and retention (`secod-crypto-data-protection`);
dependency advisories and CI pinning enforcement (`secod-packages-delivery`,
`secod-vulnerability-management`); audit/alert/backup evidence (`secod-observability-response`);
payment state machines (`secod-payments-billing` plus adapters); AI context isolation
(`secod-ai-api-integrations` plus adapters); container hardening details
(`secod-container-runtime`); launch verdicts (`secod-ship-check`).

Direct dependencies: none.

Conditional routes: every baseline skill in `recommendedBaseline`, plus every conditional
adapter resolved from the live `references/catalog.json` at review time — Next.js and Vercel
platform; auth providers via `secod-auth-provider-integrations`; Supabase, Neon, Convex,
Firebase; AWS and Google Cloud families with their account/IAM routers; Cloudflare family
with its account/zone router; OpenAI, Anthropic, Gemini, xAI, Vercel AI SDK; Stripe, Polar,
Lemon Squeezy, Dodo Payments, Whop. Never hardcode assumptions about catalog membership here;
resolve exact slugs from the catalog.

## Required inputs

Repository inputs: full file tree including nested workspaces/packages; manifests and lockfiles;
framework/provider configuration files; source for imports, routes, initialization; CI workflows
and deployment definitions; infrastructure-as-code; committed example environment schemas.

Environment-variable **names** only, never values.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
deployed versions and build outputs; dashboard/project/tenant/zone/account settings; Git
integration status; OIDC enablement; environment-variable scope and values per environment;
provider-side webhook endpoint status and delivery logs; plan/tier/region; production data
state; preview URL protection status.

Human-supplied evidence: authorized read-only dashboard/API exports, deployment logs, and
environment inventories covering development, preview, staging, and production separately.

## Applicability and discovery

Always applicable: this skill runs first on every review.

Signal groups:

- Package/SDK: manifest dependencies, lockfile-resolved versions, imports, initialization calls.
- Environment variables: names referenced in code, config, examples, and schema validators.
- Routes/webhooks: HTTP handlers, Server Actions, proxy/middleware files, callback/logout/
  webhook paths, cron/schedule entries, queue consumers/producers, worker entrypoints.
- Configuration: framework configs, provider configs, IaC, CI pipelines, wrangler/compose/
  Kubernetes/Helm/Terraform definitions.
- Deployment/provider evidence: `.vercel/project.json`, generated URLs, build artifacts,
  authorized dashboard/API evidence.

Classification:

- `Candidate`: package present, example variable name, dormant file, or weak signal only; no
  corroborating use.
- `Likely`: code/configuration exists and correlates with use, but deployed/provider state is
  unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API,
  or other provider evidence.

Record every signal with path/line, evidence class, and environment. Maintain separate
inventories for development, preview, staging, and production. Conflicting or shared
environment signals are classified `Conflicting` and force affected controls to `Not verified`.
Discovery commands, per-family signals, the closure algorithm, and conflict rules live in
[`references/discovery-routing.md`](discovery-routing.md).

## Review workflow

1. Inventory environments and trust boundaries: repo roots, workspaces, environments, deploy
   targets. Parallelizable across roots when strictly read-only.
2. Correlate active features and flows: classify every signal; build flow records (source,
   destination, protocol, authentication/capability, tenant boundary, data classes, exceptional
   path). Parallelizable per root after step 1 completes there.
3. Verify the controls below and resolve conditional routes from the live catalog.
4. Run safe negative tests: classification and closure checks are local/read-only; no provider
   or dashboard calls from this skill.
5. Classify evidence, emit findings, route each finding to its owner, hand off aggregated
   applicability inventory to `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-core-N` and require catalog approval before promotion.

### `PROVISIONAL-core-1` — Complete repository inventory

**Applicability:** Every review. Protects against unreviewed code paths silently lacking coverage.

**Inspect and verify:** Enumerate repo roots, workspaces, nested applications, workers, and
packages before searching (`rg --files` per root). Parse manifests/config structurally where
practical. Record unreadable/excluded/erroring scopes as incomplete. Search env-var names, never
values; never read `.env` contents.

**Unsafe evidence:** Skipped or unreadable roots not recorded; generated/vendor exclusions not
justified by lockfile/repo evidence; env values captured anywhere in output.

**Required negative test:** Fixture with an unreadable root or search timeout must produce an
inventory gap record naming the missing scope, never a clean pass.

**Passing / Not verified:** Pass requires complete recorded tree coverage of all discovered
roots with method noted. Any inaccessible scope, failed search, or cancelled enumeration keeps
inventory completeness `Not verified`.

**Related skill routing:** Gaps in specific families route to the owning adapter once resolved;
global gaps go to `secod-ship-check`.

### `PROVISIONAL-core-2` — Signal classification and environment separation

**Applicability:** Every detected framework/provider/integration signal.

**Inspect and verify:** Assign `Candidate`/`Likely`/`Active` per the definitions above with
path/line and environment. Keep development/preview/staging/production inventories separate.
Search legacy and current terminology together (Next.js `middleware.ts` deprecated, renamed
`proxy.ts` with Node runtime default in v16).

**Unsafe evidence:** Package presence reported as active use; one provider's documented behavior
applied to another; merged cross-environment inventories.

**Required negative test:** Manifest-only `@clerk/nextjs` fixture must classify `Candidate`,
never `Active` or secure.

**Passing / Not verified:** Pass requires every signal classified with cited evidence. Signals
lacking corroborating use stay `Candidate`. Conflicting classifications keep affected controls
`Not verified`.

**Related skill routing:** Deep verification of every non-Candidate signal routes to its owning
skill below.

### `PROVISIONAL-core-3` — Framework and deployment detection

**Applicability:** Web frameworks, hosting platforms, containers, IaC.

**Inspect and verify:** Next.js/React versions from lockfiles (not ranges), App versus Pages
Router, `proxy.ts`/legacy `middleware.ts`, Route Handlers, Server Actions; Vercel linkage,
config, CI integration, `VERCEL_*` names, Functions/Crons/Queues; Dockerfile/Compose/Kubernetes/
Helm/Terraform signals with build/deploy corroboration. Route active/Likely matches:
`secod-nextjs`, `secod-vercel-platform` (only when Vercel signals are Active/Likely),
`secod-container-runtime`.

**Unsafe evidence:** App Router inferred solely from an `app/` directory; deployed version
inferred from a range; Dockerfile alone treated as deployed runtime.

**Required negative test:** Lockfile-versus-production-artifact version conflict must classify
`Conflicting`, route `secod-nextjs`, and block launch coverage until reconciled.

**Passing / Not verified:** Pass requires versions pinned by lockfile evidence plus router/build
corroboration. Dashboard/Git-integration/runtime questions without supplied evidence remain
`Not verified` and route to `secod-vercel-platform`.

**Related skill routing:** `secod-nextjs`, `secod-vercel-platform`, `secod-container-runtime`.

### `PROVISIONAL-core-4` — Identity, messaging, and job flow inventory

**Applicability:** Authentication/session/OAuth/share-link flows; email/SMS/notification flows;
webhooks; queues, cron, scheduled/background jobs, workers.

**Inspect and verify:** Inventory login/logout/callback/refresh/exchange/link/unlink/
organization-selection/invitation/recovery/magic-link/OTP/share-link routes with credential
type, storage category, issuer/audience/subject names, privilege transitions, expiry owner,
revocation path — never secret values. Map provider SDK signals (Clerk `@clerk/*` +
`clerkMiddleware` + `CLERK_*`, Auth0 SDK + `AUTH0_*`, WorkOS SDKs + `WORKOS_*`, Auth.js,
Better Auth) to the exact adapter. Record webhook endpoints, queue bindings/consumers/producers,
schedule expressions, worker entrypoints, retry/DLQ code, idempotency stores.

**Unsafe evidence:** A source-level handler claimed to prove provider-side signature config,
active delivery, retry policy, or endpoint enablement.

**Required negative test:** Webhook route fixture without provider evidence must route
signature/replay controls as `Not verified`, owned by `secod-inputs-apis` plus the provider
adapter.

**Passing / Not verified:** Pass requires every flow inventoried with classification and named
route target. Provider-side state stays `Not verified` without current authorized evidence.

**Related skill routing:** `secod-identity-access`, `secod-auth-provider-integrations` plus the
exact auth adapter, `secod-email-messaging`, `secod-inputs-apis`, `secod-abuse-limits`,
hosting adapters for queues/cron/workers.

### `PROVISIONAL-core-5` — Data, API, browser, integration, and execution-surface inventory

**Applicability:** API surfaces, data stores, file/export flows, browser surfaces, outbound
requests, OS/shell/subprocess/template-engine/dynamic-evaluation surfaces.

**Inspect and verify:** Build the API/data inventory from OpenAPI/GraphQL/gRPC definitions,
framework routes, RPC routers, Server Actions, realtime channels, internal endpoints, provider
callbacks; include versioned paths and any deprecated/legacy/beta/debug/mock/test/shadow/admin/
internal surface. Record database clients/schemas/policies, object stores, caches, backups,
exports, deletion jobs; multipart/file inputs, presigned URLs, rendering calls; browser SDKs,
iframes, postMessage, service workers, third-party scripts; every outbound `fetch`/HTTP-client
path. Detect child-process APIs (`exec`, `spawn`, `execFile`, `system`, equivalents), template
engines rendering user-influenced sources, dynamic evaluation constructs, LDAP/XPath queries.
For each flow record source, destination, protocol, authentication/capability, tenant boundary,
data classes, region, retention/deletion owner, backup/recovery owner, exceptional path.

**Unsafe evidence:** Debug/admin/internal surfaces omitted from the plan; undocumented export
contents treated as non-sensitive; execution-surface presence ignored because "unused".

**Required negative test:** Admin-export fixture with undocumented contents must classify the
flow `Unknown`, route `secod-crypto-data-protection` review, and prevent launch readiness until
authorized evidence reclassifies it.

**Passing / Not verified:** Pass requires a recorded inventory entry for every discovered flow
and surface with classification and route targets. Data-class uncertainty keeps affected flows
`Not verified`.

**Related skill routing:** `secod-inputs-apis`, `secod-runtime-execution`,
`secod-data-files`, `secod-web-app-security`, `secod-identity-access`,
`secod-crypto-data-protection`, `secod-abuse-limits`, `secod-threat-model`.

### `PROVISIONAL-core-6` — Cloud, payment, and AI adapter routing

**Applicability:** Supabase, Firebase, Neon, Convex; AWS and Google Cloud families;
Cloudflare family; payment providers; AI providers.

**Inspect and verify:** Apply the per-family signal lists in
[`references/discovery-routing.md`](discovery-routing.md): Supabase config/migrations/SDK/`SUPABASE_*`;
Firebase config/rules/SDK/`FIREBASE_*`; AWS SDK modules/IaC providers/ARNs/service variables;
Google Cloud client libraries/Terraform/service references; Cloudflare wrangler configs/bindings/product
profiles; payment SDK/checkout/webhook/
entitlement code; AI SDK/model identifiers/streaming/retrieval/vector stores/agents. Route each
Active/Likely family to its router skill and exact product adapters from the live catalog.
Multiple present providers are routed independently — never assume compatible authentication,
retention, regions, retries, or controls across them.

**Unsafe evidence:** Wrangler binding or SDK import treated as deployed existence, dashboard
policy, plan availability, or secure control behavior; one family's router skipped because
another was reviewed.

**Required negative test:** Payment SDK import without checkout/webhook routes stays `Likely`
at most and still routes `secod-payments-billing`; AI SDK import routes
`secod-ai-api-integrations` plus the exact model-provider adapter even without deployed keys.

**Passing / Not verified:** Pass requires each Active/Likely family mapped to its exact catalog
slugs. Package-only signals stay `Candidate` but are still listed in the Security Plan with
their conditional route.

**Related skill routing:** Family routers (`secod-supabase`, `secod-firebase`, `secod-neon`,
`secod-convex`, `secod-aws-web`, `secod-google-cloud-web`,
`secod-cloudflare`) and product adapters; `secod-auth-provider-integrations`;
`secod-payments-billing` plus Stripe/Polar/Lemon Squeezy/Dodo Payments/Whop adapters;
`secod-ai-api-integrations` plus OpenAI/Anthropic/Gemini/xAI/Vercel AI SDK adapters;
`secod-vercel-ai` when AI Gateway/AI SDK signals exist.

### `PROVISIONAL-core-7` — Dependency-closure validation

**Applicability:** Every direct selection and its full transitive closure before any review
verdict downstream.

**Inspect and verify:** Compute closure from every directly applicable skill using the algorithm
in [`references/discovery-routing.md`](discovery-routing.md) against the live catalog: detect
cycles, unknown slugs, missing skill directories, load failures. Retain catalog path/hash,
direct selections, dependency edges, closure order, and failures. Continue independent branches
after a branch failure; mark all affected coverage `Not verified`. Never silently repair a
cycle, drop a suspicious edge, infer dependencies from prose, or substitute a missing adapter;
propose catalog changes separately for maintainer approval.

**Unsafe evidence:** Closure computed from memory of a previous run; missing dependency ignored
because the parent skill loaded; cycle broken by deleting an edge.

**Required negative test:** Fixtures `a -> b -> a` and `x -> unknown` must terminate both
branches, report the cycle and the unknown slug by name, keep unrelated branches green, mark
affected controls `Not verified`, and prohibit launch readiness.

**Passing / Not verified:** Pass requires a complete acyclic closure over the current catalog
with retained edges. Any missing/unresolvable node keeps affected coverage `Not verified`.

**Related skill routing:** `secod-ship-check` consumes the closure result and blocks on gaps.

### `PROVISIONAL-core-8` — Routing is not proof

**Applicability:** Every emitted route and the final handoff.

**Inspect and verify:** Emit findings per control with status, then produce the Security Plan:
applicability inventory, signal classifications, closure result, routed owners, outstanding
external-evidence requests. Hand off to `secod-ship-check`. A routed control remains unevaluated
until its owning skill returns evidence; report it `Not verified` in this skill's output.

**Unsafe evidence:** Launch-readiness language anywhere in core output; routing recorded as a
pass; Security Plan omitting Candidate signals.

**Required negative test:** Active Next.js fixture routed to `secod-nextjs` must show Next.js
controls `Not verified` at core completion.

**Passing / Not verified:** Not applicable — this control gates output shape. Violations are
process failures (`Do not ship` for the core artifact).

**Related skill routing:** `secod-ship-check` owns the verdict.

## Exceptional and failure conditions

- Discovery/search timeout, cancelled search, unreadable root, or skill-load error: record the
  mechanism failure, searched scope, partial evidence, limitation, and next verification step.
  Never emit `Passed with evidence` from partial runs.
- Partial inventory after interruption: keep completed branches, mark incomplete scopes
  `Not verified`, name what rerunning would cover.
- Catalog unavailability or malformed entries: treat every closure-dependent control as
  `Not verified`; do not reconstruct dependencies from prose.
- Conflicting repository versus deployment/provider evidence: record both with scope and time,
  classify `Conflicting`, name the reconciling owner, block affected coverage until resolved.
- Revocation/webhook/runtime events are not observable by this skill; they belong to routed
  owners (`secod-inputs-apis`, `secod-observability-response`, hosting adapters).
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `references/catalog.json`): none.

Conditional routes: resolve at review time from the live catalog — all baseline skills in
`recommendedBaseline` plus applicable adapters per `PROVISIONAL-core-3` through
`PROVISIONAL-core-6`. When an applicable dependency, route, or adapter skill is absent,
unresolved, malformed, or fails to load: mark affected controls `Not verified`, name the missing
owner or evidence, never invent replacement dependencies, never issue or imply launch readiness.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: complete inventory, every signal classified with cited path/line and
  environment, closure complete and acyclic over the live catalog, routes resolved to existing
  skills.
- `Fix before launch`: inventory or closure defects that leave known attack surfaces unrouted;
  conflicting classifications on security-relevant versions/signals.
- `Recommended hardening`: Candidate-only signals left unmonitored; legacy/current terminology
  mismatches worth cleanup.
- `Not verified`: inaccessible roots, failed searches, unresolved conflicts, unavailable
  catalogs, missing adapter skills, snapshot-only documentation.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (signals by class and environment); test results;
requested external evidence (dashboard/API exports needed, by owner); `Not verified` items with
the next verification step; launch blockers. Route overall launch readiness to
`secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-core/README.md` | Documentation-only plan | PROVISIONAL-core-1, -2, -7 |
| Manifest-only Clerk package | Documentation-only case | PROVISIONAL-core-2 (Candidate discipline) |
| Lockfile vs production version conflict | Documentation-only case | PROVISIONAL-core-3 (Conflicting) |
| Cycle `a -> b -> a`, unknown `x -> unknown` | Documentation-only case | PROVISIONAL-core-7 |
| Source-timeout / unreadable-root mechanism failure | Documentation-only case | PROVISIONAL-core-1 (never pass partial) |
| Admin export with undocumented contents | Documentation-only case | PROVISIONAL-core-5 (Unknown data class) |
| Routed Next.js app before adapter execution | Behavior case | PROVISIONAL-core-8 (routing is not proof) |

Safe local commands: read-only `rg` searches per [`references/discovery-routing.md`](discovery-routing.md).
Never claim Markdown fixture plans executed as code. Never run destructive, production-changing,
user-creating, payment-creating, refunding, key-rotating, dashboard-changing, or
account-changing tests without explicit authorization.

## References

- [`references/discovery-routing.md`](discovery-routing.md) — safe discovery commands, per-family
  signal lists, closure algorithm, conflict and evidence rules.
- [`references/sources.md`](sources.md) — source register and review-expiry tracking.
