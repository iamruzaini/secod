# Source register: secod-observability-response

Use official documentation indexes (`llms.txt`, and `llms-full.txt` where published) for
discovery only. Verify security-critical claims against the direct primary source and refresh
this register before its review-expiry date.

This is a general baseline skill: it has no single provider. Per-review, discover
provider/framework-specific observability features through that provider's official
`llms.txt` index (and `llms-full.txt` where published), then verify against directly linked
official pages and record them here before relying on any provider capability claim.
Snapshot-only or unverified provider claims are `Not verified`.

| Source ID | Title | Direct official URL | Owner | Reviewed | Review expiry / refresh trigger | Status | Control IDs | Version/plan/region assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-1 | OWASP Logging Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | OWASP Foundation | 2026-08-16 | 12 months, or on page change notice | Reviewed | SECOD-OBS-01, SECOD-OBS-02, SECOD-OBS-06 | Provider-neutral; applies to all stacks |
| S-2 | NIST SP 800-61 Rev. 3 (Incident Response Recommendations and Considerations for Cybersecurity Risk Management) | https://csrc.nist.gov/pubs/sp/800/61/r3/final | NIST | 2026-08-16 | 12 months, or on SP revision | Reviewed | SECOD-OBS-04, SECOD-OBS-05 | CSF 2.0-aligned edition |
| S-3 | OWASP Application Security Verification Standard (ASVS), logging/exception sections | https://owasp.org/www-project-application-security-verification-standard/ | OWASP Foundation | 2026-08-16 | On new ASVS release | Reviewed | SECOD-OBS-01..SECOD-OBS-07 | Mappings recorded version-qualified at review time by `secod-ship-check` |
| S-4 | OWASP Error Handling Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html | OWASP Foundation | 2026-08-16 | 12 months, or on page change notice | Reviewed | SECOD-OBS-02 | Provider-neutral; applies to all stacks |

Notes:

- HTTP status checked 2026-08-16: S-1, S-2, S-3, S-4 returned `200 OK`.
- No provider-specific sources are retained in this baseline register; add per-provider rows
  only with direct official URLs, reviewed date and expiry when a triggered adapter's evidence
  is relied upon.
- An expired review, changed page, inaccessible URL, or snapshot-only evidence marks affected
  controls `Not verified` until re-reviewed against the current primary source.

For every retained source, record version/SDK version, reviewed date, review expiry, content
hash or ETag where obtainable, owner, plan/tier, region, feature maturity, and SECOD control IDs.
