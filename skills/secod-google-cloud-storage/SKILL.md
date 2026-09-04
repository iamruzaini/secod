---
name: secod-google-cloud-storage
description: Satisfy secod-google-cloud-web, secod-data-files, secod-secrets-config and secod-abuse-limits. Apply when Cloud Storage buckets, managed folders, object ACLs, signed URLs/policy…
---

# SECOD Google Cloud Storage

## Scope and applicability

Satisfy `secod-google-cloud-web`, `secod-data-files`, `secod-secrets-config` and `secod-abuse-
limits`. Apply when Cloud Storage buckets, managed folders, object ACLs, signed URLs/policy
documents, transfer jobs, static hosting or Cloud Storage notifications are detected. Default to
private, IAM-controlled buckets and bounded object sharing.

## Control requirements

Exact bucket/project/Region, owner, Uniform bucket-level access, public-access-prevention,
IAM/ACL, object prefix, retention/versioning/lifecycle, encryption/KMS key, website/CORS, signed
URL/POST, notification, replication/logging and environment inventory; Uniform bucket-level
access is enabled and legacy object/bucket ACLs are removed unless a documented compatibility
exception exists, public-access prevention is enforced at the strongest applicable
organization/project/bucket scope, no public write and no public-read exception for PII/private
uploads, exact minimum bucket/managed-folder IAM with service identity separation,
TLS/encryption/KMS access review and no client/browser broad storage credential; signed URLs and
signed POST policies are treated as bearer capabilities—not authorization—issued only after
tenant/owner/action/prefix/content-type/content-length/checksum validation, restricted to one
operation and short expiry, never logged or stored as durable credentials, with
lifecycle/revocation/replace/delete strategy, CORS policy and referrer/redirect behavior
reviewed; uploads/downloads inherit file magic-byte/type/size/quarantine/authorization/expiry
controls, notifications use a dedicated least-privilege publisher/consumer and idempotent event
handling, and retention/legal-hold/versioning/backup/restore/data-residency/export decisions are
documented; negative tests for public bucket/object/ACL or broad IAM, cross-tenant prefix/key
signed-URL abuse, signature/expiry/content-type/length bypass, browser credential leakage,
CORS/static-hosting disclosure, notification replay and production-preview bucket/KMS/lifecycle
drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-google-cloud-web`, `secod-data-files`, `secod-secrets-config`, `secod-abuse-limits`.

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
