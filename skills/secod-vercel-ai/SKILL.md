---
name: secod-vercel-ai
description: Satisfy every secod-ai-api-integrations requirement; scope AI Gateway and AI SDK access to the correct project, providers, models, budgets and telemetry policy.
---

# SECOD Vercel AI

## Scope and applicability

Satisfy every `secod-ai-api-integrations` requirement; scope AI Gateway and AI SDK access to the
correct project, providers, models, budgets and telemetry policy.

## Control requirements

`ai`, `@ai-sdk/*` and AI Gateway detection; prefer short-lived Vercel OIDC over long-lived
Gateway API keys; project/team scoping; team-wide provider and model allowlists; per-key budgets
and usage monitoring; BYOK credentials being team-scoped; prevent request-scoped BYOK credential
exposure; explicit approval of fallback from BYOK to Vercel system credentials; identical
privacy, region and retention guarantees across fallback providers; fallback/retry/stream
limits; AI SDK DevTools forbidden in production; telemetry prompt/output redaction; structured
output validation; safe logging without sensitive prompts or private output.

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
