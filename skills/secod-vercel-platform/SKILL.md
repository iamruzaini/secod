---
name: secod-vercel-platform
description: Satisfy every applicable general baseline requirement; apply when .vercel/project.json, vercel.json/vercel.ts, a Vercel Git/CLI deployment, VERCEL_* system variables, Vercel…
---

# SECOD Vercel Platform

## Scope and applicability

Satisfy every applicable general baseline requirement; apply when `.vercel/project.json`,
`vercel.json`/`vercel.ts`, a Vercel Git/CLI deployment, `VERCEL_*` system variables, Vercel
Functions/Cron/Queues, OIDC or a Vercel deployment URL is detected; verify repository
configuration plus current team/project dashboard or API evidence because code alone cannot
prove deployment protection, access, environment, domain or plan-dependent controls; never allow
`secod-vercel-ai` to substitute for deployment-platform review.

## Control requirements

Inventory the Vercel team/project IDs and names, linked repository, production branch and new-
project first-deployment behavior, root/build/install settings, plan/tier, regions and runtimes;
prevent an unreviewed repository from becoming the initial Production deployment; inventory
Local/Development, Preview, Production and custom environments plus every current and retained
deployment URL, generated URL, branch alias, production alias and custom domain, with an
explicit retention/deletion owner for old deployments; record which URLs are public and which
protection method/scope actually covers each URL class, including Standard, All Deployments,
legacy modes, Trusted IPs, Password, Vercel Authentication/Passport, plan limitations and
unauthenticated negative tests; never assume Standard Protection covers production domains;
inventory and review every Deployment Protection Exception, OPTIONS allowlist, Shareable Link
and automation bypass; treat `VERCEL_AUTOMATION_BYPASS_SECRET`, share-link query values and
bypass cookies as revocable bearer capabilities; use separate least-privilege automation
secrets, prefer the header over query strings, permit query parameters only when a third party
cannot send headers, prevent URL/log/referrer leakage, constrain cookie `SameSite`, monitor use,
rotate/revoke promptly and redeploy when required; explicitly account for automation bypass
disabling deployment protection and some firewall/bot mitigations across the project; enforce
exact Production/Preview/Development/custom/branch targeting for project, shared and integration
environment variables; keep preview deployments and untrusted branches away from production
credentials, databases, regulated data and write-capable services unless explicitly approved and
isolated; use Sensitive Environment Variables where supported, review users who can read
ordinary values, prevent client/framework-public prefixes from exposing secrets, protect local
`vercel env pull` files and verify rotations/redeployments across every linked project and
retained deployment because old deployments keep old values; enable Git Fork Protection and
prevent untrusted fork/PR builds from receiving privileged variables, OIDC tokens, protected
caches, production deploy rights or deploy-hook secrets; review Vercel access tokens, deploy
hooks, Git integration permissions, team/project/access-group roles, production-deployment
permissions, owner/admin separation, MFA/SSO policy where available and periodic access removal;
prefer short-lived Vercel OIDC over static cloud credentials and restrict trust to the expected
team-scoped issuer, audience, subject, team/project and environment claims with JWKS
signature/time validation; account for team/project renames changing claims; review
`vercel.json`/`vercel.ts`, project settings, ignored-build commands, Build Output API,
install/build scripts, build cache and CLI `--public`/`public: true` overrides as privileged
configuration; verify immutable commit/deployment identity and re-run security gates against the
resulting Production deployment because promoting a Preview deployment can rebuild with
Production environment variables rather than promote the identical artifact; require protected
promotion/rollback permissions, health checks, audit evidence, rollback drills and
database/schema/credential compatibility because rollback can route traffic to an older
deployment without rebuilding it; compare repository, dashboard/API, Preview and Production
configuration to detect environment drift; verify domain DNS ownership, team/project assignment,
aliases, branch domains, TLS, canonical redirects, wildcard/custom-domain tenant ownership and
removal of dangling or stale domains; when Vercel Firewall/WAF/Bot/Attack Mode is used, review
rule scope, order, bypass actions, managed/custom rules, environment/domain coverage, logging-
before-deny rollout and plan capabilities while retaining application-layer authentication,
authorization, validation and rate limiting; when Secure Compute, private connectivity or static
egress IPs are used, verify environment/network isolation, region and failover assumptions,
destination allowlists and credential boundaries; keep Build Logs and Source Protection enabled,
prohibit accidental `/_src`/`/_logs`, `--public` or `public: true` exposure, minimize temporary
Vercel Support code visibility and protect log drains, activity/audit logs and retention; verify
or delete retained deployments because changing source/log protection does not necessarily
repair earlier deployments; use Protected Source Maps or remove public maps, while separately
checking inline maps, server-side maps and copies uploaded to third parties because Vercel's
protected-map control does not cover them; never rely solely on automatic build-log redaction
and scan build/runtime/drain logs for short, derived, encoded and multiline secrets; inventory
Vercel Functions, public paths, runtimes, regions, memory, duration, concurrency, retry and cost
limits; authenticate Cron endpoints with a strong rotated `CRON_SECRET`, fail closed when
absent, and require idempotency/replay/race controls for scheduled work; when Vercel Queues is
detected, verify project/environment/topic and consumer-group scope, OIDC or credential
boundaries, retry/idempotency, poison-message handling and reconciliation; alert on
protection/bypass/domain/RBAC/OIDC/environment/firewall/source-visibility changes, abnormal
spend, deployment failures and rollback events.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-vercel-ai`.

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
