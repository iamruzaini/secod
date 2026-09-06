# Trigger case: secod-payments-billing

## Should trigger

```text
Add checkout, subscriptions, refunds, and entitlement state.
```

Expected: Use server-owned commercial state, authenticated provider events, idempotent transitions, reconciliation, and replay tests.

## Should not trigger

```text
Add a free feature with no billing state.
```

Expected: skill excluded.
