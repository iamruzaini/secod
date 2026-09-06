# Trigger case: secod-secrets-config

## Should trigger

```text
Add a provider API key and production environment configuration.
```

Expected: Keep credentials server-only, validate configuration, scope authority, separate environments, and document rotation/revocation.

## Should not trigger

```text
Add a public theme color variable.
```

Expected: skill excluded.
