# Source register: secod-failure-safety

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct URL | Owner | Reviewed | Review expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-OWASP-A10-2025 | A10:2025 Mishandling of Exceptional Conditions (OWASP Top 10:2025) | https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/ | OWASP Foundation | 2026-08-26 | Refresh on next OWASP Top 10 edition or category revision, or after 12 months | Reviewed | SECOD-FAIL-01..10 | Category-level guidance; no version/plan/region dependency |

Notes:

- Verified content used in controls: fail-closed semantics ("roll back every part of the
  transaction ... also known as failing closed"), centralized handling plus global exception
  handler, resource-exhaustion and sensitive-error-disclosure scenarios, mapped CWEs including
  CWE-209 (error-message disclosure) and CWE-636 (failing open).
- Referenced by the source but not separately retained here (route through owning skills):
  OWASP ASVS V16.5 Error Handling, OWASP Error Handling and Logging Cheat Sheets,
  OWASP WSTG 4.8.1 Testing for Error Handling.
- No provider-specific resilience claims are made from this register; provider retry schedules,
  DLQ retention and delivery guarantees must be evidenced by the owning provider skill's sources.
