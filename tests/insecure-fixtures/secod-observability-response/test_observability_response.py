"""Executable expectations for maintained observability-response fixture cases."""

from __future__ import annotations

import json
import unittest

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
            "secure pattern confirmed",
        )
        self.assertEqual(
            runbook_status(covers_applicable_breaches=True, dated_exercise=False),
            "external state not inspected",
        )

    def test_08_backup_schedule_without_restore(self) -> None:
        self.assertEqual(
            recovery_status(restore_artifact=True, partial_recovery_observed=True),
            "secure pattern confirmed",
        )
        self.assertEqual(
            recovery_status(restore_artifact=False, partial_recovery_observed=True),
            "external state not inspected",
        )

    def test_09_repository_only_external_evidence(self) -> None:
        self.assertEqual(
            external_evidence_status(
                production_sink=False,
                alert_delivery=False,
                runbook_exercise=False,
                restore_drill=False,
            ),
            "external state not inspected",
        )

if __name__ == "__main__":
    unittest.main()
