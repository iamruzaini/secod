# Trigger case: secod-abuse-limits

## Should trigger

```text
Add public invitation sending and a retrying background job.
```

Expected: Apply layered limits, atomic invariants, idempotency, bounded jittered retries, and duplicate/concurrency tests.

## Should not trigger

```text
Change local formatting with no request or resource behavior.
```

Expected: skill excluded.
