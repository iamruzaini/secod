# Next.js capability map

Use this map after discovery and before making a claim about Next.js-specific framework or runtime
behavior. It translates retained official documentation into concrete inspection targets; it does
not prove the project's deployed configuration. Sources are recorded in [sources.md](sources.md);
every section below traces to a `NEXTJS-SRC-*` entry.

## Contents

1. [Runtime and router topology](#runtime-and-router-topology)
2. [React Server Components and Data Access Layer](#react-server-components-and-data-access-layer)
3. [Environment variables and static export](#environment-variables-and-static-export)
4. [Server Actions security and public exposure](#server-actions-security-and-public-exposure)
5. [Server Actions configuration and multi-instance](#server-actions-configuration-and-multi-instance)
6. [Public route surfaces and proxy/middleware](#public-route-surfaces-and-proxymiddleware)
7. [Caching and Cache Components](#caching-and-cache-components)
8. [Image optimization and sandboxing](#image-optimization-and-sandboxing)
9. [Source maps and build artifact hygiene](#source-maps-and-build-artifact-hygiene)

## Runtime and router topology

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Router architecture | App Router (`app/`) uses React Server Components, Route Handlers, and Server Actions; Pages Router (`pages/`) uses Pages, API Routes, `getServerSideProps`, `getStaticProps`. | Identify coexisting routers; ensure security policies cover both App and Pages paths. |
| Runtime environments | Server components and routes run on Node.js runtime or Edge runtime (`runtime: 'nodejs' \| 'edge'`). | Check Edge runtime limitations (crypto APIs, dynamic code, package support); verify Node runtime security controls. |
| Supported versions | Active Next.js versions receive security patches and CVE fixes; outdated releases contain known vulnerabilities. | Inventory exact `next` and `react` versions from lockfile; cross-check GitHub Security Advisories (`NEXTJS-SRC-ADVISORIES`). |
| Deployment target | Deployments can be Vercel, containerized Node.js (`output: 'standalone'`), custom server, or static export (`output: 'export'`). | Verify topology-specific security: multi-instance key sharing, cache stores, reverse proxy headers. |

## React Server Components and Data Access Layer

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| RSC vs Client boundary | Server Components run on the server and never bundle into client JavaScript; Client Components prerender on server then hydrate in browser. | Enforce clear component boundaries; ensure Client Components receive only sanitized public DTOs. |
| `server-only` isolation | `import 'server-only'` causes a build error if the module is imported into a Client Component bundle. | Require `server-only` on all Data Access Layer (DAL), database, and secret-handling modules. |
| Data Access Layer (DAL) | Centralized internal library running only on server, checking authorization close to data access, returning minimal DTOs. | Prohibit direct database queries in UI components; ensure authorization occurs in DAL before data retrieval. |
| DTO minimization | Server-to-client props, hydration payloads, and RSC serialization transmit over the wire to browser. | Return narrow DTOs (`{ id, name }`); never pass full database model records or privileged objects. |
| React Taint APIs | `experimental_taintObjectReference` and `experimental_taintUniqueValue` block specific objects/values from client serialization (`experimental.taint: true`). | Use taint APIs as defense-in-depth to catch accidental leaks of sensitive records or tokens. |

## Environment variables and static export

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Variable prefixing | Variables prefixed with `NEXT_PUBLIC_` are inlined into client JavaScript bundles at build time; non-prefixed variables remain server-only. | Audit all `NEXT_PUBLIC_*` variables; assert zero secret keys, tokens, or private endpoints are exposed. |
| Build-time freezing | `NEXT_PUBLIC_*` values are frozen during `next build`. Dynamic runtime changes do not update client bundles without a rebuild. | Review staging/production build pipelines for environment value drift or accidental secret baking. |
| Static export mode | `output: 'export'` generates static HTML/CSS/JS without a Node.js server runtime. Server Actions, Route Handlers, headers, and middleware are unavailable. | Prohibit server-side auth/authz assumptions when `output: 'export'` is active; route client auth to external APIs. |

## Server Actions security and public exposure

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Public POST endpoints | Every exported `'use server'` function is reachable via a direct public HTTP POST request by anyone knowing or generating its action ID. | Treat every Server Action as a public endpoint; require per-action authentication and tenant authorization. |
| Action ID generation | Compiler generates encrypted action IDs cached up to 14 days or regenerated upon rebuild; dead-code elimination drops unused actions. | Do not rely on unguessable action IDs for security; always perform server-side authorization inside the action. |
| Input validation | Client input (FormData, serialized JSON arguments) is completely untrusted and modifiable. | Validate all arguments with strict schemas (e.g., Zod) inside the Server Action or DAL before execution. |
| Return value filtering | Return values are serialized and returned in the HTTP response to the client. | Return only minimal success flags or UI-safe DTOs; never return updated database rows with internal fields. |
| Render side effects | Next.js disallows cookie setting and cache invalidation inside render methods. Mutations must happen in Server Actions. | Assert mutations occur only in Server Actions or Route Handlers, never during page/component render. |

## Server Actions configuration and multi-instance

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Allowed origins | `serverActions.allowedOrigins` configures extra safe domains for Server Action POST requests (comparing `Origin` to `Host` / `X-Forwarded-Host`). | Set narrow allowed origins when using reverse proxies or custom CDN hosts to prevent CSRF. |
| Body size limit | `serverActions.bodySizeLimit` sets the maximum raw POST body size (default 1MB). | Configure appropriate limits; account for 10–20 KB multipart encoding overhead to avoid DoS. |
| Encryption key consistency | Closed-over variables in Server Actions are encrypted with an AES key generated at build time. Multi-instance setups need `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`. | Require base64-encoded 16/24/32-byte AES key configured consistently across all cluster instances and rolling deploys. |
| Version skew protection | `deploymentId` in `next.config.*` configures a unique deployment identifier for skew protection and cache busting. | Provision `deploymentId` across rolling deployments to prevent old clients invoking mismatched action signatures. |

## Public route surfaces and proxy/middleware

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Route Handlers & APIs | `app/**/route.ts` and `pages/api/**` accept HTTP requests (GET, POST, PUT, DELETE, PATCH) directly from the public internet. | Enforce authentication, resource authorization, rate limiting, and schema validation on every route handler. |
| Dynamic route params | `[param]`, `[...slug]`, and query parameters are unvalidated user-controlled input strings. | Validate and sanitize all path parameters before database queries or external API calls. |
| Draft / Preview mode | `draftMode().enable()` sets a secure bypass cookie for CMS previewing. | Authenticate CMS webhook/preview requests with secret tokens; prevent public arbitrary preview activation. |
| Proxy / Middleware role | `proxy.ts` (or `middleware.ts`) runs before route rendering; useful for redirects, rewrites, and header decoration. | Never rely on proxy/middleware alone for authorization; verify auth inside page DALs and route handlers. |
| Matcher & bypass audit | Proxy matchers (`config.matcher`) may fail to match alternate encodings, prefetch requests, or internal framework headers (`_next/data`, RSC headers). | Audit regex matchers against negative matches and bypass patterns; test with bypass probe requests. |

## Caching and Cache Components

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Cache Components model | `cacheComponents: true` prerenders static shells; request-time session reads sit behind `<Suspense>`. | Keep session reads (`cookies()`, `headers()`) inside `<Suspense>` boundaries and out of top-level layouts. |
| Private vs shared cache | `use cache: private` caches in browser only (reads `cookies()`, `headers()`); plain `use cache` / `use cache: remote` caches on server. | Use `use cache: private` for session-dependent data; pass explicit user/tenant IDs to plain `use cache` functions. |
| Cache key scoping | Server cache keys are derived from function arguments. | Include stable non-secret user/tenant IDs in cache keys; never store secrets or PII in plaintext cache tags. |
| Cache invalidation | `cacheTag()`, `revalidateTag()`, `revalidatePath()`, `updateTag()` invalidate cached entries on mutation. | Trigger revalidation on user logout, role change, ownership transfer, or data mutation; coordinate across instances. |
| Multi-instance caching | Multi-server deployments require shared cache handlers (`cacheHandlers` / incremental cache handler). | Configure shared remote cache (e.g., Redis) or ensure local caches do not serve stale or cross-tenant data. |

## Image optimization and sandboxing

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Remote image domains | `images.remotePatterns` restricts domains and protocols from which Next.js will fetch and optimize images. | Require strict hostname and path patterns; avoid overly broad wildcards (`**`) that permit arbitrary remote fetching. |
| Local IP SSRF protection | `images.dangerouslyAllowLocalIP` blocks private/loopback IP optimization by default (`false`). | Keep `dangerouslyAllowLocalIP: false` to prevent Server-Side Request Forgery against internal infrastructure. |
| SVG image sandboxing | `images.dangerouslyAllowSVG` allows SVG optimization (disabled by default). | If enabled, require `contentDispositionType: 'attachment'` and restrictive `contentSecurityPolicy` to prevent XSS. |
| Redirect limits | `images.maximumRedirects` limits HTTP redirects when fetching upstream images. | Set bounded redirect limits to prevent redirect loops or open redirect SSRF attacks. |

## Source maps and build artifact hygiene

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Production source maps | `productionBrowserSourceMaps` outputs `.map` files in `.next/static` and serves them publicly (disabled by default). | Keep disabled (`false`), or privately upload to error trackers and strip from public web server artifacts. |
| Build artifact inspection | `.next/` and standalone build outputs contain compiled chunks, server bundles, and embedded manifests. | Inspect build output for accidental secret inlining, server code in client chunks, or exposed stack traces. |
| Powered-by header | Next.js adds `X-Powered-By: Next.js` header by default. | Disable via `poweredByHeader: false` in `next.config.*` to minimize technology disclosure. |
| Security headers | `headers()` in `next.config.*` configures HTTP response headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy). | Verify comprehensive security headers and Content Security Policy across all application routes. |
