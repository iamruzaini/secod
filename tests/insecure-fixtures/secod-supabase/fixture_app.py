"""Local model of Supabase RLS, Storage, and service-role boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    user_id: str | None
    tenant_id: str | None
    authenticated: bool = True


@dataclass(frozen=True)
class Row:
    row_id: str
    tenant_id: str
    owner_id: str
    value: str


@dataclass(frozen=True)
class StorageObject:
    path: str
    tenant_id: str
    owner_id: str
    content: bytes
    private: bool


def insecure_select(rows: list[Row]) -> list[Row]:
    """Insecure table access: no RLS predicate is applied."""
    return list(rows)


def secure_select(session: Session, rows: list[Row]) -> list[Row]:
    if not session.authenticated or session.user_id is None or session.tenant_id is None:
        return []
    return [
        row
        for row in rows
        if row.tenant_id == session.tenant_id and row.owner_id == session.user_id
    ]


def insecure_browser_config(credentials: dict[str, str]) -> dict[str, str]:
    """Insecure build: exposes elevated service-role credential."""
    return dict(credentials)


def secure_browser_config(credentials: dict[str, str]) -> dict[str, str]:
    return {
        key: value
        for key, value in credentials.items()
        if key in {"SUPABASE_URL", "SUPABASE_ANON_KEY"}
    }


def insecure_storage_read(session: Session | None, stored: StorageObject) -> tuple[int, bytes | None]:
    return 200, stored.content


def secure_storage_read(session: Session | None, stored: StorageObject) -> tuple[int, bytes | None]:
    if stored.private:
        if session is None or not session.authenticated:
            return 401, None
        if session.tenant_id != stored.tenant_id or session.user_id != stored.owner_id:
            return 404, None
    return 200, stored.content


def unsafe_update_owner(row: Row, requested_owner: str) -> Row:
    """Insecure update: caller can rewrite ownership."""
    return Row(row.row_id, row.tenant_id, requested_owner, row.value)


def secure_update_value(session: Session, row: Row, value: str) -> tuple[int, Row | None]:
    if not session.authenticated or session.user_id != row.owner_id or session.tenant_id != row.tenant_id:
        return 403, None
    return 200, Row(row.row_id, row.tenant_id, row.owner_id, value)
