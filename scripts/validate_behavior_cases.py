"""Validate minimum behavior cases for every SECOD skill."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys


REQUIRED_LABELS = (
    "Trigger request",
    "Non-trigger request",
    "Missing-evidence scenario",
    "Expected finding",
    "Expected non-finding",
)


def validate_matrix(root: Path) -> list[str]:
    catalog_path = root / "catalog.json"
    matrix_path = root / "tests" / "behavior-cases" / "skill-behavior-matrix.md"
    problems: list[str] = []

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"Cannot read skill catalog: {error}"]

    expected = {item["slug"] for item in catalog.get("skills", [])}
    if not matrix_path.is_file():
        return ["Behavior matrix is missing: tests/behavior-cases/skill-behavior-matrix.md"]

    content = matrix_path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## `([^`]+)`\s*$", content, re.MULTILINE))
    actual = [match.group(1) for match in headings]
    duplicates = sorted({slug for slug in actual if actual.count(slug) > 1})
    missing = sorted(expected - set(actual))
    unexpected = sorted(set(actual) - expected)
    if duplicates:
        problems.append("Duplicate behavior sections: " + ", ".join(duplicates))
    if missing:
        problems.append("Skills missing behavior sections: " + ", ".join(missing))
    if unexpected:
        problems.append("Unexpected behavior sections: " + ", ".join(unexpected))
    if "not proof" not in content.lower():
        problems.append("Behavior matrix must state that cases are not proof of execution")

    for index, heading in enumerate(headings):
        slug = heading.group(1)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        section = content[heading.end() : end]
        for label in REQUIRED_LABELS:
            match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", section, re.MULTILINE)
            if not match or not match.group(1).strip():
                problems.append(f"{slug} lacks {label}")
        missing_match = re.search(
            r"^- Missing-evidence scenario:\s*(.+)$", section, re.MULTILINE
        )
        if missing_match:
            missing_text = missing_match.group(1).lower()
            if "not verified" not in missing_text:
                problems.append(f"{slug} missing-evidence case must require Not verified")
            if "passed with evidence" in missing_text:
                problems.append(f"{slug} missing-evidence case permits an unsupported pass")
        nonfinding_match = re.search(
            r"^- Expected non-finding:\s*(.+)$", section, re.MULTILINE
        )
        if nonfinding_match and not re.search(
            r"\b(no|none|without)\b", nonfinding_match.group(1), re.IGNORECASE
        ):
            problems.append(f"{slug} expected non-finding is not explicit")

    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    problems = validate_matrix(root)
    if problems:
        print("SECOD behavior-case validation failed:")
        for problem in problems:
            print("- " + problem)
        return 1
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    print(f"Validated behavior cases for {len(catalog['skills'])} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
