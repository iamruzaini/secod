"""Local model of Next.js server/client and Server Action boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    user_id: str
    tenant_id: str
    roles: frozenset[str]
    authenticated: bool = True


@dataclass(frozen=True)
class Record:
    record_id: str
    tenant_id: str
    owner_id: str
    value: str


def unsafe_server_action(
    records: dict[tuple[str, str], Record],
    request: dict[str, str],
) -> tuple[int, str | None]:
    """Insecure action: trusts hidden-form identity and role fields."""
    record = records.get((request.get("tenant_id", ""), request.get("record_id", "")))
    if record is None or request.get("role") not in {"member", "tenant-admin"}:
        return 404, None
    return 200, record.value


def secure_server_action(
    records: dict[tuple[str, str], Record],
    session: Session,
    *,
    record_id: str,
    cache: dict[str, str],
) -> tuple[int, str | None]:
    """Authorize inside the server action from verified session state."""
    if not session.authenticated:
        return 401, None
    record = records.get((session.tenant_id, record_id))
    if record is None:
        return 404, None
    if record.owner_id != session.user_id and "tenant-admin" not in session.roles:
        return 403, None
    cache[secure_cache_key(session, record_id)] = record.value
    return 200, record.value


def unsafe_client_config(environment: dict[str, str]) -> dict[str, str]:
    """Insecure build: sends server credentials to browser code."""
    return dict(environment)


def secure_client_config(environment: dict[str, str]) -> dict[str, str]:
    """Only explicitly public configuration crosses client boundary."""
    return {
        name: value
        for name, value in environment.items()
        if name.startswith("NEXT_PUBLIC_")
    }


def unsafe_cache_key(record_id: str) -> str:
    """Insecure cache: unrelated tenants share one key."""
    return f"record:{record_id}"


def secure_cache_key(session: Session, record_id: str) -> str:
    return f"record:{session.tenant_id}:{session.user_id}:{record_id}"
