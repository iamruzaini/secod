"""Synchronize SECOD-owned catalog projections."""

from __future__ import annotations

from pathlib import Path
import json


SECOD = Path(__file__).resolve().parents[1]
CATALOG = SECOD / "catalog.json"
RUNTIME_CATALOG = SECOD / "skills" / "secod-core" / "references" / "catalog.json"
MATRIX = SECOD / "docs" / "SKILL-CONTRACT-MATRIX.md"


def sync_current_catalog() -> int:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("catalog.json contains no skills")

    slugs = [item.get("slug") for item in skills]
    if any(not isinstance(slug, str) or not slug for slug in slugs):
        raise ValueError("catalog.json contains a missing or invalid skill slug")
    if len(set(slugs)) != len(slugs):
        raise ValueError("catalog.json contains duplicate skill slugs")

    known = set(slugs)
    unknown = sorted(
        dependency
        for item in skills
        for dependency in item.get("dependencies", [])
        if dependency not in known
    )
    if unknown:
        raise ValueError("catalog.json contains unknown dependencies: " + ", ".join(unknown))

    serialized = json.dumps(payload, indent=2) + "\n"
    RUNTIME_CATALOG.write_text(serialized, encoding="utf-8")

    rows = []
    for item in skills:
        dependencies = ", ".join(item.get("dependencies", [])) or "None"
        rows.append(
            "| `{slug}` | {layer} | {summary} | {dependencies} |".format(
                slug=item["slug"],
                layer=item.get("layer", "Unclassified"),
                summary=item.get("summary", "Migration pending"),
                dependencies=dependencies,
            )
        )
    matrix = """# Skill Catalog Matrix

Generated from `catalog.json` by `scripts/sync_catalog.py`. Implementation contracts live in
each skill directory.

| Skill | Layer | Current catalog summary | Dependencies |
|---|---|---|---|
""" + "\n".join(rows) + "\n"
    MATRIX.write_text(matrix, encoding="utf-8")
    return len(skills)


def main() -> None:
    count = sync_current_catalog()
    print(f"Synced {count} SECOD catalog entries from catalog.json.")


if __name__ == "__main__":
    main()
