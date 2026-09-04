"""Run package-delivery fixtures and emit machine-readable local evidence."""

from __future__ import annotations

from datetime import date
import io
import json
import unittest

from fixture_app import CONTROL_IDS, parse_source_register, source_register_ready
from test_packages_delivery import PackagesDeliveryFixtures, SOURCE_REGISTER


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PackagesDeliveryFixtures)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    sources = parse_source_register(SOURCE_REGISTER)
    payload = {
        "fixture": "secod-packages-delivery",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expectations_reproduced": result.wasSuccessful(),
        "controls_exercised": list(CONTROL_IDS),
        "source_records": len(sources),
        "source_register_validated": source_register_ready(sources, date.today()),
        "dashboard_evidence": False,
        "registry_evidence": False,
        "production_evidence": False,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
