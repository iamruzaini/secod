---
name: secod-convex
description: Authenticate and authorize every public Convex function at the server boundary; make privileged, scheduled and ctx.run* implementation paths internal-only; treat storage URLs and…
---

# SECOD Convex

## Scope and applicability

Authenticate and authorize every public Convex function at the server boundary; make privileged,
scheduled and `ctx.run*` implementation paths internal-only; treat storage URLs and deploy keys
as bearer capabilities; and preserve deployment, recovery, audit and usage-control evidence.
Apply to each detected Convex team, project, production/development/preview deployment, custom
domain, HTTP Actions endpoint, file store, deploy key, log stream and backup configuration.

## Control requirements

Exact Convex team/project, deployment name/reference/type/region/class,
production/development/preview URL, custom domain, Convex/npm/CLI version, auth provider,
environment variable, deploy key, HTTP Action route, file-storage, scheduled/cron,
backup/restore, usage-limit, deployment-history, audit-log and log-stream inventory; CI/CD has a
fixed intended deployment target with explicit production versus preview/development evidence,
never lets branch, pull-request, user-controlled configuration or an implicit CLI default select
production, keeps production and non-production credentials/configuration/data isolated, expires
non-production deployments, and requires protected release/promotion/rollback evidence; every
exported public `query`, `mutation`, `action` and `httpAction` has explicit argument validation,
return validation where it constrains data exposure, authentication and
resource/tenant/owner/role authorization before reads, writes, file issuance or external
effects, bounded pagination/query work, and no identity, tenant, role, email, storage ID or
authorization fact trusted merely because the client supplied it; every `internalQuery`,
`internalMutation` and `internalAction` retains invariant/argument checks appropriate to its
callers, and all scheduler/cron targets plus every `ctx.runQuery`, `ctx.runMutation` and
`ctx.runAction` invocation use the generated `internal.*` reference rather than an externally
callable `api.*` reference unless a documented, separately authenticated public trigger is
required; scheduled/action workflows account for the fact that actions are at-most-once and may
leave scheduled side effects after a later error, mutations schedule atomically, scheduler
authentication is not propagated, cancellation/replay/idempotency is explicit, and privileged
Dashboard/CLI function execution is separately access-controlled and audited; HTTP Actions have
a complete method/path/origin/body/content-type/authorization/webhook-signature inventory,
authenticate and authorize before processing, verify raw-body webhook signatures with
replay/timestamp/idempotency controls, allow only exact CORS origins/methods/headers, set `Vary:
Origin`, never reflect arbitrary origins or combine credentialed requests with `*`, set app-
level request/body/upload, timeout, concurrency and outbound-fetch limits, and honor Convex's
HTTP Action response-size limit rather than proxying unbounded private data; generated upload
URLs are issued only after authorization, requested immediately before use and treated as short-
lived upload capabilities, while generated download URLs are classified as bearer capabilities
because anyone holding the URL can read the file—issue them only for intentionally shareable
access, do not use a storage ID as authorization, delete and re-upload to revoke a shared URL,
and use an authenticated/authorized HTTP Action for private files whose access can change, with
file type/size/content, tenant/owner, metadata and lifecycle checks inherited from `secod-data-
files`; deployment-scoped deploy keys use the minimum named action set (for normal CI
deployment, only `deployment:deploy`), are stored only in managed CI/server secret storage,
never emitted to repository, browser, preview build, logs or command output, have an
owner/purpose/target/deployment/review and immediate revoke/rotation plan, and do not substitute
a broad user token, project token or admin key where a narrowly scoped deployment key suffices;
all secrets/configuration use the correct deployment environment, are not returned from public
functions or logs, are rotated/revoked after exposure, and external credentials receive least
privilege and egress/timeout/retry handling; usage limits/budgets, function/action/scheduled-
job/concurrency/storage/file-egress and log-stream capacity are set or explicitly accepted per
deployment and plan, with abuse/cost alerting, error/exception response, no
secret/PII/prompt/body logging, and application-layer WAF/rate-limit/bot controls evaluated for
public custom-domain, realtime and HTTP Action surfaces rather than assuming network-level DDoS
protection is sufficient; backup schedule, retention, encryption/access, database-plus-file
inclusion, RPO/RTO and restore exercise evidence, with the documented restore limitations
addressed because backups do not restore source/deployment configuration, environment variables
or pending scheduled functions and a restore can require a known-good code/configuration rollout
and manual data repair; deployment configuration history/team audit review, Dashboard edit-
confirmation policy, audit-log/log-stream destination access, event selection,
redaction/retention, health monitoring and at-least-once/duplicate or best-effort delivery
handling, with durable audit logging only claimed when its plan/deployment prerequisites and
destination evidence are present; exact dashboard/CLI settings and source URL/status or
version/last-modified evidence, reviewed date and review expiry; negative tests for public-
function validator/authz/tenant/object bypass, client-supplied identity/ID confusion, public
`api.*` scheduling or `run*` invocation, action retry/schedule/cancel/replay defects, HTTP
CORS/body/signature/replay abuse, bearer file URL/share/revocation/private-file bypass,
generated-upload abuse, preview-to-production deployment or secret/config drift, over-
scoped/revoked deploy-key use, environment/log disclosure, usage-limit/cost-abuse failure, log-
stream duplicate/loss/redaction defects, and incomplete backup/restore recovery.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`.

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
