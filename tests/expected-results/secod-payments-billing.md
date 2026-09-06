# Expected result: secod-payments-billing

Use server-owned commercial state, authenticated provider events, idempotent transitions, reconciliation, and replay tests.

Missing context: Product, tenant, entitlement, event, or provider model is unclear; inspect before implementing transitions.

Rejected behavior: Never trust browser payment state or assume events are unique and ordered.
