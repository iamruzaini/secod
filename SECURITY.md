# Security policy

SECOD is an early public release. It is security guidance and verification
assistance, not a security certification.

## Supported versions

| Version | Support status |
| --- | --- |
| `0.1.x` | Current public release line; security reports accepted |
| `0.1.0-beta.1` | Historical prerelease; upgrade to `0.1.x` before reporting unless the issue is reproducible there only |
| Other versions | Not supported; reproduce on the current `0.1.x` release first |

The current supported version is the latest published `0.1.x` release. Source
registers and provider guidance can change when official documentation or
service behavior changes.

## How to report a vulnerability

Do not report sensitive details through a public GitHub issue, discussion,
pull request or chat message.

After private vulnerability reporting is enabled for this repository, use:

1. Open the repository's **Security** tab.
2. Open **Advisories**.
3. Select **Report a vulnerability**.
4. Provide affected version or commit, impact, reproduction steps, and a safe
   remediation suggestion if available.

Do not include real credentials, private customer data, production URLs with
embedded secrets, or exploit material that is unnecessary to reproduce the
issue. Use synthetic test values and redact logs.

If the private-reporting option is unavailable, do not put vulnerability
details in a public issue. Open a non-sensitive issue asking maintainers to
provide a private reporting path.

## Response targets

- Acknowledgement: within five business days.
- Initial triage: within 10 business days where reproduction details are
  sufficient.
- Status updates: at least every 14 calendar days until resolution or an agreed
  disclosure date.

These are maintenance targets, not a guarantee. Reports may require provider,
framework or agent-runtime verification before severity can be determined.

## Coordinated disclosure

Maintainers will work with the reporter to:

1. Confirm scope, affected versions and severity.
2. Develop and test a fix or mitigation.
3. Publish a patched release or documented mitigation.
4. Agree on a disclosure date that gives users reasonable time to update.
5. Credit the reporter when requested and safe.

Do not publicly disclose details before an agreed date. If exploitation is
active or users face immediate risk, maintainers may publish an accelerated
warning with the minimum information needed to protect users.

## Scope

Reports may cover:

- Malicious or unsafe instructions in a SECOD skill.
- Incorrect security guidance that creates a material vulnerability.
- Credential exposure, unsafe scripts or unintended network/file actions.
- Vulnerabilities in release tooling, source-register validation or packaged
  skill contents.

Provider service vulnerabilities should also be reported to the affected
provider through its own security channel. SECOD cannot remediate provider
platform defects.
