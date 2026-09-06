"""Run secure abuse-limit implementation fixtures."""

from __future__ import annotations

import io
import json
import unittest

from test_abuse_limits import AbuseLimitsFixtures


TEST_NAMES = (
    "test_01_layered_shared_rate_limits",
    "test_02_missing_or_instance_local_limiter",
    "test_03_login_and_recovery_enumeration",
    "test_04_idempotency_and_replay",
    "test_05_concurrent_redemption_race",
    "test_06_bounded_retry_and_stable_quota",
    "test_07_export_caps_cancellation_and_queue_shedding",
)


def main() -> int:
    suite = unittest.TestSuite(AbuseLimitsFixtures(name) for name in TEST_NAMES)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "fixture": "secod-abuse-limits",
        "tests_run": result.testsRun,
        "expected_tests": len(TEST_NAMES),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "secure_patterns_exercised": result.wasSuccessful(),
        "production_state_inspected": False,
        "application_certification": "not_produced",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() and result.testsRun == len(TEST_NAMES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
