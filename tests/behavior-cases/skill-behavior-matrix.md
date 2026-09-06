# SECOD implementation behavior matrix

Every public skill is evaluated as coding guidance. Cases test activation, routing, generated secure implementation, missing context, external handoff, and API honesty. This matrix is a review plan, not proof that an agent executed each case.

## `secod-core`

- Trigger request: `Add Firebase Auth, Firestore, and secure tenant-isolated document access to this Next.js app.`
- Non-trigger request: `Fix spelling and punctuation in README only.`
- Dependency routing: Include none plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: `secod-core` identifies current feature, relevant application root, stack and resolved versions, provider products, trust boundaries, sensitive data, likely changed files, and existing tests. It selects only applicable generalized/framework/provider/mobile skills, computes complete transitive dependency closure, excludes unused providers, and passes same compact task context to each selected skill. Selected skills then guide secure code and tests without expanding into unrelated review work or certifying application security.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-threat-model`

- Trigger request: `Add tenant file sharing; identify trust boundaries and abuse cases before coding.`
- Non-trigger request: `Fix README punctuation only.`
- Dependency routing: Consume already-selected skills and `secod-core` context; do not initiate unrelated provider routing or repository-wide review.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Produce feature-scoped security requirements, implement them with selected skills, and add abuse-case tests. Missing context: Feature scope, actors, assets, or trust boundaries are unclear; inspect architecture and ask narrowly before designing controls. Rejected behavior: Do not emit a generic threat report or claim STRIDE labels prove mitigation.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-identity-access`

- Trigger request: `Add tenant-scoped invoice access and an admin role to this authenticated API.`
- Non-trigger request: `Change the public landing-page heading.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent implements a reusable server authorization boundary that derives identity from a verified session, loads resource ownership from trusted storage, denies by default, and does not trust browser-supplied roles or tenant identifiers. Tests cover authorized and denied paths. If the identity provider, tenancy model, or session library version is missing, the agent asks for or inspects that context before choosing provider APIs. It does not emit a scanner report or claim that deployed identity settings were checked.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-web-app-security`

- Trigger request: `Add a rich-text form using authenticated cookies.`
- Non-trigger request: `Change server-only database indexing.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Use safe rendering, server authorization, appropriate CSRF protection, narrow origins, and browser-boundary tests. Missing context: Rendering context or cookie/origin model is unclear; inspect framework and deployment before choosing controls. Rejected behavior: Never trust CORS, hidden UI, or browser headers as authorization.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-inputs-apis`

- Trigger request: `Add a webhook endpoint and an API that fetches a user-submitted preview URL.`
- Non-trigger request: `Rename a local TypeScript variable without changing behavior.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent defines schemas at the trust boundary, rejects unknown or oversized input, authorizes server-side, avoids shell/string interpolation, and constrains URL scheme, host, resolved address, redirects, timeout, and response size. Negative tests prove malformed, unauthorized, and private network requests are rejected. No post-hoc finding report replaces implementation.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-runtime-execution`

- Trigger request: `Add image conversion by invoking a server-side executable.`
- Non-trigger request: `Adjust static CSS colors.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Use fixed executables, structured arguments, allowlists, least privilege, resource bounds, and injection tests. Missing context: Runtime, executable, or process API version is unclear; inspect environment before writing calls. Rejected behavior: Never concatenate untrusted input into shell, template, expression, or code execution.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-crypto-data-protection`

- Trigger request: `Encrypt a sensitive profile field and add token generation.`
- Non-trigger request: `Rename a public UI label.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Use maintained libraries, purpose-specific primitives, separated keys, rotation, retention, deletion, and known-answer/failure tests. Missing context: Data classification, primitive requirements, or key service is unclear; resolve context before selecting algorithms or APIs. Rejected behavior: Never invent cryptography, hardcode keys, reuse nonces, or store passwords reversibly.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-data-files`

