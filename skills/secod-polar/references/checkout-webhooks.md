# Polar: secure implementation recipe

## Security boundaries

- Resolve product, price, customer, tenant, and entitlement from trusted server state.
- Keep secret credentials server-side and separate test/live environments.
- Verify webhook authenticity over required raw payload and deduplicate durable event IDs.
- Grant access only from verified provider state and reconcile delayed/out-of-order events.
- Keep organization tokens server-side, use trusted product/customer mapping, verify webhooks, deduplicate events, and reconcile benefits.

Resolve products, prices, customers, tenants, and entitlements from server-owned state. Verify raw webhook payloads before parsing, deduplicate durable event IDs, and reconcile delayed events.

## Implementation sequence

1. Record exact package/runtime/API version and selected product feature.
2. Use direct documentation matching that version or API surface.
3. Adapt official example to repository architecture; do not copy secret values or omit local authorization.
4. Compile/type-check and run provider mocks, emulators, sandboxes, or local tests available to project.
5. Test rejected and failure paths before handoff.

## External configuration

Name project/account/resource, environment, Region/location where relevant, setting, and official verification path without asserting inaccessible state.
