"""Validate SECOD's fail-closed evidence and verdict boundaries."""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BOUNDARY_TERMS = (
    "Inaccessible dashboard",
    "Documentation-only plan",
    "Reachable source URL",
    "Missing control evidence",
    "Security verdict boundary",
    "Not verified",
)


def main() -> int:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    skills = catalog.get("skills", [])
    problems: list[str] = []
    if len(skills) != 57:
        problems.append(f"Expected 57 catalog skills, found {len(skills)}")

    for entry in skills:
        slug = entry.get("slug", "<missing-slug>")
        path = ROOT / "skills" / slug / "SKILL.md"
        if not path.is_file():
            problems.append(f"{slug}: SKILL.md is missing")
            continue
        content = path.read_text(encoding="utf-8")
        if "Not verified" not in content:
            problems.append(f"{slug}: missing Not verified boundary")
        if "launch readiness" not in content.lower():
            problems.append(f"{slug}: missing launch-readiness boundary")
        if "inaccessible" not in content.lower():
            problems.append(f"{slug}: missing inaccessible-evidence boundary")

    boundary_path = ROOT / "tests" / "behavior-cases" / "evidence-boundaries.md"
    boundary_text = boundary_path.read_text(encoding="utf-8")
    for term in REQUIRED_BOUNDARY_TERMS:
        if term.lower() not in boundary_text.lower():
            problems.append(f"Evidence-boundary cases missing: {term}")

    matrix = (ROOT / "tests" / "behavior-cases" / "skill-behavior-matrix.md").read_text(
        encoding="utf-8"
    )
    if "not proof" not in matrix.lower() or "Not verified" not in matrix:
        problems.append("Skill behavior matrix does not preserve evidence boundaries")

    critical_runner = (
        ROOT / "tests" / "insecure-fixtures" / "secod-critical-behaviors" / "run_fixtures.py"
    ).read_text(encoding="utf-8")
    required_runner_terms = (
        '"production_evidence": False',
        '"readiness_verdict": "not_issued"',
    )
    for term in required_runner_terms:
        if term not in critical_runner:
            problems.append(f"Critical fixture runner missing boundary: {term}")

    if problems:
        print("SECOD evidence-boundary validation failed:")
        for problem in problems:
            print("- " + problem)
        return 1

    print("Validated evidence boundaries for 57 skills and critical fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
