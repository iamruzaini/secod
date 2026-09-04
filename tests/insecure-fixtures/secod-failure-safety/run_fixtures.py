"""Run failure-safety fixtures and emit machine-readable local evidence."""

from __future__ import annotations

import io
import json
import unittest

from test_failure_safety import FailureSafetyFixtures


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FailureSafetyFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "fixture": "secod-failure-safety",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expectations_reproduced": result.wasSuccessful(),
        "production_evidence": False,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
