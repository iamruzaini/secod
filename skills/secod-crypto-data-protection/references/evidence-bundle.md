# External evidence bundle contract

This bundle makes non-repository evidence reviewable without treating structure as proof. Keep all
artifact files beside the manifest or below its directory. Redact credentials and protected data.

Run from `secod/`:

```text
python skills/secod-crypto-data-protection/scripts/validate_evidence_bundle.py path/to/manifest.json
```

## Manifest

Required top-level fields:

- `schema_version`: `1`.
- `applicable_controls`: non-empty subset of `SECOD-CDP-01`, `SECOD-CDP-04`, `SECOD-CDP-08`,
  `SECOD-CDP-09`.
- `expected_tls_endpoints`: complete endpoint inventory when `SECOD-CDP-01` applies.
- `expected_managed_resource_ids`: complete managed-store inventory when `SECOD-CDP-04` applies.
- `expected_deletion_store_ids`: every provider/store requiring deletion confirmation when
  `SECOD-CDP-08` applies.
- `expected_backup_ids`: backups covered by supplied encryption evidence when `SECOD-CDP-09`
  applies.
- `artifacts`: evidence artifact objects.

Every artifact requires `id`, `kind`, `control_ids`, `environment`, `deployment_id`, `source`,
`captured_at`, `valid_until`, `path`, `sha256`, `redacted: true`, and `authorized: true`.
Timestamps must include timezones. `path` must be relative and remain inside the bundle. `sha256`
must match the referenced non-empty file. Evidence is stale when `valid_until` is not after review
time.

## Kind-specific fields

- `deployed_tls_posture`: `endpoints`, `minimum_protocol` (`TLSv1.2` or `TLSv1.3`), and
  `certificate_validation: true`.
- `managed_service_encryption_at_rest`: `resource_ids`, `encryption_at_rest: true`, and
  `key_management` (`provider_managed` or `customer_managed`).
- `provider_deletion_outcome`: `store_ids`, `deletion_event_id`, and `outcome`
  (`confirmed_deleted` or `policy_bounded`). `policy_bounded` also requires `residual_until`.
- `backup_encryption_at_rest`: `backup_ids`, `encrypted: true`, and
  `key_separated_from_primary: true`.
- `restore_test_result`: `restore_tested_at`, positive `policy_max_age_days`,
  `restored_backup_id`, `successful: true`, `integrity_verified: true`, and
  `deletion_policy_reapplied: true`. `valid_until` may not exceed the restore test date plus the
  policy maximum age.

Validator reports `Bundle complete` only when every required kind and scoped ID is present and
current. Review artifact contents and correlate deployment targets before assigning any control
status. Overall launch readiness remains owned by `secod-ship-check`.
