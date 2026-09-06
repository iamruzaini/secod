# Trigger case: secod-packages-delivery

## Should trigger

```text
Add a dependency and update CI release workflow.
```

Expected: Justify dependency need, update lockfile reproducibly, pin immutable CI inputs, minimize permissions, and test build/rollback.

## Should not trigger

```text
Edit application copy without package or delivery changes.
```

Expected: skill excluded.
