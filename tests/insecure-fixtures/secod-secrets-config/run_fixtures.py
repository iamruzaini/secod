"""Run secrets-config fixtures and emit machine-readable local evidence."""

from __future__ import annotations

import io
import json
import unittest

from test_secrets_config import SecretsConfigFixtures


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SecretsConfigFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "artifact_type": "executable_fixture",
        "fixture": "secod-secrets-config",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expectations_reproduced": result.wasSuccessful(),
        "production_state_inspected": False,
        "release_handoff": {
            "completion_owner": "secod-ship-check",
            "application_verdict": "not_produced",
        },
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
