"""Deterministic secure and unsafe behaviors for failure-safety fixture tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class DependencyFailure(RuntimeError):
    pass


def secure_error_response(_: Exception) -> dict[str, str]:
    return {"error": "Internal error", "correlation_id": "fixture-correlation-id"}


def unsafe_error_response(error: Exception) -> dict[str, str]:
    return {"error": repr(error), "stack": "db.internal:5432/query"}


def authorize(identity_provider: Callable[[], bool], *, fail_closed: bool) -> bool:
    try:
        return identity_provider()
    except DependencyFailure:
        return False if fail_closed else True


@dataclass
class MutationStore:
    order: bool = False
    entitlement: bool = False

    def mutate(self, *, transactional: bool, interrupt: bool) -> None:
        before = (self.order, self.entitlement)
        try:
            self.order = True
            if interrupt:
                raise DependencyFailure("provider unavailable")
            self.entitlement = True
        except DependencyFailure:
            if transactional:
                self.order, self.entitlement = before
            raise


def blind_retry(operation: Callable[[], None], attempts: int = 2) -> None:
    for attempt in range(attempts):
        try:
            operation()
            return
        except DependencyFailure:
            if attempt + 1 == attempts:
                raise


class CircuitBreaker:
    def __init__(self, threshold: int = 2) -> None:
        self.threshold = threshold
        self.failures = 0
        self.open = False

    def call(self, dependency: Callable[[], None]) -> None:
        if self.open:
            raise DependencyFailure("breaker open")
        try:
            dependency()
        except DependencyFailure:
            self.failures += 1
            self.open = self.failures >= self.threshold
            raise


class ResourceTracker:
    def __init__(self) -> None:
        self.held: set[str] = set()

    def interrupted_flow(self, *, deterministic_cleanup: bool) -> None:
        self.held.add("temporary-object")
        try:
            raise DependencyFailure("cancelled")
        finally:
            if deterministic_cleanup:
                self.held.discard("temporary-object")


class DegradedCache:
    def __init__(self, *, tenant_scoped: bool) -> None:
        self.tenant_scoped = tenant_scoped
        self.values: dict[object, str] = {}

    def put(self, tenant: str, key: str, value: str) -> None:
        cache_key: object = (tenant, key) if self.tenant_scoped else key
        self.values[cache_key] = value

    def get(self, tenant: str, key: str) -> str | None:
        cache_key: object = (tenant, key) if self.tenant_scoped else key
        return self.values.get(cache_key)


def evidence_status(repository: bool, runtime: bool, deployment: bool) -> str:
    return "Passed with evidence" if all((repository, runtime, deployment)) else "Not verified"
