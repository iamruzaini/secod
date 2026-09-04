# Polar capability map

Use this map after discovery and before making a claim about a Polar-specific API or dashboard
behavior. It translates the retained official pages into inspection targets; it does not prove the
project's deployed configuration.

## Authentication and environments

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Core API | OAT authorizes organization-level resources, including checkout, orders, subscriptions, benefits, and refunds. | Require a server-only, scope-limited OAT with expiry and exact organization evidence. |
| Customer Portal API | A backend creates a Customer Access Token for a customer session; it is restricted to that customer's surface and cannot perform privileged organization mutations. | Require backend authorization from application user/tenant to the requested Polar customer before issuing it. |
| Sandbox | Sandbox data, organizations, users, and tokens are isolated; use `sandbox-api.polar.sh` and a sandbox token. | Compare the actual API host, SDK environment parameter, account, and organization; no test/live token reuse. |
| SDKs | The current API overview labels the new TypeScript/Python SDKs public preview. | Capture resolved and deployed version; do not infer API behavior from a package range or preview example. |
| Changelog | Polar publishes Product Updates; its separately discovered API changelog was not directly retrievable during this review. | Review current release notes and direct API reference before an upgrade; mark API-changelog-only deprecation claims Not verified. |

## Checkout and state

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Checkout session | Requires checkout write authority; accepts customer/external customer IDs, metadata, and `embed_origin`. `confirmed` means Pay was clicked, not that payment succeeded. | Server owns product/price/tenant/customer/origin selection. Prohibit redirect or `confirmed` grants. |
| Customer State | Carries current active subscriptions and granted benefits; `customer.state_changed` covers customer, subscription, and benefit changes. | Prefer verified state/event transitions over UI claims. Bind retrieved state to the exact Polar customer and local tenant. |
| Refunds | A refund can revoke one-time-purchase benefits, but refunding a subscription order does not end that subscription; cancellation/revocation does. | Test and reconcile refund, cancellation, revocation, and benefit-grant rules separately. |

## Webhooks and operations

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Endpoint setup | Custom application integrations should use `raw` JSON format. Polar signs requests and follows Standard Webhooks. | Require dashboard endpoint URL, format, secret reference, enabled state, and event subscriptions as redacted evidence. |
| Verification | Polar SDK helpers validate/parse a raw request body; Standard Webhooks signs the ID, timestamp, and body. | Verify before parsing or effects; require all three headers, a documented tolerance, and durable delivery-ID uniqueness. |
| Delivery | Polar retries errors up to 10 times with exponential backoff, times out after 10 seconds, recommends response within two seconds, and treats redirects as failures. | Verify → durable handoff → quick response; use a worker/outbox and test timeout, retry, and redirect behavior. |
| Disablement | Ten consecutive non-2xx deliveries automatically disable an endpoint and notify organization members. | Require monitoring/ownership and a reconciliation plan. Do not claim the alert works without dashboard or alert-test evidence. |
| Rate limits | The API overview documents per-environment limits and a `429` with `Retry-After`. | Bound outbound retries, honor `Retry-After`, and test exhaustion; do not assert a fixed quota without current direct evidence. |

## Lifecycle event minimum

The exact set must match the application's products and entitlement model. At minimum evaluate
`order.paid`, `order.refunded`, subscription updates/cancellation/revocation, benefit grant
creation/revocation, and `customer.state_changed` when customer state drives access. The official
event page documents that delayed and ordered sequences exist; the application must be idempotent
and converge through reconciliation rather than assume arrival order proves current state.
