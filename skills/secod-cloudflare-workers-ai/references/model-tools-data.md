# Cloudflare Workers AI: secure implementation recipe

## Security boundaries

- Keep long-lived provider and management credentials server-side.
- Treat model input, output, retrieved content, and tool arguments as untrusted.
- Authorize retrieval and every tool effect against trusted user/tenant/resource state.
- Minimize data and bound model, token, file, stream, retry, and spending scope.
- Use bindings or scoped tokens server-side, constrain model/input/output, authorize tools/retrieval, and bound usage.

Keep credentials server-side. Treat model input, output, retrieval, and tool arguments as untrusted. Authorize tool effects deterministically and isolate tenant data.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
