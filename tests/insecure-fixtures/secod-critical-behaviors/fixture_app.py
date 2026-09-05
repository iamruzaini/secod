"""Deterministic insecure and guarded behaviors for cross-skill fixtures."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import hmac
import ipaddress
import re
from urllib.parse import urlparse


@dataclass(frozen=True)
class TenantRecord:
    tenant_id: str
    record_id: str
    value: str


@dataclass
class TenantStore:
    records: dict[str, TenantRecord] = field(
        default_factory=lambda: {
            "invoice-a": TenantRecord("tenant-a", "invoice-a", "tenant-a invoice"),
            "invoice-b": TenantRecord("tenant-b", "invoice-b", "tenant-b invoice"),
        }
    )

    def insecure_read(self, authenticated_tenant: str, requested_tenant: str, record_id: str) -> str | None:
        del authenticated_tenant
        record = self.records.get(record_id)
        return record.value if record and record.tenant_id == requested_tenant else None

    def secure_read(self, authenticated_tenant: str, requested_tenant: str, record_id: str) -> str | None:
        record = self.records.get(record_id)
        if not record or requested_tenant != authenticated_tenant:
            return None
        return record.value if record.tenant_id == authenticated_tenant else None


def insecure_server_authorization(authenticated_role: str, requested_role: str) -> bool:
    del authenticated_role
    return requested_role in {"owner", "admin"}


def secure_server_authorization(authenticated_role: str, requested_role: str) -> bool:
    return authenticated_role in {"owner", "admin"} and requested_role == authenticated_role


def insecure_client_payload(secret: str) -> dict[str, str]:
    return {"api_key": secret, "theme": "dark"}


def secure_client_payload(secret: str) -> dict[str, str | None]:
    del secret
    return {"api_key": None, "theme": "dark"}


def sign_webhook(secret: bytes, raw_body: bytes) -> str:
    return hmac.new(secret, raw_body, hashlib.sha256).hexdigest()


def insecure_verify_webhook(raw_body: bytes, signature: str) -> bool:
    del raw_body, signature
    return True


def secure_verify_webhook(secret: bytes, raw_body: bytes, signature: str) -> bool:
    return hmac.compare_digest(sign_webhook(secret, raw_body), signature)


@dataclass
class PaymentLedger:
    entitlements: list[str] = field(default_factory=list)
    seen_events: set[str] = field(default_factory=set)

    def insecure_apply(self, event_id: str, user_id: str) -> None:
        del event_id
        self.entitlements.append(user_id)

    def secure_apply(self, event_id: str, user_id: str) -> None:
        if event_id in self.seen_events:
            return
        self.seen_events.add(event_id)
        self.entitlements.append(user_id)


def insecure_upload(filename: str, contents: bytes) -> bool:
    del filename, contents
    return True


def secure_upload(filename: str, contents: bytes, *, maximum_bytes: int = 1024) -> bool:
    if len(contents) > maximum_bytes:
        return False
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    signatures = {
        "png": b"\x89PNG\r\n\x1a\n",
        "jpg": b"\xff\xd8\xff",
        "jpeg": b"\xff\xd8\xff",
    }
    return extension in signatures and contents.startswith(signatures[extension])


@dataclass(frozen=True)
class StorageObject:
    key: str
    visibility: str


def insecure_storage_object(key: str) -> StorageObject:
    return StorageObject(key, "public")


def secure_storage_object(key: str) -> StorageObject:
    return StorageObject(key, "private")


def insecure_command(filename: str) -> str:
    return f"convert {filename} /tmp/output.png"


def secure_command(filename: str) -> tuple[str, str, str] | None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}", filename):
        return None
    return ("convert", filename, "/tmp/output.png")


def insecure_fetch_allowed(url: str) -> bool:
    del url
    return True


def secure_fetch_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower().rstrip(".")
    if hostname in {"localhost", "metadata.google.internal"}:
        return False
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return hostname == "api.example.test"
    return not (address.is_private or address.is_loopback or address.is_link_local or address.is_reserved)


@dataclass
class UnboundedEndpoint:
    requests: int = 0

    def request(self) -> bool:
        self.requests += 1
        return True


@dataclass
class BoundedEndpoint:
    limit: int = 2
    requests_by_user: dict[str, int] = field(default_factory=dict)

    def request(self, user_id: str) -> bool:
        count = self.requests_by_user.get(user_id, 0)
        if count >= self.limit:
            return False
        self.requests_by_user[user_id] = count + 1
        return True


def insecure_retry(maximum_attempts: int) -> int:
    return maximum_attempts


def secure_retry(maximum_attempts: int, *, policy_limit: int = 3) -> int:
    return min(maximum_attempts, policy_limit)


def insecure_log(token: str) -> str:
    return f"authorization={token}"


def secure_log(token: str) -> str:
    del token
    return "authorization=[REDACTED]"


def insecure_ai_tool_call(tool_name: str, arguments: dict[str, str]) -> dict[str, object]:
    return {"executed": tool_name, "arguments": arguments}


def secure_ai_tool_call(
    tool_name: str,
    arguments: dict[str, str],
    *,
    allowed_tools: set[str],
    user_confirmed: bool,
) -> dict[str, object]:
    if tool_name not in allowed_tools or not user_confirmed:
        return {"executed": None, "reason": "denied"}
    return {"executed": tool_name, "arguments": arguments}


@dataclass(frozen=True)
class VectorDocument:
    tenant_id: str
    document_id: str
    text: str


VECTOR_DOCUMENTS = (
    VectorDocument("tenant-a", "doc-a", "shared product design"),
    VectorDocument("tenant-b", "doc-b", "shared product design"),
)


def insecure_vector_search(query: str) -> list[VectorDocument]:
    del query
    return list(VECTOR_DOCUMENTS)


def secure_vector_search(query: str, tenant_id: str) -> list[VectorDocument]:
    del query
    return [document for document in VECTOR_DOCUMENTS if document.tenant_id == tenant_id]
