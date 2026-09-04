---
name: secod-cloudflare-workers
description: Satisfy secod-cloudflare, secod-identity-access, secod-inputs-apis, secod-secrets-config, secod-abuse-limits, secod-data-files and secod-observability-response. Apply when…
---

# SECOD Cloudflare Workers

## Scope and applicability

Satisfy `secod-cloudflare`, `secod-identity-access`, `secod-inputs-apis`, `secod-secrets-
config`, `secod-abuse-limits`, `secod-data-files` and `secod-observability-response`. Apply when
Workers, Pages Functions, Durable Objects, R2, D1, KV, service bindings, Browser Rendering,
WebRTC/Realtimes, `wrangler.*` or Workers runtime testing are detected. Verify the selected
controls in the actual workerd/Workers runtime.

## Control requirements

Exact script/version/route/custom domain, compatibility date/flag, handler/service binding,
environment/binding/secret, Durable Object class/namespace/migration, R2 bucket, D1 database, KV
namespace, Browser Rendering/WebRTC configuration, outbound host/egress,
CPU/memory/request/subrequest/concurrency limits, local/remote test and production/preview
inventory; every Worker route has deliberate public/private authentication and backend
tenant/object/action authorization, no raw Access, session, share, Durable Object or service
capability bearer verifier reaches browser code, user-authored code or client RPC, and service
bindings are scoped to a named target with a documented caller/authorization boundary; each
Durable Object has one authoritative writer and explicit tenant/object keying, serialization,
alarm/retry/idempotency, migration and deletion behavior, does not use a client-provided object
ID as authorization, and has no long-lived privileged bearer token in client RPC; R2/D1/KV data
access is tenant/owner/role checked in Worker code and, where supported, storage
policy/namespace/bucket/database bindings are separately scoped, D1 SQL is parameterized with
migration/backup/restore evidence, R2 signed/capability URLs inherit expiry/revocation/upload
validation, and KV cache/state is not used as authoritative authorization without
expiry/invalidation; every user-controlled `fetch` has scheme/credential/host/DNS/IP/private-
address/redirect-hop/response-size/time/concurrency validation, strips credentials on cross-
origin redirect and has egress/cost failure tests; Workers secrets are encrypted secrets rather
than `vars`, `wrangler` environments bind the expected resource IDs/types, production rejects
local `.dev.vars`, process environment and insecure compatibility overrides, and every
compatibility-date/flag change is reviewed for runtime and security impact; test suites run in
workerd/Workers and fail if they silently fall back to Node, with production runtime, binding
and remote-service differences evidenced; Browser Rendering/export has navigation, host, time,
input/output size, page/item, memory, pending-call and concurrency limits plus cancellation and
deterministic browser/session cleanup, while WebRTC/STUN/TURN egress is contained/tested or
explicitly accepted; negative tests for route/authz/capability/DO-ID bypass, cross-tenant
R2/D1/KV access, binding or Wrangler environment confusion, SSRF/redirect/credential-forwarding
bypass, compatibility/runtime fallback, rendering resource leak and WebRTC egress escape.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare`, `secod-identity-access`, `secod-inputs-apis`, `secod-secrets-config`, `secod-abuse-limits`, `secod-data-files`, `secod-observability-response`.

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
