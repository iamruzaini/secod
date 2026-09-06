"""Exercise SECOD's static dependency-routing contract.

This is a catalog test, not an LLM execution test. It proves that every checked-in
catalog entry has a complete, acyclic, transitively closed route. Representative
stack profiles test exact provider selection, and an all-generalized baseline
proves every provider/framework adapter remains unselected without its signal.
Catalog data is migration inventory; the implementation-first PRD no longer embeds
a fixed-size machine-readable table.
"""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
PROVIDER_ADAPTER_CATEGORIES = {"provider-family", "provider-feature", "framework"}
PROVIDER_ADAPTER_LAYERS = {"Mobile framework adapter"}

SCENARIOS = (
    {
        "name": "authenticated web API feature",
        "roots": {
            "secod-core",
            "secod-identity-access",
            "secod-inputs-apis",
            "secod-secrets-config",
            "secod-failure-safety",
        },
        "provider_skills": set(),
        "excluded_skills": {"secod-payments-billing", "secod-ai-api-integrations"},
    },
    {
        "name": "Next.js web application without a provider",
        "roots": {
            "secod-core",
            "secod-nextjs",
            "secod-web-app-security",
            "secod-inputs-apis",
        },
        "provider_skills": {"secod-nextjs"},
        "excluded_skills": {"secod-vercel-platform", "secod-firebase"},
    },
    {
        "name": "Next.js Firebase tenant document feature",
        "roots": {
            "secod-core",
            "secod-nextjs",
            "secod-identity-access",
            "secod-inputs-apis",
            "secod-firebase",
        },
        "provider_skills": {"secod-nextjs", "secod-firebase"},
        "excluded_skills": {"secod-supabase", "secod-stripe", "secod-openai"},
    },
    {
        "name": "framework-neutral native mobile feature",
        "roots": {"secod-core", "secod-mobile-app-security"},
        "provider_skills": {"secod-mobile-app-security"},
        "excluded_skills": {"secod-react-native-expo", "secod-flutter", "secod-nextjs"},
    },
    {
        "name": "Expo mobile feature",
        "roots": {"secod-core", "secod-react-native-expo"},
        "provider_skills": {"secod-mobile-app-security", "secod-react-native-expo"},
        "excluded_skills": {"secod-flutter", "secod-nextjs", "secod-firebase"},
    },
    {
        "name": "Flutter mobile feature",
        "roots": {"secod-core", "secod-flutter"},
        "provider_skills": {"secod-mobile-app-security", "secod-flutter"},
        "excluded_skills": {"secod-react-native-expo", "secod-nextjs", "secod-firebase"},
    },
    {
        "name": "Supabase Auth application",
        "roots": {
            "secod-core",
            "secod-identity-access",
            "secod-auth-provider-integrations",
            "secod-supabase",
            "secod-supabase-auth",
        },
        "provider_skills": {
            "secod-auth-provider-integrations",
            "secod-supabase",
            "secod-supabase-auth",
        },
        "excluded_skills": {"secod-clerk", "secod-auth0", "secod-firebase"},
    },
    {
        "name": "AWS S3 and CloudFront application",
        "roots": {"secod-core", "secod-aws-web", "secod-aws-s3-cloudfront"},
        "provider_skills": {"secod-aws-web", "secod-aws-s3-cloudfront"},
        "excluded_skills": {"secod-google-cloud-web", "secod-firebase"},
    },
    {
        "name": "Google Cloud application without Firebase",
        "roots": {"secod-core", "secod-google-cloud-web"},
        "provider_skills": {"secod-google-cloud-web"},
        "excluded_skills": {"secod-firebase", "secod-aws-web"},
    },
    {
        "name": "static Cloudflare Pages application",
        "roots": {"secod-core", "secod-cloudflare", "secod-cloudflare-pages"},
        "provider_skills": {"secod-cloudflare", "secod-cloudflare-pages"},
        "excluded_skills": {"secod-cloudflare-workers", "secod-vercel-platform"},
    },
    {
        "name": "Cloudflare Workers AI application",
        "roots": {
            "secod-core",
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
        "excluded_skills": {"secod-openai", "secod-anthropic"},
    },
    {
        "name": "Vercel application without AI",
        "roots": {"secod-core", "secod-vercel-platform"},
        "provider_skills": {"secod-vercel-platform"},
        "excluded_skills": {"secod-vercel-ai", "secod-openai"},
    },
    {
        "name": "Stripe and OpenAI application",
        "roots": {
            "secod-core",
            "secod-ai-api-integrations",
            "secod-openai",
            "secod-payments-billing",
            "secod-stripe",
        },
        "provider_skills": {"secod-openai", "secod-stripe"},
        "excluded_skills": {"secod-anthropic", "secod-polar"},
    },
    {
        "name": "Stripe checkout without AI",
        "roots": {"secod-core", "secod-payments-billing", "secod-stripe"},
        "provider_skills": {"secod-stripe"},
        "excluded_skills": {"secod-openai", "secod-polar"},
    },
    {
        "name": "OpenAI tool feature without payments",
        "roots": {"secod-core", "secod-ai-api-integrations", "secod-openai"},
        "provider_skills": {"secod-openai"},
        "excluded_skills": {"secod-stripe", "secod-anthropic"},
    },
)


def load_graph() -> tuple[
    dict[str, list[str]],
    set[str],
    set[str],
    set[str],
    set[str],
]:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = payload.get("skills", [])
    names = [entry.get("slug") for entry in entries]
    if not entries:
        raise AssertionError("Catalog contains no skills")
    if len(set(names)) != len(names):
        raise AssertionError("Catalog contains duplicate skill slugs")
    graph = {entry["slug"]: entry.get("dependencies", []) for entry in entries}
    unknown = sorted({dep for deps in graph.values() for dep in deps} - set(graph))
    if unknown:
        raise AssertionError("Catalog has unknown dependencies: " + ", ".join(unknown))
    provider_skills = {
        entry["slug"] for entry in entries if entry.get("layer") != "General baseline"
    }
    provider_adapters = {
        entry["slug"]
        for entry in entries
        if entry.get("category") in PROVIDER_ADAPTER_CATEGORIES
        or entry.get("layer") in PROVIDER_ADAPTER_LAYERS
    }
    general_baselines = {
        entry["slug"] for entry in entries if entry.get("layer") == "General baseline"
    }
    if not provider_adapters:
        raise AssertionError("Catalog contains no provider/framework adapters")
    if "secod-core" not in general_baselines:
        raise AssertionError("secod-core must be a General baseline skill")
    return graph, set(names), provider_skills, provider_adapters, general_baselines


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


def validate_catalog_entry_routes(
    graph: dict[str, list[str]], names: set[str]
) -> list[dict[str, object]]:
    """Exercise every catalog skill as a route root."""
    checked: list[dict[str, object]] = []
    for name in sorted(names):
        actual = dependency_closure(graph, {name})
        if name not in actual:
            raise AssertionError(f"{name}: route does not include itself")
        if name != "secod-core" and "secod-core" not in actual:
            raise AssertionError(f"{name}: route does not include secod-core")
        missing_direct = set(graph[name]) - actual
        if missing_direct:
            raise AssertionError(
                f"{name}: route omits direct dependencies: {sorted(missing_direct)}"
            )
        if dependency_closure(graph, actual) != actual:
            raise AssertionError(f"{name}: dependency closure is not transitive")
        checked.append({"skill": name, "closure": len(actual)})

    covered = {item["skill"] for item in checked}
    if covered != names:
        raise AssertionError(
            "Catalog routing coverage mismatch; "
            f"missing={sorted(names - covered)}, unexpected={sorted(covered - names)}"
        )
    return checked


def validate_provider_non_selection(
    graph: dict[str, list[str]],
    provider_adapters: set[str],
    general_baselines: set[str],
) -> list[str]:
    """Prove each adapter stays out when only generalized skills are selected."""
    baseline_route = dependency_closure(graph, general_baselines)
    checked: list[str] = []
    for adapter in sorted(provider_adapters):
        if adapter in baseline_route:
            raise AssertionError(
                f"{adapter}: selected without a provider/framework signal"
            )
        checked.append(adapter)
    return checked


def main() -> int:
    (
        graph,
        names,
        provider_skills,
        provider_adapters,
        general_baselines,
    ) = load_graph()
    catalog_entry_checks = validate_catalog_entry_routes(graph, names)
    provider_non_selection_checks = validate_provider_non_selection(
        graph, provider_adapters, general_baselines
    )
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
        excluded_skills = set(scenario["excluded_skills"])
        leaked = actual & excluded_skills
        if leaked:
            raise AssertionError(
                f"{scenario['name']}: unrelated skills selected: {sorted(leaked)}"
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
                "catalog_entry_routes_checked": len(catalog_entry_checks),
                "provider_non_selection_checks": len(provider_non_selection_checks),
                "representative_scenarios": checked,
                "routing_graph": "passed",
                "llm_execution": "not tested by this script",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
