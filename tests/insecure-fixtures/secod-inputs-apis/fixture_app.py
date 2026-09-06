"""Local models for SSRF, webhook, schema, and command-input boundaries."""

from __future__ import annotations

from dataclasses import dataclass
import hmac
import hashlib
import ipaddress
import json
from urllib.parse import urlparse


def unsafe_fetch(url: str, requester) -> str:
    """Insecure boundary: forwards caller URL without policy checks."""
    return requester(url)


def safe_fetch(
    url: str,
    requester,
    *,
    allowed_hosts: set[str],
    resolved_ips: list[str],
) -> tuple[int, str | None]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        return 400, None
    host = (parsed.hostname or "").lower().rstrip(".")
    if not host or host not in allowed_hosts:
        return 403, None
    try:
        addresses = [ipaddress.ip_address(value) for value in resolved_ips]
    except ValueError:
        return 400, None
    if not addresses or any(
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_multicast
        or address.is_unspecified
        for address in addresses
    ):
        return 403, None
    return 200, requester(url)


def unsafe_webhook_event(parsed_payload: dict[str, object], signature: str) -> dict[str, object] | None:
    """Insecure boundary: trusts parsed fields before authenticating raw bytes."""
    return parsed_payload if signature else None


def verify_webhook(raw_body: bytes, signature: str, secret: bytes) -> dict[str, object] | None:
    expected = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return None
    try:
        event = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return event if isinstance(event, dict) and isinstance(event.get("id"), str) else None


def unsafe_command(host: str, executor) -> list[str]:
    """Insecure boundary: constructs a shell command from raw input."""
    return executor(f"ping {host}")


def safe_command(host: str, executor) -> list[str] | None:
    if not host or any(character in host for character in ";|&$`\n\r"):
        return None
    if len(host) > 253 or any(not label or len(label) > 63 for label in host.split(".")):
        return None
    if any(not all(character.isalnum() or character == "-" for character in label) for label in host.split(".")):
        return None
    return executor(["ping", "--", host])


@dataclass(frozen=True)
class WebhookRequest:
    raw_body: bytes
    signature: str


def validate_payload(payload: object) -> tuple[int, dict[str, object] | None]:
    if not isinstance(payload, dict):
        return 422, None
    if not isinstance(payload.get("id"), str) or not payload["id"]:
        return 422, None
    if not isinstance(payload.get("amount"), int) or payload["amount"] < 0:
        return 422, None
    return 200, payload
