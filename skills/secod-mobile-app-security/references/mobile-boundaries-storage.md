# Mobile trust boundaries and storage

## Device and backend boundary

- Assume users and malware can inspect or modify application bundles, client state, local databases, network requests, and route inputs.
- Authenticate each backend request and authorize the requested object/action from server-owned identity, tenant, ownership, and policy data.
- Treat biometrics and device integrity signals as local risk or key-release signals, never sole server authorization.
- Keep service credentials and unrestricted provider keys behind a backend. Public mobile configuration identifiers are not secrets, but still require provider-side restrictions.

## Storage decision

1. Keep short-lived sensitive values in memory when restart persistence is unnecessary.
2. Use platform-backed secure storage for small session credentials or cryptographic keys.
3. Use ordinary preferences/databases/files only for non-sensitive or application-encrypted data whose key is protected separately.
4. Define expiry, account binding, logout/account-switch deletion, backup behavior, and corruption recovery.
5. Never persist whole application state when it can include credentials, personal data, form input, or provider responses.

Secure storage reduces extraction risk; it does not make a compromised device trusted. Revoke or
rotate server-side sessions when device credentials are lost.

## Local persistence and disclosure

- Minimize offline records and separate them by authenticated account/tenant.
- Redact logs, analytics, crash breadcrumbs, screenshots, clipboard contents, and notification previews.
- Clear sensitive cached files after upload/use; avoid shared/external storage unless feature requires explicit sharing.
- Validate files and values read from device storage as untrusted input.

## WebViews and provider SDKs

- Prefer system browser or provider-supported native authentication. Use OAuth authorization code flow with PKCE for public mobile clients.
- For WebViews, allowlist HTTPS origins/navigation, disable unnecessary bridges and file access, and never pass bearer credentials in URLs.
- Resolve exact provider SDK and framework versions from lockfiles. Follow selected provider adapter; do not copy server SDK secrets into mobile code.
