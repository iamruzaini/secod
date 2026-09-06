# Whop: secure implementation recipe

## Security boundaries

- Resolve product, price, customer, tenant, and entitlement from trusted server state.
- Keep secret credentials server-side and separate test/live environments.
- Verify webhook authenticity over required raw payload and deduplicate durable event IDs.
- Grant access only from verified provider state and reconcile delayed/out-of-order events.
- Use correct key type server-side, bind company/user/resource ownership, verify webhooks, and reconcile access state.

Resolve products, prices, customers, tenants, and entitlements from server-owned state. Verify raw webhook payloads before parsing, deduplicate durable event IDs, and reconcile delayed events.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