- Trigger request: `Add tenant-scoped PDF uploads and private downloads.`
- Non-trigger request: `Add a text field with no file or object handling.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Authorize each object operation, validate real content, generate identifiers, bound processing, store privately, and test denial paths. Missing context: Storage provider, ownership, accepted content, or processing limits are unclear; inspect before choosing APIs. Rejected behavior: Do not trust extensions, client paths, or public buckets by default.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-abuse-limits`

- Trigger request: `Add public invitation sending and a retrying background job.`
- Non-trigger request: `Change local formatting with no request or resource behavior.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Apply layered limits, atomic invariants, idempotency, bounded jittered retries, and duplicate/concurrency tests. Missing context: Identity scopes, business invariant, or infrastructure support is unclear; inspect before selecting limit storage or atomic operations. Rejected behavior: Never rely on one global limit or blindly retry non-idempotent effects.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-secrets-config`

- Trigger request: `Add a provider API key and production environment configuration.`
- Non-trigger request: `Add a public theme color variable.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Keep credentials server-only, validate configuration, scope authority, separate environments, and document rotation/revocation. Missing context: Runtime boundary, deployment environment, or secret store is unclear; inspect before naming configuration APIs. Rejected behavior: Never expose privileged credentials through client configuration or insecure fallbacks.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-packages-delivery`

- Trigger request: `Add a dependency and update CI release workflow.`
- Non-trigger request: `Edit application copy without package or delivery changes.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Justify dependency need, update lockfile reproducibly, pin immutable CI inputs, minimize permissions, and test build/rollback. Missing context: Ecosystem, lockfile, registry, or CI platform is unclear; inspect before changing dependency or workflow syntax. Rejected behavior: Do not add unnecessary packages, floating CI actions, or broad release tokens.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-vulnerability-management`

- Trigger request: `Remediate a vulnerable package advisory without breaking its consumers.`
- Non-trigger request: `Design a feature with no dependency, advisory, or remediation work.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Remove or upgrade vulnerable path, migrate callers, update lockfile, add exploit/regression tests, and record narrow residual risk. Missing context: Advisory, affected path, fixed version, or compatibility surface is unclear; establish reachability and migration context first. Rejected behavior: Never stop at scanner output, blindly upgrade, or suppress without owner and expiry.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-observability-response`

- Trigger request: `Add audit events for role changes and webhook failures.`
- Non-trigger request: `Change a static image asset.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Emit structured redacted events, stable correlation, bounded metrics, actionable alerts, and containment/recovery tests. Missing context: Event taxonomy, sensitive fields, or response owner is unclear; inspect before defining telemetry. Rejected behavior: Never log secrets or add noisy alerts without owners and actions.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-payments-billing`

- Trigger request: `Add checkout, subscriptions, refunds, and entitlement state.`
- Non-trigger request: `Add a free feature with no billing state.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Use server-owned commercial state, authenticated provider events, idempotent transitions, reconciliation, and replay tests. Missing context: Product, tenant, entitlement, event, or provider model is unclear; inspect before implementing transitions. Rejected behavior: Never trust browser payment state or assume events are unique and ordered.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-ai-api-integrations`

- Trigger request: `Add RAG and an AI tool that updates customer records.`
- Non-trigger request: `Add deterministic local filtering with no model integration.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Protect keys, minimize data, authorize retrieval/tools, validate output, confirm effects, and add prompt-injection/cross-tenant tests. Missing context: Provider, model capability, data class, tenant scope, or tool authority is unclear; inspect before choosing APIs. Rejected behavior: Never treat model output, system prompts, or schema mode as authorization.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-container-runtime`

- Trigger request: `Add Docker and Kubernetes deployment for an API.`
- Non-trigger request: `Run app directly with no container artifacts.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Use minimal immutable images, non-root identity, dropped privileges, protected build secrets, health checks, and runtime tests. Missing context: Base image, runtime, orchestrator, or writable-path need is unclear; inspect before choosing directives. Rejected behavior: Never default to root, privileged mode, broad mounts, or mutable production identity.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-email-messaging`

