"""Run cross-skill critical behavior fixtures and emit local evidence."""

from __future__ import annotations

import io
import json
import unittest

from test_critical_behaviors import CriticalBehaviorFixtures


EXPECTED_TESTS = {
    f"test_critical_behaviors.CriticalBehaviorFixtures.test_{number:02d}_{name}"
    for number, name in (
        (1, "broken_tenant_authorization"),
        (2, "missing_server_side_authorization"),
        (3, "exposed_secret"),
        (4, "weak_webhook_verification"),
        (5, "payment_replay"),
        (6, "unrestricted_file_upload"),
        (7, "public_storage_object"),
        (8, "command_injection"),
        (9, "ssrf"),
        (10, "missing_rate_limits"),
        (11, "retry_storm"),
        (12, "sensitive_log_entry"),
        (13, "unsafe_ai_tool_execution"),
        (14, "cross_tenant_vector_search"),
    )
}


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.started_ids: list[str] = []

    def startTest(self, test: unittest.case.TestCase) -> None:
        self.started_ids.append(test.id())
        super().startTest(test)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CriticalBehaviorFixtures)
    result = unittest.TextTestRunner(
        stream=io.StringIO(), verbosity=0, resultclass=RecordingResult
    ).run(suite)
    actual = set(result.started_ids)
    incomplete = {
        *(test.id() for test, _ in result.failures),
        *(test.id() for test, _ in result.errors),
        *(test.id() for test, _ in result.skipped),
        *(test.id() for test, _ in result.expectedFailures),
        *(test.id() for test in result.unexpectedSuccesses),
    }
    missing = sorted(EXPECTED_TESTS - actual)
    unexpected = sorted(actual - EXPECTED_TESTS)
    complete = not missing and not unexpected and not incomplete
    reproduced = result.wasSuccessful() and complete
    payload = {
        "fixture": "secod-critical-behaviors",
        "tests_run": result.testsRun,
        "expected_tests": len(EXPECTED_TESTS),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "unexpected_successes": len(result.unexpectedSuccesses),
        "missing_test_ids": missing,
        "unexpected_test_ids": unexpected,
        "expectations_reproduced": reproduced,
        "production_evidence": False,
        "readiness_verdict": "not_issued",
        "blockers": [
            "local fixtures reproduce guarded and insecure behavior only",
            "fixture execution does not prove reviewed application or production behavior",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
