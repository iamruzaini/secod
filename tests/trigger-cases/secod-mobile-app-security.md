# Trigger case: secod-mobile-app-security

## Should trigger

```text
Add persistent login, a password-reset deep link, photo permission, and push notifications to our Android and iOS app.
```

Expected: treat device and inbound payloads as untrusted, choose secure credential storage, verified
links, minimal permissions, minimal notification data, backend authorization, and mobile tests.

## Should not trigger

```text
Change a backend-only batch job with no mobile client behavior or SDK.
```

Expected: mobile baseline excluded.
