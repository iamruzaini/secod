# SECOD Product Requirements Document

**Product:** SECOD — Secure implementation skills for AI coding agents

**Status:** Draft product reset

**Target release:** SECOD v0.1.0

**Last updated:** 2026-09-06

**Owner:** iamruzaini / SECOD maintainers
**License:** Apache License 2.0

## 1. Product decision

SECOD helps AI coding agents build safer web and mobile applications from the first line of
code. It supplies secure defaults, provider-specific implementation guidance, official
documentation, reference patterns, and security-focused tests during normal coding sessions.

SECOD is not a vulnerability scanner, penetration-testing product, compliance engine, security
certification, or launch-verdict service. Its primary job is to improve what an agent writes,
not to assign a security score after code already exists.

### North-star statement

> SECOD helps AI coding agents build safer web and mobile applications with secure defaults,
> provider-specific implementation guidance, official documentation, and security-focused
> tests.

### Product outcome

When a user asks an agent to add or change an application feature, SECOD should help the agent:

1. Detect the relevant framework, runtime, provider, SDK, and application boundary.
2. Select only the generalized and provider-specific skills needed for that task.
3. Choose a secure design before writing code.
4. Implement the design in the project's existing language, framework, and conventions.
5. Add tests for security-critical behavior and expected failure paths.
6. Use current official provider documentation to support implementation decisions.
7. Separate repository changes from provider-console or production actions that require user
   access or approval.
8. Summarize protections added, tests run, remaining manual steps, and relevant official
   sources.

## 2. Problem

AI coding agents can build functional applications quickly, but secure implementation knowledge
is fragmented across framework guides, provider documentation, SDK references, security
standards, and incident learnings. Generic model knowledge is often insufficient because secure
behavior depends on:

- Exact framework, runtime, SDK, and API versions.
- Server, browser, mobile-device, worker, and provider trust boundaries.
- Provider-specific authentication, storage, webhook, IAM, retry, and deployment behavior.
- Product plan, region, environment, and feature availability.
- Interactions between multiple providers in one application.
- Tests that prove a chosen implementation rejects unsafe behavior.

Post-development scanners remain useful, but they act after code exists and cannot replace secure
design and implementation. Builders need security guidance inside the coding loop, while the
agent is deciding architecture, writing handlers, configuring providers, and adding tests.

## 3. Positioning and differentiation

| Post-development scanner | SECOD |
| --- | --- |
| Inspects code or deployments after implementation | Guides implementation before and while code is written |
| Produces alerts, findings, scores, or verdicts | Produces secure implementation decisions, code changes, and tests |
| Often applies generic rules | Adds framework- and provider-specific context |
| Explains what is wrong | Helps the agent write the safer form first |
| May run as a separate security workflow | Runs inside the user's ordinary coding workflow |
| May claim coverage based on scan scope | States exact implementation scope and any external step it could not perform |

SECOD must not claim that an application is secure. The product promise is narrower and
testable: an installed SECOD skill gives an agent curated security instructions for the
applicable coding task and provider.

## 4. Product principles

### 4.1 Coding-time first

Skills trigger on build, integration, migration, and modification requests. Repository review is
secondary and occurs only when needed to implement the requested change safely or when the user
explicitly asks for review.

### 4.2 Implementation over commentary

Skills must tell the agent what to implement, where the trust boundary belongs, which unsafe
patterns to avoid, and which tests to add. A skill that only describes risks or returns findings
does not satisfy the SECOD contract.

### 4.3 Secure defaults

When several valid designs exist, skills choose the safest practical default compatible with the
project. The agent explains a meaningful tradeoff only when the choice affects product behavior,
cost, compatibility, data handling, or user experience.

### 4.4 Provider-aware layering

Generalized skills own portable security principles. Provider skills translate those principles
into the exact provider SDK, API, configuration, and documented constraints. Provider guidance
extends the generalized baseline; it does not replace it.

### 4.5 Official sources close to code

Implementation guidance must be backed by direct official documentation pages. An official
`llms.txt` or `llms-full.txt` file may be used to discover current documentation, but it is
never the sole authority for a security-sensitive recipe.

### 4.6 Tests ship with security-sensitive code

Authentication, authorization, tenant isolation, webhooks, uploads, payments, retries, secrets,
AI tool use, storage access, and similar boundaries require tests for both allowed and rejected
behavior.

### 4.7 Web and mobile are first-class

SECOD must cover browser/server applications and mobile applications. Mobile guidance must
address device storage, deep links, OAuth/PKCE, platform key stores, WebViews, logs, backups,
offline data, push notifications, permissions, and provider SDK boundaries.

### 4.8 Minimal relevant context

The router loads only skills relevant to the current task. Installing the full pack must not
cause every skill to influence every coding request.

