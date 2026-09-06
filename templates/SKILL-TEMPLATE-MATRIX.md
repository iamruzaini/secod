# SECOD skill-to-template matrix

This matrix assigns every current SECOD skill—and the three planned mobile additions in the PRD—to an implementation-first template. It is a migration plan, not a promise that every current skill should retain its present name or scope.

## Current catalog

| Skill | Assigned template | Migration focus |
|---|---|---|
| `secod-core` | Core router | Detect the feature stack and activate the smallest applicable skill closure. |
| `secod-threat-model` | Generalized | Turn feature data flows into concrete trust-boundary and abuse-resistant design decisions. |
| `secod-identity-access` | Generalized | Implement authentication, server-side authorization, ownership, roles, sessions, and tenant isolation. |
| `secod-web-app-security` | Generalized | Implement browser/web defaults: origin boundaries, cookies, CSRF, XSS defenses, headers, and navigation safety. |
| `secod-inputs-apis` | Generalized | Implement request schemas, normalization, authorization placement, webhook boundaries, and safe responses. |
| `secod-runtime-execution` | Generalized | Implement safe process execution, sandboxing, path/argument handling, SSRF defenses, and resource limits. |
| `secod-crypto-data-protection` | Generalized | Choose supported cryptographic primitives, key boundaries, encryption, hashing, rotation, and migration patterns. |
| `secod-data-files` | Generalized | Implement upload validation, object authorization, private delivery, retention, deletion, and content handling. |
| `secod-abuse-limits` | Generalized | Implement identity-aware rate, quota, concurrency, payload, and cost limits with safe degradation. |
| `secod-secrets-config` | Generalized | Keep secrets out of clients/source, validate configuration, rotate credentials, and fail safely. |
| `secod-packages-delivery` | Generalized | Implement dependency, build, artifact, release, and CI defaults that reduce supply-chain risk. |
| `secod-vulnerability-management` | Generalized | Reframe from scanning to safe dependency/remediation implementation during package changes. |
| `secod-observability-response` | Generalized | Add privacy-aware logs, audit events, metrics, alerts, correlation, and actionable failure telemetry. |
| `secod-payments-billing` | Generalized | Implement authoritative billing state, webhook verification, idempotency, entitlement reconciliation, and safe money handling. |
| `secod-ai-api-integrations` | Generalized | Implement prompt/data boundaries, output validation, tool authorization, retrieval isolation, and cost controls. |
| `secod-container-runtime` | Generalized | Implement least-privileged images, runtime identities, filesystem/network constraints, health, and shutdown behavior. |
| `secod-email-messaging` | Generalized | Implement trusted templates, address/content validation, unsubscribe/consent, webhook handling, and data minimization. |
| `secod-failure-safety` | Generalized | Implement bounded retries, idempotency, rollback, compensation, reconciliation, and safe partial failure. |
| `secod-ship-check` | Task completion | Check only the changed feature's implementation and test evidence before handoff; never certify the app. |
| `secod-supabase-auth` | Provider feature | Implement Supabase Auth sessions, server/client boundaries, authorization integration, and secure redirects. |
| `secod-auth0` | Provider feature | Implement Auth0 flows, token validation, sessions, organizations/tenants, actions, and logout safely. |
| `secod-workos` | Provider feature | Implement WorkOS authentication, organizations, directory/webhook flows, and tenant mapping safely. |
| `secod-better-auth` | Provider feature | Implement Better Auth sessions, adapters, cookies, plugins, and trusted callbacks using supported APIs. |
| `secod-nextjs` | Framework | Implement secure App/Pages Router, server/client boundaries, route handlers, actions, middleware, caching, and headers. |
| `secod-vercel-platform` | Provider feature | Implement Vercel environment, runtime, deployment, preview, cache, function, and protection settings needed by code. |
| `secod-auth-provider-integrations` | Provider family | Route identity-provider tasks to the exact adapter and apply shared OAuth/OIDC/session defaults. |
| `secod-clerk` | Provider feature | Implement Clerk middleware/helpers, server authorization, organizations, sessions, and webhooks safely. |
| `secod-cloudflare` | Provider family | Route Cloudflare product use and apply shared account, token, binding, observability, and edge-runtime defaults. |
| `secod-cloudflare-workers` | Provider feature | Implement Worker request boundaries, bindings, secrets, outbound requests, limits, and failure behavior. |
| `secod-cloudflare-pages` | Provider feature | Implement Pages/Functions deployment, environment, headers, previews, and server/client boundaries. |
| `secod-cloudflare-queues` | Provider feature | Implement producers/consumers, batching, retries, deduplication, dead letters, and idempotent processing. |
| `secod-cloudflare-workflows` | Provider feature | Implement durable steps, retries, state, idempotency, compensation, and cancellation. |
| `secod-cloudflare-hyperdrive` | Provider feature | Implement database credentials, connection use, query boundaries, pooling, and failure behavior. |
| `secod-cloudflare-vectorize` | Provider feature | Implement tenant-isolated indexes/metadata, validated queries, safe ingestion, deletion, and retrieval. |
| `secod-cloudflare-workers-ai` | Provider feature | Implement model calls, inputs/outputs, bindings, tool boundaries, limits, and sensitive-data handling. |
| `secod-cloudflare-ai-gateway` | Provider feature | Implement gateway credentials, routing, caching, logging, fallbacks, and provider/model boundaries. |
| `secod-supabase` | Provider feature | Implement database/RLS, service-role boundaries, storage, functions, realtime, and tenant isolation. |
| `secod-firebase` | Provider feature | Implement Auth, Security Rules, Admin SDK boundaries, App Check integration, storage, functions, and emulator tests. |
| `secod-neon` | Provider feature | Implement connection credentials, pooling/serverless drivers, roles, branching, migrations, and tenant-safe queries. |
| `secod-convex` | Provider feature | Implement authenticated functions, argument/return validation, authorization, indexes, actions, and scheduled work. |
| `secod-aws-web` | Provider family | Route AWS products and apply shared IAM, workload identity, region, logging, retry, and data defaults. |
| `secod-aws-lambda-api-gateway` | Provider feature | Implement API authorization, event validation, Lambda permissions, timeouts, concurrency, retries, and responses. |
| `secod-aws-cognito` | Provider feature | Implement user/app clients, token verification, groups/claims, hosted flows, triggers, and logout/revocation. |
| `secod-aws-s3-cloudfront` | Provider feature | Implement private objects, scoped keys, signed delivery, upload validation, origins, caching, and deletion. |
| `secod-aws-data-services` | Provider feature | Implement least-privileged database access, tenant keys/conditions, encryption, consistency, retries, and backups. |
| `secod-google-cloud-web` | Provider family | Route Google Cloud products and apply shared IAM, service identity, project, region, telemetry, and quota defaults. |
| `secod-google-cloud-storage` | Provider feature | Implement private buckets/objects, IAM, signed operations, upload constraints, delivery, retention, and deletion. |
| `secod-stripe` | Provider feature | Implement Checkout/PaymentIntents/subscriptions, verified webhooks, idempotency, authoritative prices, and reconciliation. |
| `secod-polar` | Provider feature | Implement Polar checkout, subscriptions, benefits, webhook verification, idempotency, and entitlement state. |
| `secod-lemonsqueezy` | Provider feature | Implement Lemon Squeezy checkout, variants, subscriptions, signed webhooks, and entitlement reconciliation. |
| `secod-dodo-payments` | Provider feature | Implement Dodo Payments checkout, product/price authority, webhook verification, retries, and entitlement state. |
| `secod-whop` | Provider feature | Implement Whop access/products, authorization, webhook verification, membership state, and revocation. |
| `secod-openai` | Provider feature | Implement OpenAI server-side calls, key handling, structured outputs, tool authorization, files/data, and cost controls. |
| `secod-anthropic` | Provider feature | Implement Anthropic server-side calls, key handling, tool use, output validation, data boundaries, and limits. |
| `secod-google-genai` | Provider feature | Implement Google GenAI/Gemini calls, credentials, structured output, tools, files/data, and quota controls. |
| `secod-xai-grok` | Provider feature | Implement xAI/Grok calls, credentials, tools, output validation, data handling, and limits using supported APIs. |
| `secod-vercel-ai` | Provider feature | Implement Vercel AI SDK providers, streaming, tools, structured output, server/client boundaries, and telemetry safely. |

## Planned mobile catalog additions

| Skill | Assigned template | Migration focus |
|---|---|---|
| `secod-mobile-app-security` | Mobile | Portable mobile device/backend, credential, storage, links, permissions, privacy, and release defaults. |
| `secod-react-native-expo` | Mobile | React Native/Expo secure storage, linking, native modules, builds, updates, networking, and backend boundaries. |
| `secod-flutter` | Mobile | Flutter/Dart secure storage, navigation/links, platform channels, builds, networking, and backend boundaries. |

## Migration order

1. Prove routing with `secod-core`.
2. Convert foundational generalized skills used by most features.
3. Convert `secod-nextjs` and representative identity, data, payment, and AI provider adapters.
4. Update behavior tests and validators to enforce implementation-first output.
5. Convert provider families and remaining product adapters.
6. Add mobile skills with executable sample coverage.
7. Reassess names and boundaries; merge or split skills when that improves activation precision.

The catalog count may change. Coverage quality, routing precision, safe code, and useful tests matter more than preserving 57 as a permanent number.
