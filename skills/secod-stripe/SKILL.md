---
name: secod-stripe
description: >-
  Help coding agents implement Stripe checkout, PaymentIntents, subscriptions,
  webhooks, refunds, and entitlements with server-owned prices, restricted keys,
  signature verification, idempotency, and reconciliation.
license: Apache-2.0
compatibility: "Requires Stripe; recipes target current server SDK patterns and sandbox testing."
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# Secure Stripe implementation

## Purpose

Build Stripe flows where server chooses products/prices, Stripe state is authoritative, webhook
events are authenticated and deduplicated, retries are safe, and entitlements reconcile correctly.

## When to use

Use for Stripe API, Checkout, PaymentIntents, subscriptions, portal, Connect, webhooks, refunds,
disputes, or entitlement changes. Do not activate for unrelated payment providers.

## Context to inspect

Resolve Stripe SDK/API version, sandbox/live environment, key type, account/Connect scope, product
mapping, customer ownership, webhook route/raw body, event store, idempotency, and entitlement model.

## Secure defaults

- Keep restricted/secret keys and webhook secrets server-side; prefer restricted keys.
- Resolve price, currency, quantity limits, customer, and account scope on server.
- Verify webhook signature against raw request body before parsing or effects.
- Persist event IDs and process effects idempotently inside transaction/reconciliation boundary.
- Grant entitlement from verified Stripe state, not browser redirect or client claims.

## Implementation workflow

1. Map application user/customer/product/price/account and entitlement state.
2. Implement server-owned Stripe request with stable operation idempotency key.
3. Implement raw-body webhook verification and event deduplication.
4. Handle duplicates, retries, out-of-order events, refunds, disputes, and subscription changes.
5. Add sandbox and Stripe CLI tests plus reconciliation path.

## Implementation recipes

- [`references/stripe-server-webhooks.md`](references/stripe-server-webhooks.md) — TypeScript server
  client, idempotent creation, verified webhooks, deduplication, and entitlement handoff.

## Unsafe patterns to avoid

- Accepting amount, price, entitlement, customer, or connected-account authority from client.
- Exposing restricted/secret keys or confusing API keys with webhook secrets.
- Parsing/re-encoding body before signature verification.
- Treating checkout success redirect as payment completion.
- Retrying POST operations without stable idempotency key.

## Tests to add

Test authorized checkout, tampered price/customer, invalid signature, duplicate/out-of-order event,
retry after timeout, refund/dispute/revocation, sandbox/live separation, and reconciliation.

## Provider and deployment steps

Configure sandbox/live keys separately, register exact HTTPS webhook, select required event types,
and verify with Stripe CLI/sandbox. State unperformed dashboard steps precisely.

## Official sources

Use [`references/sources.md`](references/sources.md); Stripe `llms.txt` is discovery index only.

## Completion handoff

State authoritative mappings, key category, webhook/idempotency design, tests run, reconciliation,
and external endpoint setup. No payment-security verdict.