### 4.9 Honest external boundaries

Repository code cannot establish every deployed provider setting. During ordinary coding, the
agent should implement the repository side and list any required console step. Only an explicit
verification request may produce language such as “Could not verify this deployed setting.”
Unknown external state must not become the central output of a coding skill.

## 5. Goals

### 5.1 Product goals

1. Make secure implementation guidance available through installable Agent Skills.
2. Guide agents during normal feature development without requiring a separate scan command.
3. Provide concrete generalized and provider-specific implementation playbooks.
4. Make official documentation understandable and actionable in the project's current stack.
5. Generate or modify production-quality code rather than generic pseudo-code when repository
   context is available.
6. Add security-focused tests alongside implementation changes.
7. Support selective installation and automatic task-specific routing.
8. Support Codex, Claude Code, Cursor, and compatible Agent Skills clients.
9. Treat web and mobile development as explicit product surfaces.
10. Keep SECOD's repository, catalog, documentation, and website synchronized through versioned
    imports.

### 5.2 Quality goals

1. Every release-visible skill contains at least one tested secure implementation path.
2. Every provider recipe identifies the supported provider feature, SDK/API version assumptions,
   environment, and direct official source.
3. Code examples compile, type-check, lint, or execute in maintained fixtures where applicable.
4. Agent evaluations prove that SECOD produces secure code and tests, not only a report.
5. Skills do not expose credentials, encourage production mutations, or invent provider
   capabilities.
6. Documentation discovery failures degrade to direct official pages rather than fabricated
   `llms.txt` URLs.
7. Public guidance never relies on a source that is merely reachable but not substantively
   reviewed.

## 6. Non-goals

- Building or hosting a general-purpose vulnerability scanner.
- Replacing SAST, DAST, dependency scanning, secret scanning, penetration testing, or cloud
  posture-management products.
- Issuing whole-application pass/fail, “secure,” “certified,” or compliance verdicts.
- Replacing professional security, privacy, legal, or compliance advice.
- Automatically changing production credentials, billing, domains, IAM, data retention, or
  provider settings without explicit user authorization.
- Supporting every framework, language, mobile platform, provider, or provider feature in the
  first release.
- Teaching complete provider or framework usage unrelated to secure implementation.
- Copying large portions of provider documentation into the repository.

## 7. Primary users and jobs

| User | Job | SECOD outcome |
| --- | --- | --- |
| Solo builder or “vibe coder” | Build a feature without knowing every security pitfall | Agent writes a safer implementation and explains important boundaries |
| Application developer | Add a provider integration quickly and correctly | Provider-specific code, configuration guidance, and tests |
| Mobile developer | Connect device code to authentication, storage, APIs, and notifications | Platform-appropriate storage, token, link, WebView, and backend guidance |
| Small product team | Standardize secure coding behavior across agents | Shared, versioned implementation playbooks |
| Security-conscious maintainer | Keep generated code aligned with official guidance | Traceable recipes, direct sources, regression fixtures, and update cadence |

## 8. Core user experience

### 8.1 Installation

Users can browse or install SECOD through the Skills CLI:

```powershell
# Browse available skills
npx skills add iamruzaini/secod --list

# Install the full pack for Codex
npx skills add iamruzaini/secod --skill '*' --agent codex --yes

# Install one skill
npx skills add iamruzaini/secod --skill secod-core --agent codex --yes
```

The full pack provides availability. Task routing determines which skills the agent should use.

### 8.2 Normal coding request

The user should not need to invoke a scan or special audit prompt. A normal request is enough:

> Add Firebase Auth, Firestore-backed organizations, file uploads, and a Stripe subscription to
> this Next.js application.

SECOD should:

1. Detect Next.js, Firebase, Stripe, relevant language/tooling, and current project conventions.
2. Route `secod-nextjs`, `secod-firebase`, `secod-stripe`, and only the relevant generalized
   skills for identity, inputs, files, secrets, payments, and abuse resistance.
3. Decide server/client responsibilities before editing.
4. Implement backend authorization and tenant-scoped data access.
5. Add restrictive Firebase Rules and Emulator tests where Firebase client access is used.
6. Keep privileged credentials and Stripe operations server-side.
7. Verify Stripe webhooks from the raw request body and make event processing idempotent.
8. Add upload type, size, ownership, and storage-policy checks.
9. Run available project tests and report exact results.
10. Provide separate manual steps for console settings the code cannot configure safely.
11. Cite the direct Firebase, Next.js, and Stripe pages used for the implementation.

### 8.3 Existing-code modification

When changing an existing feature, SECOD must preserve project conventions and compatible public
behavior unless security requires a deliberate migration. It should patch the narrowest
responsible layer, add regression coverage, and state any compatibility or rollout impact.

