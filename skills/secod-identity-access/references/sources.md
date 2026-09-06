# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| ID-SRC-001 | Authentication Cheat Sheet | Direct implementation guide | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP | 2026-09-06 | Guide revision | Reviewed | server-authorization.md: authentication lifecycle and reauthentication boundary | Apply with provider-specific documentation. |
| ID-SRC-002 | Authorization Cheat Sheet | Direct implementation guide | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | OWASP | 2026-09-06 | Guide revision | Reviewed | server-authorization.md: deny-by-default and per-request authorization | Application must define resource and tenant policy. |
| ID-SRC-003 | OAuth 2.0 Security Best Current Practice | Standard | https://www.rfc-editor.org/info/rfc9700 | IETF | 2026-09-06 | RFC errata or successor | Reviewed | server-authorization.md: OAuth credential and redirect security | Exact provider flow belongs to adapter. |
