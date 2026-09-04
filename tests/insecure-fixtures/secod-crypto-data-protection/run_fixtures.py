"""Run crypto-data-protection evidence fixtures and emit machine-readable local results."""

from __future__ import annotations

import io
import json
import unittest

from test_evidence_validator import CryptoEvidenceFixtures


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CryptoEvidenceFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "fixture": "secod-crypto-data-protection",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "expectations_reproduced": result.wasSuccessful(),
        "production_evidence": False,
        "launch_readiness_owner": "secod-ship-check",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
