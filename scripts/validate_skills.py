"""Read-only structural validation for the SECOD skill catalog."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys


IMPLEMENTATION_FORMAT = "implementation-v1"
IMPLEMENTATION_CATEGORIES = {
    "router",
    "generalized",
    "framework",
    "provider-family",
    "provider-feature",
    "mobile",
    "task-completion",
}
IMPLEMENTATION_MATURITY = {"draft", "provisional", "stable"}
IMPLEMENTATION_SECTIONS = (
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
LEGACY_OUTPUT_HEADINGS = {
    "Control requirements",
    "Evidence to inspect",
    "Evidence and status rules",
    "Output schema",
    "Required output",
    "Review workflow",
    "Verification and safe failure",
}
LEGACY_OUTPUT_PHRASES = (
    "generate the Security Plan",
    "Passed with evidence",
    "Fix before launch",
    "Recommended hardening",
    "final launch-readiness verdict",
)
TEMPLATE_PLACEHOLDER = re.compile(
    r"<(?:skill-name|secod-[^>\n]*|human-readable[^>\n]*|security outcome|"
    r"concrete[^>\n]*|specific[^>\n]*|feature[^>\n]*|provider[^>\n]*|"
    r"framework[^>\n]*|runtime[^>\n]*|recipe[^>\n]*|other-skill|boundary|"
    r"default[^>\n]*|unsafe[^>\n]*|safe alternative|language)[^>\n]*>",
    re.IGNORECASE,
)


def frontmatter(content: str) -> str | None:
    match = re.match(r"^---\n(?P<body>.*?)\n---(?:\n|$)", content, re.DOTALL)
    return match.group("body") if match else None


def frontmatter_value(content: str, key: str) -> str | None:
    body = frontmatter(content)
    if body is None:
        return None
    match = re.search(r"^" + re.escape(key) + r":\s*(.+)$", body, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else None


def metadata_value(content: str, key: str) -> str | None:
    body = frontmatter(content)
    if body is None:
        return None
    metadata = re.search(r"^metadata:\s*\n(?P<body>(?:^[ \t]+.*(?:\n|$))*)", body, re.MULTILINE)
    if metadata is None:
        return None
    match = re.search(
        r"^[ \t]+" + re.escape(key) + r":\s*(.+)$",
        metadata.group("body"),
        re.MULTILINE,
    )
    return match.group(1).strip().strip('"').strip("'") if match else None


def markdown_reference_targets(content: str) -> set[str]:
    return {
        match.group(1).replace("\\", "/")
        for match in re.finditer(r"\]\((references/[^)#?]+)(?:#[^)]*)?\)", content)
    }


def implementation_source_register_problems(
    skill: str, content: str, recipe_names: set[str]
) -> list[str]:
    problems: list[str] = []
    lowered = content.lower()
    if "<official" in lowered or "src-<" in lowered or "yyyy-mm-dd" in lowered:
        problems.append(skill + " implementation source register contains template placeholders")

    table_lines = [line.strip() for line in content.splitlines() if line.strip().startswith("|")]
    header_index = next(
        (
            index
            for index, line in enumerate(table_lines)
            if "source id" in line.lower() and "direct official url" in line.lower()
        ),
        None,
    )
    if header_index is None:
        return problems + [skill + " implementation source register lacks required source table"]

    headers = [cell.strip().lower() for cell in table_lines[header_index].strip("|").split("|")]
    required_headers = {
        "source id",
        "title",
        "source type",
        "direct official url",
        "owner",
        "reviewed date",
        "refresh trigger",
        "status",
        "recipes or decisions supported",
    }
    missing_headers = sorted(required_headers - set(headers))
    if missing_headers:
        problems.append(
            skill + " implementation source register lacks columns: " + ", ".join(missing_headers)
        )
        return problems

    rows: list[dict[str, str]] = []
    for line in table_lines[header_index + 1 :]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))

    if not rows:
        return problems + [skill + " implementation source register has no source rows"]

    reviewed = 0
    recognized_statuses = {"Reviewed", "Pending review", "Unavailable"}
    for row in rows:
        source_id = row.get("source id", "<unknown>")
        status = row.get("status", "")
        if status not in recognized_statuses:
            problems.append(skill + " source " + source_id + " has unsupported status: " + status)
        url = row.get("direct official url", "")
        if not re.fullmatch(r"https://[^\s|]+", url):
            problems.append(skill + " source " + source_id + " lacks a direct HTTPS URL")
        if status != "Reviewed":
            continue
        reviewed += 1
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("reviewed date", "")):
            problems.append(skill + " source " + source_id + " lacks an exact reviewed date")
        mapping = row.get("recipes or decisions supported", "")
        if not any(recipe in mapping for recipe in recipe_names):
            problems.append(skill + " source " + source_id + " is not mapped to a linked recipe")

    if reviewed == 0:
        problems.append(skill + " implementation source register has no Reviewed source")
    return problems


def implementation_skill_problems(skill: str, skill_root: Path, content: str) -> list[str]:
    problems: list[str] = []
    category = metadata_value(content, "secod-category")
    maturity = metadata_value(content, "secod-maturity")
    if category not in IMPLEMENTATION_CATEGORIES:
        problems.append(skill + " has invalid or missing metadata.secod-category")
    if maturity not in IMPLEMENTATION_MATURITY:
        problems.append(skill + " has invalid or missing metadata.secod-maturity")

    headings = set(re.findall(r"^##\s+(.+?)\s*$", content, re.MULTILINE))
    for section in IMPLEMENTATION_SECTIONS:
        if section not in headings:
            problems.append(skill + " implementation-v1 skill lacks section: " + section)
    for heading in sorted(LEGACY_OUTPUT_HEADINGS & headings):
        problems.append(skill + " implementation-v1 skill retains legacy heading: " + heading)
    for phrase in LEGACY_OUTPUT_PHRASES:
        if phrase.lower() in content.lower():
            problems.append(skill + " implementation-v1 skill retains legacy output phrase: " + phrase)

    if "[TODO:" in content or TEMPLATE_PLACEHOLDER.search(content):
        problems.append(skill + " implementation-v1 skill contains an unfinished template placeholder")

    reference_targets = markdown_reference_targets(content)
    for target in sorted(reference_targets):
        if not (skill_root / target).is_file():
            problems.append(skill + " links missing reference: " + target)

    recipe_targets = {
        target for target in reference_targets if target.lower() != "references/sources.md"
    }
    if not recipe_targets:
        problems.append(skill + " implementation-v1 skill links no implementation recipe")

    source_file = skill_root / "references" / "sources.md"
    if source_file.is_file():
        recipe_names = {Path(target).name for target in recipe_targets}
        problems.extend(
            implementation_source_register_problems(
                skill, source_file.read_text(encoding="utf-8"), recipe_names
            )
        )
    return problems


def source_register_problems(skill: str, content: str) -> list[str]:
    """Validate release-visible evidence registers without claiming URL review."""
    problems: list[str] = []
    lowered = content.lower()
    if "add the control-specific primary sources" in lowered:
        problems.append(skill + " source register still contains placeholder evidence")
    if not re.search(r"https://[^\s|)]+", content):
        problems.append(skill + " source register has no HTTPS source URL")

    required_headers = {
        "source identifier": r"\b(source\s+id|id)\b",
        "title": r"\btitle\b|direct primary source",
        "direct URL": r"direct[^|]*(url|source)",
        "owner": r"\bowner\b",
        "reviewed date": r"\breview(ed| date)\b",
        "refresh trigger": r"\b(refresh|expiry)\b",
        "status": r"\bstatus\b",
        "control mapping": r"\bcontrols?(\s+ids?)?\b|applicable control ids",
        "assumptions": r"\bassumptions?\b",
    }
    header_text = "\n".join(
        line for line in content.splitlines() if line.startswith("|") and "---" not in line
    )
    for label, pattern in required_headers.items():
        # Older reviewed registers may keep owner/review cadence in prose above a richer table.
        search_text = content if label in {"owner", "reviewed date", "refresh trigger"} else header_text
        if not re.search(pattern, search_text, re.IGNORECASE):
            problems.append(skill + " source register lacks " + label)

    if not re.search(r"\b(Reviewed|Pending review|Not verified)\b", content):
        problems.append(skill + " source register lacks a recognized status")
    if not re.search(r"\b\d{4}-\d{2}-\d{2}\b", content):
        problems.append(skill + " source register lacks a review date")
    if "| Reviewed |" in content and not all(
        re.search(pattern, content, re.IGNORECASE)
        for pattern in (r"\b\d{4}-\d{2}-\d{2}\b", r"\bowner\b", r"\bcontrols?\b")
    ):
        problems.append(skill + " has Reviewed evidence without date, owner, and control mapping")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skills_root = root / "skills"
    catalog_file = root / "catalog.json"
    runtime_catalog_file = skills_root / "secod-core" / "references" / "catalog.json"
    problems: list[str] = []

    if not runtime_catalog_file.is_file():
        problems.append("secod-core runtime catalog is missing")
    else:
        try:
            json.loads(runtime_catalog_file.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            problems.append("secod-core runtime catalog is invalid JSON: " + str(error))
        # Git checkouts may use LF or CRLF; compare the generated JSON content
        # independently of platform line endings.
        normalized_runtime = runtime_catalog_file.read_bytes().replace(b"\r\n", b"\n")
        normalized_catalog = catalog_file.read_bytes().replace(b"\r\n", b"\n")
        if normalized_runtime != normalized_catalog:
            problems.append("secod-core runtime catalog differs from catalog.json")

    catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    expected_skills = {item["slug"] for item in catalog["skills"]}
    catalog_skills = {item["slug"]: item for item in catalog["skills"]}
    actual_skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    seen_control_ids: set[str] = set()
    implementation_count = 0

    if actual_skills != expected_skills:
        missing = sorted(expected_skills - actual_skills)
        unexpected = sorted(actual_skills - expected_skills)
        if missing:
            problems.append("Missing skills: " + ", ".join(missing))
        if unexpected:
            problems.append("Unexpected skills: " + ", ".join(unexpected))

    for skill in sorted(expected_skills):
        skill_file = skills_root / skill / "SKILL.md"
        metadata_file = skills_root / skill / "agents" / "openai.yaml"

        if not skill_file.is_file():
            problems.append(skill + " has no SKILL.md")
            continue
        if not metadata_file.is_file():
            problems.append(skill + " has no agents/openai.yaml")
        else:
            metadata = metadata_file.read_text(encoding="utf-8")
            for key in ("display_name", "short_description", "default_prompt"):
                if not re.search(r"^\s*" + key + r':\s*".+"\s*$', metadata, re.MULTILINE):
                    problems.append(skill + " agents/openai.yaml needs " + key)
            if "$" + skill not in metadata:
                problems.append(skill + " default prompt does not name the skill")

        content = skill_file.read_text(encoding="utf-8")
        skill_format = metadata_value(content, "secod-format")
        is_implementation = skill_format == IMPLEMENTATION_FORMAT
        if skill_format and not is_implementation:
            problems.append(skill + " has unsupported metadata.secod-format: " + skill_format)
        if is_implementation:
            implementation_count += 1
            problems.extend(implementation_skill_problems(skill, skills_root / skill, content))

        approved_controls = catalog_skills[skill].get("controls", [])
        for control in approved_controls:
            control_id = control.get("id", "")
            if not re.fullmatch(r"SECOD-[A-Z0-9]+-[0-9]{2}", control_id):
                problems.append(skill + " has malformed approved control ID: " + control_id)
            if control_id in seen_control_ids:
                problems.append("Duplicate approved control ID: " + control_id)
            seen_control_ids.add(control_id)
            if control.get("status") != "approved" or not control.get("approvedOn"):
                problems.append(skill + " control lacks approval metadata: " + control_id)
            if not is_implementation and f"### `{control_id}`" not in content:
                problems.append(skill + " does not define catalog control " + control_id)
        if not is_implementation and approved_controls and re.search(r"PROVISIONAL-[A-Z0-9]+-", content):
            problems.append(skill + " retains provisional IDs after catalog approval")
        if "[TODO:" in content:
            problems.append(skill + " still contains a TODO template")
        if not content.startswith("---\n"):
            problems.append(skill + " has no YAML frontmatter")
            continue
        if frontmatter_value(content, "name") != skill:
            problems.append(skill + " frontmatter name does not match its folder")
        description = frontmatter_value(content, "description")
        if not description or description.startswith("[TODO"):
            problems.append(skill + " needs an informative description")
        if len(content.splitlines()) > 500:
            problems.append(skill + " exceeds the 500-line SKILL.md limit")
        source_file = skills_root / skill / "references" / "sources.md"
        if not source_file.is_file():
            problems.append(skill + " has no references/sources.md")
        elif not is_implementation and not re.search(
            r"^\s*internal:\s*true\s*$", content, re.MULTILINE
        ):
            problems.extend(source_register_problems(skill, source_file.read_text(encoding="utf-8")))
        if not (root / "tests" / "trigger-cases" / (skill + ".md")).is_file():
            problems.append(skill + " has no trigger case")
        if not (root / "tests" / "insecure-fixtures" / skill / "README.md").is_file():
            problems.append(skill + " has no insecure fixture plan")
        if not (root / "tests" / "expected-results" / (skill + ".md")).is_file():
            problems.append(skill + " has no expected result")

    ship_check = (skills_root / "secod-ship-check" / "SKILL.md").read_text(encoding="utf-8")
    for required_term in (
        "files changed during the current task",
        "selected SECOD skill instructions",
        "tests added or executed",
        "accidentally introduced secrets",
        "external provider actions",
        "Ignore unrelated repository conditions",
    ):
        if required_term.lower() not in ship_check.lower():
            problems.append("secod-ship-check missing scoped completion rule: " + required_term)
    for prohibited_term in (
        "final launch-readiness verdict",
        "Passed with evidence",
        "Do not ship",
        "generate the Security Plan",
    ):
        if prohibited_term.lower() in ship_check.lower():
            problems.append("secod-ship-check retains launch-owner behavior: " + prohibited_term)

    failure_fixture = root / "tests" / "insecure-fixtures" / "secod-failure-safety"
    for name in ("fixture_app.py", "test_failure_safety.py", "run_fixtures.py"):
        if not (failure_fixture / name).is_file():
            problems.append("secod-failure-safety executable fixture missing " + name)

    payment_fixture = root / "tests" / "insecure-fixtures" / "secod-payments-billing"
    for name in ("fixture_app.py", "test_payments_billing.py", "run_fixtures.py"):
        if not (payment_fixture / name).is_file():
            problems.append("secod-payments-billing executable fixture missing " + name)

    observability_fixture = root / "tests" / "insecure-fixtures" / "secod-observability-response"
    for name in ("fixture_app.py", "test_observability_response.py", "run_fixtures.py"):
        if not (observability_fixture / name).is_file():
            problems.append("secod-observability-response executable fixture missing " + name)

    packages_fixture = root / "tests" / "insecure-fixtures" / "secod-packages-delivery"
    for name in ("fixture_app.py", "test_packages_delivery.py", "run_fixtures.py"):
        if not (packages_fixture / name).is_file():
            problems.append("secod-packages-delivery executable fixture missing " + name)

    secrets_fixture = root / "tests" / "insecure-fixtures" / "secod-secrets-config"
    for name in ("fixture_app.py", "test_secrets_config.py", "run_fixtures.py"):
        if not (secrets_fixture / name).is_file():
            problems.append("secod-secrets-config executable fixture missing " + name)

    abuse_fixture = root / "tests" / "insecure-fixtures" / "secod-abuse-limits"
    for name in (
        "fixture_app.py",
        "test_abuse_limits.py",
        "run_fixtures.py",
    ):
        if not (abuse_fixture / name).is_file():
            problems.append("secod-abuse-limits executable fixture missing " + name)

    crypto_fixture = root / "tests" / "insecure-fixtures" / "secod-crypto-data-protection"
    for name in ("fixture_app.py", "test_secure_patterns.py", "run_fixtures.py"):
        if not (crypto_fixture / name).is_file():
            problems.append("secod-crypto-data-protection executable fixture missing " + name)

    if problems:
        print("SECOD skill validation failed:")
        for problem in problems:
            print("- " + problem)
        return 1

    legacy_count = len(expected_skills) - implementation_count
    print(
        "Validated "
        + str(len(expected_skills))
        + " SECOD skill structures ("
        + str(implementation_count)
        + " implementation-v1, "
        + str(legacy_count)
        + " legacy)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