- Trigger request: `Add password-reset email and SMS OTP.`
- Non-trigger request: `Change an in-app label without messaging.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Generate purpose-bound tokens, store verifiers safely, prevent enumeration, constrain redirects, rate-limit, and test replay. Missing context: Provider, identity binding, expiry, redirect policy, or delivery behavior is unclear; inspect before choosing SDK calls. Rejected behavior: Never use reusable codes, caller-controlled recipients, or sensitive URL/template data.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-failure-safety`

- Trigger request: `Add a multi-step mutation that calls a provider and database.`
- Non-trigger request: `Change static documentation.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Fail authorization closed, bound timeouts/retries, preserve invariants with transaction/compensation, and test injected failures. Missing context: Transaction boundary, retry semantics, or provider idempotency is unclear; inspect before implementing failure behavior. Rejected behavior: Never catch and continue with privilege or blindly retry non-idempotent writes.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-ship-check`

- Trigger request: `Finish this Firebase upload feature, run its security tests, and tell me exact console action remaining.`
- Non-trigger request: `Rewrite this marketing paragraph without reviewing or changing application behavior.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Inspect only current feature and changed files. Check selected-skill invariants, tests added and executed, accidental secrets in changed content, and exact external configuration remaining. Unrelated repository conditions do not block handoff. Never decide shipping or certify application security.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-supabase-auth`

- Trigger request: `Implement a Supabase Auth feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Supabase Auth code or configuration.`
- Dependency routing: Include `secod-core`, `secod-identity-access`, `secod-auth-provider-integrations`, `secod-supabase` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Verify sessions, use current signing-key model, and enforce identity/tenant policy through RLS and server checks. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-auth0`

- Trigger request: `Implement a Auth0 feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Auth0 code or configuration.`
- Dependency routing: Include `secod-core`, `secod-auth-provider-integrations`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Validate access tokens against fixed issuer/audience and map Auth0 subject to local identity. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-workos`

- Trigger request: `Implement a WorkOS feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no WorkOS code or configuration.`
- Dependency routing: Include `secod-core`, `secod-auth-provider-integrations`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Bind WorkOS organization and immutable subject to local tenant membership and reconcile lifecycle events. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-better-auth`

- Trigger request: `Implement a Better Auth feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Better Auth code or configuration.`
- Dependency routing: Include `secod-core`, `secod-auth-provider-integrations`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep server configuration authoritative and preserve CSRF/origin, cookie, session, and plugin boundaries. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-nextjs`

- Trigger request: `Create a Next.js App Router Server Action that updates a tenant document.`
- Non-trigger request: `Update a Vite-only static site with no Next.js dependency or convention.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent treats Server Actions and Route Handlers as directly callable server endpoints, validates and authorizes within them, uses `server-only` for privileged modules, and prevents cross-user cache leakage. It inspects the lockfile before relying on version-specific APIs and does not invent config keys when version context is missing.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-mobile-app-security`

- Trigger request: `Add persistent login, a reset deep link, photo access, and push notifications to an Android and iOS app.`
- Non-trigger request: `Change a backend-only batch job with no mobile client behavior or SDK.`
- Dependency routing: Include `secod-core`, `secod-identity-access`, `secod-data-files`, and `secod-secrets-config`; add exact mobile framework and provider adapters only when requested or detected.
- Missing-context scenario: Inspect mobile framework/version, targets, application IDs, session model, local data, link domains, permissions, notifications, provider SDKs, release variants, and tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Treat device, binary, storage, link and notification payloads as untrusted; keep secrets and authorization on backend; use platform-backed credential storage, verified links, minimal permissions/data, and release-mode tests.
- Expected rejected behavior: Reject embedded private credentials, ordinary token storage, client-authoritative tenant/object/device claims, sensitive links/notifications, broad permissions, and security certification.
- External configuration handoff: Name exact Android/iOS application, environment, association file, entitlement/manifest permission, notification credential, signing/store setting, direct official page, and verification action.
- API support boundary: Resolve mobile OS, framework, and SDK/plugin versions; use only supported documented APIs and never infer device/store/provider state.

