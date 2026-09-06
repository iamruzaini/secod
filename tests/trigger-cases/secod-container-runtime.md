# Trigger case: secod-container-runtime

## Should trigger

```text
Add Docker and Kubernetes deployment for an API.
```

Expected: Use minimal immutable images, non-root identity, dropped privileges, protected build secrets, health checks, and runtime tests.

## Should not trigger

```text
Run app directly with no container artifacts.
```

Expected: skill excluded.