### 8.4 Explicit verification request

If the user explicitly asks to verify existing code, SECOD may inspect relevant implementation
and tests. It should report concrete code evidence and proposed fixes. It must not turn that
request into an unrestricted penetration test or claim provider-console state without access.

## 9. Product modes

### 9.1 Build mode — default

Used when creating a feature or integration. Output is working code, configuration, tests, and
manual provider steps.

### 9.2 Change or migration mode

Used when upgrading an SDK, replacing a provider, moving trust boundaries, or tightening a
security-sensitive design. Output includes compatibility handling, rollout steps, and regression
tests.

### 9.3 Explain mode

Used when the user wants to understand a secure implementation. Output is a concise explanation,
small relevant examples, and direct official sources.

### 9.4 Scoped verification mode — secondary

Used only when explicitly requested. It verifies the code or configuration in scope and may
state that a deployed setting could not be confirmed. It does not issue a whole-application
security verdict.

SECOD has no default scanner mode.

## 10. Skill architecture

Each public skill lives under `skills/<slug>/` and follows this structure:

```text
skills/<slug>/
├── SKILL.md
├── references/
│   ├── sources.md
│   └── implementation-guides.md      # optional when SKILL.md would become too large
├── examples/                         # optional maintained reference implementations
└── scripts/                          # optional deterministic helpers
```

Repository-level fixtures and behavior evaluations remain under `tests/`.

### 10.1 Required SKILL.md contract

Every release-visible `SKILL.md` must contain:

1. **Purpose** — one sentence describing what the skill helps the agent implement securely.
2. **When to use** — coding requests, stack signals, supported features, and clear exclusions.
3. **Context to inspect** — only files, versions, routes, schemas, and configuration needed for
   the current task.
4. **Secure defaults** — decisions the agent should apply unless project evidence requires a
   different design.
5. **Implementation workflow** — ordered steps from design through code and tests.
6. **Implementation recipes** — concrete patterns for supported frameworks, languages, or SDKs.
7. **Unsafe patterns to avoid** — concise counterexamples tied to the safe recipe.
8. **Tests to add** — positive, negative, tenant-boundary, replay, failure, and authorization
   cases appropriate to the feature.
9. **Provider or deployment steps** — clearly separated manual actions and safe automation
   boundaries.
10. **Official sources** — direct documentation pages supporting each security-sensitive recipe.

### 10.2 Disallowed default structure

A public skill must not default to:

- A repository-wide audit workflow.
- A mandatory finding or risk-rating report.
- A universal `Do not ship`, `Passed with evidence`, or `Not verified` status schema.
- A long undifferentiated checklist with no implementation sequence.
- Provider-dashboard evidence collection unrelated to the coding request.
- A launch-readiness or certification claim.

Existing audit-oriented content may remain as optional reference material only when it improves a
specific implementation or explicit verification task.

### 10.3 Implementation recipe requirements

Each recipe must include the parts relevant to its feature:

- Supported language, framework, runtime, provider product, and SDK/API version assumptions.
- Required packages and imports.
- Server, browser, mobile, worker, and provider trust boundaries.
- Authentication and resource/tenant authorization.
- Input and output validation.
- Secret and credential placement.
- Data minimization and safe persistence.
- Bounded timeouts, retries, concurrency, and idempotency where applicable.
- Safe errors and logs.
- Cleanup, rollback, revocation, or reconciliation behavior.
- Positive and negative tests.
- Direct official documentation links.

Examples must use placeholders, never real credentials or production identifiers. Examples must
not silently weaken security to shorten code.

## 11. Agent execution contract

During an applicable coding task, the agent must:

1. Read the smallest relevant project surface before deciding the implementation.
2. Detect actual package and SDK versions from lockfiles or equivalent resolved metadata.
3. Prefer the project's existing language, framework, validation library, test runner, and
   architectural conventions.
4. Load the generalized skills required by the feature and the exact provider adapters detected
   or requested.
5. Consult the relevant direct official source before relying on version-sensitive provider
   behavior.
6. Implement the complete security boundary rather than leaving a critical TODO.
7. Add or update tests that demonstrate rejected unsafe behavior.
8. Run proportionate validation and report the exact commands and results.
9. Keep production/provider actions separate and request authority when they would change
   external state.
10. Summarize files changed, security decisions, tests, manual steps, assumptions, and official
    sources.

The agent must not:

- Load unrelated provider guidance.
- Read or print secret values when names and structure are sufficient.
- Assume a client SDK enforces server authorization.
- Trust UI visibility as access control.
- Invent provider features, settings, webhook fields, or `llms.txt` endpoints.
- Replace implementation with a generic security checklist.
- Claim the whole application is secure.

