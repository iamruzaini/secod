from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import implementation_skill_problems, metadata_value


SECTIONS = (
    "Purpose",
    "When to use",
    "Context to inspect",
    "Secure defaults",
    "Implementation workflow",
    "Implementation recipes",
    "Unsafe patterns to avoid",
    "Tests to add",
    "Provider and deployment steps",
    "Official sources",
)


def skill_content(*, extra: str = "", omit: str | None = None) -> str:
    headings = "\n\n".join(
        f"## {section}\n\nImplementation guidance."
        for section in SECTIONS
        if section != omit
    )
    return f'''---
name: secod-example
description: Help coding agents implement an example securely. Use for example integrations.
license: Apache-2.0
metadata:
  secod-category: "provider-feature"
  secod-format: "implementation-v1"
  secod-maturity: "draft"
---

# SECOD example

{headings}

[Read recipe](references/recipe.md)
[Official sources](references/sources.md)
{extra}
'''


SOURCES = """# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| SRC-EXAMPLE-001 | Official guide | Direct implementation page | https://example.com/security | Example | 2026-09-06 | API change | Reviewed | recipe.md: initialization | Current API |
"""


class ImplementationFormatTests(unittest.TestCase):
    def make_skill(self, content: str, sources: str = SOURCES) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        references = root / "references"
        references.mkdir()
        (references / "recipe.md").write_text("# Recipe\n", encoding="utf-8")
        (references / "sources.md").write_text(sources, encoding="utf-8")
        return temporary, root

    def test_valid_implementation_skill(self) -> None:
        temporary, root = self.make_skill(skill_content())
        self.addCleanup(temporary.cleanup)
        self.assertEqual([], implementation_skill_problems("secod-example", root, skill_content()))

    def test_metadata_is_read_only_from_nested_metadata(self) -> None:
        content = skill_content()
        self.assertEqual("implementation-v1", metadata_value(content, "secod-format"))
        self.assertEqual("provider-feature", metadata_value(content, "secod-category"))

    def test_missing_required_section_fails(self) -> None:
        content = skill_content(omit="Tests to add")
        temporary, root = self.make_skill(content)
        self.addCleanup(temporary.cleanup)
        problems = implementation_skill_problems("secod-example", root, content)
        self.assertIn("secod-example implementation-v1 skill lacks section: Tests to add", problems)

    def test_legacy_output_contract_fails(self) -> None:
        content = skill_content(extra="\n## Output schema\n\nPassed with evidence\n")
        temporary, root = self.make_skill(content)
        self.addCleanup(temporary.cleanup)
        problems = implementation_skill_problems("secod-example", root, content)
        self.assertTrue(any("legacy heading: Output schema" in problem for problem in problems))
        self.assertTrue(any("legacy output phrase: Passed with evidence" in problem for problem in problems))

    def test_template_placeholder_and_missing_reference_fail(self) -> None:
        content = skill_content(extra="\nUse <provider feature>.\n[Missing](references/missing.md)\n")
        temporary, root = self.make_skill(content)
        self.addCleanup(temporary.cleanup)
        problems = implementation_skill_problems("secod-example", root, content)
        self.assertTrue(any("unfinished template placeholder" in problem for problem in problems))
        self.assertTrue(any("links missing reference: references/missing.md" in problem for problem in problems))

    def test_reviewed_source_must_map_to_linked_recipe(self) -> None:
        sources = SOURCES.replace("recipe.md: initialization", "unlinked.md: initialization")
        content = skill_content()
        temporary, root = self.make_skill(content, sources)
        self.addCleanup(temporary.cleanup)
        problems = implementation_skill_problems("secod-example", root, content)
        self.assertTrue(any("is not mapped to a linked recipe" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
