# Firebase Auth and session boundaries

- Treat Firebase ID tokens as authentication evidence, not resource authorization.
- Verify tokens in a trusted server or Function before privileged work.
- Resolve tenant, membership, role, and resource ownership from trusted application data.
- Keep refresh/session tokens in platform-appropriate protected storage; never log them.
- App Check can reduce abuse for supported products but never replaces Auth or Security Rules.

Tests: valid user, expired/invalid token, missing user, disabled user, wrong tenant, and App Check
failure where feature enables enforcement.
