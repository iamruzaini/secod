"""Generate SECOD's catalog and contract matrix from its repository PRD.

The PRD's 57 table rows are the source of truth for the current v1 catalog.
This script never rewrites reviewed skill contracts or test fixtures, reaches a
provider account or the network, or writes outside the SECOD repository.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import textwrap


SECOD = Path(__file__).resolve().parents[1]
PRD = SECOD / "docs" / "PRD.md"
CATALOG = SECOD / "catalog.json"
RUNTIME_CATALOG = SECOD / "skills" / "secod-core" / "references" / "catalog.json"

PROVIDERS = [
    {
        "slug": "supabase",
        "title": "Supabase",
        "skill": "secod-supabase",
        "coverage": "Checks database, Storage, Realtime, Edge Function, key, and production settings.",
    },
    {
        "slug": "firebase",
        "title": "Firebase",
        "skill": "secod-firebase",
        "coverage": "Checks Firebase rules, App Check, privileged credentials, Functions, and IAM.",
    },
    {
        "slug": "neon",
        "title": "Neon",
        "skill": "secod-neon",
        "coverage": "Checks Postgres roles, RLS, branches, backups, connections, and network boundaries.",
    },
    {
        "slug": "convex",
        "title": "Convex",
        "skill": "secod-convex",
        "coverage": "Checks Convex function visibility, validation, authorization, webhooks, and deployment access.",
    },
    {
        "slug": "aws",
        "title": "AWS",
        "skill": "secod-aws-web",
        "coverage": "Routes AWS web, Lambda/API Gateway, Cognito, S3/CloudFront, data, IAM, and secret checks.",
    },
    {
        "slug": "google-cloud",
        "title": "Google Cloud",
        "skill": "secod-google-cloud-web",
        "coverage": "Routes Google Cloud IAM, secret, and Storage checks.",
    },
]

FEATURES = [
    {"id": "authentication", "label": "User login or accounts", "skills": ["secod-identity-access"]},
    {"id": "uploads", "label": "User uploads", "skills": ["secod-data-files"]},
    {"id": "payments", "label": "Payments or incoming webhooks", "skills": ["secod-payments-billing"]},
    {"id": "ai", "label": "AI features", "skills": ["secod-ai-api-integrations"]},
    {"id": "admin", "label": "Admin area", "skills": ["secod-identity-access", "secod-observability-response"]},
    {"id": "multitenancy", "label": "Separate customer workspaces", "skills": ["secod-identity-access"]},
    {"id": "delivery", "label": "Automated build or deployment", "skills": ["secod-packages-delivery", "secod-failure-safety"]},
]

# Stable controls approved in catalog. New entries require contract review before addition;
# skill-local PROVISIONAL identifiers are never promoted implicitly.
APPROVED_CONTROLS = {
    "secod-crypto-data-protection": [
        ("SECOD-CDP-01", "TLS and secure communication"),
        ("SECOD-CDP-02", "CSPRNG for tokens, nonces, and salts"),
        ("SECOD-CDP-03", "Password and secret-derivation KDFs"),
        ("SECOD-CDP-04", "Algorithm selection, authenticated encryption, no custom cryptography"),
        ("SECOD-CDP-05", "Key management lifecycle, agility, and migration"),
        ("SECOD-CDP-06", "Data classification, minimization, sharing, residency"),
        ("SECOD-CDP-07", "Analytics, cookie, telemetry, and tracking-data inventory"),
        ("SECOD-CDP-08", "Retention schedules and deletion propagation"),
        ("SECOD-CDP-09", "Backup encryption and restore verification"),
    ],
    "secod-observability-response": [
        ("SECOD-OBS-01", "Structured security audit events"),
        ("SECOD-OBS-02", "Redaction and log-data minimization"),
        ("SECOD-OBS-03", "API-key lifecycle visibility"),
        ("SECOD-OBS-04", "Security alerting for control failures"),
        ("SECOD-OBS-05", "Incident runbooks and breach-to-containment mapping"),
        ("SECOD-OBS-06", "Evidence preservation"),
        ("SECOD-OBS-07", "Recovery drills for partial operations and backup restore"),
    ],
    "secod-failure-safety": [
        ("SECOD-FAIL-01", "Centralized global exception handling"),
        ("SECOD-FAIL-02", "Fail-closed authentication and authorization dependencies"),
        ("SECOD-FAIL-03", "Rollback of partial database, payment, and entitlement mutations"),
        ("SECOD-FAIL-04", "Safe retry classification"),
        ("SECOD-FAIL-05", "Circuit breakers on failing dependencies"),
        ("SECOD-FAIL-06", "Timeout and cancellation propagation"),
        ("SECOD-FAIL-07", "Deterministic cleanup"),
        ("SECOD-FAIL-08", "Safe degraded states"),
        ("SECOD-FAIL-09", "Redacted error responses"),
        ("SECOD-FAIL-10", "Failure-mode tests for storage, provider, and network"),
    ],
}

CONTROL_APPROVAL_DATES = {
    "secod-crypto-data-protection": "2026-08-28",
    "secod-failure-safety": "2026-08-26",
    "secod-observability-response": "2026-08-27",
}


def title_from_slug(slug: str) -> str:
    names = {
        "ai": "AI",
        "api": "API",
        "apis": "APIs",
        "aws": "AWS",
        "cloudflare": "Cloudflare",
        "gcp": "GCP",
        "google": "Google",
        "id": "ID",
        "iam": "IAM",
        "llm": "LLM",
        "mcp": "MCP",
        "nextjs": "Next.js",
        "oidc": "OIDC",
        "rbac": "RBAC",
        "s3": "S3",
        "sdk": "SDK",
        "ssrf": "SSRF",
        "vercel": "Vercel",
    }
    words = slug.removeprefix("secod-").split("-")
    return " ".join(names.get(word, word.capitalize()) for word in words)


def parse_rows() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    in_baseline = False
    for line in PRD.read_text(encoding="utf-8").splitlines():
        if line.startswith("### 8.1"):
            in_baseline = True
            continue
        if line.startswith("### 8.2"):
            in_baseline = False
        match = re.match(r"^\| `(secod-[a-z0-9-]+)` \| (.*) \| (.*) \|$", line)
        if not match:
            continue
        slug, promise, controls = match.groups()
        skills.append(
            {
                "slug": slug,
                "title": title_from_slug(slug),
                "layer": "General baseline" if in_baseline else "Framework / provider adapter",
                "promise": promise,
                "controls": controls,
            }
        )
    if len(skills) != 57:
        raise ValueError(f"Expected 57 PRD catalog rows, found {len(skills)}")
    return skills


def dependencies_for(skill: dict[str, str]) -> list[str]:
    slug = skill["slug"]
    if slug == "secod-core":
        return []
    prefix = skill["promise"].split("Apply when", 1)[0]
    direct = re.findall(r"`(secod-[a-z0-9-]+)`", prefix)
    dependencies = [name for name in direct if name != slug]
    if "secod-core" not in dependencies:
        dependencies.insert(0, "secod-core")
    return list(dict.fromkeys(dependencies))


def summary(text: str) -> str:
    plain = re.sub(r"\[[^\]]+\]\([^)]+\)", "", text)
    plain = re.sub(r"`", "", plain)
    return textwrap.shorten(plain, width=180, placeholder="…")


def write_catalog(skills: list[dict[str, str]]) -> list[dict[str, object]]:
    catalog_skills: list[dict[str, object]] = []
    baseline = [skill["slug"] for skill in skills if skill["layer"] == "General baseline"]
    for skill in skills:
        catalog_skill = {
            "slug": skill["slug"],
            "title": skill["title"],
            "layer": skill["layer"],
            "summary": summary(skill["promise"]),
            "purpose": summary(skill["controls"]),
            "dependencies": dependencies_for(skill),
        }
        if skill["slug"] in APPROVED_CONTROLS:
            catalog_skill["controls"] = [
                {
                    "id": control_id,
                    "title": title,
                    "status": "approved",
                    "approvedOn": CONTROL_APPROVAL_DATES[skill["slug"]],
                }
                for control_id, title in APPROVED_CONTROLS[skill["slug"]]
            ]
        catalog_skills.append(catalog_skill)
    payload = {
        "schemaVersion": 1,
        "source": "docs/PRD.md section 8",
        "skills": catalog_skills,
        "recommendedBaseline": baseline,
        "providers": PROVIDERS,
        "features": FEATURES,
    }
    serialized = json.dumps(payload, indent=2) + "\n"
    CATALOG.write_text(serialized, encoding="utf-8")
    RUNTIME_CATALOG.write_text(serialized, encoding="utf-8")
    return catalog_skills


def markdown_lines(text: str) -> str:
    return "\n".join(textwrap.wrap(text, width=96, break_long_words=False))


def reference_links(controls: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", controls)


def write_skill_contract(skill: dict[str, str], catalog_skill: dict[str, object]) -> None:
    skill_root = SECOD / "skills" / skill["slug"]
    (skill_root / "agents").mkdir(parents=True, exist_ok=True)
    (skill_root / "references").mkdir(parents=True, exist_ok=True)
    dependencies = catalog_skill["dependencies"]
    dependency_text = ", ".join(f"`{name}`" for name in dependencies) or "None"
    description = summary(skill["promise"]).replace('"', "'")
    skill_markdown = f"""---
