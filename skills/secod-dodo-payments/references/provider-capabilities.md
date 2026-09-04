# Dodo Payments capability map

Use this map after discovery and before making a claim about a Dodo-specific API or dashboard
behavior. It translates the retained official pages into inspection targets; it does not prove
the project's deployed configuration. Sources are recorded in
[sources.md](sources.md); every row below must remain traceable to a `DODO-SRC-*` entry.

## Contents

1. [Authentication and environments](#authentication-and-environments)
2. [Checkout and state](#checkout-and-state)
3. [Webhooks and delivery](#webhooks-and-delivery)
4. [Lifecycle events](#lifecycle-events)
5. [Outbound idempotency](#outbound-idempotency)

## Authentication and environments

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| API authentication | Bearer API key (`DODO_PAYMENTS_API_KEY`); keys carry `dodo_test_...` or `dodo_live_...` prefixes. | Require server-only storage, mode prefix matching the deployed environment, and redacted rotation evidence. |
| Environments | Live mode defaults to `https://live.dodopayments.com`; test mode uses `https://test.dodopayments.com` (`DODO_PAYMENTS_BASE_URL` / SDK `environment`). | Assert the deployed host, SDK environment, and key prefix agree; no cross-environment key or host reuse. |
| Webhook signing secret | Displayed on the endpoint's Overview tab; `DODO_PAYMENTS_WEBHOOK_KEY` configures SDK verification. Rotate via dashboard; the old secret stays valid for 24 hours after rotation. | Require a redacted secret reference, a rotation plan, and completion of rotation within the 24-hour overlap. |
| SDKs and adapters | Official TypeScript, Python, Go, PHP, Ruby, Java, Kotlin, C#, Rust SDKs and `@dodopayments/*` framework adapters; env vars `DODO_PAYMENTS_API_KEY`, `DODO_PAYMENTS_BASE_URL`, `DODO_PAYMENTS_ENVIRONMENT`. | Capture resolved and deployed versions; never infer behavior from a package range. |
| Public license endpoints | `POST /licenses/validate`, activate, and deactivate require no API key and are safe for client/CLI use. | Other endpoints must stay server-side; check that only license validation is exposed client-side. |

## Checkout and state

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Checkout sessions | Server creates sessions with dashboard-defined `product_id`/`product_cart`, quantity, and `return_url`; unified endpoint covers one-time, subscription, and usage billing. | Server owns product/price/quantity/tenant selection; record user/tenant-to-customer mapping before fulfillment. |
| Checkout link lifetime | Links generated through the Checkout Sessions API are not reusable and expire within 24 hours. | Generate per customer and attempt; treat stale links as failed, not paid. |
| Fulfillment trigger | Fulfill on the `payment.succeeded` webhook, never on the browser redirect; the redirect can be missed while the webhook is retried until acknowledged. | Prohibit redirect/callback/client-reported paid grants. |
| Customer Portal | Backend creates a customer-portal session for a specific customer. | Require backend authorization from application user/tenant to the requested Dodo customer. |
| Metadata | Objects accept application metadata (e.g., tenant/user IDs). | Use metadata for binding evidence, but never as the authorization decision itself. |

## Webhooks and delivery

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Signature scheme | Standard Webhooks: `webhook-id`, `webhook-timestamp` (Unix seconds), `webhook-signature` (HMAC-SHA256 over `id.timestamp.body`) with the endpoint signing secret. SDK `webhooks.unwrap()` verifies; `unsafe_unwrap()` skips verification. | Require original raw bytes, all three headers, verification before parsing/effects, and an explicit short timestamp tolerance. |
| Test events | Dashboard-triggered test events are not signed; docs direct disabling verification during testing only. | `unsafe_unwrap()` must be unreachable in production code paths. |
| Acknowledgement | Only 2xx acknowledges; any other response is treated as failure and retried. | Verify then durably enqueue before responding; never acknowledge invalid events. |
| Timeout | 15-second window covering connection and read. | Respond fast; process asynchronously; test worker timeout and cancellation. |
| Retries | Exponential backoff: immediately, 5s, 5m, 30m, 2h, 5h, 10h, 10h; at most 8 retry attempts, then the delivery is marked failed. Manual retry (single or bulk) is available from the dashboard. | Persist `webhook-id` uniquely before effects; monitor failed deliveries; keep a manual-redelivery runbook and reconciliation job. |
| Ordering | Events may arrive out of order; each delivery carries the latest payload at delivery time. | Derive current state per event idempotently; never assume arrival order. |
| Envelope | Body contains `business_id`, `type`, `timestamp`, and `data.payload_type` (`Payment`, `Subscription`, `Refund`, `Dispute`, `LicenseKey`, `CreditLedgerEntry`, `CreditBalanceLow`, `AbandonedCheckout`, `DunningAttempt`, `EntitlementGrant`, `Payout`). | Validate `type` and `payload_type` against the expected schema before dispatch. |
| Endpoint configuration | Developer → Webhooks; per-endpoint event selection; deselecting all events silences the endpoint. | Require redacted evidence of endpoint URL, enabled state, subscribed events, and delivery history. |

## Lifecycle events

The exact subscribed set must match the application's products and entitlement model. At minimum
evaluate the events its handlers actually consume against this documented catalog:

- **Payments:** `payment.succeeded`, `payment.failed` (carries `error_code`; soft declines on
  subscriptions are retried automatically by Dodo's recovery features).
- **Subscriptions:** `subscription.active`, `subscription.cancelled`, `subscription.expired`,
  `subscription.on_hold`, `subscription.plan_changed`, `subscription.renewed`,
  `subscription.updated`, `subscription.failed`.
- **Refunds and disputes:** `refund.*` (e.g., `refund.succeeded`); `dispute.opened`,
  `dispute.challenged`, `dispute.accepted`, `dispute.cancelled`, `dispute.expired`,
  `dispute.won`, `dispute.lost`.
- **Licenses and grants:** `license_key.*`; `entitlement_grant.created`, `.delivered`, `.failed`,
  `.revoked` (a single grant emits at most one created, one terminal, and one revoked event;
  dedupe on grant `id` plus `type`).
- **Credits:** `credit.added`, `credit.deducted`, `credit.overage_charged`,
  `credit.balance_low` (credit entitlements, distinct from monetary customer wallets).
- **Recovery:** dunning (`dunning.started`, `dunning.recovered`) and abandoned-cart events.
- **Payouts:** `payout.created`, `payout.success`, `payout.failed`, `payout.not_initiated`.

Credit policy must be an explicit decision: plan and top-up credits can outlive a cancelled
subscription, so gate cost-bearing endpoints on subscription status or debit on cancel if policy
requires it.

## Outbound idempotency

| Surface | Officially documented behavior | Inspect and decide |
| --- | --- | --- |
| Usage ingestion | The `event_id` of an ingested usage event is unique and acts as the idempotency key; reused IDs are treated as duplicates and not double-counted. | Derive deterministic IDs (e.g., `${customer_id}_${action}_${timestamp}`-style stable values); test replay. |
| Wallet ledger entries | Wallet fund add/deduct calls take an idempotency key to avoid applying funds twice. | Require stable keys derived from the originating event. |
| Manual license fulfillment | Fulfilling a grant uses the grant `id` as the idempotency key; a retry after a successful-but-unacknowledged call returns 409 instead of a second key. | Retry on timeout/5xx with the same key; treat 409 as success. |
| Other mutations | Refunds, subscription changes, and on-demand charges have no universally documented idempotency key in the retained sources. | Require a local outbox/deduplication guard before the call; mark unsupported-case claims **Not verified** against current documentation. |
