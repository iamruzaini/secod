"""Local model of Firebase Rules, Storage, and Admin SDK boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    uid: str | None
    tenant_id: str | None
    roles: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant_id: str
    owner_id: str
    value: str


@dataclass(frozen=True)
class Upload:
    content_type: str
    content: bytes


def insecure_firestore_read(request: Request, document: Document) -> bool:
    """Insecure rule: any signed-in user can read every document."""
    return request.uid is not None


def secure_firestore_read(request: Request, document: Document) -> bool:
    if request.uid is None or request.tenant_id != document.tenant_id:
        return False
    return request.uid == document.owner_id or "tenant-admin" in request.roles


def insecure_storage_write(request: Request, path: str, upload: Upload) -> bool:
    """Insecure rule: authentication alone grants arbitrary storage writes."""
    return request.uid is not None


def secure_storage_write(
    request: Request,
    path: str,
    upload: Upload,
    *,
    maximum_bytes: int = 1024,
) -> bool:
    if request.uid is None or not request.tenant_id:
        return False
    expected_prefix = f"tenants/{request.tenant_id}/users/{request.uid}/"
    if not path.startswith(expected_prefix) or ".." in path:
        return False
    if len(upload.content) > maximum_bytes:
        return False
    if upload.content_type == "image/png":
        return upload.content.startswith(b"\x89PNG\r\n\x1a\n")
    return upload.content_type == "text/plain" and not upload.content.startswith((b"MZ", b"#!"))


def insecure_admin_sdk_call(execution_boundary: str) -> bool:
    """Insecure boundary: privileged Admin SDK works from client code."""
    return execution_boundary in {"client", "server"}


def secure_admin_sdk_call(execution_boundary: str) -> bool:
    return execution_boundary == "server"


def insecure_client_config(credentials: dict[str, str]) -> dict[str, str]:
    return dict(credentials)


def secure_client_config(credentials: dict[str, str]) -> dict[str, str]:
    return {
        key: value
        for key, value in credentials.items()
        if key in {"FIREBASE_API_KEY", "FIREBASE_PROJECT_ID"}
    }
