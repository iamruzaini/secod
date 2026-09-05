# SECOD

Security coding skills for AI builders.

[![skills.sh](https://skills.sh/b/iamruzaini/secod)](https://skills.sh/iamruzaini/secod)

## What SECOD is

SECOD is an open-source library of 57 Agent Skills for security work on
websites, web applications, mobile backends, APIs, infrastructure and AI
integrations. It combines generalized security skills with conditional
framework and provider skills.

The generalized skills cover areas such as identity and access, web security,
input and API boundaries, runtime execution, cryptography, files, abuse limits,
secrets, delivery, vulnerability management, observability, payments, AI
integrations, containers, messaging, failure safety and ship checks.

Provider skills add stack-specific guidance for services such as AWS, Google
Cloud, Firebase, Cloudflare, Vercel, Supabase, authentication providers,
payments providers and AI providers. Provider detection never replaces the
generalized baseline or proves that a control passed.

The canonical product repository is
[`iamruzaini/secod`](https://github.com/iamruzaini/secod). The SECOD website is
a separate catalog and documentation surface that imports tagged SECOD
releases.

## Current maturity

Current status: early public release.

SECOD v0.1.0 provides 57 generalized and provider-specific security skills. It
is not a security certification. Controls without sufficient technical or
provider evidence must be reported as `Not verified`.

All 57 skills remain publicly discoverable. Provider adapters whose source
registers contain `Pending review` entries are provisional: their direct
official URLs have been identified, but their claims have not completed
substantive control-by-control review. URL reachability alone is never treated
as reviewed evidence.

## Installation

SECOD is distributed as Agent Skills directories through the open Skills CLI.
It does not require a separate SECOD npm package.

```powershell
# Browse all available SECOD skills
npx skills add iamruzaini/secod --list

# Install every skill for Codex
npx skills add iamruzaini/secod --skill '*' --agent codex --yes

# Install every skill for Claude Code
npx skills add iamruzaini/secod --skill '*' --agent claude-code --yes

# Install every skill for Cursor
npx skills add iamruzaini/secod --skill '*' --agent cursor --yes

# Install one skill
npx skills add iamruzaini/secod --skill secod-core --agent codex --yes

# Install globally
npx skills add iamruzaini/secod --skill '*' --agent codex --global --yes

# Update installed skills
npx skills update
```

## Selective installation

Install only skills relevant to an application. For example:

```powershell
# General baseline entry point
npx skills add iamruzaini/secod --skill secod-core --agent codex --yes

# Authentication and Next.js coverage
npx skills add iamruzaini/secod --skill secod-identity-access,secod-nextjs --agent codex --yes

# AWS web application coverage
npx skills add iamruzaini/secod --skill secod-aws-web,secod-aws-lambda-api-gateway --agent codex --yes

# Firebase and Google Cloud coverage
npx skills add iamruzaini/secod --skill secod-firebase,secod-google-cloud-web --agent codex --yes
```

Use `--list` first when checking exact skill names. `secod-core` routes the
applicable generalized and provider coverage; installing a provider adapter
does not make that provider applicable to every project.

## Supported agents

SECOD uses the open Agent Skills directory format. Current documented
distribution targets are:

- OpenAI Codex
- Claude Code
- Cursor

The Skills CLI supports additional agents. Compatibility depends on each
agent's Agent Skills support and installation location. Installation smoke
verification for Codex, Claude Code and Cursor remains a release gate and is
not evidence that a security control passes in an application.

## Updating

Update installed skills from their source repository:

```powershell
npx skills update
```

Review changes before relying on updated security guidance. Pin and test a
known SECOD Git tag when reproducibility is more important than tracking the
latest commit.

## Uninstalling

Remove selected skills with the Skills CLI:

```powershell
npx skills remove secod-core --agent codex --yes
```

To remove all skills installed for one agent, use the CLI's `--all` option:

```powershell
npx skills remove --all --agent codex --yes
```

Repeat for each agent and scope where SECOD was installed. Confirm that
unrelated skills remain installed.

## Evidence model

SECOD separates security guidance from evidence about a particular project.
Skills inspect repository, deployment, provider and dashboard evidence when it
is available. Missing, inaccessible, stale or contradictory evidence is
reported as `Not verified`.

Each skill keeps a source register in `references/sources.md`. Statuses mean:

- `Reviewed`: source content was read and mapped to controls.
- `Pending review`: an official source was identified, but substantive mapping
  is incomplete.
- `Not verified`: evidence is inaccessible, stale or insufficient.

An official documentation URL, package name or provider detection signal does
not prove that a project is configured securely. SECOD never provides a
security certification or a passing conclusion without technical evidence.

## Testing status

Seven skills currently have executable insecure-fixture suites. The remaining
fixture directories are documentation-only test plans unless explicitly marked
otherwise.

Repository validation currently covers catalog structure, Agent Skills
metadata, source-register requirements, test layout and repository hygiene.
The executable fixture suites are:

- `secod-abuse-limits`
- `secod-crypto-data-protection`
- `secod-failure-safety`
- `secod-observability-response`
- `secod-packages-delivery`
- `secod-payments-billing`
- `secod-secrets-config`

Run repository checks from a clone:

```powershell
python scripts/validate_skills.py
python scripts/validate_test_layout.py
python scripts/check_repo_hygiene.py
```

## Limitations

- Some provider source registers remain provisional and contain `Pending review`
  entries.
- Not every skill has an executable insecure fixture.
- Documentation-only fixture plans are not executable test results.
- Provider dashboard, plan, region, runtime and deployment settings cannot be
  inferred from package presence.
- Skills provide security guidance and review structure; they do not replace
  application testing, provider configuration review, incident response,
  professional security assessment or compliance advice.
- Supported-agent installation and behavior verification must be completed
  before treating this release as fully validated.

## Security reporting

Do not disclose sensitive vulnerability details in public issues, discussions,
pull requests or chat.

Use the repository's GitHub Security tab and private vulnerability reporting
once enabled. Include a minimal reproduction, affected version or commit,
impact, prerequisites, and a safe contact path. Remove credentials, personal
data and production secrets from all reports.

Maintainers should acknowledge valid reports within five business days and
provide a status update at least every 14 calendar days until resolution or an
agreed disclosure date. See [`SECURITY.md`](SECURITY.md) for the supported
version policy and coordinated-disclosure process.

## License

SECOD is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for
the full terms.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a change. Security
guidance changes should include applicable official source evidence, control
mappings, trigger coverage and fixture updates. Never include real credentials
or private project data.
