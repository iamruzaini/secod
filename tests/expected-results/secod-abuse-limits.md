# Expected result: secod-abuse-limits

Apply layered limits, atomic invariants, idempotency, bounded jittered retries, and duplicate/concurrency tests.

Missing context: Identity scopes, business invariant, or infrastructure support is unclear; inspect before selecting limit storage or atomic operations.

Rejected behavior: Never rely on one global limit or blindly retry non-idempotent effects.
