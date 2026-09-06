<!-- SECOD template for a framework-specific secure implementation skill. -->

---
name: <secod-framework>
description: >-
  Help AI coding agents implement secure <framework> web or mobile features using
  its current execution model and APIs. Use when <framework-specific triggers>.
license: Apache-2.0
compatibility: "Requires a <framework> project; recipes state supported versions."
metadata:
  secod-category: "framework"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# Secure <framework> implementation

## Purpose

Translate SECOD's generalized security invariants into the framework's actual routing, rendering, data-loading, mutation, caching, middleware, and deployment model. Help the agent put enforcement in the correct runtime boundary and use APIs supported by the project's version.

## When to use

Use when the repository or request uses <framework> for:

- <route/handler/action pattern>;
- <rendering/data-loading pattern>;
- <middleware/server/client boundary>.

Do not activate for projects that merely contain <similar package or unrelated tool>.

## Context to inspect

- Exact framework, runtime, router, and deployment versions.
- Server-only, client, middleware, edge, worker, and build-time boundaries.
- Route handlers, actions/mutations, loaders, middleware, and caching behavior.
- Authentication/session integration and authorization location.
- Existing validation, error handling, headers, tests, and framework configuration.
- Providers selected for the current feature.

## Framework security invariants

- Privileged code and credentials never enter the client bundle.
- Authorization executes at the trusted data/effect boundary, not only in UI or middleware.
- Framework caching cannot mix users, tenants, permissions, or sensitive responses.
- Inputs crossing route/action boundaries are validated server-side.
- Redirects, errors, rendering, and serialization do not leak sensitive data.
- Version-specific APIs are confirmed before use.

## Secure defaults

- Prefer server-only modules for privileged SDKs and credentials.
- Keep request-specific authorization near each protected read or mutation.
- Opt sensitive or identity-dependent data out of shared caching unless isolation is proven.
- Use framework-native security primitives when they enforce the invariant at the correct boundary.
- Keep security headers and platform configuration compatible with the application's actual content and integrations.

## Implementation workflow

1. Confirm the framework version and execution boundary.
2. Map the feature to route, action, loader, component, middleware, and deployment responsibilities.
3. Select relevant generalized and provider skills.
4. Implement the framework recipe for the current feature.
5. Test server/client separation, authorization, caching, serialization, and failure behavior.
6. Confirm any version-sensitive API against direct official documentation.

## Implementation recipes

- [`references/<version>-<feature>.md`](references/<version>-<feature>.md) — <framework version and feature>.
- [`references/<runtime>-boundaries.md`](references/<runtime>-boundaries.md) — <runtime-specific guidance>.
- [`references/security-headers.md`](references/security-headers.md) — <when headers are in scope>.

Recipes should include safe code that matches supported framework APIs, not framework-neutral pseudocode presented as runnable code.

## Unsafe patterns to avoid

- Treating middleware as the only authorization layer.
- Importing server secrets or privileged SDKs through client-reachable modules.
- Caching authenticated or tenant-specific data under a shared key.
- Trusting client-side validation or hidden UI as access control.
- Copying an example written for a different framework version or runtime.

## Tests to add

- Protected routes/actions reject missing and insufficient identity.
- Cross-tenant access fails at the data boundary.
- Privileged modules and secrets are absent from client artifacts.
- User-specific content is not served from another user's cache context.
- Malformed input fails before side effects.
- Error and redirect behavior reveals no sensitive implementation detail.

## Provider and deployment steps

Include only framework hosting settings required by the feature, such as environment-variable scope, runtime selection, headers, or cache configuration. Name exact verification steps and never imply that an inaccessible deployment was inspected.

## Official sources

Use [`references/sources.md`](references/sources.md). Record the framework documentation homepage, official `llms.txt` endpoint when available, and direct version-relevant pages supporting each recipe.

## Completion handoff

State the framework boundary used, security decisions implemented, versions assumed, tests run, and exact deployment steps left to the user.
