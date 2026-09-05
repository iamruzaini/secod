# Source register: secod-threat-model

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP Top 10:2025 (A01 Broken Access Control now includes SSRF; A03 Software Supply Chain Failures; A10 Mishandling of Exceptional Conditions new) | https://owasp.org/Top10/2025/ | OWASP Foundation | 2026-08-24 | Refresh on next OWASP Top 10 edition or page change | Reviewed | PROVISIONAL-threat-model-2, -4, -5 | See register assumptions below. |
| S2 | OWASP Threat Modeling Cheat Sheet (four-question framework, STRIDE phases) | https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html | OWASP Foundation | 2026-08-24 | Refresh on cheat-sheet revision | Reviewed | PROVISIONAL-threat-model-3, -4 | See register assumptions below. |
| S3 | MDN Threat modeling frameworks (STRIDE and LINDDUN categories) | https://developer.mozilla.org/en-US/docs/Web/Security/Threat_modeling/Frameworks | Mozilla | 2026-08-24 | Refresh on guide revision | Reviewed | PROVISIONAL-threat-model-4 | See register assumptions below. |

Assumptions: STRIDE used as primary identification method per OWASP guidance; LINDDUN-style
privacy questions applied where personal data crosses boundaries. No plan/tier/region
assumptions apply to this skill.
