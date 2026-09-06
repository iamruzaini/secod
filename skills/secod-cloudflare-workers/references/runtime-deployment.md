# Cloudflare Workers: secure implementation recipe

## Security boundaries

- Keep privileged credentials and provider management calls server/runtime-only.
- Authenticate, validate, and authorize every reachable handler or event boundary.
- Separate production, preview, and development resources/configuration.
- Bound concurrency, retries, subrequests, execution time, and failure effects.
- Validate and authorize requests, keep secrets in bindings, bound subrequests/resources, and separate environments.

Keep deployment bindings, execution identity, public routes, retries, background effects, and environment separation explicit. Use least privilege and bounded failure behavior.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
