"""Local model of tenant and server-side authorization boundaries."""

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


def unsafe_read_record(
    records: dict[tuple[str, str], Record],
    *,
    requested_tenant: str,
    requested_record: str,
) -> tuple[int, str | None]:
    """Insecure endpoint: trusts tenant selection supplied by the caller."""
    record = records.get((requested_tenant, requested_record))
    return (200, record.value) if record else (404, None)


def unsafe_authorize_role(*, requested_role: str, required_role: str) -> bool:
    """Insecure endpoint: trusts a client-controlled role claim."""
    return requested_role == required_role


def secure_read_record(
    records: dict[tuple[str, str], Record],
    session: Session,
    *,
    record_id: str,
) -> tuple[int, str | None]:
    """Authorize from verified session identity and server-loaded record data."""
    if not session.authenticated:
        return 401, None

    record = records.get((session.tenant_id, record_id))
    if record is None:
        return 404, None
    if record.owner_id != session.user_id and "tenant-admin" not in session.roles:
        return 403, None
    return 200, record.value


def secure_authorize_role(session: Session, *, required_role: str) -> bool:
    """Use server-verified role membership, never request-body role data."""
    return session.authenticated and required_role in session.roles