name: {skill['slug']}
description: {description}
---

# SECOD {skill['title']}

## Scope and applicability

{markdown_lines(skill['promise'])}

## Control requirements

{markdown_lines(skill['controls'])}

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: {dependency_text}.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
"""
    (skill_root / "SKILL.md").write_text(skill_markdown, encoding="utf-8")

    source_rows = reference_links(skill["controls"])
    if source_rows:
        links = "\n".join(f"| {label} | {url} | Pending review |" for label, url in source_rows)
    else:
        links = "| Direct official sources | Add the control-specific primary sources required by the PRD. | Pending review |"
    source_markdown = f"""# Source register: {skill['slug']}

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source | URL | Status |
| --- | --- | --- |
{links}

For every retained source, record version/SDK version, reviewed date, review expiry, content
hash or ETag where obtainable, owner, plan/tier, region, feature maturity, and SECOD control IDs.
"""
    (skill_root / "references" / "sources.md").write_text(source_markdown, encoding="utf-8")

    prompt = f'Use ${skill["slug"]} to review this project. Preserve missing evidence as Not verified.'
    metadata = f'''display_name: "{skill['title']}"
short_description: "{summary(skill['promise']).replace('"', "'")}"
default_prompt: "{prompt}"
'''
    (skill_root / "agents" / "openai.yaml").write_text(metadata, encoding="utf-8")


def write_test_plan(skill: dict[str, str]) -> None:
    slug = skill["slug"]
    trigger = SECOD / "tests" / "trigger-cases" / f"{slug}.md"
    fixture = SECOD / "tests" / "insecure-fixtures" / slug / "README.md"
    expected = SECOD / "tests" / "expected-results" / f"{slug}.md"
    trigger.parent.mkdir(parents=True, exist_ok=True)
    fixture.parent.mkdir(parents=True, exist_ok=True)
    expected.parent.mkdir(parents=True, exist_ok=True)
    trigger.write_text(
        f"# Trigger case: {slug}\n\nPositive prompt: `Use {slug} to review this project.`\n\n"
        "Negative prompt: a request outside this skill's stated applicability must not claim coverage.\n",
        encoding="utf-8",
    )
    fixture.write_text(
        f"# Insecure fixture plan: {slug}\n\nCreate a minimal reproducible unsafe case for the control requirements in the skill contract. "
        "Include a missing-evidence case and, where applicable, a partial-failure or replay case.\n",
        encoding="utf-8",
    )
    expected.write_text(
        f"# Expected result: {slug}\n\nThe skill identifies the insecure fixture, reports evidence safely, provides a verification path, "
        "and uses `Not verified` for unavailable evidence.\n",
        encoding="utf-8",
    )


def write_matrix(skills: list[dict[str, str]], catalog_skills: list[dict[str, object]]) -> None:
    by_slug = {item["slug"]: item for item in catalog_skills}
    rows = []
    for skill in skills:
        deps = ", ".join(by_slug[skill["slug"]]["dependencies"]) or "None"
        rows.append(
            "| {slug} | {promise} | Repository plus dashboard/API evidence; direct primary sources and source-register metadata. | "
            "Read-only review; structured finding output. | {deps}; unsafe fixture, trigger case, and expected result required. |".format(
                slug=skill["slug"], promise=summary(skill["promise"]), deps=deps
            )
        )
    matrix = """# Skill Contract Matrix

This matrix is generated from the 57-row PRD catalog by `scripts/sync_catalog.py`.
It is an index of contracts; the detailed requirements and source register live with each skill.

| Skill | Promise and trigger | Inputs and references | Script and output | Dependencies and v1 acceptance |
| --- | --- | --- | --- | --- |
""" + "\n".join(rows) + "\n"
    (SECOD / "docs" / "SKILL-CONTRACT-MATRIX.md").write_text(matrix, encoding="utf-8")


def main() -> None:
    skills = parse_rows()
    catalog_skills = write_catalog(skills)
    write_matrix(skills, catalog_skills)
    print(f"Synced {len(skills)} SECOD catalog entries from docs/PRD.md section 8.")


if __name__ == "__main__":
    main()
