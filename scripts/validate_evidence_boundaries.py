"""Validate SECOD's narrow honesty boundaries."""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CASES = (
    "Inaccessible external setting",
    "Documentation-only test",
    "Unsupported provider API",
    "Application security claim",
)
PROHIBITED_OUTCOMES = (
    "claim setting was inspected",
    "claim test executed",
    "invent API",
    "certify application",
)


def main() -> int:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    skills = catalog.get("skills", [])
    problems: list[str] = []
    if not skills:
        problems.append("Catalog contains no skills")

    boundary_path = ROOT / "tests" / "behavior-cases" / "evidence-boundaries.md"
    boundary_text = boundary_path.read_text(encoding="utf-8")
    for term in (*REQUIRED_CASES, *PROHIBITED_OUTCOMES):
        if term.lower() not in boundary_text.lower():
            problems.append(f"Honesty-boundary cases missing: {term}")

    matrix = (ROOT / "tests" / "behavior-cases" / "skill-behavior-matrix.md").read_text(
        encoding="utf-8"
    )
    for term in (
        "External configuration handoff",
        "API support boundary",
        "documentation-only",
        "certify",
    ):
        if term.lower() not in matrix.lower():
            problems.append(f"Behavior matrix missing implementation boundary: {term}")

    for entry in skills:
        slug = entry["slug"]
        content = (ROOT / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        if "secod-format: \"implementation-v1\"" not in content:
            problems.append(f"{slug}: not migrated to implementation-v1")

    if problems:
        print("SECOD honesty-boundary validation failed:")
        for problem in problems:
            print("- " + problem)
        return 1

    print(f"Validated narrow honesty boundaries for {len(skills)} implementation-v1 skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
