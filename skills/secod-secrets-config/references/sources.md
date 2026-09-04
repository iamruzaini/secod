# Source register: secod-secrets-config

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-1 | git-filter-repo documentation: Sensitive Data Removal (`--sensitive-data-removal`) | https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt | newren (git-filter-repo maintainers) | 2026-08-24 | Expires 2027-02-24; refresh on tool release changing the flow | Reviewed | PROVISIONAL-secrets-config-9 | Tool version current at review; flow names may change between releases |
| S-2 | GitHub Docs: Removing sensitive data from a repository | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | GitHub | 2026-08-24 | Expires 2027-02-24; refresh on docs revision affecting purge/ref guidance | Reviewed | PROVISIONAL-secrets-config-9 | GitHub.com; Enterprise Server behavior may differ by version |
| S-3 | Gitleaks: secret detection for git repos, files and stdin (pre-commit hook) | https://github.com/gitleaks/gitleaks | Gitleaks (Zachary Rice / maintainers) | 2026-08-24 | Expires 2027-02-24; refresh on major version change | Reviewed | PROVISIONAL-secrets-config-1, -9 | CLI capability as of reviewed version; rule coverage evolves |
| S-4 | TruffleHog Docs: Pre-commit hooks and CI scanning with secret verification | https://docs.trufflesecurity.com/scanning-in-ci | Truffle Security | 2026-08-24 | Expires 2027-02-24; refresh on docs restructure or verifier change | Reviewed | PROVISIONAL-secrets-config-1, -9 | Verified-secret scanning behavior as of reviewed docs snapshot |
| S-5 | CISA Secure by Design Alert: Eliminating Default Passwords | https://www.cisa.gov/resources-tools/resources/secure-design-alert-how-manufacturers-can-protect-customers-eliminating-default-passwords | CISA | 2026-08-24 | Expires 2027-02-24; refresh on alert revision | Reviewed | PROVISIONAL-secrets-config-10 | Guidance aimed at manufacturers; applied here to deployment verification |
| S-6 | CISA Product Security Bad Practices (default passwords, SSDF PW.9.1) | https://www.cisa.gov/resources-tools/resources/product-security-bad-practices | CISA | 2026-08-24 | Expires 2027-02-24; refresh on list revision | Reviewed | PROVISIONAL-secrets-config-10 | Maps default-password use to SSDF PW.9.1 bad practice |

No provider-specific `llms.md`/`llms-full.md` context exists for this skill; it is a
provider-agnostic general baseline. All retained sources above are direct official sources.

For every retained source, also record content hash/ETag where obtainable, plan/tier, region,
and feature maturity when they affect a control conclusion.
