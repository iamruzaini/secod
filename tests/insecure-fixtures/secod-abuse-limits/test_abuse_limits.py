"""Executable expectations for abuse-limits fixture cases."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import unittest

from fixture_app import (
    BoundedQueue,
    ConcurrencyGate,
    CounterStore,
    IdempotentWriter,
    Inventory,
    Job,
    JobLimits,
    LayeredLimiter,
    RateLimiter,
    StableQuota,
    checkout_amount,
    invoke_limited,
    recovery_response,
    retry_call,
)


class AbuseLimitsFixtures(unittest.TestCase):
    def test_01_layered_shared_rate_limits(self) -> None:
        tenant_store = CounterStore()
        user_store = CounterStore()
        source_store = CounterStore()
        instance_a = LayeredLimiter(
            RateLimiter(2, tenant_store),
            RateLimiter(2, user_store),
            RateLimiter(2, source_store),
        )
        instance_b = LayeredLimiter(
            RateLimiter(2, tenant_store),
            RateLimiter(2, user_store),
            RateLimiter(2, source_store),
        )
        effects: list[str] = []
        self.assertEqual(invoke_limited(instance_a, ("tenant-a", "user-a", "ip-a"), effects), 200)
        self.assertEqual(invoke_limited(instance_b, ("tenant-a", "user-a", "ip-a"), effects), 200)
        self.assertEqual(invoke_limited(instance_a, ("tenant-a", "user-a", "ip-b"), effects), 429)
        self.assertEqual(invoke_limited(instance_b, ("tenant-b", "user-b", "ip-a"), effects), 429)
        self.assertEqual(effects, ["executed", "executed"])

    def test_02_missing_or_instance_local_limiter(self) -> None:
        effects: list[str] = []
        for _ in range(3):
            self.assertEqual(invoke_limited(None, ("paid-flow",), effects), 200)
        self.assertEqual(len(effects), 3)

        first = RateLimiter(1, CounterStore())
        second = RateLimiter(1, CounterStore())
        self.assertTrue(first.allow("same-tenant"))
        self.assertTrue(second.allow("same-tenant"))

    def test_03_login_and_recovery_enumeration(self) -> None:
        account_failures = RateLimiter(2, CounterStore())
        source_failures = RateLimiter(2, CounterStore())
        decisions = [
            account_failures.allow("account-a") and source_failures.allow("ip-a")
            for _ in range(3)
        ]
        self.assertEqual(decisions, [True, True, False])
        reset_accounts = RateLimiter(1, CounterStore())
        reset_sources = RateLimiter(1, CounterStore())

        def reset_allowed(account: str, source: str) -> bool:
            decisions = (reset_accounts.allow(account), reset_sources.allow(source))
            return all(decisions)

        self.assertTrue(reset_allowed("account-a", "ip-a"))
        self.assertFalse(reset_allowed("account-a", "ip-b"))
        self.assertFalse(reset_allowed("account-b", "ip-a"))
        self.assertEqual(
            recovery_response(True, uniform=True),
            recovery_response(False, uniform=True),
        )
        self.assertNotEqual(
            recovery_response(True, uniform=False),
            recovery_response(False, uniform=False),
        )

    def test_04_idempotency_and_replay(self) -> None:
        secure = IdempotentWriter()
        first = secure.write("tenant-a", "event-1", "refund", atomic=True)
        second = secure.write("tenant-a", "event-1", "refund", atomic=True)
        self.assertEqual(first, second)
        self.assertEqual(secure.effects, ["refund"])

        unsafe = IdempotentWriter()
        unsafe.write("tenant-a", "event-1", "refund", atomic=False)
        unsafe.write("tenant-a", "event-1", "refund", atomic=False)
        self.assertEqual(unsafe.effects, ["refund", "refund"])

    def test_05_concurrent_redemption_race(self) -> None:
        secure = Inventory()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: secure.claim(atomic=True), range(2)))
        self.assertEqual(sum(results), 1)
        self.assertEqual(secure.remaining, 0)

        unsafe = Inventory()
        barrier = Barrier(2)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(
                pool.map(
                    lambda _: unsafe.claim(atomic=False, read_barrier=barrier),
                    range(2),
                )
            )
        self.assertEqual(sum(results), 2)

    def test_06_bounded_retry_and_stable_quota(self) -> None:
        writer = IdempotentWriter()

        def unavailable() -> None:
            writer.write("tenant-a", "retry-key", "paid-effect", atomic=True)
            raise TimeoutError("dependency unavailable")

        jitter = {1: 17, 2: 23}
        attempts, delays = retry_call(
            unavailable,
            maximum_attempts=3,
            base_delay_ms=100,
            jitter_ms=lambda attempt: jitter[attempt],
        )
        self.assertEqual(attempts, 3)
        self.assertEqual(delays, [117, 223])
        self.assertEqual(writer.effects, ["paid-effect"])

        stable = StableQuota(limit=1, stable_identity=True)
        self.assertTrue(stable.allow(tenant="tenant-a", session="session-1"))
        self.assertFalse(stable.allow(tenant="tenant-a", session="session-2"))
        bypassable = StableQuota(limit=1, stable_identity=False)
        self.assertTrue(bypassable.allow(tenant="tenant-a", session="session-1"))
        self.assertTrue(bypassable.allow(tenant="tenant-a", session="session-2"))
        self.assertEqual(
            checkout_amount(catalog_amount=2500, client_amount=1, trust_client=False),
            (422, None),
        )
        self.assertEqual(
            checkout_amount(catalog_amount=2500, client_amount=1, trust_client=True),
            (200, 1),
        )

    def test_07_export_caps_cancellation_and_queue_shedding(self) -> None:
        limits = JobLimits(
            maximum_requests=2,
            maximum_items=100,
            maximum_cpu_ms=1000,
            maximum_memory_bytes=2048,
            maximum_input_bytes=512,
            maximum_output_bytes=1024,
            maximum_pending_calls=4,
            maximum_concurrent_jobs=2,
            timeout_ms=5000,
        )
        accepted = {
            "requests": 2,
            "items": 100,
            "cpu_ms": 1000,
            "memory_bytes": 2048,
            "input_bytes": 512,
            "output_bytes": 1024,
            "pending_calls": 4,
            "concurrent_jobs": 2,
        }
        self.assertTrue(limits.accepts(**accepted))
        for field in accepted:
            oversized = dict(accepted)
            oversized[field] += 1
            self.assertFalse(limits.accepts(**oversized), field)

        secure_job = Job()
        self.assertEqual(
            secure_job.run(
                elapsed_ms=5001,
                limits=limits,
                propagate_cancellation=True,
            ),
            "timed_out",
        )
        self.assertFalse(secure_job.child_running)
        self.assertEqual(secure_job.temporary_resources, set())
        unsafe_job = Job()
        self.assertEqual(
            unsafe_job.run(
                elapsed_ms=5001,
                limits=limits,
                propagate_cancellation=False,
            ),
            "timed_out",
        )
        self.assertTrue(unsafe_job.child_running)
        self.assertEqual(unsafe_job.temporary_resources, {"temporary-export"})

        queue = BoundedQueue(maximum_depth=1)
        self.assertEqual(queue.enqueue("job-1"), "accepted")
        self.assertEqual(queue.enqueue("job-2"), "rejected")
        concurrency = ConcurrencyGate(maximum_active=1)
        self.assertEqual(concurrency.acquire(), "accepted")
        self.assertEqual(concurrency.acquire(), "rejected")
        concurrency.release()
        self.assertEqual(concurrency.acquire(), "accepted")

if __name__ == "__main__":
    unittest.main()