## `secod-react-native-expo`

- Trigger request: `Implement Expo Router authentication, SecureStore persistence, Universal Links, camera permission, and notification navigation.`
- Non-trigger request: `Build a React DOM Vite page with no React Native, Expo, native target, or EAS configuration.`
- Dependency routing: Include `secod-core` and `secod-mobile-app-security`; add identity, data, messaging, and provider adapters only when feature boundaries require them.
- Missing-context scenario: Inspect lockfile, Expo SDK, React Native, Router, app config, EAS profiles, native targets/modules, provider packages, and tests; ask one narrow question only when version/workflow cannot be derived.
- Expected implementation: Keep secrets out of `EXPO_PUBLIC_` and bundle, use version-supported SecureStore/link/permission/notification APIs, authorize backend effects, isolate release profiles, and state whether tests ran in Expo Go, development build, device, or release artifact.
- Expected rejected behavior: Reject AsyncStorage token persistence, client-only navigation authorization, sensitive link/push payloads, invented Expo config keys, and claims that Expo Go proved native release behavior.
- External configuration handoff: Name exact Expo project, Android/iOS application, EAS environment/profile/channel, link association, push credential, store setting, direct official page, and verification action.
- API support boundary: Resolve installed Expo, React Native, Router, and `expo-*` versions; use matching direct docs and never invent module APIs or provider state.

## `secod-flutter`

- Trigger request: `Add Flutter mobile session storage, app links, notification actions, and signed Android/iOS release flavors.`
- Non-trigger request: `Change a Dart command-line utility that has no Flutter or mobile platform target.`
- Dependency routing: Include `secod-core` and `secod-mobile-app-security`; add identity, data, messaging, and provider adapters only when feature boundaries require them.
- Missing-context scenario: Inspect Flutter/Dart constraints, `pubspec.lock`, targets, flavors, router, plugins, manifests/entitlements, provider configuration, release signing, and tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Keep secrets and authorization server-side, use maintained version-compatible platform-backed storage, validate links and platform channels, minimize permissions/notification data, isolate flavors, and test signed release artifacts.
- Expected rejected behavior: Reject secrets in Dart/assets/defines, credentials in `shared_preferences`, client-authoritative routing/device claims, debug release configuration, invented plugin APIs, or claims that obfuscation protects secrets.
- External configuration handoff: Name exact Flutter flavor, Android/iOS application, association file, permission/entitlement, push credential, signing/store setting, direct official page, and verification action.
- API support boundary: Resolve Flutter/Dart and locked plugin/native target versions; use matching official docs and never invent plugin methods or remote state.

## `secod-vercel-platform`

- Trigger request: `Implement a Vercel Platform feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Vercel Platform code or configuration.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Separate preview/production secrets and data, authorize functions, constrain deployment access, and protect production domains. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-auth-provider-integrations`

- Trigger request: `Add Clerk authentication and a callback to this Next.js app.`
- Non-trigger request: `Add local password authentication with no third-party provider.`
- Dependency routing: Include `secod-core`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Select secod-clerk plus identity and framework dependencies; implement provider-specific callback/session code and tests. Missing context: Provider and installed SDK version are unclear; inspect imports, lockfile, callback routes, and configuration before routing. Rejected behavior: Do not select Auth0, WorkOS, Better Auth, Supabase Auth, or Cognito and do not produce account-wide findings.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-clerk`

- Trigger request: `Implement a Clerk feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Clerk code or configuration.`
- Dependency routing: Include `secod-core`, `secod-auth-provider-integrations`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Verify Clerk sessions server-side and authorize local tenant/resources independently. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare`

