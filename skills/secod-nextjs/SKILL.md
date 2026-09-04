---
name: secod-nextjs
description: Satisfy every applicable general baseline requirement; apply when the next package, next.config.*, App Router, Pages Router, Route Handlers/API Routes, Server Actions,…
---

# SECOD Next.js

## Scope and applicability

Satisfy every applicable general baseline requirement; apply when the `next` package,
`next.config.*`, App Router, Pages Router, Route Handlers/API Routes, Server Actions,
Proxy/Middleware or Next.js build output is detected; require supported, security-patched
Next.js and React versions and verify controls against the application's actual router, build,
runtime and deployment topology.

## Control requirements

Inventory the exact Next.js/React versions, package lock, App versus Pages Router, Node versus
Edge runtime, static export, self-hosted/serverless deployment and official security advisories;
inventory App Router pages/layouts/Route Handlers/Server Actions and Pages Router pages/API
Routes plus `getServerSideProps`, `getStaticProps` and `getStaticPaths`; enforce React Server
Component versus Client Component boundaries, `server-only` imports, a server-only Data Access
Layer with authorization close to data access, minimal DTOs and optional tainting as defense in
depth; prohibit secrets, privileged objects and unnecessary fields crossing RSC serialization,
props, Server Action closures, hydration data or client bundles; review every `NEXT_PUBLIC_*`
variable and build-time environment-value freezing; when `output: 'export'` is used, identify
unavailable server protections and prohibit client-only authentication or authorization
assumptions; treat every Server Action/Server Function as a directly reachable public POST
endpoint and require per-action authentication, resource/tenant authorization, argument/schema
validation, safe return-value minimization, rate/cost limits, idempotency where needed and safe
error handling; configure the narrowest `serverActions.allowedOrigins` and
`serverActions.bodySizeLimit`; store `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` as a secret, validate
its base64-encoded AES key length, consistently provision it across multi-instance deployments,
plan rotation and rolling-deployment compatibility, and set a deployment identifier where
version skew is possible; treat Route Handlers, API Routes, dynamic route parameters, rewrites,
redirects, Preview/Draft Mode endpoints and metadata/image-generation handlers as public input
boundaries; never rely on layouts, UI hiding or Proxy/Middleware alone for authorization; audit
Proxy/Middleware matchers, negative matches, rewrites, RSC/data requests, prefetches, alternate
path encodings and client-supplied internal framework headers with bypass tests; keep per-
user/per-tenant cached data isolated, derive authorization before cache lookup, include stable
non-secret tenant/user scope in cache keys, keep secrets and sensitive personal data out of
plaintext cache keys/tags, choose `use cache`, `use cache: private` and remote caches according
to sensitivity, and invalidate authorization-sensitive data after mutations, logout,
role/ownership changes and revocation; coordinate cache tags and shared cache behavior across
instances; test cache-key confusion/poisoning, RSC payload/header variance, CDN cache behavior
and cross-tenant responses; review `next/image` `remotePatterns`/`localPatterns`, redirect
limits and `dangerouslyAllowLocalIP`, keep `dangerouslyAllowSVG` disabled unless required, and
if enabled force attachment plus restrictive image CSP/sandboxing; keep production browser
source maps disabled, or privately upload and remove them from public artifacts when
operationally required, because enabling `productionBrowserSourceMaps` makes them publicly
served; inspect `.next`, standalone and deployment artifacts for source, stack, environment, RSC
payload and secret disclosure; review `next.config.*` security headers/CSP, powered-by
disclosure, experimental flags and production/development parity; run negative tests through
`next build` plus the production runtime rather than relying only on development mode.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
