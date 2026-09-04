---
name: secod-google-genai
description: Satisfy every secod-ai-api-integrations requirement; restrict Gemini credentials and projects, proxy ordinary requests through the backend, and constrain direct Live API access.
---

# SECOD Google Genai

## Scope and applicability

Satisfy every `secod-ai-api-integrations` requirement; restrict Gemini credentials and projects,
proxy ordinary requests through the backend, and constrain direct Live API access.

## Control requirements

`@google/genai`, Gemini API and Live API detection; explicit prohibition of production browser
API keys except constrained Live API ephemeral tokens; API-key restrictions or managed
authentication; project and billing separation; backend proxy; project-level model, rate and
quota limits; billing alerts; leak rotation; training, data-use, retention, region and telemetry
settings; Live API ephemeral-token use count, expiry and locked configuration where officially
supported; Files API 48-hour lifecycle; File Search indefinite retention and deletion; SDK
automatic-retry bounds; safety-setting evidence; structured output validation and safe logging.

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
