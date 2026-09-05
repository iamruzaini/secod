# Source register: secod-inputs-apis

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP API Security Top 10 (2023 edition): API1-API10 including BOLA, broken authentication, BOPLA, unrestricted resource consumption, SSRF, improper inventory management, unsafe consumption of APIs | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | OWASP Foundation | 2026-08-25 | Refresh on new edition or list revision | Reviewed | PROVISIONAL-api-1 through -7, -11, -13 | See register assumptions below. |
| S2 | OWASP Application Security Verification Standard v5.0.0 (validation and business-logic requirements; cite version-qualified identifiers) | https://owasp.org/www-project-application-security-verification-standard/ | OWASP Foundation | 2026-08-25 | Refresh on ASVS release affecting V5/V13-class chapters | Reviewed | PROVISIONAL-api-3, -4, -6, -12 | See register assumptions below. |
| S3 | OWASP Server-Side Request Forgery Prevention Cheat Sheet (allowlists, IP-range denial, redirect handling, DNS pinning, metadata addresses) | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | OWASP Foundation | 2026-08-25 | Refresh on cheat-sheet revision | Reviewed | PROVISIONAL-api-11 | See register assumptions below. |
| S4 | OWASP Injection Prevention Cheat Sheet (parameterized queries, allowlisted identifiers, safe query construction) | https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html | OWASP Foundation | 2026-08-25 | Refresh on cheat-sheet revision | Reviewed | PROVISIONAL-api-8 | See register assumptions below. |
| S5 | GraphQL: Security (introspection, depth/complexity limiting suggestions, pagination guidance; suggestions not mandates — enforce server-side limits regardless) | https://graphql.org/learn/security/ | GraphQL Foundation | 2026-08-25 | Refresh on guide revision or spec release affecting security section | Reviewed | PROVISIONAL-api-7 | See register assumptions below. |
| S6 | RFC 9110: HTTP Semantics (field-value syntax, framing-related message rules, hop-by-hop header semantics underlying CRLF/splitting and desync review) | https://www.rfc-editor.org/info/rfc9110 | IETF HTTP WG | 2026-08-25 | Refresh on errata/update affecting field/framing sections | Reviewed | PROVISIONAL-api-10 | See register assumptions below. |
| S7 | RFC 6455: The WebSocket Protocol (opening-handshake authentication expectations, per-frame processing baseline for WS authorization) | https://www.rfc-editor.org/info/rfc6455 | IETF HyBi WG | 2026-08-25 | Refresh on errata/update affecting handshake/security sections | Reviewed | PROVISIONAL-api-6 | See register assumptions below. |

Provider-specific webhook mechanisms, retry schedules, and capability matrices are registered in
each routed provider adapter's own source register (`secod-payments-billing` family,
`secod-email-messaging`, AI adapters); this skill never invents provider guarantees. No local
provider `llms-full.md` snapshot applies to this general-baseline skill; framework reference
discovery at review time uses official `llms.txt`/`llms-full.txt` indexes with conclusions tied to
directly linked official documentation.
