# Source register: secod-email-messaging

Discovery snapshots and indexes are not proof of current provider behavior. Verify every
security-critical claim against the direct primary source and refresh this register before its
review-expiry date. Mark affected controls `Not verified` when required evidence is missing, stale,
contradictory, inaccessible or snapshot-only.

| Source ID | Title | Direct URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Version / assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | RFC 7208 — Sender Policy Framework (SPF) v1 | https://datatracker.ietf.org/doc/html/rfc7208 | IETF | 2026-08-26 | On new RFC obsoleting/update notice, or 2027-08-26 | Reviewed | EMAIL-10 | Proposed Standard; updated by RFC 8616, RFC 7372, RFC 8553; obsoletes RFC 4408. No plan/region dependency. |
| S2 | RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures | https://datatracker.ietf.org/doc/html/rfc6376 | IETF | 2026-08-26 | On new obsoleting/update notice, or 2027-08-26 | Reviewed | EMAIL-10 | Internet Standard; updated by RFC 8301, RFC 8463, RFC 8553, RFC 8616; obsoletes RFC 4871/5672. |
| S3 | RFC 9989 — Domain-Based Message Authentication, Reporting, and Conformance (DMARC) | https://datatracker.ietf.org/doc/html/rfc9989 | IETF | 2026-08-26 | On new RFC obsoleting/update notice, errata affecting EMAIL-10, or 2027-08-26 | Reviewed | EMAIL-10 | Standards Track; obsoletes RFC 7489 and RFC 9091. A DMARC pass requires at least one authenticated SPF or DKIM identifier aligned with the RFC5322.From Author Domain. `p=none` is monitoring mode only when aggregate reports are received; `pct` is removed and historic. Domains publishing `p=reject` must not rely only on SPF and must apply valid DKIM signatures. |
| S4 | RFC 9990 — DMARC Aggregate Reporting | https://datatracker.ietf.org/doc/html/rfc9990 | IETF | 2026-08-26 | On new RFC obsoleting/update notice, errata affecting EMAIL-10, or 2027-08-26 | Reviewed | EMAIL-10 | Standards Track; obsoletes RFC 7489 for aggregate-reporting rules. Defines XML aggregate reports, report discovery/delivery, duplicate handling and DNS authorization for external report destinations. Reporting evidence supports monitoring; it is not DNS authentication evidence by itself. |
| S5 | RFC 9991 — DMARC Failure Reporting | https://datatracker.ietf.org/doc/html/rfc9991 | IETF | 2026-08-26 | On new RFC obsoleting/update notice, errata affecting EMAIL-10, or 2027-08-26 | Reviewed | EMAIL-10 | Standards Track; obsoletes RFC 7489 for failure-reporting rules and updates RFC 6591. Failure reports are optional, can expose message data and require external-destination verification plus rate/loop safeguards. Absence of failure reports does not establish DMARC failure. |
| S6 | OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP Cheat Sheet Series | 2026-08-26 | On upstream page change, or 2027-02-26 | Reviewed | EMAIL-03, EMAIL-04 | Live web page; used for enumeration-uniform responses and recovery-flow guidance. References NIST SP 800-63B rev 4 (https://pages.nist.gov/800-63-3/sp800-63b.html and rev-4 pages linked therein). |

## Pending review

| Title | URL | Needed for | Reason |
| --- | --- | --- | --- |
| OWASP Forgot Password Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | EMAIL-03, EMAIL-04, EMAIL-11 | Relevant recovery-flow guidance discovered but not yet reviewed this cycle. |
| NIST SP 800-63B (Digital Identity Guidelines: Authentication and Lifecycle Management) | https://pages.nist.gov/800-63-3/sp800-63b.html | EMAIL-03 | OTP/expiry/authenticator guidance cited by S6; direct review pending. Confirm current revision (rev 4 pages exist) before relying on specific clause numbers. |

For EMAIL-10, use S1/S2 for SPF/DKIM and S3/S4/S5 for current DMARC protocol and reporting
claims. RFC 7489 is obsolete and must not be used as current normative authority.

No email-provider documentation snapshot is authoritative for this skill. Provider-specific
signing algorithms, retry schedules and Dashboard settings are never asserted from archived
indexes—cite the provider's own live documentation at review time or leave affected controls
`Not verified`.
