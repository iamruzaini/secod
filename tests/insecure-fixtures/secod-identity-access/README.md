# Insecure fixture plan: secod-identity-access

Minimal reproducible unsafe cases, one per control family. Documentation-only plan; no
executable code is maintained in this repository.

## F1 — Missing object-level authorization (IDOR)

`GET /api/invoices/:id` loads by ID from session-authenticated context but never checks
`invoice.owner_id == session.user_id`. Expected finding: `Fix before launch`. Expected secure
result: cross-tenant read denied server-side with no existence leak.

## F2 — Enumeration-distinct recovery responses

Password reset returns "email sent" for known accounts but "no such user" for unknown ones.
Expected finding: `Fix before launch`; uniform response and timing required.

## F3 — MFA factor removal without step-up

`DELETE /mfa/totp` accepts any authenticated session regardless of recency. Expected:
re-authentication challenge required; factor-change notification to previous channel.

## F4 — WebAuthn ceremony without origin pinning

Verification library configured with `rpID` taken from the request `Host` header; challenges
reusable within 5 minutes. Expected: fixed RP-ID/origin constants, single-use short-lived
challenge, replay rejection.

## F5 — Session fixation and non-revocation

Login keeps pre-authentication cookie value; logout clears the client cookie without destroying
the server-side record. Expected: session regeneration at privilege change; server-side
invalidation verified on next request.

## F6 — Refresh-token reuse undetected

Refresh tokens long-lived, non-rotating; stolen token usable indefinitely. Expected: rotation
with reuse detection and family revocation.

## F7 — JWT verification gaps

`jwt.verify(token, key)` without algorithm allowlist; JWKS URL read from token `jku` header;
audience never checked. Expected: pinned algorithms, fixed JWKS origin, iss/aud/exp/sub checks.

## F8 — Plaintext API-key storage and no revocation path

API keys stored verbatim, looked up by equality; revocation endpoint absent. Expected: keyed
hash storage with prefix identifier, immediate revocation honored on next call.

## F9 — Blind email-only account linking

OAuth callback merges provider identity when email matches an existing local account, with no
user initiation or re-authentication. Expected: explicit authenticated linking flow with
verified provider identity; no auto-merge.

## F10 — Default credentials in production seed

Seed script creates `admin@example.com` with documented password; deployed environment ran it.
Expected finding: `Do not ship`; default accounts absent/disabled, break-glass rotated with MFA.

## Missing-evidence case

Session store is a managed provider service; maximum-lifetime and idle-timeout settings not
establishable from code. Expected status: `Not verified` for PROVISIONAL-identity-6 lifetime
aspects, routed to the auth adapter for dashboard evidence.
