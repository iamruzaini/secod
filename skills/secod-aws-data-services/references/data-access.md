# AWS Data Services: secure implementation recipe

## Security boundaries

- Authorize every query/object against trusted user, tenant, and ownership state.
- Use parameterized/structured APIs and least-privilege workload credentials.
- Keep data private by default and bound query, upload, result, and connection resources.
- Test cross-tenant, unauthorized, malformed, duplicate, and dependency-failure paths.
- Use service-specific least privilege, private connectivity, encryption, parameterized access, and tenant-safe data keys.

Keep credentials server-side, authorize every record or object against trusted tenant state, use structured queries, constrain resource use, and make private access default.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
