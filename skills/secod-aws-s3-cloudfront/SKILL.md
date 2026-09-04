---
name: secod-aws-s3-cloudfront
description: Satisfy secod-aws-web, secod-data-files, secod-secrets-config and secod-abuse-limits. Apply when S3 buckets/access points/object-lambda, CloudFront…
---

# SECOD AWS S3 Cloudfront

## Scope and applicability

Satisfy `secod-aws-web`, `secod-data-files`, `secod-secrets-config` and `secod-abuse-limits`.
Apply when S3 buckets/access points/object-lambda, CloudFront
distributions/functions/Lambda@Edge, signed URLs/cookies, S3 website hosting, presigned
upload/downloads, or static assets are detected. Default to private origins and explicit,
bounded sharing.

## Control requirements

Exact bucket/access point/object prefix, owner/account/Region, Block Public Access, Object
Ownership/ACL, bucket/access-point policy, encryption/KMS key,
versioning/lifecycle/replication/logging, static website, presigned URL/POST, CloudFront
distribution/behavior/cache/origin/OAC/OAI/WAF/function/domain/certificate/signed URL/cookie and
environment inventory; all non-public buckets have account and bucket Block Public Access,
Bucket owner enforced Object Ownership with ACLs disabled unless a documented exception, minimum
bucket/access-point policy and IAM role access, TLS-only `aws:SecureTransport` denial,
encryption/KMS key/grant separation, versioning/lifecycle/retention and access/data-event
logging, no wildcard public write, no browser/server secret or unrestricted bucket credential,
and presigned upload/download URLs limited by object key/prefix, content type/length/checksum,
expiry, operation, tenant/owner authorization and revocation/lifecycle plan; CloudFront is the
only intended viewer path to a private S3 origin, uses Origin Access Control with signed origin
requests rather than legacy OAI unless an accepted migration exception exists, restricts the
bucket policy to the exact distribution, keeps the S3 origin private, validates SSE-KMS key
permission, enforces viewer HTTPS, uses exact cache/origin-request policy with no unintended
forwarding/caching of authorization, cookies or private responses, applies WAF/rate-limit/bot
and signed URL/cookie policy when required, and protects custom domain/certificate/DNS changes;
static website hosting or intentionally public content has an explicit read-only public
decision, no secrets/PII/private uploads, upload/write path separated from public asset origin,
and no reliance on obscurity, CORS or CloudFront alone for authorization; negative tests for
public bucket/access point/ACL or wildcard policy, direct S3-origin bypass, unsigned/overbroad
CloudFront origin access, presigned URL cross-tenant/key/content/expiry abuse, cache/private-
response leakage, insecure transport/KMS denial, public website write, and production-preview
bucket/domain policy drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-aws-web`, `secod-data-files`, `secod-secrets-config`, `secod-abuse-limits`.

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
