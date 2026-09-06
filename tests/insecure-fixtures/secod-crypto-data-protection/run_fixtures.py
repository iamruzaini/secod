"""Run secure cryptography implementation fixtures."""

from __future__ import annotations

import io
import json
import unittest

from test_secure_patterns import CryptoDataProtectionFixtures


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CryptoDataProtectionFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    payload = {
        "fixture": "secod-crypto-data-protection",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "secure_patterns_exercised": result.wasSuccessful(),
        "production_state_inspected": False,
        "application_certification": "not_produced",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
