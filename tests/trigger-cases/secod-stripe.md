# Trigger case: secod-stripe

## Should trigger

```text
Add Stripe Checkout, a webhook, and subscription entitlements.
```

Expected: create sessions server-side from trusted price identifiers, use idempotency, verify raw
webhook signatures, deduplicate events, reconcile state, and test replay and forged redirects.

## Should not trigger

```text
Add a free local feature with no payment, billing, entitlement, or Stripe integration.
```

Expected: Stripe excluded.
