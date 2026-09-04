# Source register: secod-packages-delivery

Official documentation indexes (`llms.txt`, `llms-full.txt`) are discovery aids only. Direct
primary content below was read on 2026-08-27. Refresh expired or drifted entries before using
them for a decisive claim. A reviewed source supports only its recorded scope; it never proves
that an inspected repository, dashboard, registry or release satisfies a control.

| Source ID | Title | Direct primary URL | Owner | Reviewed | Refresh deadline / trigger | Status | Control IDs | Assumptions and reviewed scope | Retrieval fingerprint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PKG-S1 | Secure use reference for GitHub Actions | https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions | GitHub | 2026-08-27 | 2026-11-25 or GitHub Actions security-doc change | Reviewed | PROVISIONAL-packages-4, -5, -6 | Hosted and self-hosted Actions; reviewed privileged triggers, full-SHA pins, least privilege and OIDC guidance | normalized Markdown SHA-256 `e039c41499a5f757278555feb77008414416dcf059be1e9964990e5055ce924c` |
| PKG-S2 | About supply chain security | https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security | GitHub | 2026-08-27 | 2026-11-25 or GitHub supply-chain feature change | Reviewed | PROVISIONAL-packages-2 | All current plans; reviewed direct/transitive inventory, dependency review, Dependabot alerts and updates; availability still plan-dependent | normalized Markdown SHA-256 `8955a60252a5c560b8e01bbc0dbdcec02cd5385e6ae11adba868a33fccd95479` |
| PKG-S3 | Using artifact attestations to establish provenance for builds | https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds | GitHub | 2026-08-27 | 2026-11-25 or artifact-attestation feature/plan change | Reviewed | PROVISIONAL-packages-9 | Available on current plans; public repositories only on Free, Pro and Team; private/internal require Enterprise Cloud; reviewed generation and `gh attestation verify` flows | normalized Markdown SHA-256 `cbc704b60dcd5967e36ca797fc7d65b4fa74819b9d5002650b713d65b8b6e423` |
| PKG-S4 | npm-ci | https://docs.npmjs.com/cli/v10/commands/npm-ci | npm, Inc. | 2026-08-27 | 2026-11-25 or npm CLI major/config-semantics change | Reviewed | PROVISIONAL-packages-1, -3 | npm v10; reviewed lockfile requirement, frozen writes, matching install flags and `ignore-scripts` behavior | normalized Markdown SHA-256 `974a2af073f69d37923d599dff5f9a021e030a723e2a0d4ddbbdcaf9d405e3ee`; origin ETag `"6a8f5f20-88c46"` |
| PKG-S5 | SLSA specification v1.0 — Guiding principles | https://slsa.dev/spec/v1.0/principles | OpenSSF (SLSA) | 2026-08-27 | 2027-02-23 or SLSA specification revision | Reviewed | PROVISIONAL-packages-8, -9 | SLSA v1.0 principles; reviewed artifact verification, source traceability and explicit provenance attestations; no product-specific implementation claim | normalized Markdown SHA-256 `b9138985808d2bac00904027653a63d3c214d0fea569ce5342db825e0bc0f8ce`; origin ETag `"168ff589c44e0115db39b1882e35b2c4-ssl"` |
| PKG-S6 | OWASP CI/CD Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html | OWASP | 2026-08-27 | 2027-02-23 or cheat-sheet change | Reviewed | PROVISIONAL-packages-1, -3, -4, -5, -6, -7, -8, -10 | Provider-neutral guidance; reviewed untrusted change paths, least privilege, dependency-chain controls, immutable references, hashes and signing | normalized Markdown SHA-256 `70c5333577603dbd40f045cf457b3d2a2c5a7cfe9193bdcf96c53e2011ecd3e8`; origin last-modified `2026-08-25T20:44:32Z` |
| PKG-S7 | OWASP Software Component Verification Standard | https://scvs.owasp.org/scvs/ | OWASP | 2026-08-27 | 2027-02-23 or SCVS release/site change | Reviewed | PROVISIONAL-packages-2, -3, -9 | Online SCVS v1 index plus V1 inventory, V2 SBOM, V5 component analysis and V6 provenance sections; reviewed direct/transitive inventory, version currency, signature verification and origin/custody | index SHA-256 `b61790db3583a2617a5b8261408f15b87e7a4403d85ffd1d2769fc02887685a0`; reviewed-section aggregate SHA-256 `e1850abd8266ce3fe93d4f9e0765974bd70eb3061bc2656b5dc3578cd6960e80` |
| PKG-S8 | NIST SP 800-218 SSDF v1.1 | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf | NIST | 2026-08-27 | 2027-08-27 or SP 800-218 revision/update notice | Reviewed | PROVISIONAL-packages-2, -4, -6, -8, -9, -10, -11 | v1.1; reviewed PO.3 toolchains, PS.1 least privilege/integrity, PS.2 release verification, PS.3 release archive/provenance and third-party provenance requirements; PS.3 supports retained rollback inputs, not proof of a drill | extracted PDF Markdown SHA-256 `f02c0bff8eeec1572c4dc4621721249c09d00a78c568ec868fb13f2ca33cf99a` |

## Claim review notes

- PKG-S1: full-length commit SHA is GitHub's immutable Action reference; privileged
  `pull_request_target`/`workflow_run` combined with untrusted checkout can expose secrets or
  write access; OIDC avoids stored long-lived cloud credentials.
- PKG-S2: dependency graph covers direct and transitive dependencies and feeds dependency
  review, Dependabot alerts and update features. Feature presence does not prove alert currency.
- PKG-S3: generation needs explicit permissions and an artifact path/digest; verification is a
  separate consumer command. Generation alone cannot satisfy provenance consumption.
- PKG-S4: `npm ci` requires an existing lockfile, exits on manifest/lock mismatch, does not
  rewrite manifests or locks, and requires tree-shaping flags to match lockfile creation.
- PKG-S5: SLSA calls for automated artifact verification, traceability to source and explicit
  provenance attestations instead of inferring integrity from platform configuration.
- PKG-S6: OWASP recommends controlling untrusted production paths, applying least privilege,
  pinning and hash-checking dependencies, enforcing lockfiles, scoping private packages and
  protecting artifact integrity. It does not prove any provider-side setting.
- PKG-S7: SCVS requires known direct/transitive components, current version analysis, signature
  verification at higher levels and verifiable component origin/chain of custody.
- PKG-S8: SSDF requires secured toolchains, least-privileged code access, release-integrity
  verification data, and protected release/provenance archives. Retained releases can supply a
  rollback input; the source does not prove that rollback was wired or exercised.

## Refresh rule

At review time, require all eight IDs, `Reviewed` status, an unexpired deadline and a direct
primary URL. Re-fetch changed content, compare the fingerprint, re-read mapped sections and
record a new review date/fingerprint. Any missing, expired, unreadable or drifted decisive source
forces affected conclusions to `Not verified`; no source row pre-passes a delivery control.
