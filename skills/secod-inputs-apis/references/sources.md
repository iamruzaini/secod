# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| API-SRC-001 | Input Validation Cheat Sheet | Direct implementation guide | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html | OWASP | 2026-09-06 | Guide revision | Reviewed | typescript-api-boundary.md: allowlisting, schema validation, and boundary checks | Language-neutral principles adapted to project stack. |
| API-SRC-002 | SSRF Prevention Cheat Sheet | Direct implementation guide | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | OWASP | 2026-09-06 | Guide revision | Reviewed | typescript-api-boundary.md: outbound destination and redirect controls | Network enforcement depends on deployment. |
| API-SRC-003 | OWASP API Security Top 10 2023 | Security standard | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | OWASP | 2026-09-06 | New edition | Reviewed | typescript-api-boundary.md: authorization, resource limits, SSRF, and third-party response boundaries | Use direct provider docs for webhook algorithms. |
