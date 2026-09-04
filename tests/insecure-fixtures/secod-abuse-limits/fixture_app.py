"""Deterministic provider-neutral abuse-limit behaviors for fixture tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Barrier, Lock
from typing import Callable


@dataclass
class CounterStore:
    counts: dict[tuple[str, ...], int] = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)

    def increment(self, key: tuple[str, ...]) -> int:
        with self.lock:
            value = self.counts.get(key, 0) + 1
            self.counts[key] = value
            return value


@dataclass
class RateLimiter:
    limit: int
    store: CounterStore

    def allow(self, *identity: str) -> bool:
        return self.store.increment(tuple(identity)) <= self.limit


@dataclass
class LayeredLimiter:
    tenant: RateLimiter
    user: RateLimiter
    source: RateLimiter

    def allow(self, tenant: str, user: str, source: str) -> bool:
        decisions = (
            self.tenant.allow(tenant),
            self.user.allow(user),
            self.source.allow(source),
        )
        return all(decisions)


def invoke_limited(
    limiter: RateLimiter | LayeredLimiter | None,
    identity: tuple[str, ...],
    effect: list[str],
) -> int:
    if limiter is not None and not limiter.allow(*identity):
        return 429
    effect.append("executed")
    return 200


def recovery_response(account_exists: bool, *, uniform: bool) -> str:
    if uniform:
        return "If eligible, recovery instructions will be sent."
    return "sent" if account_exists else "account not found"


@dataclass
class IdempotentWriter:
    results: dict[tuple[str, str], str] = field(default_factory=dict)
    effects: list[str] = field(default_factory=list)
    lock: Lock = field(default_factory=Lock)

    def write(self, tenant: str, key: str, effect: str, *, atomic: bool) -> str:
        scoped_key = (tenant, key)
        if atomic:
            with self.lock:
                return self._write(scoped_key, effect)
        self.effects.append(effect)
        result = f"result-{len(self.effects)}"
        self.results[scoped_key] = result
        return result

    def _write(self, scoped_key: tuple[str, str], effect: str) -> str:
        if scoped_key in self.results:
            return self.results[scoped_key]
        self.effects.append(effect)
        result = f"result-{len(self.effects)}"
        self.results[scoped_key] = result
        return result


@dataclass
class Inventory:
    remaining: int = 1
    lock: Lock = field(default_factory=Lock)

    def claim(self, *, atomic: bool, read_barrier: Barrier | None = None) -> bool:
        if atomic:
            with self.lock:
                if self.remaining < 1:
                    return False
                self.remaining -= 1
                return True
        observed = self.remaining
        if read_barrier is not None:
            read_barrier.wait()
        if observed < 1:
            return False
        self.remaining = observed - 1
        return True


def retry_call(
    operation: Callable[[], None],
    *,
    maximum_attempts: int,
    base_delay_ms: int,
    jitter_ms: Callable[[int], int] | None = None,
) -> tuple[int, list[int]]:
    attempts = 0
    delays: list[int] = []
    while attempts < maximum_attempts:
        attempts += 1
        try:
            operation()
            break
        except TimeoutError:
            if attempts == maximum_attempts:
                break
            jitter = jitter_ms(attempts) if jitter_ms is not None else 0
            delays.append(base_delay_ms * (2 ** (attempts - 1)) + jitter)
    return attempts, delays


@dataclass
class StableQuota:
    limit: int
    stable_identity: bool
    counts: dict[str, int] = field(default_factory=dict)

    def allow(self, *, tenant: str, session: str) -> bool:
        key = tenant if self.stable_identity else session
        count = self.counts.get(key, 0)
        if count >= self.limit:
            return False
        self.counts[key] = count + 1
        return True


def checkout_amount(
    *, catalog_amount: int, client_amount: int, trust_client: bool
) -> tuple[int, int | None]:
    if trust_client:
        return 200, client_amount
    if client_amount != catalog_amount:
        return 422, None
    return 200, catalog_amount


@dataclass(frozen=True)
class JobLimits:
    maximum_requests: int
    maximum_items: int
    maximum_cpu_ms: int
    maximum_memory_bytes: int
    maximum_input_bytes: int
    maximum_output_bytes: int
    maximum_pending_calls: int
    maximum_concurrent_jobs: int
    timeout_ms: int

    def accepts(
        self,
        *,
        requests: int,
        items: int,
        cpu_ms: int,
        memory_bytes: int,
        input_bytes: int,
        output_bytes: int,
        pending_calls: int,
        concurrent_jobs: int,
    ) -> bool:
        return all(
            (
                requests <= self.maximum_requests,
                items <= self.maximum_items,
                cpu_ms <= self.maximum_cpu_ms,
                memory_bytes <= self.maximum_memory_bytes,
                input_bytes <= self.maximum_input_bytes,
                output_bytes <= self.maximum_output_bytes,
                pending_calls <= self.maximum_pending_calls,
                concurrent_jobs <= self.maximum_concurrent_jobs,
            )
        )


@dataclass
class Job:
    child_running: bool = False
    temporary_resources: set[str] = field(default_factory=set)

    def run(
        self,
        *,
        elapsed_ms: int,
        limits: JobLimits,
        propagate_cancellation: bool,
    ) -> str:
        self.child_running = True
        self.temporary_resources.add("temporary-export")
        if elapsed_ms <= limits.timeout_ms:
            self.child_running = False
            self.temporary_resources.clear()
            return "completed"
        if not propagate_cancellation:
            return "timed_out"
        self.child_running = False
        self.temporary_resources.clear()
        return "timed_out"


@dataclass
class BoundedQueue:
    maximum_depth: int
    jobs: list[str] = field(default_factory=list)

    def enqueue(self, job: str) -> str:
        if len(self.jobs) >= self.maximum_depth:
            return "rejected"
        self.jobs.append(job)
        return "accepted"


@dataclass
class ConcurrencyGate:
    maximum_active: int
    active: int = 0
    lock: Lock = field(default_factory=Lock)

    def acquire(self) -> str:
        with self.lock:
            if self.active >= self.maximum_active:
                return "rejected"
            self.active += 1
            return "accepted"

    def release(self) -> None:
        with self.lock:
            if self.active > 0:
                self.active -= 1


def evidence_status(
    *, repository: bool, deployment: bool, runtime: bool, provider: bool
) -> str:
    return (
        "Passed with evidence"
        if all((repository, deployment, runtime, provider))
        else "Not verified"
    )


def release_handoff(
    applicable_controls: list[str],
    statuses: dict[str, str],
    blockers: list[str],
    requested_external_evidence: list[str],
    fixture_execution: dict[str, object],
) -> dict[str, object]:
    expected = set(applicable_controls)
    if len(expected) != len(applicable_controls) or set(statuses) != expected:
        raise ValueError("control statuses must exactly cover applicable controls")
    valid_statuses = {
        "Do not ship",
        "Fix before launch",
        "Recommended hardening",
        "Passed with evidence",
        "Not verified",
    }
    if any(status not in valid_statuses for status in statuses.values()):
        raise ValueError("control status is invalid")
    return {
        "verdict_owner": "secod-ship-check",
        "readiness_verdict": "not_issued",
        "control_statuses": statuses,
        "blockers": blockers,
        "requested_external_evidence": requested_external_evidence,
        "fixture_execution": fixture_execution,
    }
