---
name: secod-cloudflare-pages
description: Satisfy secod-cloudflare, secod-packages-delivery, secod-secrets-config, secod-web-app-security and secod-cloudflare-workers when Pages Functions/bindings are present. Apply when…
---

# SECOD Cloudflare Pages

## Scope and applicability

Satisfy `secod-cloudflare`, `secod-packages-delivery`, `secod-secrets-config`, `secod-web-app-
security` and `secod-cloudflare-workers` when Pages Functions/bindings are present. Apply when
Pages projects, Pages Functions, Git integration, Direct Upload, `pages.dev` deployment URLs,
preview aliases, branch controls, Pages bindings or Pages environment variables/secrets are
detected.

## Control requirements

Exact Pages project, production branch, Git/Direct Upload deployment mode, production and
preview build controls, commit/deployment ID and URL, `pages.dev`/branch/hash/custom domain,
Pages Function/binding, build/runtime environment variable/secret, Access policy, custom-
domain/DNS/TLS and production/preview inventory; production deploys only from the named
protected release branch or an explicitly approved Direct Upload release input, preview branch
controls exclude untrusted/noisy branches where appropriate, build identity and
dependency/install-script policy follow `secod-packages-delivery`, and every deployment is
traceable to immutable source/artifact; preview URLs are treated as public by default, including
immutable hash deployment URLs that can remain directly reachable after a branch alias changes,
so previews receive no production secret, credential, private data or privileged binding and are
protected with Access where sensitive, while Access coverage is tested independently for preview
hashes, `*.pages.dev` and every custom domain because protecting previews alone does not protect
the project/default/custom domain; Pages production and preview use distinct binding IDs and
secrets, variables are classified as plaintext versus encrypted secret, build-time and runtime
values are reviewed separately, no secret reaches static client assets, source maps or build
logs, and Pages Functions follow Workers authorization/binding/egress requirements; custom
domain ownership/DNS/certificate/redirect policy, cache headers and static/private-content
separation are reviewed, branch aliases are never used as immutable release evidence, and
delete/archive/rollback behavior is recorded; negative tests for public
preview/hash/default/custom-domain bypass, preview production-secret/binding/data access,
untrusted branch build/deploy, direct-upload/production-branch confusion, Access policy coverage
gap, build-log/static-asset/source-map disclosure and Pages Function runtime drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare`, `secod-packages-delivery`, `secod-secrets-config`, `secod-web-app-security`.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
