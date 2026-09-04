---
name: secod-aws-lambda-api-gateway
description: Satisfy secod-aws-web, secod-identity-access, secod-inputs-apis, secod-abuse-limits and secod-secrets-config. Apply when Lambda, Lambda Function URLs, API Gateway…
---

# SECOD AWS Lambda API Gateway

## Scope and applicability

Satisfy `secod-aws-web`, `secod-identity-access`, `secod-inputs-apis`, `secod-abuse-limits` and
`secod-secrets-config`. Apply when Lambda, Lambda Function URLs, API Gateway REST/HTTP/WebSocket
APIs, ALB Lambda targets, SAM/CDK/serverless framework API definitions, Lambda layers or Lambda
event-source mappings are detected. Every internet-reachable invocation path must be identified
and intentionally authenticated/authorized.

## Control requirements

Exact function, alias/version, runtime, architecture, layer, Function URL, API Gateway
API/stage/route/method/authorizer/integration, ALB, custom domain, CORS, WAF, throttling, usage
plan, event-source, concurrency, DLQ/destination, VPC/subnet/security-group, environment/secret
and production/preview inventory; a unique least-privilege Lambda execution role per workload
with only required logs/data/network permissions, separate deployment/invoker roles, no shared
administrator role, scoped Lambda resource policies for every service/cross-account invoker
using the expected principal and `SourceArn`/`SourceAccount`, and review of aliases, versions,
layers and code-signing/deployment provenance; each Function URL has an explicit `AWS_IAM` or
intentionally public `NONE` decision, with public `NONE` URLs treated as unauthenticated
internet endpoints requiring application authentication/authorization, request limits and abuse
controls, and resource-policy conditions such as `lambda:InvokedViaFunctionUrl` so access cannot
expand through another invocation path; API Gateway uses a real authorizer, Cognito JWT
authorizer, Lambda authorizer or IAM authorization for protected routes, verifies authorization
at the backend as well as at the gateway, has exact route/method/stage/domain/CORS/request-
validation/body-size/timeout/throttle/quota/WAF/resource-policy/private-endpoint configuration,
and never treats API Gateway API keys or usage plans as authentication or authorization—they are
consumer-usage tracking and limiting controls only; correct authorizer/JWT issuer, JWKS,
audience/client, algorithm, expiry, scopes and tenant claims, no credentials/tokens in query
strings or logs, webhook raw-body signature/replay handling, strict integration response/error
redaction and no unauthenticated proxy to privileged AWS APIs; reserved/provisioned concurrency,
event-source batch/visibility/retry/failure/DLQ/destination, idempotency and partial-failure
behavior bounded against duplicate delivery, and safe deploy/rollback/canary/alias traffic
policy; no public Lambda/API Gateway/ALB route, permissive CORS, `NONE` Function URL, wildcard
invocation policy, overbroad execution role, unauthenticated authorizer fallthrough, API-key-
only protection, layer/runtime CVE, event replay, or public backend integration without explicit
evidence and negative tests.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-aws-web`, `secod-identity-access`, `secod-inputs-apis`, `secod-abuse-limits`, `secod-secrets-config`.

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