- Trigger request: `Add a Cloudflare Worker using Queues and Hyperdrive.`
- Non-trigger request: `Deploy an AWS Lambda with no Cloudflare signals.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Select Workers, Queues, and Hyperdrive adapters with shared token/environment defaults and required generalized dependencies. Missing context: Exact bindings and Wrangler version are unclear; inspect configuration and lockfile before routing. Rejected behavior: Do not select Pages, Vectorize, Workers AI, or AI Gateway and do not audit unrelated zones.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-workers`

- Trigger request: `Implement a Cloudflare Workers feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Workers code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare`, `secod-identity-access`, `secod-inputs-apis`, `secod-secrets-config`, `secod-abuse-limits`, `secod-data-files`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Validate and authorize requests, keep secrets in bindings, bound subrequests/resources, and separate environments. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-pages`

- Trigger request: `Implement a Cloudflare Pages feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Pages code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare`, `secod-packages-delivery`, `secod-secrets-config`, `secod-web-app-security` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Separate preview and production bindings/data, protect previews when needed, and authorize Pages Functions server-side. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-queues`

- Trigger request: `Implement a Cloudflare Queues feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Queues code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare`, `secod-inputs-apis`, `secod-abuse-limits`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Validate messages, make consumers idempotent, bound retries/batches, and route poison messages safely. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-workflows`

- Trigger request: `Implement a Cloudflare Workflows feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Workflows code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare`, `secod-inputs-apis`, `secod-abuse-limits`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Validate events, make steps replay-safe, authorize starts/signals, and bound retries and retained sensitive state. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-hyperdrive`

- Trigger request: `Implement a Cloudflare Hyperdrive feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Hyperdrive code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare-workers`, `secod-secrets-config`, `secod-inputs-apis`, `secod-data-files` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep credentials in bindings/secrets, verify database identity with TLS, and authorize/query safely in Worker code. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-vectorize`

- Trigger request: `Implement a Cloudflare Vectorize feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Vectorize code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-data-files`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Encode tenant/resource scope in trusted metadata filters and authorize retrieval before returning matches. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-workers-ai`

- Trigger request: `Implement a Cloudflare Workers AI feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare Workers AI code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-abuse-limits`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use bindings or scoped tokens server-side, constrain model/input/output, authorize tools/retrieval, and bound usage. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-cloudflare-ai-gateway`

- Trigger request: `Implement a Cloudflare AI Gateway feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Cloudflare AI Gateway code or configuration.`
- Dependency routing: Include `secod-core`, `secod-cloudflare`, `secod-ai-api-integrations`, `secod-secrets-config`, `secod-abuse-limits`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Authenticate gateway use, protect provider keys, minimize/redact logs, constrain cache/route scope, and preserve application authorization. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-supabase`

- Trigger request: `Create tenant projects in Supabase with browser reads, server administration, and private Storage.`
- Non-trigger request: `Create tenant documents in Firestore with no Supabase dependency or configuration.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent enables RLS and writes explicit tenant/member policies, preserves caller identity for ordinary requests, confines secret/service authority to trusted server paths, and tests owner, member, cross-tenant, unauthenticated, Storage, and elevated-operation cases. Missing schema or JWT claim context is resolved before emitting policy SQL.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-firebase`

- Trigger request: `Add Firebase Auth, tenant Firestore documents, Storage uploads, and App Check to this app.`
- Non-trigger request: `Add authentication using Supabase; Firebase is not installed or referenced.`
- Dependency routing: Include `secod-core`, `secod-identity-access`, `secod-secrets-config`, `secod-abuse-limits`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent implements least-privilege client access through Rules, uses Admin SDK only in trusted server code with independent authorization, and adds Emulator tests for owner, cross-tenant, unauthenticated, invalid-metadata, and oversized-upload cases. If deployed App Check enforcement is inaccessible, it supplies exact deployment steps and states only that the setting was not inspected.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-neon`

- Trigger request: `Implement a Neon feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Neon code or configuration.`
- Dependency routing: Include `secod-core`, `secod-identity-access` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use scoped roles, TLS, parameterized queries, safe branch/environment separation, and bounded pooling. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-convex`

