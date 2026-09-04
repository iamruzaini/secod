# External evidence contract

Use this contract when repository evidence cannot establish deployed sink behavior, delivered
alerts, exercised containment, evidence-store protection, or successful restore behavior. Blank
templates, unexecuted plans, screenshots without resource identity, and unchecked manifests are
not evidence.

## Bundle layout

Store a JSON manifest beside the redacted artifacts it describes. Use relative paths that remain
inside the bundle directory. Each artifact entry requires:

- `id`: unique stable name within the bundle;
- `kind`: one artifact class listed below;
- `control_ids`: applicable approved `SECOD-OBS-*` IDs;
- `environment`, `deployment_id`, `source`, and timezone-qualified `captured_at`;
- `path` and lowercase SHA-256 `sha256` for a non-empty artifact file;
- `redacted: true` and `authorized: true`.

Manifest root requires `schema_version: 1`, `applicable_controls`, and `artifacts`. The validator
rejects unknown controls, duplicate IDs, path traversal, missing files, empty files, bad hashes,
timestamps without timezones, and missing required artifact classes.

```json
{
  "schema_version": 1,
  "applicable_controls": ["SECOD-OBS-01", "SECOD-OBS-04"],
  "artifacts": [
    {
      "id": "prod-sink-2026-08-27",
      "kind": "production_sink",
      "control_ids": ["SECOD-OBS-01"],
      "environment": "production",
      "deployment_id": "deploy-123",
      "source": "provider dashboard export",
      "captured_at": "2026-08-27T09:30:00+05:30",
      "path": "prod-sink.json",
      "sha256": "<64 lowercase hexadecimal characters>",
      "redacted": true,
      "authorized": true
    }
  ]
}
```

## Required artifact classes

- `SECOD-OBS-01`: `production_sink`, `emitted_security_event`
- `SECOD-OBS-02`: `redaction_marker_test`, `retention_access_decision`
- `SECOD-OBS-03`: `revoked_key_replay`, `key_lifecycle_events`
- `SECOD-OBS-04`: `alert_definition`, `alert_delivery`
- `SECOD-OBS-05`: `runbook`, `runbook_exercise`
- `SECOD-OBS-06`: `evidence_store_controls`, `exercised_export`
- `SECOD-OBS-07`: `restore_drill`, `partial_operation_recovery`

`production_sink` must identify the production environment. Other artifacts must identify the
environment actually exercised. One artifact may support multiple controls only when its content
contains evidence for each listed control.

## Intake and review

Run from `secod/`:

```text
python skills/secod-observability-response/scripts/validate_evidence_bundle.py path/to/manifest.json
```

Exit `0` means the bundle is structurally complete for its declared applicable controls. It does
not authenticate the source, prove the captured behavior, or grant `Passed with evidence`.
Inspect each artifact, correlate resource and deployment identities with the reviewed system,
confirm capture currency and scope, and record contradictions. Missing, stale, inaccessible,
unauthorized, unredacted, or contradictory evidence remains `Not verified`.

Do not commit secrets, raw production logs, customer data, or unredacted screenshots. Keep
sensitive bundles in an approved evidence store and review a redacted export or controlled link.
Route launch readiness exclusively to `secod-ship-check`.
