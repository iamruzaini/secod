"""Executable expectations for all maintained failure-safety fixture cases."""

from __future__ import annotations

import unittest

from fixture_app import (
    CircuitBreaker,
    DegradedCache,
    DependencyFailure,
    MutationStore,
    ResourceTracker,
    authorize,
    blind_retry,
    evidence_status,
    secure_error_response,
    unsafe_error_response,
)


def unavailable() -> bool:
    raise DependencyFailure("identity provider timeout")


class FailureSafetyFixtures(unittest.TestCase):
    def test_01_clean(self) -> None:
        response = secure_error_response(RuntimeError("secret-token"))
        self.assertNotIn("secret-token", str(response))
        self.assertFalse(authorize(unavailable, fail_closed=True))

        store = MutationStore()
        with self.assertRaises(DependencyFailure):
            store.mutate(transactional=True, interrupt=True)
        self.assertEqual((store.order, store.entitlement), (False, False))

        dependency_hits = 0

        def dead_dependency() -> None:
            nonlocal dependency_hits
            dependency_hits += 1
            raise DependencyFailure("down")

        breaker = CircuitBreaker(threshold=2)
        for _ in range(5):
            with self.assertRaises(DependencyFailure):
                breaker.call(dead_dependency)
        self.assertEqual(dependency_hits, 2)

        resources = ResourceTracker()
        with self.assertRaises(DependencyFailure):
            resources.interrupted_flow(deterministic_cleanup=True)
        self.assertEqual(resources.held, set())

        cache = DegradedCache(tenant_scoped=True)
        cache.put("tenant-a", "invoice", "tenant-a-data")
        self.assertIsNone(cache.get("tenant-b", "invoice"))

    def test_02_exception_leak(self) -> None:
        response = unsafe_error_response(RuntimeError("secret-token"))
        self.assertIn("secret-token", str(response))
        self.assertIn("db.internal", str(response))

    def test_03_idp_timeout_fail_open(self) -> None:
        self.assertTrue(authorize(unavailable, fail_closed=False))

    def test_04_interrupted_multi_step_mutation(self) -> None:
        store = MutationStore()
        with self.assertRaises(DependencyFailure):
            store.mutate(transactional=False, interrupt=True)
        self.assertEqual((store.order, store.entitlement), (True, False))

    def test_05_blind_retry_and_replay(self) -> None:
        writes: list[str] = []

        def non_idempotent_write() -> None:
            writes.append("charge")
            if len(writes) == 1:
                raise DependencyFailure("response lost")

        blind_retry(non_idempotent_write)
        self.assertEqual(writes, ["charge", "charge"])

        delivered_events: list[str] = []
        for event_id in ("evt-1", "evt-1"):
            delivered_events.append(event_id)
        self.assertEqual(delivered_events.count("evt-1"), 2)

    def test_06_no_breaker(self) -> None:
        dependency_hits = 0

        def dead_dependency() -> None:
            nonlocal dependency_hits
            dependency_hits += 1
            raise DependencyFailure("down")

        for _ in range(5):
            with self.assertRaises(DependencyFailure):
                dead_dependency()
        self.assertEqual(dependency_hits, 5)

    def test_07_orphaned_cleanup(self) -> None:
        resources = ResourceTracker()
        with self.assertRaises(DependencyFailure):
            resources.interrupted_flow(deterministic_cleanup=False)
        self.assertEqual(resources.held, {"temporary-object"})

    def test_08_cross_tenant_degraded_cache(self) -> None:
        cache = DegradedCache(tenant_scoped=False)
        cache.put("tenant-a", "invoice", "tenant-a-data")
        self.assertEqual(cache.get("tenant-b", "invoice"), "tenant-a-data")

    def test_09_missing_evidence(self) -> None:
        self.assertEqual(
            evidence_status(repository=True, runtime=False, deployment=False),
            "Not verified",
        )


if __name__ == "__main__":
    unittest.main()
