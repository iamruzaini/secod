# Supabase Auth: secure implementation recipe

## Security boundaries

- Validate provider credentials and tokens at trusted server boundary.
- Keep client/server redirect, cookie, state, nonce, PKCE, and secret boundaries intact.
- Map provider identity to local user/tenant using immutable identifiers.
- Authorize each application resource and action independently.
- Verify sessions, use current signing-key model, and enforce identity/tenant policy through RLS and server checks.

Keep callbacks, sessions, token validation, immutable subject mapping, tenant membership, and local authorization explicit. Provider authentication never replaces application authorization.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
