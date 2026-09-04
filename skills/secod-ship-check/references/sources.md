# Source register: secod-ship-check

Security-critical sources supporting this skill's mapping and gate-verification controls.
Discovery indexes (`llms.txt`/`llms-full.txt`) are snapshots only; security-critical
conclusions must be verified against the direct primary sources below and this register
refreshed before its review-expiry trigger.

| Source ID | Title | Direct official URL | Owner | Reviewed | Review expiry / refresh trigger | Status | Applicable control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-1 | OWASP Application Security Verification Standard (ASVS), stable release 5.0.0 | https://owasp.org/www-project-application-security-verification-standard/ | OWASP Foundation | 2026-08-26 | On new stable ASVS release, or 12 months | Reviewed | PROVISIONAL-ship-3, PROVISIONAL-ship-4 | Requirement IDs cited as `v<version>-<chapter>.<section>.<requirement>`; v5.0.0 latest stable at review. Mappings recorded version-qualified per finding |
| S-2 | OWASP API Security Top 10 (2023 edition) | https://owasp.org/API-Security/editions/2023/en/0x00-header/ | OWASP Foundation | 2026-08-26 | On publication of a newer API Security Top 10 edition, or 12 months | Reviewed | PROVISIONAL-ship-3, PROVISIONAL-ship-4 | 2023 is the current edition at review time; contributing skills cite `API<n>:2023` entries |
| S-3 | OWASP Top 10 for LLM Applications (GenAI Security Project) | https://genai.owasp.org/llm-top-10/ | OWASP GenAI Security Project | 2026-08-26 | On publication of a newer LLM Top 10 edition, or 12 months | Reviewed | PROVISIONAL-ship-3, PROVISIONAL-ship-4 (AI gate) | Editions change (2023/24, 2025, 2026 published); every AI-related finding records the exact edition cited |

## Register rules

For every retained source, record: source ID, title, direct official URL, owner, reviewed
date, review expiry or refresh trigger, status (`Reviewed`, `Pending review`, `Stale`,
`Changed`, `Unavailable`, `Not published`), applicable control IDs, and relevant
version/edition, plan, region, or maturity assumptions.

A control whose required source evidence is missing, stale, contradictory, inaccessible,
unsupported, or snapshot-only is marked **Not verified** in findings until refreshed.
