# Trigger case: secod-auth-provider-integrations

## Should trigger

```text
Add Clerk authentication and a callback to this Next.js app.
```

Expected: Select secod-clerk plus identity and framework dependencies; implement provider-specific callback/session code and tests.

## Should not trigger

```text
Add local password authentication with no third-party provider.
```

Expected: family router excluded unless stated provider-family routing is required.
