# Expected result: secod-failure-safety

Fail authorization closed, bound timeouts/retries, preserve invariants with transaction/compensation, and test injected failures.

Missing context: Transaction boundary, retry semantics, or provider idempotency is unclear; inspect before implementing failure behavior.

Rejected behavior: Never catch and continue with privilege or blindly retry non-idempotent writes.
