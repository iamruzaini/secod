"""Run abuse-limits fixtures and emit machine-readable local evidence."""

from __future__ import annotations

import io
import json
import unittest

from test_abuse_limits import AbuseLimitsFixtures
from test_evidence_validator import AbuseEvidenceValidatorFixtures
from fixture_app import release_handoff


ALL_CONTROLS = tuple(f"PROVISIONAL-ABUSE-{number:02d}" for number in range(1, 9))
EXPECTED_TEST_CONTROLS = {
    "test_abuse_limits.AbuseLimitsFixtures.test_01_layered_shared_rate_limits": {ALL_CONTROLS[0]},
    "test_abuse_limits.AbuseLimitsFixtures.test_02_missing_or_instance_local_limiter": {ALL_CONTROLS[0]},
    "test_abuse_limits.AbuseLimitsFixtures.test_03_login_and_recovery_enumeration": {ALL_CONTROLS[1]},
    "test_abuse_limits.AbuseLimitsFixtures.test_04_idempotency_and_replay": {ALL_CONTROLS[2]},
    "test_abuse_limits.AbuseLimitsFixtures.test_05_concurrent_redemption_race": {ALL_CONTROLS[3]},
    "test_abuse_limits.AbuseLimitsFixtures.test_06_bounded_retry_and_stable_quota": {ALL_CONTROLS[4], ALL_CONTROLS[5]},
    "test_abuse_limits.AbuseLimitsFixtures.test_07_export_caps_cancellation_and_queue_shedding": {ALL_CONTROLS[6], ALL_CONTROLS[7]},
    "test_abuse_limits.AbuseLimitsFixtures.test_08_missing_external_evidence_and_ship_handoff": set(ALL_CONTROLS),
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_09_complete_limiter_bundle": {ALL_CONTROLS[0]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_10_missing_provider_spend_evidence": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_11_stale_evidence_refused": {ALL_CONTROLS[0]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_12_malformed_types_return_structured_refusal": {ALL_CONTROLS[0]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_13_weak_provider_metadata_refused": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_14_unknown_control_returns_structured_refusal": set(),
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_15_early_refusals_keep_readiness_boundary": set(),
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_16_evidence_is_complete_per_deployment": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_17_unhashable_membership_values_return_refusal": {ALL_CONTROLS[0], ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_18_deployment_result_keys_do_not_collide": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_19_future_capture_refused": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_20_complete_bundle_for_every_control_and_deployment": set(ALL_CONTROLS),
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_21_incomplete_bundle_refused_for_every_control": set(ALL_CONTROLS),
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_22_missing_capture_identity_refused": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_23_non_finite_spend_amount_refused": {ALL_CONTROLS[7]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_24_shared_store_probe_requires_two_instances": {ALL_CONTROLS[0]},
    "test_evidence_validator.AbuseEvidenceValidatorFixtures.test_25_over_age_unexpired_evidence_refused": {ALL_CONTROLS[7]},
}


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.started_ids: list[str] = []

    def startTest(self, test: unittest.case.TestCase) -> None:
        self.started_ids.append(test.id())
        super().startTest(test)


def main() -> int:
    suite = unittest.TestSuite(
        (
            unittest.defaultTestLoader.loadTestsFromTestCase(AbuseLimitsFixtures),
            unittest.defaultTestLoader.loadTestsFromTestCase(AbuseEvidenceValidatorFixtures),
        )
    )
    result = unittest.TextTestRunner(
        stream=io.StringIO(), verbosity=0, resultclass=RecordingResult
    ).run(suite)
    expected_ids = set(EXPECTED_TEST_CONTROLS)
    actual_ids = set(result.started_ids)
    missing_test_ids = sorted(expected_ids - actual_ids)
    unexpected_test_ids = sorted(actual_ids - expected_ids)
    skipped_test_ids = sorted(test.id() for test, _ in result.skipped)
    expected_failure_ids = sorted(test.id() for test, _ in result.expectedFailures)
    unexpected_success_ids = sorted(test.id() for test in result.unexpectedSuccesses)
    incomplete_ids = {
        *(test.id() for test, _ in result.failures),
        *(test.id() for test, _ in result.errors),
        *skipped_test_ids,
        *expected_failure_ids,
        *unexpected_success_ids,
    }
    successful_expected_ids = (actual_ids & expected_ids) - incomplete_ids
    controls_exercised = sorted(
        set().union(*(EXPECTED_TEST_CONTROLS[test_id] for test_id in successful_expected_ids))
    )
    coverage_complete = not any(
        (
            missing_test_ids,
            unexpected_test_ids,
            skipped_test_ids,
            expected_failure_ids,
            unexpected_success_ids,
        )
    )
    expectations_reproduced = result.wasSuccessful() and coverage_complete
    blockers = ["local fixtures do not prove reviewed application or deployed behavior"]
    if not result.wasSuccessful():
        blockers.append("local fixture execution failed")
    if not coverage_complete:
        blockers.append("fixture coverage incomplete or non-normal test outcome detected")
    fixture_execution = {
        "execution_status": "passed" if expectations_reproduced else "failed",
        "tests_run": result.testsRun,
        "expected_tests": len(EXPECTED_TEST_CONTROLS),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "unexpected_successes": len(result.unexpectedSuccesses),
        "failed_tests": [str(test) for test, _ in result.failures],
        "errored_tests": [str(test) for test, _ in result.errors],
        "missing_test_ids": missing_test_ids,
        "unexpected_test_ids": unexpected_test_ids,
        "skipped_test_ids": skipped_test_ids,
        "expected_failure_ids": expected_failure_ids,
        "unexpected_success_ids": unexpected_success_ids,
    }
    handoff = release_handoff(
        list(ALL_CONTROLS),
        {control_id: "Not verified" for control_id in ALL_CONTROLS},
        blockers,
        [
            "topology-matched deployed control configuration and negative-test captures",
            "provider spend ceiling or billing-alert evidence",
        ],
        fixture_execution,
    )
    payload = {
        "fixture": "secod-abuse-limits",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "failed_tests": [str(test) for test, _ in result.failures],
        "errored_tests": [str(test) for test, _ in result.errors],
        "skipped": len(result.skipped),
        "expectations_reproduced": expectations_reproduced,
        "coverage_complete": coverage_complete,
        "expected_tests": len(EXPECTED_TEST_CONTROLS),
        "controls_exercised": controls_exercised,
        "provider_evidence": False,
        "production_evidence": False,
        "readiness_verdict": "not_issued",
        "verdict_owner": "secod-ship-check",
        "release_handoff": handoff,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if expectations_reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
