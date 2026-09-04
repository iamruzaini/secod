"""Executable expectations for package-delivery fixtures."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path
import unittest

from fixture_app import (
    CONTROL_IDS,
    EXTERNAL_EVIDENCE_CONTROLS,
    ISSUE_OUTCOMES,
    SourceRecord,
    action_ref_is_full_sha,
    artifact_ref_is_immutable,
    complete_evidence,
    evaluate,
    parse_source_register,
    privileged_pr_flow_is_safe,
    source_register_ready,
    verification_fails_closed,
)


SECOD_ROOT = Path(__file__).resolve().parents[3]
SOURCE_REGISTER = SECOD_ROOT / "skills" / "secod-packages-delivery" / "references" / "sources.md"


class PackagesDeliveryFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.reviewed_on = date.today()
        self.sources = parse_source_register(SOURCE_REGISTER)

    def test_01_source_register_is_reviewed_current_and_complete(self) -> None:
        self.assertEqual(len(self.sources), 8)
        self.assertTrue(source_register_ready(self.sources, self.reviewed_on))

    def test_02_complete_synthetic_evidence_passes_all_controls(self) -> None:
        outcomes = evaluate(complete_evidence(self.sources, self.reviewed_on))
        self.assertEqual(set(outcomes), set(CONTROL_IDS))
        self.assertEqual(set(outcomes.values()), {"Passed with evidence"})

    def test_03_each_insecure_case_has_specific_status(self) -> None:
        baseline = complete_evidence(self.sources, self.reviewed_on)
        for issue, (control_id, expected_status) in ISSUE_OUTCOMES.items():
            with self.subTest(issue=issue):
                outcomes = evaluate(replace(baseline, issues=frozenset({issue})))
                self.assertEqual(outcomes[control_id], expected_status)

    def test_04_missing_dashboard_and_registry_evidence_never_passes(self) -> None:
        evidence = replace(
            complete_evidence(self.sources, self.reviewed_on),
            external_controls=frozenset(),
        )
        outcomes = evaluate(evidence)
        for control_id in CONTROL_IDS:
            expected = (
                "Not verified"
                if control_id in EXTERNAL_EVIDENCE_CONTROLS
                else "Passed with evidence"
            )
            self.assertEqual(outcomes[control_id], expected)

    def test_05_missing_repository_or_negative_test_evidence_never_passes(self) -> None:
        baseline = complete_evidence(self.sources, self.reviewed_on)
        no_repository_evidence = replace(
            baseline,
            repository_controls=frozenset(set(CONTROL_IDS) - {"PROVISIONAL-packages-1"}),
        )
        failed_negative_test = replace(
            baseline,
            negative_test_controls=frozenset(set(CONTROL_IDS) - {"PROVISIONAL-packages-9"}),
        )
        self.assertEqual(
            evaluate(no_repository_evidence)["PROVISIONAL-packages-1"], "Not verified"
        )
        self.assertEqual(
            evaluate(failed_negative_test)["PROVISIONAL-packages-9"], "Not verified"
        )

    def test_06_pending_or_expired_source_blocks_passes(self) -> None:
        baseline = complete_evidence(self.sources, self.reviewed_on)
        pending = replace(self.sources[0], status="Pending review")
        expired = replace(self.sources[0], expires=self.reviewed_on - timedelta(days=1))
        for source in (pending, expired):
            with self.subTest(source=source):
                records = (source,) + self.sources[1:]
                outcomes = evaluate(replace(baseline, sources=records))
                self.assertEqual(set(outcomes.values()), {"Not verified"})

    def test_07_static_unsafe_patterns_are_reproduced(self) -> None:
        full_sha = "actions/checkout@" + "a" * 40
        digest = "registry.example/app@sha256:" + "b" * 64
        self.assertTrue(action_ref_is_full_sha(full_sha))
        self.assertFalse(action_ref_is_full_sha("actions/checkout@v4"))
        self.assertTrue(artifact_ref_is_immutable(digest))
        self.assertFalse(artifact_ref_is_immutable("registry.example/app:latest"))
        self.assertFalse(
            privileged_pr_flow_is_safe(
                trigger="pull_request_target",
                checkout_pr_head=True,
                privileged_credentials=True,
            )
        )
        self.assertTrue(
            privileged_pr_flow_is_safe(
                trigger="pull_request",
                checkout_pr_head=True,
                privileged_credentials=False,
            )
        )

    def test_08_attestation_verification_must_fail_closed(self) -> None:
        self.assertTrue(verification_fails_closed("gh attestation verify artifact -R org/repo"))
        self.assertFalse(
            verification_fails_closed("gh attestation verify artifact -R org/repo || true")
        )
        self.assertFalse(
            verification_fails_closed("continue-on-error: true; gh attestation verify artifact")
        )


if __name__ == "__main__":
    unittest.main()
