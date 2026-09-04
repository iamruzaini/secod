# Source register: secod-abuse-limits

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Version / assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OWASP-API4-2023 | API4:2023 Unrestricted Resource Consumption (OWASP API Security Top 10 2023) | https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/ | OWASP Foundation | 2026-08-26 | 12 months, or on new API Security Top 10 edition | Reviewed | PROVISIONAL-ABUSE-01, -05, -07, -08 | Edition 2023; prevention list includes timeouts, payload caps, rate limiting, per-operation throttling, provider spending limits |
| OWASP-API6-2023 | API6:2023 Unrestricted Access to Sensitive Business Flows (OWASP API Security Top 10 2023) | https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/ | OWASP Foundation | 2026-08-26 | 12 months, or on new API Security Top 10 edition | Reviewed | PROVISIONAL-ABUSE-06 | Edition 2023; two-layer business/engineering mitigation, anti-automation measures |
| OWASP-AUTH-CS | Authentication Cheat Sheet (login throttling, lockout, automated-attack protection) | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP Cheat Sheet Series project | 2026-08-26 | 12 months, or on cheat-sheet revision notice | Reviewed | PROVISIONAL-ABUSE-02 | Current published cheat sheet; sections "Protect Against Automated Attacks", "Login Throttling", "Account Lockout" |

For every retained source, record version/SDK version, reviewed date, review expiry,
hash/ETag when obtainable, owner, plan/tier, region, feature maturity, and linked control IDs.

Gaps:

- No provider-specific sources retained: this is a general baseline skill with no single provider.
- `Not verified` items depending on external evidence: deployed limiter store consistency,
  provider-side spend ceilings and billing alerts, production traffic behavior. These require
  Dashboard/API or human-supplied evidence at review time.
