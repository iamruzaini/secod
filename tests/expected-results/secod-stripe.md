# Expected result: secod-stripe

The agent keeps secret keys server-side, separates test/live configuration, derives price and
customer ownership from trusted storage, passes idempotency keys for retryable mutations, verifies
webhooks over raw bytes, and grants entitlement from verified Stripe state rather than redirects.
Tests cover duplicates, out-of-order events, invalid signatures, and tenant mismatch.
