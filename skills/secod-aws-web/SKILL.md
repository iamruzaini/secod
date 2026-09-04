---
name: secod-aws-web
description: >-
  Act as the AWS account and IAM security router: use workforce/workload federation and short-lived per-workload roles, least-privilege identity and resource policies, explicit…
---

# SECOD AWS Web

## Scope and applicability

Act as the AWS account and IAM security router: use workforce/workload federation and short-
lived per-workload roles, least-privilege identity and resource policies, explicit public-
exposure decisions, protected secrets and keys, and centralized evidence. It must route every
detected AWS service profile below; no service profile replaces the general app-security
baseline or this common account/IAM layer.

## Control requirements

Exact AWS Organization, account, partition, Region, environment, VPC, availability zone,
service, endpoint, public DNS/domain, IaC stack, principal, role, permission boundary, SCP,
resource policy, KMS key, secret, logging/security service and cross-account inventory; separate
production accounts or an explicit equivalent isolation control, human access through
SSO/federation with MFA and no routine root-user or long-lived IAM-user access keys,
service/workload identities through STS/instance-task-pod/Lambda roles rather than static
credentials, a distinct minimal execution role for every workload rather than a shared broad
role, scoped trust policies with `aws:SourceAccount`, `aws:SourceArn`, audience and external-
ID/confused-deputy protections as applicable, permission boundaries/SCPs/tag conditions where
used, and periodic unused-role/key/policy, Access Analyzer and IAM Access Advisor review; exact
identity, resource, endpoint, key and service-control policies with no unreviewed wildcard
principal/action/resource or public access, explicit cross-account owner/purpose/condition
evidence, mandatory TLS and encryption-in-transit, KMS key policy/grant/rotation/disablement and
encryption-context review, Secrets Manager or Parameter Store secret ownership, rotation,
retrieval role, no secret in source/client/artifact/log/metadata/user data, and
environment/region/production separation; CloudTrail organization/trail and data-event coverage,
CloudWatch/log retention/redaction/alarms, Config/Security Hub/GuardDuty/Access Analyzer
findings and response ownership, backup/restore and incident-access evidence, infrastructure
change review/drift detection, source URL/status or version/last-modified evidence, reviewed
date and review expiry; negative tests for cross-account/principal confusion, overbroad
identity/resource/KMS/secret policy, static credential or secret exposure, unintended public
DNS/resource endpoint, missing regional/environment boundary, logging/alerting bypass, and
service-profile configuration drift.

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
