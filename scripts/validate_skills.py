"""Read-only structural validation for the SECOD skill catalog."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys


def frontmatter_value(content: str, key: str) -> str | None:
    match = re.search(r"^" + re.escape(key) + r":\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else None


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
        if runtime_catalog_file.read_bytes() != catalog_file.read_bytes():
            problems.append("secod-core runtime catalog differs from catalog.json")

    catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    expected_skills = {item["slug"] for item in catalog["skills"]}
    catalog_skills = {item["slug"]: item for item in catalog["skills"]}
    actual_skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    seen_control_ids: set[str] = set()

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
            if f"### `{control_id}`" not in content:
                problems.append(skill + " does not define catalog control " + control_id)
        if approved_controls and re.search(r"PROVISIONAL-[A-Z0-9]+-", content):
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
        elif not re.search(r"^\s*internal:\s*true\s*$", content, re.MULTILINE):
            problems.extend(source_register_problems(skill, source_file.read_text(encoding="utf-8")))
        if not (root / "tests" / "trigger-cases" / (skill + ".md")).is_file():
            problems.append(skill + " has no trigger case")
        if not (root / "tests" / "insecure-fixtures" / skill / "README.md").is_file():
            problems.append(skill + " has no insecure fixture plan")
        if not (root / "tests" / "expected-results" / (skill + ".md")).is_file():
            problems.append(skill + " has no expected result")

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
        "test_evidence_validator.py",
        "run_fixtures.py",
    ):
        if not (abuse_fixture / name).is_file():
            problems.append("secod-abuse-limits executable fixture missing " + name)

    abuse_evidence_validator = (
        root / "skills" / "secod-abuse-limits" / "scripts" / "validate_evidence_bundle.py"
    )
    if not abuse_evidence_validator.is_file():
        problems.append("secod-abuse-limits evidence validator is missing")

    observability_evidence_validator = (
        root / "skills" / "secod-observability-response" / "scripts" / "validate_evidence_bundle.py"
    )
    if not observability_evidence_validator.is_file():
        problems.append("secod-observability-response evidence validator is missing")

    crypto_evidence_validator = (
        root / "skills" / "secod-crypto-data-protection" / "scripts" / "validate_evidence_bundle.py"
    )
    if not crypto_evidence_validator.is_file():
        problems.append("secod-crypto-data-protection evidence validator is missing")

    crypto_fixture = root / "tests" / "insecure-fixtures" / "secod-crypto-data-protection"
    for name in ("test_evidence_validator.py", "run_fixtures.py"):
        if not (crypto_fixture / name).is_file():
            problems.append("secod-crypto-data-protection executable fixture missing " + name)

    if problems:
        print("SECOD skill validation failed:")
        for problem in problems:
            print("- " + problem)
        return 1

    print("Validated " + str(len(expected_skills)) + " catalog-derived SECOD skill structures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
