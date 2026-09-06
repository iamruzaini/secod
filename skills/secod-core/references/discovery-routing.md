# Feature discovery and skill routing

Use this reference only when `secod-core` must select skills for a coding task. Resolve names and
dependencies from `catalog.json`; this document supplies decision rules, not a second catalog.

## Discover current task

Start from requested behavior. Inspect only relevant repository areas:

```powershell
rg --files -g "package.json" -g "*lock*" -g "*.csproj" -g "pyproject.toml" -g "go.mod" -g "pubspec.yaml"
rg --files -g "next.config.*" -g "vercel.*" -g "firebase.json" -g ".firebaserc" -g "wrangler.*" -g "Dockerfile*" -g "*.tf"
rg -n "process\.env\.[A-Z0-9_]+|import\.meta\.env\.[A-Z0-9_]+" --glob "!**/node_modules/**"
```

Adapt searches to repository language and structure. Search environment-variable names, never
values. Do not read `.env` files merely to route skills.

Record feature, acceptance behavior, relevant app root, stack and resolved versions, provider
products, trust boundaries, data classes, likely changed files, and nearby tests.

## Select generalized skills

Select only rows whose boundary current work crosses.

| Feature or boundary | Select |
|---|---|
| New high-impact flow, multiple trust boundaries, unclear attacker path | `secod-threat-model` |
| Authentication, sessions, roles, ownership, tenants, admin actions | `secod-identity-access` |
| Browser rendering, cookies, origins, CSP, embedded content | `secod-web-app-security` |
| API input, server actions, webhooks, realtime, outbound URLs | `secod-inputs-apis` |
| Processes, shells, templates, dynamic execution, user-controlled paths | `secod-runtime-execution` |
| Encryption, hashing, tokens, keys, retention, deletion | `secod-crypto-data-protection` |
| Uploads, downloads, objects, exports, media/document processing | `secod-data-files` |
| Rate, quota, concurrency, replay, expensive operations | `secod-abuse-limits` |
| Credentials, environment configuration, secret scope or rotation | `secod-secrets-config` |
| Dependency, CI, build, artifact, or release changes | `secod-packages-delivery` |
| Vulnerable dependency remediation or security update policy | `secod-vulnerability-management` |
| Security events, redacted logs, alerts, recovery telemetry | `secod-observability-response` |
| Checkout, billing, subscription, entitlement, refund, dispute | `secod-payments-billing` |
| Model calls, prompts, retrieval, embeddings, tools, AI streaming | `secod-ai-api-integrations` |
| Container image, orchestrator, runtime identity, container network | `secod-container-runtime` |
| Email, SMS, OTP, invitations, magic links, notifications | `secod-email-messaging` |
| Retry, timeout, partial mutation, compensation, cleanup | `secod-failure-safety` |
| Explicit current-feature completion check | `secod-ship-check` |

Do not use `recommendedBaseline` as an unconditional selection list.

## Select framework and provider skills

Select a framework/provider when explicitly requested or when reachable task-relevant code or
configuration demonstrates use. Package-only or dormant examples are Possible signals, not
automatic activation.

| Signal | Select |
|---|---|
| Native Android/iOS feature or framework-agnostic mobile boundary | `secod-mobile-app-security` |
| React Native, Expo, Expo Router, EAS, or `expo-*` mobile module | `secod-react-native-expo` plus mobile baseline |
| Flutter mobile target, Dart mobile plugin, Android/iOS Flutter runner | `secod-flutter` plus mobile baseline |
| Next.js routes, actions, rendering, middleware/proxy, or configuration | `secod-nextjs` |
| Vercel runtime, deployment, environment, cache, functions, or protection | `secod-vercel-platform` |
| Clerk, Auth0, WorkOS, Better Auth, or Supabase Auth | `secod-auth-provider-integrations` plus exact adapter |
| Supabase database, Storage, Realtime, Functions | `secod-supabase` |
| Firebase Auth, Firestore, Storage, Functions, Rules, App Check | `secod-firebase` |
| Neon or Convex APIs | exact Neon or Convex adapter |
| AWS product | `secod-aws-web` plus exact AWS product adapter |
| Google Cloud product | `secod-google-cloud-web` plus exact product adapter |
| Cloudflare product | `secod-cloudflare` plus exact product adapter |
| Stripe, Polar, Lemon Squeezy, Dodo Payments, Whop | payment baseline plus exact adapter |
| OpenAI, Anthropic, Gemini, xAI, Vercel AI SDK | AI baseline plus exact adapter |

For Firebase, do not also select Google Cloud family skills unless task uses a separate Google
Cloud product or IAM boundary owned by those skills. For Vercel AI SDK, select exact underlying
model-provider adapter too when provider-specific API behavior is in scope.

## Resolve versions

Prefer lockfile-resolved version, then imported API plus manifest constraint, explicit
configuration, manifest constraint alone, then user-supplied target. If version remains unknown
and API choice differs materially, ask one focused question. Otherwise record narrow assumption.

## Compute dependency closure

Use catalog edges exactly:

```text
visit(skill):
  reject skill when absent from catalog
  reject current branch when skill already exists in active stack
  return when skill already exists in ordered result
  push skill onto active stack
  visit each declared dependency
  pop skill from active stack
  append skill to ordered result
```

Start with every directly selected skill. Continue independent roots after one branch fails.
Never invent, drop, or infer edges from prose. Report catalog defects to SECOD maintainers; do
not repair catalog ownership during an application task.

## Exclude unrelated skills

Before implementation, verify each generalized skill maps to a current boundary, each provider
is Requested or Detected, provider families include only used child products, transitive skills
came from catalog edges, no duplicate remains, and no dormant dependency caused selection.

## Load progressively

Read selected `SKILL.md` files first. Load only recipes matching current language, framework,
provider product, runtime, and version. Do not preload every provider reference or copy whole
provider manuals into context.
