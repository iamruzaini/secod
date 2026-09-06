---
name: secod-nextjs
description: >-
  Help coding agents implement secure Next.js features across App Router or Pages
  Router, Server Components, Server Actions, route handlers, API routes, caching,
  cookies, and server/client module boundaries.
license: Apache-2.0
compatibility: "Requires a Next.js project; inspect lockfile and router before choosing APIs."
metadata:
  secod-category: "framework"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Next.js implementation

## Purpose

Place validation, authorization, secrets, data access, and side effects in correct Next.js runtime
boundary using APIs supported by project's resolved version.

## When to use

Use for App/Pages Router, Server Components, Server Actions, route/API handlers, Proxy/Middleware,
cookies, caching, image/redirect configuration, or Next.js server/client boundaries. Do not activate
for React-only projects without Next.js.

## Context to inspect

Resolve `next`, React, router, runtime, deployment target, server/client modules, auth integration,
data access, cache behavior, route/action inputs, cookies, headers, and nearby tests.

## Secure defaults

- Keep privileged SDKs and environment access in `server-only` modules.
- Treat Server Actions and route handlers as directly reachable endpoints.
- Authenticate and authorize inside each protected action/handler or trusted data-access function.
- Validate action/route arguments and return minimal data-transfer objects.
- Avoid shared caching for identity-, tenant-, or permission-dependent data unless keying/isolation is proven.
- Perform mutations only in explicit actions/handlers, never during rendering.

## Implementation workflow

1. Confirm resolved Next.js version and router.
2. Map component, action/handler, data layer, cache, provider, and client boundaries.
3. Select generalized/provider skills for feature.
4. Implement thin action/handler and server-only authorized data layer.
5. Add direct-request, unauthorized, cross-tenant, validation, cache-isolation, and client-bundle tests.

## Implementation recipes

- [`references/app-router-boundaries.md`](references/app-router-boundaries.md) — App Router server
  action/route and data-access pattern.

## Unsafe patterns to avoid

- Relying on hidden UI, Proxy/Middleware, or action IDs for authorization.
- Importing privileged code through a client-reachable module.
- Trusting Server Action arguments or returning whole database/provider records.
- Caching personalized data under shared keys.

## Tests to add

Test direct action/route invocation, unauthenticated and cross-tenant access, malformed arguments,
minimal response shape, server-only module isolation, cache separation, and safe redirects/errors.

## Provider and deployment steps

Hosting adapter owns environment scope, runtime, headers, preview protection, and deployment checks.
Do not infer Vercel merely from Next.js.

## Official sources

Use [`references/sources.md`](references/sources.md). Read official `llms.txt` for discovery, then
direct version-relevant pages.

## Completion handoff

State router/version, trusted boundary, code/tests changed, cache decisions, and deployment actions.
Do not issue launch or security verdicts.