- Trigger request: `Implement a Convex feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Convex code or configuration.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Authorize every public function with trusted identity, validate arguments, and prevent cross-tenant reads/writes. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-aws-web`

- Trigger request: `Add an AWS Lambda API backed by DynamoDB.`
- Non-trigger request: `Add a Google Cloud Run service with no AWS signals.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Select Lambda/API Gateway and data-services adapters, apply short-lived identity and scoped IAM defaults, then implement tests. Missing context: Exact AWS services, SDK versions, account, Region, and workload identity are unclear; inspect code and IaC before routing. Rejected behavior: Do not select Cognito or S3/CloudFront without use and do not inventory the whole AWS account.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-aws-lambda-api-gateway`

- Trigger request: `Implement a AWS Lambda and API Gateway feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no AWS Lambda and API Gateway code or configuration.`
- Dependency routing: Include `secod-core`, `secod-aws-web`, `secod-identity-access`, `secod-inputs-apis`, `secod-abuse-limits`, `secod-secrets-config` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use minimal execution roles, explicit invocation permissions, route authorization, schema validation, and bounded concurrency/retries. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-aws-cognito`

- Trigger request: `Implement a AWS Cognito feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no AWS Cognito code or configuration.`
- Dependency routing: Include `secod-core`, `secod-aws-web`, `secod-identity-access`, `secod-auth-provider-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Verify Cognito tokens and app-client purpose, constrain federation, and keep application authorization independent. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-aws-s3-cloudfront`

- Trigger request: `Implement a AWS S3 and CloudFront feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no AWS S3 and CloudFront code or configuration.`
- Dependency routing: Include `secod-core`, `secod-aws-web`, `secod-data-files`, `secod-secrets-config`, `secod-abuse-limits` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep S3 private, use scoped object authorization and Origin Access Control, and bound presigned operations. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-aws-data-services`

- Trigger request: `Implement a AWS Data Services feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no AWS Data Services code or configuration.`
- Dependency routing: Include `secod-core`, `secod-aws-web`, `secod-data-files`, `secod-inputs-apis`, `secod-secrets-config`, `secod-observability-response` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use service-specific least privilege, private connectivity, encryption, parameterized access, and tenant-safe data keys. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-google-cloud-web`

- Trigger request: `Add private Cloud Storage uploads to a Google Cloud application.`
- Non-trigger request: `Add Firebase Auth only; no general Google Cloud service adapter is required beyond Firebase routing.`
- Dependency routing: Include `secod-core` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Select Google Cloud Storage with shared project/IAM defaults; select Firebase only when Firebase products are used. Missing context: Exact Google Cloud products, client versions, project, location, and workload identity are unclear; inspect code and IaC before routing. Rejected behavior: Do not select Firebase for unrelated Google Cloud code and do not audit organization-wide settings.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-google-cloud-storage`

- Trigger request: `Implement a Google Cloud Storage feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Google Cloud Storage code or configuration.`
- Dependency routing: Include `secod-core`, `secod-google-cloud-web`, `secod-data-files`, `secod-secrets-config`, `secod-abuse-limits` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use uniform access where appropriate, dedicated identities, private defaults, bounded signed URLs, and object authorization. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-stripe`

- Trigger request: `Add Stripe Checkout, a webhook, and subscription entitlements.`
- Non-trigger request: `Add a free local feature with no payment, billing, entitlement, or Stripe integration.`
- Dependency routing: Include `secod-core`, `secod-payments-billing` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent keeps secret keys server-side, separates test/live configuration, derives price and customer ownership from trusted storage, passes idempotency keys for retryable mutations, verifies webhooks over raw bytes, and grants entitlement from verified Stripe state rather than redirects. Tests cover duplicates, out-of-order events, invalid signatures, and tenant mismatch.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-polar`

