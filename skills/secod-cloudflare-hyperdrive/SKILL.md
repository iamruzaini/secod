---
name: secod-cloudflare-hyperdrive
description: Satisfy secod-cloudflare-workers, secod-secrets-config, secod-inputs-apis and secod-data-files. Apply when Hyperdrive configurations/bindings, database connection strings,…
---

# SECOD Cloudflare Hyperdrive

## Scope and applicability

Satisfy `secod-cloudflare-workers`, `secod-secrets-config`, `secod-inputs-apis` and `secod-data-
files`. Apply when Hyperdrive configurations/bindings, database connection strings, Cloudflare
Tunnel/Workers VPC database paths, TLS/mTLS certificates, Hyperdrive credential rotation or
supported database drivers are detected. Hyperdrive is transport/pooling; application and
database authorization remain mandatory.

## Control requirements

Exact Hyperdrive configuration/binding/environment, origin database/role/host/network path,
connection-string/local-connection-string, TLS mode/CA/client certificate, Tunnel/Access service
token or Workers VPC service, database firewall, driver/ORM/version, query
timeout/transaction/pool behavior, credential rotation and production/preview inventory; origin
database connection credentials, CA and client-key material remain in Cloudflare
secret/configuration storage and never source, CLI history/build log/browser or
`localConnectionString` shared with production, production and preview bind distinct
Hyperdrive/database roles, and Worker code never returns the generated Hyperdrive connection
string; database connections use TLS with `verify-full`/equivalent hostname and CA validation
where supported, mTLS is used when required, private databases use Workers VPC or Cloudflare
Tunnel with an exact Access service-auth/token policy rather than broad public firewall
exposure, and any Cloudflare-IP allowlist is minimum and reviewed; database roles are least
privilege with parameterized queries, RLS/tenant/object authorization, backup/restore and
credential rotation/revocation tests, while Hyperdrive binding alone is not treated as database
authorization; database client is created inside each request/queue/workflow handler rather than
global scope, long transactions and persistent Durable Object connections are bounded to avoid
pool exhaustion, and connection/error/timeout metrics exclude credentials; negative tests for
direct public database path, TLS/CA/hostname downgrade, leaked local/origin/Hyperdrive
credential, broad Access Tunnel/service token or firewall, app/admin database role use,
SQL/tenant bypass, global-client/pool exhaustion and production-preview binding/database drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare-workers`, `secod-secrets-config`, `secod-inputs-apis`, `secod-data-files`.

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
