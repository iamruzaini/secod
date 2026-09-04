---
name: secod-aws-data-services
description: Satisfy secod-aws-web, secod-data-files, secod-inputs-apis, secod-secrets-config and secod-observability-response. Apply when RDS/Aurora, DynamoDB, ElastiCache, OpenSearch,…
---

# SECOD AWS Data Services

## Scope and applicability

Satisfy `secod-aws-web`, `secod-data-files`, `secod-inputs-apis`, `secod-secrets-config` and
`secod-observability-response`. Apply when RDS/Aurora, DynamoDB, ElastiCache, OpenSearch,
Redshift, DocumentDB, database proxies, data streams/backups or database credentials are
detected. Keep databases non-public by default and enforce tenant/object authorization in the
application and database mechanisms appropriate to the selected service.

## Control requirements

Exact database/table/cluster/cache/search domain/proxy, engine/version, account/Region,
subnet/security group/VPC endpoint, public endpoint, IAM/database role, user/credential, KMS
key, TLS, parameter/option group, backup/snapshot/PITR, replication, export, stream, log/audit
and environment inventory; RDS/Aurora and other relational databases are private in controlled
subnets/security groups with least-privilege ingress only from identified workloads, TLS
certificate verification, no public endpoint without an accepted exception, distinct
database/application/migration/admin roles, no shared superuser URL, Secrets Manager or IAM
database authentication where compatible, rotation/connection-pool/revocation behavior,
parameterized queries/RLS or equivalent tenant enforcement, encrypted storage/backups/snapshots,
audit/error logs, backup retention/PITR and restore drills; DynamoDB uses per-workload roles and
minimum table/index/stream actions, IAM condition keys/fine-grained item/attribute access where
the architecture needs it, no client-side broad table credentials, encryption/KMS key policy,
PITR/backup, TTL/stream/export access and VPC endpoint policy where selected, with application
tenant-key/object checks and idempotency for conditional writes; every data export, replica,
read replica, snapshot, test copy, analytics/search index, cache or stream has a data-
classification, authorization, encryption, retention/deletion and production-to-preview
isolation decision; negative tests for public database/search endpoint, network/security-group
bypass, TLS downgrade, database admin/migration credential use in application paths, SQL/NoSQL
injection, cross-tenant query/key/attribute access, overbroad DynamoDB role/stream/export,
plaintext/unauthorized backup or snapshot sharing, failed PITR restore, and data/service
environment drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-aws-web`, `secod-data-files`, `secod-inputs-apis`, `secod-secrets-config`, `secod-observability-response`.

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
