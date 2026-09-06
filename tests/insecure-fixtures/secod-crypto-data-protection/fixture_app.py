"""Small secure cryptography patterns used by executable fixtures."""

from __future__ import annotations

import hashlib
import hmac
import os


def hash_password(password: str, *, salt: bytes | None = None) -> tuple[bytes, bytes]:
    actual_salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), actual_salt, 600_000)
    return actual_salt, digest


def verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return hmac.compare_digest(actual, expected)


def public_response(secret: str) -> dict[str, str]:
    _ = secret
    return {"status": "configured"}


def validate_key_source(source: str) -> bool:
    return source in {"workload-identity", "secret-manager"}
