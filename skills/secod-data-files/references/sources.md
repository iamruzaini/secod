# Source register: secod-data-files

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP ASVS 5.0.0 (V14 Data Protection; requirement format `v5.0.0-<chapter>.<section>.<requirement>`) | https://github.com/OWASP/ASVS/tree/v5.0.0 | OWASP Foundation | 2026-08-25 (v5.0.0 tag) | Refresh on new stable ASVS release or chapter restructuring | Reviewed | PROVISIONAL-df-1, -2, -5, -6, -7, -10 | See register assumptions below. |
| S2 | OWASP File Upload Cheat Sheet (allowlists, signature validation, filename safety, storage location, upload/download limits, archive-extraction bounds, antivirus/CDR guidance) | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | OWASP Foundation | 2026-08-26 (fetched live) | Refresh on cheat sheet revision | Reviewed | PROVISIONAL-df-1, -2, -3, -4 | See register assumptions below. |
| S3 | OWASP Unrestricted File Upload (bypass techniques, `Content-Disposition: attachment` + `X-Content-Type-Options: nosniff` download guidance) | https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload | OWASP Foundation | 2026-08-26 (fetched live) | Refresh when the migrated community page is restructured or revised | Reviewed | PROVISIONAL-df-1, -5 | See register assumptions below. |
| S4 | OWASP Top 10 2025 A10: Mishandling of Exceptional Conditions (fail-closed behavior, rollback, cleanup testing) | https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/ | OWASP Foundation | 2026-08-25 (verified during secod-crypto-data-protection register review) | Refresh on 2025 list errata/update | Reviewed | Exceptional and failure conditions (all controls) | See register assumptions below. |

Notes:

- Signed/shared URL authorization decisions (PROVISIONAL-df-6), cache/CDN privacy (-7),
  export/render bounds (-8), cleanup (-9), and retention/deletion (-10) are engineering
  requirements assembled from ASVS v5.0.0-14.x objectives plus the PRD contract; platform-level
  presigning/SAS/bucket mechanics are evidenced in each routed storage adapter's own source
  register (`secod-aws-s3-cloudfront`, `secod-google-cloud-storage`, `secod-supabase`,
  `secod-firebase`, `secod-cloudflare-workers`, `secod-vercel-platform`).
  Bearer-verifier generation/hashing mechanics are registered under `secod-identity-access`.
- No provider-specific behavior is asserted by this skill's generic controls; any
  provider-dependent claim (revocation reach, lifecycle enforcement, cache normalization)
  requires that provider's direct documentation via the routed adapter.

Sources S2 and S3 were reviewed from their direct official pages on 2026-08-26. S1 and S4
were carried from the verified `secod-crypto-data-protection` register dated 2026-08-25.

For every retained source, record version/SDK version, reviewed date, review expiry, content
hash or ETag where obtainable, owner, plan/tier, region, feature maturity, and SECOD control IDs.
