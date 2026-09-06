# Trigger case: secod-observability-response

## Should trigger

```text
Add audit events for role changes and webhook failures.
```

Expected: Emit structured redacted events, stable correlation, bounded metrics, actionable alerts, and containment/recovery tests.

## Should not trigger

```text
Change a static image asset.
```

Expected: skill excluded.
