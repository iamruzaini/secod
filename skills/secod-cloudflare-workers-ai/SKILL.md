---
name: secod-cloudflare-workers-ai
description: Satisfy secod-cloudflare-workers, secod-ai-api-integrations, secod-abuse-limits and secod-observability-response. Apply when Workers AI bindings, env.AI.run, Worker/Pages AI…
---

# SECOD Cloudflare Workers AI

## Scope and applicability

Satisfy `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-abuse-limits` and
`secod-observability-response`. Apply when Workers AI bindings, `env.AI.run`, Worker/Pages AI
inference, model IDs, Workers AI batch/streaming/function-calling features or Workers AI billing
configuration are detected. This profile secures the application-owned inference integration,
not user-controlled agents or MCP servers.

## Control requirements

Exact AI binding/script/environment, model/task/version, request/stream/batch endpoint,
input/output/file/embedding path, rate/usage/billing plan, account/AI Gateway relationship,
error/timeout/abort handling, logs/retention and production/preview inventory; model/task
selection is a server-owned allowlist, client input cannot select arbitrary account model,
binding, gateway, token limit, batch or billing project, every inference request is
authenticated/tenant-scoped and has user, tenant, request, input/file, token, stream,
concurrency, retry, timeout and spend limits, with local Wrangler inference counted in test/cost
controls; streamed and structured output is schema validated and safely rendered before storage,
UI or application workflow, prompts/uploads/RAG text/model output are untrusted and receive the
prompt-injection, tenant-RAG, sensitive-context, moderation and no-consequential-access controls
in `secod-ai-api-integrations`, and application logs never retain sensitive prompts/private
output unless explicitly approved; batch requests are bounded, persisted request
IDs/status/results are tenant-bound and idempotent, worker errors/rate/capacity/abort conditions
have safe retry/degraded behavior, and model/price/limit/version deprecation and upgrade
evaluation are recorded; negative tests for client-selected model/binding/billing route, cross-
tenant inference/RAG/cache leak, prompt-injection-driven data/action exposure,
stream/structured-output rendering abuse, batch status/result IDOR, quota/cost exhaustion and
production-preview model/binding drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-abuse-limits`, `secod-observability-response`.

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
