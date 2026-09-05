# Source register: secod-crypto-data-protection

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP ASVS 5.0.0 (V11 Cryptography; V12 Secure Communication; V14 Data Protection; requirement format `v5.0.0-<chapter>.<section>.<requirement>`) | https://github.com/OWASP/ASVS/tree/v5.0.0 | OWASP Foundation | 2026-08-25 (v5.0.0 tag) | Refresh on new stable ASVS release or chapter restructuring | Reviewed | `SECOD-CDP-01`–`SECOD-CDP-08` | See register assumptions below. |
| S2 | NIST SP 800-57 Part 1 Rev. 5: Recommendation for Key Management – General (key types, cryptoperiods, rotation, compromise recovery) | https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final | NIST | 2026-08-25 (Rev. 5 final, May 2020) | Refresh when SP 800-57 Part 1 Rev. 6 finalizes (initial public draft released 2025-12-05); keep Rev. 5 authoritative while Rev. 6 remains draft | Reviewed | `SECOD-CDP-04`, `SECOD-CDP-05` | See register assumptions below. |
| S3 | NIST SP 800-38D: GCM and GMAC (IV uniqueness requirements for GCM) | https://csrc.nist.gov/pubs/sp/800/38/d/final | NIST | 2026-08-25 (final, November 2007) | Refresh on NIST revision affecting IV guidance | Reviewed | `SECOD-CDP-02`, `SECOD-CDP-04` | See register assumptions below. |
| S4 | OWASP Cryptographic Storage Cheat Sheet (algorithm/mode selection, storage encryption decisions) | https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html | OWASP Foundation | 2026-08-25 | Refresh on cheat sheet revision | Reviewed | `SECOD-CDP-01`, `SECOD-CDP-04` | See register assumptions below. |
| S5 | OWASP Key Management Cheat Sheet (key lifecycle: generation, storage, rotation, revocation) | https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html | OWASP Foundation | 2026-08-25 | Refresh on cheat sheet revision | Reviewed | `SECOD-CDP-05` | See register assumptions below. |
| S6 | OWASP Password Storage Cheat Sheet (Argon2id/bcrypt/scrypt/PBKDF2 parameter guidance) | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | OWASP Foundation | 2026-08-25 | Refresh on parameter recommendation change | Reviewed | `SECOD-CDP-03` | See register assumptions below. |
| S7 | OWASP Top 10 2025 A10: Mishandling of Exceptional Conditions (fail-closed behavior, rollback, cleanup testing) | https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/ | OWASP Foundation | 2026-08-25 | Refresh on 2025 list errata/update | Reviewed | Exceptional and failure conditions (all controls) | See register assumptions below. |

Retention/deletion-lifecycle propagation (`SECOD-CDP-08`) is engineering practice assembled
from ASVS v5.0.0-14.x data-protection objectives plus provider-documented deletion APIs; no
single standard covers cross-store verification. Provider-specific deletion/backup behavior is
registered in each routed platform/data adapter's own source register.

The direct official sources above were reviewed on 2026-08-25. All registered claims were
verified against the cited primary documentation rather than a local documentation snapshot.

For every retained source, record version/SDK version, reviewed date, review expiry, content
hash or ETag where obtainable, owner, plan/tier, region, feature maturity, and SECOD control IDs.
