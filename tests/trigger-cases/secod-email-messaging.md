# Trigger case: secod-email-messaging

## Should trigger

```text
Add password-reset email and SMS OTP.
```

Expected: Generate purpose-bound tokens, store verifiers safely, prevent enumeration, constrain redirects, rate-limit, and test replay.

## Should not trigger

```text
Change an in-app label without messaging.
```

Expected: skill excluded.
