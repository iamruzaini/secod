---
name: secod-xai-grok
description: Satisfy every secod-ai-api-integrations requirement; keep xAI credentials server-side and constrain model access, usage, retention and optional transport authentication.
---

# SECOD Xai Grok

## Scope and applicability

Satisfy every `secod-ai-api-integrations` requirement; keep xAI credentials server-side and
constrain model access, usage, retention and optional transport authentication.

## Control requirements

xAI/Grok and OpenAI-compatible client detection; server-only key; API-key endpoint/model ACLs,
expiry and per-key QPS/QPM/TPM limits; management-key separation; audit logs; rotation and
revocation; model allowlist; per-user/token/spend limits; retry and streaming bounds; training,
retention, privacy and telemetry decisions; Zero Data Retention response-header verification and
incompatible-feature detection; file/public-URL expiry; tenant-scoped prompt-cache keys;
optional mTLS review where used, including certificate lifecycle; structured output validation;
safe usage logs without sensitive prompts or private output.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-ai-api-integrations`.

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
