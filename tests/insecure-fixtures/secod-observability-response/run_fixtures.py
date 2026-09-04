"""Run observability-response fixtures and emit machine-readable local evidence."""

from __future__ import annotations

import io
import json
import unittest

from test_observability_response import ObservabilityResponseFixtures


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ObservabilityResponseFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "fixture": "secod-observability-response",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expectations_reproduced": result.wasSuccessful(),
        "production_evidence": False,
        "launch_readiness_owner": "secod-ship-check",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
