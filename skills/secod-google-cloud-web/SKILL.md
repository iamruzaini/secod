---
name: secod-google-cloud-web
description: >-
  Act as the Google Cloud organization, project and IAM security router: use short-lived federated workload identity and dedicated service accounts, least-privilege IAM and resource…
---

# SECOD Google Cloud Web

## Scope and applicability

Act as the Google Cloud organization, project and IAM security router: use short-lived federated
workload identity and dedicated service accounts, least-privilege IAM and resource policy,
deliberate public-exposure decisions, per-secret access and centralized evidence. Route every
detected Cloud Storage profile below; when
Firebase services or Firestore in Native mode are detected, also require `secod-firebase` rather
than duplicating its Rules/App Check review. No service profile replaces this common layer or
the general app-security baseline.

## Control requirements

Exact organization, folder, billing account, project number/ID, Region, environment, VPC/Shared
VPC, resource, endpoint/domain, IaC, principal, service account, IAM binding/condition,
organization policy, secret/KMS key, logging/security service and cross-project inventory;
production project separation or an explicit equivalent isolation control, human access through
Cloud Identity/SSO with MFA and no routine owner/basic-role use, workload access through ADC,
Workload Identity Federation or attached service identity rather than downloaded service-account
JSON keys, a distinct minimal runtime identity for each workload, and service-account key
inventory, expiry/rotation/revocation and exceptional-use evidence; exact project, resource and
service-account IAM with no unreviewed basic role, `allUsers`/`allAuthenticatedUsers`, wildcard
member or broad inherited binding, explicit cross-project principal/purpose/condition evidence,
least-privilege impersonation/deployment/secret roles, per-secret and where supported per-
version `Secret Manager Secret Accessor` grants, no secret in source, browser, build artifact,
environment dump or logs, encryption/KMS key separation, and private-service/VPC Service
Controls/organization-policy decisions where used; Cloud Audit Logs admin/activity and
applicable data-access coverage, Cloud Asset/IAM policy and public-exposure review, Security
Command Center or equivalent finding ownership where enabled, Logging/Monitoring
retention/redaction/alerts, backup/restore and incident-access evidence, IaC change review/drift
detection, source URL/status or version/last-modified evidence, reviewed date and review expiry;
negative tests for service-account key/metadata/impersonation abuse,
inherited/broad/public/cross-project IAM, secret/KMS access outside the named workload,
production-project/environment confusion, unintended public endpoint/storage/data access, and
logging/alert/drift evidence gaps.

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