- Trigger request: `Implement a Polar feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Polar code or configuration.`
- Dependency routing: Include `secod-core`, `secod-payments-billing` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep organization tokens server-side, use trusted product/customer mapping, verify webhooks, deduplicate events, and reconcile benefits. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-lemonsqueezy`

- Trigger request: `Implement a Lemon Squeezy feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Lemon Squeezy code or configuration.`
- Dependency routing: Include `secod-core`, `secod-payments-billing` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep API keys server-side, trust server-owned variants, verify webhook signatures, deduplicate, and reconcile entitlement/license state. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-dodo-payments`

- Trigger request: `Implement a Dodo Payments feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Dodo Payments code or configuration.`
- Dependency routing: Include `secod-core`, `secod-payments-billing` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep API keys server-side, trust catalog/customer state, verify webhooks, deduplicate events, and reconcile entitlements. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-whop`

- Trigger request: `Implement a Whop feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Whop code or configuration.`
- Dependency routing: Include `secod-core`, `secod-payments-billing` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Use correct key type server-side, bind company/user/resource ownership, verify webhooks, and reconcile access state. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-openai`

- Trigger request: `Add an OpenAI Responses API assistant that can call a refund tool and return structured JSON.`
- Non-trigger request: `Add deterministic local search with no model, OpenAI SDK, endpoint, or credential.`
- Dependency routing: Include `secod-core`, `secod-ai-api-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: The agent uses the installed OpenAI SDK's documented interfaces, holds API keys on the server, minimizes transmitted data, validates structured output, treats model-selected tools/arguments as untrusted, and independently authorizes tool execution. Tests cover unknown tools, invalid schema, cross-tenant identifiers, prompt injection, timeout, and confirmation denial.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-anthropic`

- Trigger request: `Implement a Anthropic feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Anthropic code or configuration.`
- Dependency routing: Include `secod-core`, `secod-ai-api-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep keys server-side, minimize data, validate tool inputs/output, authorize effects, and bound tokens/retries. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-google-genai`

- Trigger request: `Implement a Google GenAI feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Google GenAI code or configuration.`
- Dependency routing: Include `secod-core`, `secod-ai-api-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep standard keys server-side, use ephemeral tokens only for documented Live API cases, validate tools/output, and preserve tenant scope. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-xai-grok`

- Trigger request: `Implement a xAI Grok feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no xAI Grok code or configuration.`
- Dependency routing: Include `secod-core`, `secod-ai-api-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Separate management and inference keys, constrain ACLs/models/spend, validate tools/output, and protect tenant data. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.

## `secod-vercel-ai`

- Trigger request: `Implement a Vercel AI SDK feature using the installed provider SDK and add security tests.`
- Non-trigger request: `Change unrelated documentation with no Vercel AI SDK code or configuration.`
- Dependency routing: Include `secod-core`, `secod-ai-api-integrations` plus only task-applicable transitive dependencies; exclude unused providers.
- Missing-context scenario: Inspect repository, lockfiles, runtime configuration, trust boundaries, and existing tests; ask one narrow question only when required context cannot be derived.
- Expected implementation: Resolve and state exact SDK/runtime/API version. Keep credentials server-side, validate tools/output, authorize effects, constrain model routing, and protect streamed tenant data. Follow direct official documentation, preserve local authorization, and add positive and negative tests. Never invent provider APIs, claim inaccessible settings were checked, or emit an account-wide scanner verdict.
- Expected rejected behavior: Reject client-controlled authority, unsafe shortcuts, documentation-only test claims, external-setting claims without access, and application-security certification.
- External configuration handoff: Name exact provider, project/account, environment, setting, direct official page, and verification action without blocking unrelated repository-owned implementation.
- API support boundary: Resolve installed SDK/runtime/API version and use only APIs supported by direct official documentation; never invent methods, options, capabilities, or dashboard state.
