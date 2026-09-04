# Discovery and Routing Reference

## Table of contents

- [Purpose](#purpose)
- [Safe discovery method](#safe-discovery-method)
- [Framework and deployment signals](#framework-and-deployment-signals)
- [Identity, messaging, and job signals](#identity-messaging-and-job-signals)
- [Data, API, browser, and integration signals](#data-api-browser-and-integration-signals)
- [Cloudflare signals](#cloudflare-signals)
- [Cloud, data, payment, and AI routing](#cloud-data-payment-and-ai-routing)
- [Dependency closure](#dependency-closure)
- [Conflict and evidence rules](#conflict-and-evidence-rules)

## Purpose

Use this reference to build the application inventory required by `secod-core`. Treat file names, package names, configuration keys, and commands as discovery signals, not proof that a service is active or secure. Resolve every route against the live `secod/catalog.json`; this file does not override that catalog.

## Safe discovery method

1. Record repository roots and workspaces before searching. Include nested applications, infrastructure modules, workers, and packages.
2. List files with `rg --files`; exclude generated/vendor directories only when the repository or lockfile establishes that status.
3. Parse manifests and configuration structurally when practical. Search source for imports, initialization, reachable routes, and calls that corroborate package/configuration signals.
4. Search environment-variable **names**, never values. Prefer committed examples, schema validators, and source references such as `process.env.NAME`.
5. Correlate repository signals with supplied deployment artifacts or authorized read-only provider evidence.
6. Record each signal as `Active`, `Likely`, `Candidate`, `Conflicting`, or `Unknown`, with path/line and environment.

Illustrative read-only searches:

```powershell
rg --files -g "package.json" -g "*lock*" -g "next.config.*" -g "vercel.*" -g "wrangler.*"
rg --files -g "Dockerfile*" -g "compose.y*ml" -g "docker-compose.y*ml" -g "*.tf" -g "Chart.yaml" -g "*.yaml"
rg -n "@clerk/|@auth/|next-auth|auth0|workos|better-auth" --glob "!**/node_modules/**"
rg -n "process\.env\.[A-Z0-9_]+|import\.meta\.env\.[A-Z0-9_]+" --glob "!**/node_modules/**"
```

Do not search `.env` contents or echo environment values into logs. If a repository search errors or excludes an unreadable root, inventory the missing scope and mark completeness `Not verified`.

## Framework and deployment signals

### Next.js and React

Inspect:

- `package.json` plus the resolved lockfile entries for `next`, `react`, and `react-dom`;
- `next.config.js`, `.mjs`, `.ts`, or other supported project variants;
- `app/` and `src/app/` for layouts, pages, Route Handlers, Server Actions, metadata routes, and route groups;
- `pages/` and `src/pages/`, especially `pages/api/` and custom `_app`, `_document`, and `_error` files;
- `proxy.ts`/`.js` and legacy `middleware.ts`/`.js`, matchers, runtime selection, and rewrites/redirects;
- build/deployment artifacts that establish the deployed version and output mode.

Do not infer App Router use only from an `app/` directory; it may be unused, nested in a non-app package, or coexist with Pages Router. Do not infer the deployed version solely from a range in `package.json`. Route an active or likely Next.js application to `secod-nextjs`; add `secod-vercel-platform` only when Vercel signals are active or likely.

### Vercel

Inspect:

- `.vercel/project.json` for local project linkage, without publishing identifiers unnecessarily;
- one active project configuration: `vercel.json`, `vercel.ts`, or an officially supported variant;
- `.github/workflows/`, other CI configuration, `vercel` CLI scripts, and repository integration evidence;
- references to `VERCEL`, `VERCEL_ENV`, `VERCEL_URL`, `VERCEL_PROJECT_PRODUCTION_URL`, `VERCEL_GIT_*`, and OIDC token variable names;
- `functions`, `crons`, queue consumers/producers, runtime declarations, and generated preview/deployment URLs.

Repository configuration does not prove dashboard values, Git integration, project ownership, environment-variable scope, OIDC enablement, runtime version, or the active production deployment. Route those questions to `secod-vercel-platform`; inaccessible state is `Not verified`.

### Containers and infrastructure as code

Inspect:

- `Dockerfile*`, `.dockerignore`, build targets, base-image references, entrypoints, users, health checks, and exposed ports;
- canonical Compose files `compose.yaml`/`.yml` and legacy `docker-compose.yaml`/`.yml`, overrides, profiles, secrets, networks, volumes, health checks, and restart behavior;
- Kubernetes YAML/JSON, `kustomization.yaml`, workloads, Services, Ingress/Gateway, Jobs/CronJobs, RBAC, NetworkPolicy, secrets references, probes, security contexts, and namespaces;
- Helm `Chart.yaml`, `values*.yaml`, templates, dependencies, hooks, tests, and rendered-manifest evidence;
- Terraform/OpenTofu `.tf`, `.tf.json`, `.tfvars` naming, provider/backend configuration, modules, state location, plans, and CI identity;
- image registries, digests/tags, runtime configuration, orchestrator/dashboard evidence, and environment differences.

Route any active or likely container image/build/runtime to `secod-container`, then select exact platform/cloud adapters from the catalog. A Dockerfile alone is only a candidate until build or deployment evidence corroborates it.

## Identity, messaging, and job signals

### Identity and capability flows

Inventory login, logout, callback, session refresh, token exchange, account link/unlink, organization/tenant selection, invitation, recovery, magic-link, OTP, share-link, and capability-URL routes. Record credential type, storage location category, issuer, audience, subject, tenant, privilege transition, expiration/rotation owner, and revocation path without recording secret values.

Provider signals include:

- Clerk: `@clerk/*`, `clerkMiddleware`, `CLERK_*` names, webhook endpoints, Organizations use, JWT templates, session claims, and dashboard-supplied redirect/allowed-origin evidence;
- Auth0: Auth0 SDK imports/config, `AUTH0_*` names, callback/logout routes, Actions/Rules references, Organizations, APIs/audiences, and tenant evidence;
- WorkOS: WorkOS SDKs, `WORKOS_*` names, AuthKit/SSO/Directory Sync/Admin Portal/webhooks, organizations, and redirect URIs;
- Auth.js: `next-auth` or `@auth/*`, `auth.ts`, route handlers, providers, adapters, callbacks, and secret/database variable names;
- Better Auth: package/import/config, adapters, plugins, routes, cookie/session configuration, and secret/database variable names.

Route the applicable general identity/session/OAuth/JWT skills plus the exact provider adapter. Never use one provider's documented behavior for another provider.

### Messaging, webhooks, queues, and schedules

Inspect SDK imports and initialization, provider environment-variable names, route handlers, templates, callback/webhook endpoints, queue bindings, consumers, producers, Cron/schedule expressions, worker entrypoints, retry/DLQ code, idempotency stores, and reconciliation jobs.

Map:

- email, SMS, and notification flows to the relevant baseline and provider adapter;
- inbound webhooks to webhook/signature/replay controls and the exact provider adapter;
- queues, scheduled jobs, background tasks, workers, and DLQs to async/job controls and the hosting/provider adapter.

A handler in source proves an attack surface, not provider-side signature configuration, active delivery, retry policy, or disablement. Those remain `Not verified` without current provider evidence.

## Data, API, browser, and integration signals

Build an API and data-flow inventory from:

- OpenAPI/GraphQL/gRPC definitions, framework routes, RPC routers, server actions, webhooks, realtime channels, internal service endpoints, and provider callbacks;
- versioned directories/paths/hosts and references to deprecated, legacy, beta, preview, debug, mock, test, shadow, admin, or internal APIs;
- database clients, schemas, migrations, policies, row-level authorization, object stores, caches, analytics, logs, backups, exports, and deletion jobs;
- file inputs, multipart parsers, presigned URLs, media processing, document generation, download/export endpoints, and browser-rendering calls;
- `fetch`, HTTP clients, URL parsers, proxying, redirect following, link preview, import-by-URL, webhook dispatch, and other outbound requests;
- browser SDKs, iframes, postMessage, WebRTC, service workers, third-party scripts, payment UI, AI UI, and public runtime configuration.

For each flow record source, destination, protocol, authentication/capability, tenant boundary, data classes, region, retention/deletion owner, backup/recovery owner, and exceptional path. Route deeper checks to the general API/data/file/SSRF/browser skills plus exact adapters.

## Cloudflare signals

Inspect `wrangler.jsonc`, `wrangler.toml`, generated deploy configuration, package scripts, imports, bindings, compatibility date/flags, route/custom-domain definitions, and supplied dashboard/API evidence. Search for:

- account, zone, and API-token variable/reference **names**;
- Workers and Pages/Pages Functions entrypoints;
- Durable Object classes/migrations and namespace bindings;
- R2, D1, KV, service, dispatch, environment, and secrets bindings;
- Queues producers/consumers, DLQs, delivery delay, batch/retry settings, and HTTP pull consumers;
- Workflows definitions/bindings, retries, sleeps/waits, and instance controls;
- Hyperdrive, Vectorize, Workers AI, AI Gateway, and Browser Rendering bindings/calls;
- Access identity headers/tokens, Turnstile widgets/site keys and server-side verification calls, WAF/ruleset references, and routes/domains.

Route the family/profile skill and exact product adapters from the catalog. A Wrangler binding proves configured intent, not deployed existence, current dashboard policy, region, plan availability, data state, secret value, or secure control behavior.

## Cloud, data, payment, and AI routing

Resolve exact slugs from the catalog. Use these signals to select candidates, then corroborate activity.

- **Supabase:** `supabase/config.toml`, migrations/functions, `@supabase/*`, `SUPABASE_*` names, database URLs, auth/storage/realtime/edge-function calls, CLI or branch/deployment evidence.
- **Firebase:** `firebase.json`, `.firebaserc`, rules/index files, Functions source, Firebase SDKs, `FIREBASE_*` names, emulator/CLI scripts, and console/deployment evidence.
- **Neon/Convex:** provider SDKs and CLIs, project/config files, database/function schemas, provider variable names, branch/deployment evidence, and relevant auth/storage/integration use.
- **AWS:** SDK modules, CDK/SAM/CloudFormation/Terraform providers, ARNs, service-specific variable names, OIDC/workload identity, region/account evidence, and exact services such as Lambda, S3, SES, Cognito, Bedrock, or API Gateway.
- **Google Cloud:** client libraries, Firebase overlap, Terraform providers, service-account/workload identity references, project/region evidence, and exact services such as Storage, Tasks, Scheduler, IAM, or Vertex AI.
- **Payments:** provider SDK/imports, checkout/customer-portal routes, webhook handlers, price/product IDs, subscription/entitlement code, refunds/disputes, Connect/marketplace flows, and dashboard evidence. Route payment baseline plus exact Stripe, Polar, Lemon Squeezy, Dodo Payments, or Whop adapter.
- **AI:** provider SDK/imports, model identifiers, AI SDK use, streaming/tool/function calls, prompts, retrieval/vector stores, file inputs, agents, evals, moderation/safety settings, telemetry, provider keys by name, region/tier, and model maturity. Route AI baseline plus exact OpenAI, Anthropic, Gemini, xAI, or Vercel AI SDK adapter.

Package presence never proves that a provider handles production traffic. If multiple providers are present, route each active/likely one separately; do not assume compatible authentication, retention, regions, retries, or security controls.

## Dependency closure

Use the live catalog and retain reproducible inputs. Conceptual algorithm:

```text
closure = empty ordered set
active_stack = empty stack

visit(skill):
  if skill is in active_stack: report cycle(active_stack + skill); return failure
  if skill is already in closure: return success
  if skill is absent from catalog: report unknown slug; return failure
  push skill onto active_stack
  for dependency in catalog[skill].dependencies: visit(dependency)
  pop skill from active_stack
  add skill to closure
```

Start from every directly applicable skill, not from `secod-core` alone. Store the catalog path/hash, direct selections, dependency edges, closure order, cycles, unknown slugs, missing skill directories, and load failures. Continue independent branches after a branch failure, but mark all affected coverage `Not verified`.

Do not silently repair a cycle, remove a suspicious edge, infer a dependency from prose, or replace a missing adapter. Propose catalog changes separately for maintainer approval.

## Conflict and evidence rules

- Repository evidence and dashboard/deployment evidence must be scoped by environment and time. A current production artifact overrides a stale repository assumption only for the behavior it directly proves.
- When current sources use a new term but repositories may use a legacy term, search both. For example, current Next.js documentation calls the request-boundary feature Proxy while older applications may contain Middleware.
- Configuration redirect/generated files may alter the effective source. Follow only documented local indirection and record both origin and effective file.
- Plan/tier, region, preview/beta/GA state, and runtime version are properties to verify, not defaults to assume.
- An unavailable dashboard is not evidence that a feature is off. A missing import is not evidence that a service is unused when calls are generated or external.
- For every unresolved conflict, state which controls are affected, the evidence needed, the routed owner, and why status remains `Not verified`.
