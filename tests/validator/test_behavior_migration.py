from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_behavior_cases import validate_matrix


IMPLEMENTATION_SKILL = """---
name: secod-example
description: Help coding agents implement an example securely. Use for example integrations.
metadata:
  secod-category: provider-feature
  secod-format: implementation-v1
  secod-maturity: draft
---

# Example
"""

IMPLEMENTATION_CASE = """# Behavior matrix

## `secod-example`

- Trigger request: Add the example provider integration.
- Non-trigger request: Edit unrelated typography.
- Dependency routing: Include secod-core and only applicable dependencies.
- Missing-context scenario: SDK version is absent; inspect lockfile before choosing an API.
- Expected implementation: Add server-side initialization and negative authorization tests.
- Expected rejected behavior: Do not expose the privileged key to the browser.
- External configuration handoff: Name exact provider setting and official verification path.
- API support boundary: Use only version-matched APIs from direct official documentation.
"""


class BehaviorMigrationTests(unittest.TestCase):
    def make_root(self, matrix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "skills" / "secod-example").mkdir(parents=True)
        (root / "tests" / "behavior-cases").mkdir(parents=True)
        (root / "catalog.json").write_text(
            json.dumps({"skills": [{"slug": "secod-example"}]}), encoding="utf-8"
        )
        (root / "skills" / "secod-example" / "SKILL.md").write_text(
            IMPLEMENTATION_SKILL, encoding="utf-8"
        )
        (root / "tests" / "behavior-cases" / "skill-behavior-matrix.md").write_text(
            matrix, encoding="utf-8"
        )
        return temporary, root

    def test_implementation_behavior_contract_passes(self) -> None:
        temporary, root = self.make_root(IMPLEMENTATION_CASE)
        self.addCleanup(temporary.cleanup)
        self.assertEqual([], validate_matrix(root))

    def test_legacy_finding_labels_fail_for_implementation_skill(self) -> None:
        legacy_case = IMPLEMENTATION_CASE.replace(
            "- Missing-context scenario: SDK version is absent; inspect lockfile before choosing an API.\n",
            "- Missing-evidence scenario: Return Not verified.\n",
        ).replace(
            "- Expected implementation: Add server-side initialization and negative authorization tests.\n",
            "- Expected finding: Exposed provider key.\n",
        ).replace(
            "- Expected rejected behavior: Do not expose the privileged key to the browser.\n",
            "- Expected non-finding: No exposed key.\n",
        )
        temporary, root = self.make_root(legacy_case)
        self.addCleanup(temporary.cleanup)
        problems = validate_matrix(root)
        self.assertTrue(any("lacks Missing-context scenario" in problem for problem in problems))
        self.assertTrue(any("retains Expected finding" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
