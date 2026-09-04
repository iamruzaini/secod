---
name: secod-neon
description: Enforce least-privileged PostgreSQL roles and RLS, transaction-safe tenant context, protected production branches, encrypted and restricted database connectivity, safe preview-…
---

# SECOD Neon

## Scope and applicability

Enforce least-privileged PostgreSQL roles and RLS, transaction-safe tenant context, protected
production branches, encrypted and restricted database connectivity, safe preview-data handling
and tested recovery. Apply to every detected Neon organization, project, branch, endpoint, Data
API, Neon Auth, API/CLI key and Neon integration; route `secod-identity-access` and the selected
auth-provider adapter whenever Neon Auth or an external JWT provider is used.

## Control requirements

Exact Neon organization, project ID, cloud/region, plan, owner/admin/member access, billing,
production/default/root/protected/preview branch, database, compute, endpoint, role, connection-
string, Data API, Neon Auth, JWT provider/JWKS, API-key/CLI, IP Allow, Private Networking,
backup/snapshot/history-window and development/preview/staging/production inventory; production
or sensitive-data root branches protected against deletion/reset/archival, protected-branch and
project-deletion evidence, IP Allow restricted to protected branches where selected and
supported by plan, branch creation/restore approval and audit evidence, and no production
credentials copied into preview; preview and CI branches explicitly use schema-only data or
verified anonymized data/masking rules when production data contains secrets, PII or regulated
data, with branch expiry/cleanup, preview endpoint/connection-string isolation, anonymization
limitations and forbidden data types documented, and generated child-branch role passwords
retrieved only from approved secret delivery; TLS for every database connection with
`sslmode=verify-full` where the client supports it, hostname/CA verification, no
client/browser/public-build connection string, direct versus pooled endpoint purpose, and direct
connections only for operations that need session state such as migrations,
`pg_dump`/`pg_restore`, logical replication or long-running administrative work; least-privilege
`GRANT`/`REVOKE`, schema/default-privilege, ownership and `BYPASSRLS` review, RLS enabled with
tenant/owner and operation-specific policies on all user-exposed data, a distinct login-enabled
no-`BYPASSRLS` application role for direct backend requests, and `neondb_owner`/administrative
URLs limited to migrations, trusted privileged workers or a documented manual-authorization
boundary; when backend RLS depends on request JWT claims, fixed trusted JWKS/discovery origin
plus allowed algorithm, issuer, audience, expiry/not-before, subject and required-claim
verification before use, bounded JWKS cache/unknown-`kid` refresh/key rotation, and user claims
set only inside a per-request database transaction using transaction-local configuration so
PgBouncer/pooled connections cannot leak one tenant's identity, role or session state to
another; Data API branch/database/URL and exposure inventory, default-deny decision unless it is
deliberately used, fixed auth provider/JWKS and JWT audience when supported by the issuer, no
anonymous writes, minimum role grants, RLS on every exposed table, explicit schemas, CORS
origins, role-claim mapping, OpenAPI mode, response-row/aggregate limits and schema-cache
refresh/review; record and test the current platform constraint that Data API cannot be enabled
in a project using IP Allow or Private Networking—choose and evidence a Data API/RLS
architecture or a private/restricted direct-connection architecture rather than claiming both
network protections apply, while recognizing that Data API itself relies on PostgreSQL grants
and RLS rather than a separate Neon permission layer; scoped API/CLI credentials with project-
scoped keys preferred over organization or personal keys, one-time secret capture into managed
secret storage, no key in source, browser, preview build, logs or CI output, named
owner/purpose/expiry review, immediate revoke/replacement plan because keys remain valid until
revoked, and database-role-password rotation across every affected branch/endpoints after
exposure; IP Allow CIDR inventory and change control, PrivateLink/VPC endpoint restriction and
public-internet-blocking evidence when selected, no broad or stale developer/CI IP ranges, and
an explicit accepted-risk record where plan or architecture prevents network restriction; point-
in-time restore/history-window, manual/scheduled snapshot or external-backup retention,
encryption/access and RPO/RTO decision, a restore drill using preview before production cutover,
root-branch-only PITR and full-branch/all-database overwrite implications, automatic backup-
branch protection/cleanup and the snapshot-restore/PITR limitations documented; exact Neon
Console/API/CLI, Postgres driver/ORM and migration versions, source URL/status or version/last-
modified evidence, reviewed date and review expiry; negative tests for protected-branch
bypass/deletion/reset, preview PII or production-credential exposure, TLS downgrade,
direct/pooler misuse, over-broad grants, `BYPASSRLS`/owner URL use, missing RLS policy,
forged/expired/wrong-issuer/audience/JWKS JWT, connection-pool tenant-context leakage, Data API
anonymous/CORS/schema/role/RLS exposure, unsupported Data API plus IP Allow/Private Networking
configuration, over-scoped/revoked API key use, stale allowlist/VPC/public connection access,
and failed branch/PITR/snapshot/backup restoration.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-identity-access`.

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