## 12. Routing and dependency model

`secod-core` becomes a coding-context router, not an audit controller.

### 12.1 Routing signals

- **Requested:** user names a provider, framework, SDK, or feature to add.
- **Detected:** repository contains corroborating package, import, configuration, route, schema,
  or infrastructure evidence.
- **Not applicable:** no task or repository signal requires the skill.

Package presence alone may justify loading lightweight provider context, but the agent must
confirm actual use before changing provider-specific code.

### 12.2 Routing rules

1. Start from the user's requested feature.
2. Add generalized skills that own the feature's security boundaries.
3. Add exact framework/provider skills requested or detected.
4. Resolve transitive dependencies.
5. Remove unrelated providers and generalized skills.
6. Recompute routing when the implementation introduces a new provider or boundary.

### 12.3 Routing examples

| Coding task | Expected routing |
| --- | --- |
| Add Firebase Auth and Firestore organizations to Next.js | Core, Next.js, Firebase, identity/access, inputs/APIs, secrets, abuse limits |
| Add an S3 presigned upload behind CloudFront | Core, AWS web, S3/CloudFront, data/files, identity/access, secrets, abuse limits |
| Add a Stripe subscription webhook | Core, payments/billing, Stripe, inputs/APIs, secrets, abuse limits, failure safety |
| Add OpenAI tool calling and tenant-scoped retrieval | Core, AI API integrations, OpenAI, runtime execution, inputs/APIs, identity/access, secrets, abuse limits |
| Add Cloudflare R2-backed uploads from an Expo app | Core, mobile app security, Cloudflare, data/files, identity/access, inputs/APIs, secrets |

## 13. Catalog direction

The existing 57 skills are a migration inventory, not a permanent marketing constraint. Release
scope is determined by tested implementation coverage, not by preserving an arbitrary count.

### 13.1 Generalized implementation skills

Existing generalized skills remain useful but must be rewritten around coding tasks:

| Skill | New implementation responsibility |
| --- | --- |
| `secod-core` | Detect coding context and route only relevant skills |
| `secod-threat-model` | Make lightweight trust-boundary and abuse-case decisions before high-risk implementation |
| `secod-identity-access` | Implement authentication, authorization, sessions, tokens, capabilities, roles, and tenant isolation |
| `secod-web-app-security` | Implement browser, cookie, CSRF, CORS, CSP, rendering, navigation, and client-storage protections |
| `secod-inputs-apis` | Implement schemas, API boundaries, webhook validation, SSRF controls, and safe outbound requests |
| `secod-runtime-execution` | Implement safe process, command, template, and tool execution |
| `secod-crypto-data-protection` | Choose maintained cryptographic APIs, key boundaries, encryption, hashing, and retention patterns |
| `secod-data-files` | Implement secure uploads, downloads, storage access, scanning hooks, and lifecycle behavior |
| `secod-abuse-limits` | Implement rate limits, quotas, idempotency, replay resistance, and cost controls |
| `secod-secrets-config` | Implement server-only secret loading, environment separation, rotation-ready design, and redaction |
| `secod-packages-delivery` | Install, pin, build, and ship dependencies and artifacts safely |
| `secod-vulnerability-management` | Select supported versions and handle security updates without unsafe migrations |
| `secod-observability-response` | Add safe security logs, alerts, correlation, and recovery hooks during feature development |
| `secod-payments-billing` | Implement trusted payment state, webhook processing, entitlements, reconciliation, and refunds |
| `secod-ai-api-integrations` | Implement model boundaries, tool authorization, prompt/data handling, structured outputs, retrieval isolation, and spend limits |
| `secod-container-runtime` | Build least-privilege images and runtime configuration |
| `secod-email-messaging` | Implement safe links, OTPs, templates, delivery events, and messaging webhooks |
| `secod-failure-safety` | Implement fail-closed behavior, bounded retries, rollback, cleanup, and partial-failure recovery |
| `secod-ship-check` | Convert to an optional task-completion checklist; never issue a whole-application security verdict |

### 13.2 Current provider and framework adapters

All current adapters remain migration candidates:

| Group | Skills |
| --- | --- |
| Framework and hosting | `secod-nextjs`, `secod-vercel-platform` |
| Authentication | `secod-auth-provider-integrations`, `secod-clerk`, `secod-auth0`, `secod-workos`, `secod-better-auth`, `secod-supabase-auth`, `secod-aws-cognito` |
| Data and cloud | `secod-supabase`, `secod-firebase`, `secod-neon`, `secod-convex`, `secod-aws-web`, `secod-aws-lambda-api-gateway`, `secod-aws-s3-cloudfront`, `secod-aws-data-services`, `secod-google-cloud-web`, `secod-google-cloud-storage` |
| Cloudflare | `secod-cloudflare`, `secod-cloudflare-workers`, `secod-cloudflare-pages`, `secod-cloudflare-queues`, `secod-cloudflare-workflows`, `secod-cloudflare-hyperdrive`, `secod-cloudflare-vectorize`, `secod-cloudflare-workers-ai`, `secod-cloudflare-ai-gateway` |
| Payments | `secod-stripe`, `secod-polar`, `secod-lemonsqueezy`, `secod-dodo-payments`, `secod-whop` |
| AI providers | `secod-openai`, `secod-anthropic`, `secod-google-genai`, `secod-xai-grok`, `secod-vercel-ai` |

Provider adapters must become feature-oriented implementation playbooks. Broad provider skills
route to narrower recipes; they must not dump every provider control into every request.

### 13.3 Required mobile expansion

The current catalog does not provide enough first-class mobile implementation guidance. Before
SECOD claims mobile support, add and test at least:

- `secod-mobile-app-security` — portable mobile storage, token, deep-link, WebView, logging,
  offline-data, backup, permission, screenshot/clipboard, and device-integrity guidance.
- `secod-react-native-expo` — React Native and Expo implementation patterns.
- `secod-flutter` — Flutter and Dart implementation patterns.

Provider adapters that support mobile SDKs must include explicit mobile recipes or clearly state
that they cover backend integration only. Native Android and iOS adapters may follow after
maintained React Native/Expo and Flutter coverage exists.

## 14. Official documentation and source policy

### 14.1 Source hierarchy

Use sources in this order:

1. Direct official security or implementation page for the exact feature.
2. Official SDK, API, framework, or product reference.
3. Official migration, release-note, or advisory page for version-sensitive behavior.
4. Official `llms.txt` or `llms-full.txt` as a discovery index.
5. Versioned security standards for portable requirements.

Community examples may inform tests but cannot override official provider behavior.

### 14.2 Required source-register behavior

Every provider skill keeps `references/sources.md` with:

- Official documentation homepage.
- Official `llms.txt` and `llms-full.txt` URLs when published.
- Direct pages used by each implementation recipe.
- Provider product and feature.
- SDK/API/framework version assumptions.
- Review date, refresh trigger, owner, and linked recipe IDs.
- Status: `Reviewed`, `Pending review`, or `Unavailable`.

`Reviewed` means the source content was read, mapped to an implementation recipe, and covered
by an applicable fixture. `Pending review` is internal work and cannot substantiate a
release-visible recipe. `Unavailable` means the source cannot currently support the recipe,
which must be hidden, narrowed, or removed.

### 14.3 llms.txt rules

- Always record the provider's main documentation URL beside any `llms.txt` URL.
- Never guess an `llms.txt` path.
- Verify the effective URL, HTTP success, and text/Markdown content before recording it.
- Treat redirects within the provider's official domains as valid and record the effective URL.
- Use `llms.txt` for discovery; cite the exact direct page used for a security-sensitive claim.
- Recheck indexes for every release and whenever provider documentation structure changes.
- A missing `llms.txt` is not a provider-quality failure. Use direct official documentation.
- Do not preserve a stale `llms-full.txt` claim after the endpoint stops working.

### 14.4 Verified official documentation registry

The following roots and indexes were checked on 2026-09-06. Each source register must perform its
own release-time refresh.

