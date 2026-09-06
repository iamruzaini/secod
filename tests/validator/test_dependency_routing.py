from __future__ import annotations

import unittest

from scripts.test_dependency_routing import (
    dependency_closure,
    validate_catalog_entry_routes,
    validate_provider_non_selection,
)


class DependencyRoutingTests(unittest.TestCase):
    def test_every_catalog_entry_is_exercised(self) -> None:
        graph = {
            "secod-core": [],
            "secod-general": ["secod-core"],
            "secod-provider": ["secod-core", "secod-general"],
        }

        checked = validate_catalog_entry_routes(graph, set(graph))

        self.assertEqual(set(graph), {item["skill"] for item in checked})

    def test_provider_is_not_selected_by_generalized_baseline(self) -> None:
        graph = {
            "secod-core": [],
            "secod-general": ["secod-core"],
            "secod-provider": ["secod-core", "secod-general"],
        }

        checked = validate_provider_non_selection(
            graph,
            {"secod-provider"},
            {"secod-core", "secod-general"},
        )

        self.assertEqual(["secod-provider"], checked)

    def test_provider_leak_into_generalized_baseline_fails(self) -> None:
        graph = {
            "secod-core": [],
            "secod-general": ["secod-core", "secod-provider"],
            "secod-provider": ["secod-core"],
        }

        with self.assertRaisesRegex(
            AssertionError, "selected without a provider/framework signal"
        ):
            validate_provider_non_selection(
                graph,
                {"secod-provider"},
                {"secod-core", "secod-general"},
            )

    def test_cycle_is_detected_during_all_entry_coverage(self) -> None:
        graph = {
            "secod-core": [],
            "secod-one": ["secod-two"],
            "secod-two": ["secod-one"],
        }

        with self.assertRaisesRegex(AssertionError, "Dependency cycle"):
            validate_catalog_entry_routes(graph, set(graph))

    def test_dependency_closure_rejects_unknown_root(self) -> None:
        with self.assertRaisesRegex(AssertionError, "unknown roots"):
            dependency_closure({"secod-core": []}, {"secod-missing"})


if __name__ == "__main__":
    unittest.main()
