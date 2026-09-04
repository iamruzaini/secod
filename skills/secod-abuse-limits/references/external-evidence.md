# External evidence intake contract

Use this contract whenever repository evidence cannot establish deployed limiter/idempotency
state, provider spend controls or topology-matched runtime behavior. Blank templates, unexecuted
plans and screenshots without account, environment and capture identity are not evidence.

## Evidence bundle

Create a JSON manifest beside retained, redacted artifacts. Set `schema_version` to `1`, list only
applicable controls, then record every artifact with:

- unique `id`, `kind`, `control_ids`, `environment`, `deployment_id`, `source` and nonempty
  `captured_by` principal;
- timezone-qualified `captured_at` and later `expires_at`;
- bundle-relative `path`, lowercase SHA-256, `redacted: true`, `authorized: true`.

Declare every reviewed environment/deployment pair in `reviewed_deployments`. Required artifact
kinds must be complete within each pair; evidence from one environment never fills another.

When ABUSE-01 applies, add `deployment_topologies` rows with environment, deployment ID, topology
class, regions, instance IDs, limiter-store ID and `multi_instance`. Supply one matching
`shared_store_consistency` artifact per row. Every `*_test` artifact also records command,
thresholds, responses, side-effect count, cleanup status and execution status.

Use evidence captured within 90 days with validity no longer than 90 days. Future-dated captures
are invalid. A `shared_store_consistency` artifact always identifies at least two tested instances;
single-instance topology declarations do not reduce that probe minimum.

Run:

```text
python skills/secod-abuse-limits/scripts/validate_evidence_bundle.py path/to/manifest.json
```

Exit `0` proves structural completeness and artifact integrity only. Inspect contents, correlate
them to reviewed code/deployment, run required negative tests, then assign control status. Never
promote `Structurally complete` directly to `Passed with evidence`.

## Required captures

- ABUSE-01: deployed limiter config, multi-instance shared-store consistency, burst result.
- ABUSE-02: authentication throttling and recovery-response uniformity results.
- ABUSE-03: deployed idempotency config and duplicate-delivery result.
- ABUSE-04: atomicity config and concurrent-mutation result.
- ABUSE-05: retry config and persistent-failure injection result.
- ABUSE-06: business ceiling config and stable-identity bypass result.
- ABUSE-07: job cap config and timeout/cancellation result.
- ABUSE-08: concurrency config, load-shedding result and provider spend control.

For `shared_store_consistency`, identify at least two tested instances; cover every topology class
and region. For `provider_spend_control`, record provider, account/project, control mode
(`hard_ceiling`, `billing_alert`, or `both`), amount, currency, reset period and alert recipients.
An alert is not a hard ceiling; preserve stated provider behavior.

## Runtime safety

Run probes only in an authorized non-production environment. Capture deployment identity, limiter
store identity, instance/region identities, command, thresholds, timestamps, responses, side-effect
counts and cleanup. Abort on real-user impact, uncontrolled cost, irreversible mutation,
cross-tenant effects or lost observability.

Missing, stale, wrong-scope, inaccessible, contradictory or failed evidence keeps affected
controls `Not verified`. Route final verdict to `secod-ship-check`.
