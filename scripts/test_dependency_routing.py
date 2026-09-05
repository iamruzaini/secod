"""Exercise SECOD's static dependency-routing contract.

This is a catalog test, not an LLM execution test. It proves that the checked-in
dependency graph is complete, acyclic, transitively closed, and isolated across
the representative stack profiles below.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
sys.path.insert(0, str(ROOT))

from scripts.sync_catalog import dependencies_for, parse_rows

COMMON_BASELINE = {
    "secod-core",
    "secod-threat-model",
    "secod-identity-access",
    "secod-web-app-security",
    "secod-inputs-apis",
    "secod-runtime-execution",
    "secod-crypto-data-protection",
    "secod-data-files",
    "secod-abuse-limits",
    "secod-secrets-config",
    "secod-packages-delivery",
    "secod-vulnerability-management",
    "secod-observability-response",
    "secod-failure-safety",
    "secod-ship-check",
}

SCENARIOS = (
    {
        "name": "generic web application",
        "roots": COMMON_BASELINE,
        "provider_skills": set(),
    },
    {
        "name": "Next.js web application without a provider",
        "roots": COMMON_BASELINE | {"secod-nextjs"},
        "provider_skills": {"secod-nextjs"},
    },
    {
        "name": "Supabase Auth application",
        "roots": COMMON_BASELINE
        | {"secod-auth-provider-integrations", "secod-supabase", "secod-supabase-auth"},
        "provider_skills": {
            "secod-auth-provider-integrations",
            "secod-supabase",
            "secod-supabase-auth",
        },
    },
    {
        "name": "AWS S3 and CloudFront application",
        "roots": COMMON_BASELINE | {"secod-aws-web", "secod-aws-s3-cloudfront"},
        "provider_skills": {"secod-aws-web", "secod-aws-s3-cloudfront"},
    },
    {
        "name": "Google Cloud application without Firebase",
        "roots": COMMON_BASELINE | {"secod-google-cloud-web"},
        "provider_skills": {"secod-google-cloud-web"},
    },
    {
        "name": "static Cloudflare Pages application",
        "roots": COMMON_BASELINE | {"secod-cloudflare", "secod-cloudflare-pages"},
        "provider_skills": {"secod-cloudflare", "secod-cloudflare-pages"},
    },
    {
        "name": "Cloudflare Workers AI application",
        "roots": COMMON_BASELINE
        | {
            "secod-ai-api-integrations",
            "secod-cloudflare",
            "secod-cloudflare-workers",
            "secod-cloudflare-workers-ai",
        },
        "provider_skills": {
            "secod-cloudflare",
            "secod-cloudflare-workers",
            "secod-cloudflare-workers-ai",
        },
    },
    {
        "name": "Vercel application without AI",
        "roots": COMMON_BASELINE | {"secod-vercel-platform"},
        "provider_skills": {"secod-vercel-platform"},
    },
    {
        "name": "Stripe and OpenAI application",
        "roots": COMMON_BASELINE
        | {
            "secod-ai-api-integrations",
            "secod-openai",
            "secod-payments-billing",
            "secod-stripe",
        },
        "provider_skills": {"secod-openai", "secod-stripe"},
    },
)


def load_graph() -> tuple[dict[str, list[str]], set[str]]:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = payload.get("skills", [])
    names = [entry.get("slug") for entry in entries]
    if len(entries) != 57:
        raise AssertionError(f"Expected 57 catalog skills, found {len(entries)}")
    if len(set(names)) != len(names):
        raise AssertionError("Catalog contains duplicate skill slugs")
    graph = {entry["slug"]: entry.get("dependencies", []) for entry in entries}
    generated_graph = {
        entry["slug"]: dependencies_for(entry) for entry in parse_rows()
    }
    if graph != generated_graph:
        mismatches = sorted(
            slug
            for slug in set(graph) | set(generated_graph)
            if graph.get(slug) != generated_graph.get(slug)
        )
        raise AssertionError(
            "Catalog does not match dependency generator for: " + ", ".join(mismatches)
        )
    unknown = sorted({dep for deps in graph.values() for dep in deps} - set(graph))
    if unknown:
        raise AssertionError("Catalog has unknown dependencies: " + ", ".join(unknown))
    return graph, set(names)


def dependency_closure(graph: dict[str, list[str]], roots: set[str]) -> set[str]:
    missing_roots = sorted(roots - set(graph))
    if missing_roots:
        raise AssertionError("Routing scenario has unknown roots: " + ", ".join(missing_roots))
    visited: set[str] = set()
    active: list[str] = []

    def visit(name: str) -> None:
        if name in active:
            cycle = " -> ".join(active[active.index(name) :] + [name])
            raise AssertionError("Dependency cycle: " + cycle)
        if name in visited:
            return
        active.append(name)
        for dependency in graph[name]:
            visit(dependency)
        active.pop()
        visited.add(name)

    for root in sorted(roots):
        visit(root)
    return visited


def main() -> int:
    graph, names = load_graph()
    provider_skills = {
        name for name in names if name not in COMMON_BASELINE and name not in {
            "secod-payments-billing",
            "secod-ai-api-integrations",
            "secod-container-runtime",
            "secod-email-messaging",
        }
    }
    checked: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        roots = set(scenario["roots"])
        actual = dependency_closure(graph, roots)
        expected = set(roots)
        for name in roots:
            expected.update(dependency_closure(graph, {name}))
        if actual != expected:
            raise AssertionError(
                f"{scenario['name']}: closure mismatch; missing={sorted(expected - actual)}, "
                f"unexpected={sorted(actual - expected)}"
            )
        selected_provider_skills = actual & provider_skills
        expected_provider_skills = set(scenario["provider_skills"])
        if selected_provider_skills != expected_provider_skills:
            raise AssertionError(
                f"{scenario['name']}: provider routing mismatch; "
                f"expected={sorted(expected_provider_skills)}, "
                f"actual={sorted(selected_provider_skills)}"
            )
        if "secod-core" not in actual:
            raise AssertionError(f"{scenario['name']}: secod-core is not in the closure")
        checked.append(
            {
                "scenario": scenario["name"],
                "roots": len(roots),
                "closure": len(actual),
                "provider_skills": sorted(selected_provider_skills),
            }
        )

    print(
        json.dumps(
            {
                "catalog_skills": len(names),
                "scenarios": checked,
                "routing_graph": "passed",
                "llm_execution": "not tested by this script",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