| Family | Official documentation homepage | Official AI-readable indexes verified |
| --- | --- | --- |
| Next.js | [Next.js Docs](https://nextjs.org/docs) | [llms.txt](https://nextjs.org/docs/llms.txt), [llms-full.txt](https://nextjs.org/docs/llms-full.txt) |
| Vercel and Vercel AI SDK | [Vercel Docs](https://vercel.com/docs) | [llms.txt](https://vercel.com/docs/llms.txt), [llms-full.txt](https://vercel.com/docs/llms-full.txt) |
| Clerk | [Clerk Docs](https://clerk.com/docs) | [llms.txt](https://clerk.com/docs/llms.txt), [llms-full.txt](https://clerk.com/docs/llms-full.txt) |
| Auth0 | [Auth0 Docs](https://auth0.com/docs) | [llms.txt](https://auth0.com/docs/llms.txt), [llms-full.txt](https://auth0.com/docs/llms-full.txt) |
| Better Auth | [Better Auth Docs](https://better-auth.com/docs/introduction) | [llms.txt](https://better-auth.com/llms.txt); no working `llms-full.txt` verified |
| WorkOS | [WorkOS Docs](https://workos.com/docs) | [llms.txt](https://workos.com/docs/llms.txt), [llms-full.txt](https://workos.com/docs/llms-full.txt) |
| Supabase | [Supabase Docs](https://supabase.com/docs) | [llms.txt](https://supabase.com/llms.txt), [llms-full.txt](https://supabase.com/llms-full.txt) |
| Firebase | [Firebase Docs](https://firebase.google.com/docs) | No working root `llms.txt` or `llms-full.txt` verified; use direct docs |
| Neon | [Neon Docs](https://neon.com/docs) | [llms.txt](https://neon.com/llms.txt), [llms-full.txt](https://neon.com/llms-full.txt) |
| Convex | [Convex Docs](https://docs.convex.dev) | [llms.txt](https://docs.convex.dev/llms.txt), [llms-full.txt](https://docs.convex.dev/llms-full.txt) |
| AWS | [AWS Documentation](https://docs.aws.amazon.com/) | [llms.txt](https://docs.aws.amazon.com/llms.txt), [llms-full.txt](https://docs.aws.amazon.com/llms-full.txt) |
| Google Cloud | [Google Cloud Documentation](https://cloud.google.com/docs) | No working root `llms.txt` verified; use direct docs |
| Cloudflare | [Cloudflare Developer Docs](https://developers.cloudflare.com/) | [llms.txt](https://developers.cloudflare.com/llms.txt), [llms-full.txt](https://developers.cloudflare.com/llms-full.txt), [Workers llms.txt](https://developers.cloudflare.com/workers/llms.txt), [Workers llms-full.txt](https://developers.cloudflare.com/workers/llms-full.txt) |
| Docker | [Docker Docs](https://docs.docker.com/) | [llms.txt](https://docs.docker.com/llms.txt), [llms-full.txt](https://docs.docker.com/llms-full.txt) |
| OpenAI API | [OpenAI API Docs](https://developers.openai.com/api/docs) | [llms.txt](https://developers.openai.com/api/docs/llms.txt), [llms-full.txt](https://developers.openai.com/api/docs/llms-full.txt) |
| Anthropic / Claude API | [Claude Platform Docs](https://platform.claude.com/docs/en/home) | [llms.txt](https://platform.claude.com/llms.txt), [llms-full.txt](https://platform.claude.com/llms-full.txt) |
| Google Gemini API | [Gemini API Docs](https://ai.google.dev/gemini-api/docs) | No working root `llms.txt` verified; use direct docs |
| xAI | [xAI Docs](https://docs.x.ai/overview) | [llms.txt](https://docs.x.ai/llms.txt); no working `llms-full.txt` verified |
| Stripe | [Stripe Docs](https://docs.stripe.com/) | [llms.txt](https://docs.stripe.com/llms.txt); no working `llms-full.txt` verified |
| Polar | [Polar Docs](https://polar.sh/docs/introduction) | [llms.txt](https://polar.sh/docs/llms.txt), [llms-full.txt](https://polar.sh/docs/llms-full.txt) |
| Lemon Squeezy | [Lemon Squeezy Docs](https://docs.lemonsqueezy.com/) | No working root `llms.txt` verified; use direct docs |
| Dodo Payments | [Dodo Payments Docs](https://docs.dodopayments.com/) | [llms.txt](https://docs.dodopayments.com/llms.txt), [llms-full.txt](https://docs.dodopayments.com/llms-full.txt) |
| Whop | [Whop Docs](https://docs.whop.com/) | [llms.txt](https://docs.whop.com/llms.txt), [llms-full.txt](https://docs.whop.com/llms-full.txt) |
| GitHub | [GitHub Docs](https://docs.github.com/) | [llms.txt](https://docs.github.com/llms.txt); no working `llms-full.txt` verified |

### 14.5 Portable security standards

Generalized guidance should map to current primary standards when applicable:

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security](https://owasp.org/API-Security/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Mobile Application Security Verification Standard](https://mas.owasp.org/MASVS/)
- [OWASP Mobile Application Security Testing Guide](https://mas.owasp.org/MASTG/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)

Standards support portable principles. Exact provider behavior still requires direct provider
documentation.

## 15. Web and mobile implementation coverage

### 15.1 Web coverage

SECOD web guidance must cover:

- Server/client boundaries and browser data exposure.
- Authentication, sessions, authorization, roles, and tenant isolation.
- APIs, validation, webhooks, SSRF, uploads, redirects, and realtime connections.
- Databases, object storage, caches, queues, scheduled work, and background processing.
- Secrets, logging, errors, retries, idempotency, and abuse controls.
- Deployment, preview, domain, runtime, package, and artifact boundaries.
- Payments, AI APIs, tools, retrieval, and vector stores.

### 15.2 Mobile coverage

SECOD mobile guidance must cover:

- OAuth Authorization Code with PKCE and exact redirect/deep-link handling.
- Platform key stores and safe token/session persistence.
- Avoiding long-lived provider secrets in application packages.
- Backend authorization independent of client or device claims.
- Universal Links, App Links, custom schemes, and callback validation.
- WebView origin, navigation, JavaScript bridge, file-access, and content handling.
- Local database, cache, offline queue, backup, screenshot, clipboard, and log exposure.
- Biometric use as local user presence, not a replacement for backend authorization.
- Push-notification content minimization and authenticated notification actions.
- Mobile permissions, exported components, device-integrity signals, and graceful fallback.
- TLS defaults and narrowly justified pinning strategies with rotation and recovery plans.
- Provider SDK configuration for Firebase, Supabase, Auth0, Clerk, WorkOS, AWS, Google Cloud,
  payments, and AI features where officially supported.

## 16. Testing and evaluation strategy

SECOD tests must prove secure implementation behavior, not scanner-style finding output.

### 16.1 Per-skill gates

Every public skill must pass:

1. Agent Skills metadata and directory validation.
2. Coding-request trigger and similar non-trigger cases.
3. At least one end-to-end implementation fixture.
4. Secure-default assertions against generated or modified code.
5. Negative assertions proving rejected authorization, tenant, replay, input, secret, or failure
   behavior where applicable.
6. Build, type-check, lint, and test commands appropriate to the fixture.
7. Official source homepage and direct-link validation.
8. `llms.txt` validation only when the provider publishes it.
9. Version-compatibility or migration coverage for version-sensitive recipes.
10. Routing tests proving unused providers do not influence the implementation.

### 16.2 Agent behavior evaluations

Run representative tasks through Codex, Claude Code, and Cursor. Evaluations must confirm that
the agent:

- Produces code and tests rather than only a report.
- Applies secure defaults without requiring the user to name every security requirement.
- Uses only relevant generalized and provider skills.
- Follows repository conventions.
- Links the official pages used.
- Separates manual provider steps from completed repository changes.
- Refuses unsafe shortcuts that would expose secrets or move authorization to the client.
- Does not claim the whole application is secure.

### 16.3 Required integration fixtures

Before SECOD claims its target coverage, maintain executable fixtures for:

- Next.js + Firebase Auth + Firestore + Storage.
- Next.js + Supabase Auth + Database + Storage + Vercel.
- React Native/Expo + Firebase.
- Flutter + Supabase.
- AWS Lambda + API Gateway + Cognito + S3/CloudFront.
- Google Cloud web API + Cloud Storage.
- Cloudflare Workers + Queues + R2 or another supported storage integration.
- Stripe and each supported payment provider's documented webhook shape.
- OpenAI, Anthropic, Gemini, xAI, and Vercel AI integrations with server-only credentials,
  bounded usage, structured output, tool authorization, and tenant-scoped retrieval.
- Mixed-provider application routing.

Current insecure fixtures may be retained as regression inputs, but expected results must be
rewritten around the secure code and tests SECOD should produce.

## 17. Repository and supply-chain requirements

SECOD is installed into coding-agent context and must be maintained as a security-sensitive
supply-chain artifact.

- Protect the default branch with pull requests, required CI, current-branch enforcement,
  conversation resolution, and blocked force pushes/deletions.
- Enable private vulnerability reporting, secret scanning, push protection, dependency graph,
  Dependabot alerts, and Dependabot security updates where available.
- Pin third-party CI actions to reviewed full commit SHAs.
- Give workflows minimum permissions and prevent untrusted code from receiving write tokens or
  secrets.
- Keep `SECURITY.md`, `CONTRIBUTING.md`, changelog, catalog, and release instructions current.
- Validate generated catalog output against the canonical skills before release.
- Preserve Apache-2.0 licensing and third-party attribution requirements.
- Never place sponsor instructions or commercial preferences inside security guidance.

## 18. Documentation requirements

README, website, catalog descriptions, and skill frontmatter must use the same positioning:

> SECOD helps AI coding agents build safer web and mobile applications with secure defaults,
> provider-specific implementation guidance, official documentation, and security-focused
> tests.

Documentation must:

- Lead with coding-time assistance, not scanning, auditing, findings, or certification.
- Show normal feature-building prompts.
- Show selective and full installation.
- Explain provider routing in plain language.
- Include at least one complete web example and one complete mobile example.
- Distinguish code changes, tests, and manual provider steps.
- State current tested providers, frameworks, languages, agents, and limitations.
- Avoid claiming that installing SECOD makes an application secure.

## 19. Release gates for v0.1.0

Do not publish the normal `v0.1.0` release until:

1. PRD, README, catalog, website, changelog, and skill descriptions use the new positioning.
2. `secod-core` routes coding tasks and no longer defaults to repository-wide review.
3. Every release-visible skill follows the new implementation contract.
4. Every release-visible provider recipe is backed by reviewed direct official documentation.
5. Every provider source register includes its official documentation homepage and only verified
   `llms.txt` endpoints.
6. `Pending review` sources do not substantiate public implementation recipes.
7. Universal finding/status schemas and mandatory `Not verified` wording are removed from
   ordinary coding skills and validators.
8. `secod-ship-check` is converted to an optional task-completion checklist or removed from the
   public dependency graph.
9. Every public skill has an executable secure-implementation fixture.
10. Web integration fixtures pass.
11. React Native/Expo and Flutter integration fixtures pass before documentation claims broad
    mobile support.
12. Codex, Claude Code, and Cursor behavior evaluations show code-and-test output rather than
    scanner-style reports.
13. Full-pack and selective installations work from clean projects.
14. All source, routing, build, lint, test, repository-hygiene, and supply-chain checks pass.
15. No `v0.1.0` tag exists before all required gates pass.

The existing `v0.1.0-beta.1` release remains historical prerelease evidence and must not be
rewritten.

## 20. Migration plan

### Phase A — Freeze new contract

1. Adopt this PRD as product source of truth.
2. Create one reusable implementation-first skill template.
3. Replace audit output schemas with the coding-task response contract.
4. Replace universal evidence-boundary validation with a narrower “no unsupported deployment
   claims” check.

### Phase B — Prove the model

Rewrite and fully test:

- `secod-core`
- `secod-nextjs`
- `secod-identity-access`
- `secod-firebase`
- `secod-supabase`
- `secod-stripe`
- `secod-openai`

Use these skills to prove routing, implementation recipes, source mapping, tests, and final
coding-session output before converting the full catalog.

### Phase C — Convert generalized skills

Rewrite remaining generalized skills around secure implementation. Keep portable controls, but
move audit-only material to optional references or remove it.

### Phase D — Convert provider adapters

Split broad provider checklists into task- and feature-oriented recipes. Complete substantive
source review before making each recipe public.

### Phase E — Add mobile coverage

Add generalized mobile, React Native/Expo, and Flutter skills and integration fixtures. Update
provider skills with explicit mobile or backend-only scope.

### Phase F — Align distribution surfaces

Regenerate catalog data, update README/changelog/website, run clean installations and real-agent
evaluations, then create the normal release only after every gate passes.

## 21. Success metrics

### Product behavior

- Percentage of evaluated coding tasks that produce the expected secure implementation.
- Percentage of security-critical changes accompanied by meaningful negative tests.
- Rate of irrelevant skill/provider activation.
- Rate of scanner-style report output when the user requested implementation; target: zero.
- Percentage of provider recipes linked to reviewed direct official sources.
- Fixture pass rate across supported SDK and framework versions.

### User value

- Successful full-pack and selective installations.
- Time from feature request to tested secure implementation.
- Repeat use across coding sessions.
- User-reported avoided security regressions.
- Web and mobile example completion rates.

### Maintenance quality

- Time from official documentation or SDK change to reviewed SECOD update.
- Stale or broken official-source rate.
- Number of unsafe or misleading recipes reported.
- Time to acknowledge and remediate SECOD security reports.

## 22. Acceptance examples

### 22.1 Firebase and Next.js

Given a Next.js request to add Firebase Auth and tenant-scoped Firestore data, SECOD routes the
relevant skills, writes server/client boundaries, restrictive Rules, server-side authorization,
and Emulator tests, then links the direct official Firebase and Next.js pages used. It does not
return only a list of possible findings.

### 22.2 Payment webhook

Given a request to add a Stripe webhook, SECOD implements raw-body signature verification,
documented freshness behavior, event deduplication, idempotent state transitions, safe logging,
and tests for forged, duplicate, stale, and out-of-order events.

### 22.3 AI tool execution

Given a request to add model-selected tools, SECOD keeps provider credentials server-side,
defines an explicit tool allowlist and per-tool authorization, validates structured arguments,
isolates tenant retrieval, bounds usage, and tests rejected tools and cross-tenant requests.

### 22.4 Mobile authentication

Given an Expo or Flutter request to add OAuth login, SECOD uses Authorization Code with PKCE,
validates exact redirect/deep-link handling, stores tokens in the platform key store, keeps
privileged provider credentials off-device, enforces backend authorization, and tests replay and
wrong-redirect behavior.

## 23. Next artifacts

After adopting this PRD:

1. Create the implementation-first `SKILL.md` template.
2. Produce a migration matrix for every current skill: retain, rewrite, merge, split, add, or
   retire.
3. Rewrite the Phase B proof set.
4. Replace behavior cases with coding-task evaluations.
5. Update validators and CI to enforce the new contract.
6. Align README, changelog, catalog, and website only after the proof set works end to end.
