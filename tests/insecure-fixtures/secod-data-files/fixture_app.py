"""Local model for safe uploads and private object authorization."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class Session:
    user_id: str
    tenant_id: str


@dataclass(frozen=True)
class Upload:
    filename: str
    declared_type: str
    content: bytes


@dataclass(frozen=True)
class StoredObject:
    object_id: str
    tenant_id: str
    owner_id: str
    content_type: str
    content: bytes
    public: bool


def unsafe_upload(upload: Upload, objects: dict[str, StoredObject]) -> str:
    """Insecure boundary: trusts filename/type and publishes object."""
    object_id = upload.filename
    objects[object_id] = StoredObject(
        object_id,
        "unknown",
        "unknown",
        upload.declared_type,
        upload.content,
        True,
    )
    return object_id


def _content_matches_type(upload: Upload) -> bool:
    if upload.declared_type == "image/png":
        return upload.content.startswith(b"\x89PNG\r\n\x1a\n")
    if upload.declared_type == "text/plain":
        return not upload.content.startswith((b"MZ", b"\x7fELF", b"#!"))
    return False


def secure_upload(
    session: Session,
    upload: Upload,
    objects: dict[str, StoredObject],
    *,
    maximum_bytes: int = 1024,
) -> tuple[int, str | None]:
    if not upload.content or len(upload.content) > maximum_bytes:
        return 413, None
    if not _content_matches_type(upload):
        return 415, None
    digest = hashlib.sha256(
        session.tenant_id.encode() + b":" + session.user_id.encode() + b":" + upload.content
    ).hexdigest()
    object_id = f"{session.tenant_id}/{digest}"
    objects[object_id] = StoredObject(
        object_id,
        session.tenant_id,
        session.user_id,
        upload.declared_type,
        upload.content,
        False,
    )
    return 201, object_id


def read_object(
    session: Session | None,
    object_id: str,
    objects: dict[str, StoredObject],
) -> tuple[int, bytes | None]:
    stored = objects.get(object_id)
    if stored is None:
        return 404, None
    if stored.public:
        return 200, stored.content
    if session is None or stored.tenant_id != session.tenant_id:
        return 404, None
    if stored.owner_id != session.user_id:
        return 403, None
    return 200, stored.content
