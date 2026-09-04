"""Executable expectations for maintained observability-response fixture cases."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


SECOD_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_ROOT = SECOD_ROOT / "skills" / "secod-observability-response" / "scripts"
sys.path.insert(0, str(VALIDATOR_ROOT))

from validate_evidence_bundle import validate_bundle

from fixture_app import (
    AlertRoute,
    AuditSink,
    KeyRegistry,
    SinkUnavailable,
    external_evidence_status,
    recovery_status,
    runbook_status,
    secure_redact,
    security_event,
    unsafe_shallow_redact,
)


class ObservabilityResponseFixtures(unittest.TestCase):
    def test_01_clean_structured_event_and_visible_sink_failure(self) -> None:
        event = security_event("user-1", "access.denied", "invoice-2", "denied")
        self.assertEqual(
            set(event),
            {"actor", "action", "target", "timestamp", "outcome", "correlation_id"},
        )
        sink = AuditSink()
        self.assertTrue(sink.emit(event))
        self.assertEqual(sink.events, [event])
        with self.assertRaises(SinkUnavailable):
            AuditSink(available=False, visible_failure=True).emit(event)

    def test_02_nested_redaction_bypass(self) -> None:
        marker = "fixture-secret-marker"
        payload = {"request": {"authorization_header": marker, "profile": {"password": marker}}}
        self.assertNotIn(marker, json.dumps(secure_redact(payload)))
        self.assertIn(marker, json.dumps(unsafe_shallow_redact(payload)))

    def test_03_revoked_key_replay(self) -> None:
        secure = KeyRegistry(enforce_revocation=True)
        secure.issue("key-1")
        secure.revoke("key-1")
        self.assertFalse(secure.authorize("key-1"))
        self.assertEqual(secure.events[-1]["outcome"], "denied")

        unsafe = KeyRegistry(enforce_revocation=False)
        unsafe.issue("key-1")
        unsafe.revoke("key-1")
        self.assertTrue(unsafe.authorize("key-1"))

    def test_04_alert_definition_without_delivery(self) -> None:
        route = AlertRoute(recipients=["on-call"], delivery_enabled=False)
        self.assertFalse(route.trigger("retry_exhaustion"))
        self.assertEqual(route.deliveries, [])

    def test_05_delivered_alert_capture(self) -> None:
        route = AlertRoute(recipients=["on-call"], delivery_enabled=True)
        self.assertTrue(route.trigger("retry_exhaustion"))
        self.assertEqual(route.deliveries[0]["recipient"], "on-call")

    def test_06_silent_sink_failure(self) -> None:
        sink = AuditSink(available=False, visible_failure=False)
        self.assertFalse(sink.emit(security_event("user-1", "login", "session", "success")))
        self.assertEqual(sink.events, [])

    def test_07_unexercised_runbook(self) -> None:
        self.assertEqual(
            runbook_status(covers_applicable_breaches=True, dated_exercise=True),
            "Passed with evidence",
        )
        self.assertEqual(
            runbook_status(covers_applicable_breaches=True, dated_exercise=False),
            "Not verified",
        )

    def test_08_backup_schedule_without_restore(self) -> None:
        self.assertEqual(
            recovery_status(restore_artifact=True, partial_recovery_observed=True),
            "Passed with evidence",
        )
        self.assertEqual(
            recovery_status(restore_artifact=False, partial_recovery_observed=True),
            "Not verified",
        )

    def test_09_repository_only_external_evidence(self) -> None:
        self.assertEqual(
            external_evidence_status(
                production_sink=False,
                alert_delivery=False,
                runbook_exercise=False,
                restore_drill=False,
            ),
            "Not verified",
        )

    def test_10_evidence_bundle_validator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event_path = root / "event.json"
            sink_path = root / "sink.json"
            event_path.write_text('{"event":"redacted"}', encoding="utf-8")
            sink_path.write_text('{"sink":"retained"}', encoding="utf-8")

            def artifact(name: str, kind: str, path: Path) -> dict[str, object]:
                return {
                    "id": name,
                    "kind": kind,
                    "control_ids": ["SECOD-OBS-01"],
                    "environment": "production",
                    "deployment_id": "deploy-fixture",
                    "source": "fixture export",
                    "captured_at": "2026-08-27T09:30:00+05:30",
                    "path": path.name,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "redacted": True,
                    "authorized": True,
                }

            manifest_path = root / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["SECOD-OBS-01"],
                        "artifacts": [
                            artifact("sink", "production_sink", sink_path),
                            artifact("event", "emitted_security_event", event_path),
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = validate_bundle(manifest_path)
            self.assertTrue(result["valid"])
            self.assertEqual(
                result["controls"]["SECOD-OBS-01"]["intake_status"],
                "Bundle complete",
            )

            incomplete = json.loads(manifest_path.read_text(encoding="utf-8"))
            incomplete["artifacts"] = incomplete["artifacts"][:1]
            manifest_path.write_text(json.dumps(incomplete), encoding="utf-8")
            result = validate_bundle(manifest_path)
            self.assertFalse(result["valid"])
            self.assertEqual(
                result["controls"]["SECOD-OBS-01"]["intake_status"],
                "Not verified",
            )
            self.assertEqual(
                result["controls"]["SECOD-OBS-01"]["missing_artifact_kinds"],
                ["emitted_security_event"],
            )


if __name__ == "__main__":
    unittest.main()
