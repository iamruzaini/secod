# Trigger case: secod-failure-safety

## Should trigger

```text
Add a multi-step mutation that calls a provider and database.
```

Expected: Fail authorization closed, bound timeouts/retries, preserve invariants with transaction/compensation, and test injected failures.

## Should not trigger

```text
Change static documentation.
```

Expected: skill excluded.
