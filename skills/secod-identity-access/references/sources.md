# Source register: secod-identity-access

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | RFC 10017: OAuth 2.0 for Browser-Based Applications (Best Current Practice, August 2026; BFF pattern, PKCE requirement, browser token storage analysis) | https://www.rfc-editor.org/info/rfc10017 | IETF OAuth WG | 2026-08-24 | Refresh on RFC update or errata affecting Sections 5–8 | Reviewed | PROVISIONAL-identity-6, -9 | See register assumptions below. |
| S2 | RFC 9700: Best Current Practice for OAuth 2.0 Security | https://www.rfc-editor.org/info/rfc9700 | IETF OAuth WG | 2026-08-24 | Refresh on RFC update | Reviewed | PROVISIONAL-identity-7, -9 | See register assumptions below. |
| S3 | OWASP Authentication Cheat Sheet (NIST SP 800-63B password rules, MFA, passkeys/FIDO2 hardware-backed key storage guidance) | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP Foundation | 2026-08-24 | Refresh on cheat-sheet revision | Reviewed | PROVISIONAL-identity-2, -3, -4 | See register assumptions below. |
| S4 | OWASP Session Management Cheat Sheet (strict session IDs, renewal on privilege change, reauthentication after risk events, cookie attributes, no web-storage tokens) | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | OWASP Foundation | 2026-08-24 | Refresh on cheat-sheet revision | Reviewed | PROVISIONAL-identity-5, -6 | See register assumptions below. |

Provider-specific token validation, session policy, and dashboard evidence are registered in
each routed adapter's own `references/sources.md`. NIST SP 800-63B thresholds are cited here as
relayed by the OWASP Authentication Cheat Sheet; direct NIST publication review is not retained
in this register.
