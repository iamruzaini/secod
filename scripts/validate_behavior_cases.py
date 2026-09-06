"""Validate minimum behavior cases for every SECOD skill."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys


LEGACY_LABELS = (
    "Trigger request",
    "Non-trigger request",
    "Missing-evidence scenario",
    "Expected finding",
    "Expected non-finding",
)
IMPLEMENTATION_LABELS = (
    "Trigger request",
    "Non-trigger request",
    "Dependency routing",
    "Missing-context scenario",
    "Expected implementation",
    "Expected rejected behavior",
    "External configuration handoff",
    "API support boundary",
)


def skill_format(root: Path, slug: str) -> str | None:
    content = (root / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(?P<body>.*?)\n---(?:\n|$)", content, re.DOTALL)
    if frontmatter is None:
        return None
    metadata = re.search(
        r"^metadata:\s*\n(?P<body>(?:^[ \t]+.*(?:\n|$))*)",
        frontmatter.group("body"),
        re.MULTILINE,
    )
    if metadata is None:
        return None
    match = re.search(
        r"^[ \t]+secod-format:\s*['\"]?([^'\"\n]+)['\"]?\s*$",
        metadata.group("body"),
        re.MULTILINE,
    )
    return match.group(1).strip() if match else None


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
    formats = {slug: skill_format(root, slug) for slug in expected}
    legacy_exists = any(value != "implementation-v1" for value in formats.values())
    if legacy_exists and "not proof" not in content.lower():
        problems.append("Behavior matrix must state that cases are not proof of execution")

    for index, heading in enumerate(headings):
        slug = heading.group(1)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        section = content[heading.end() : end]
        implementation = formats.get(slug) == "implementation-v1"
        required_labels = IMPLEMENTATION_LABELS if implementation else LEGACY_LABELS
        for label in required_labels:
            match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", section, re.MULTILINE)
            if not match or not match.group(1).strip():
                problems.append(f"{slug} lacks {label}")
        if implementation:
            for legacy_label in ("Missing-evidence scenario", "Expected finding", "Expected non-finding"):
                if re.search(rf"^- {re.escape(legacy_label)}:", section, re.MULTILINE):
                    problems.append(f"{slug} implementation behavior retains {legacy_label}")
            rejected_match = re.search(
                r"^- Expected rejected behavior:\s*(.+)$", section, re.MULTILINE
            )
            if rejected_match and not re.search(
                r"\b(no|not|never|reject|deny|refuse|without)\b",
                rejected_match.group(1),
                re.IGNORECASE,
            ):
                problems.append(f"{slug} expected rejected behavior is not explicit")
            continue
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
