"""Deterministic, secret-free behaviors for secrets-config fixture tests."""

from __future__ import annotations

import re
from typing import Iterable, Mapping


FAKE_KEY = "fixture_key_0123456789abcdef0123456789abcdef"
FAKE_KEY_PATTERN = re.compile(r"fixture_key_[A-Za-z0-9]{20,}")


def finding(control: int, status: str, path: str, reason: str) -> dict[str, object]:
    return {
        "control_id": f"PROVISIONAL-secrets-config-{control}",
        "status": status,
        "evidence": {"path": path, "match": "[REDACTED]", "reason": reason},
    }


def scan_surfaces(files: Mapping[str, str]) -> list[dict[str, object]]:
    findings = []
    for path, content in files.items():
        if FAKE_KEY_PATTERN.search(content):
            findings.append(finding(1, "Do not ship", path, "credential-like literal"))
        if re.search(r"logger\.(?:info|debug|error)\([^)]*SECRET_VALUE", content):
            findings.append(finding(1, "Do not ship", path, "credential interpolated into log"))
    return findings


def check_bearer_flow(
    response_fields: Iterable[str], rpc_arguments: Iterable[str]
) -> list[dict[str, object]]:
    findings = []
    if {"session_token", "share_verifier"} & set(response_fields):
        findings.append(finding(2, "Do not ship", "fixture/response.json", "bearer in response"))
    if {"tenant_capability", "provider_token"} & set(rpc_arguments):
        findings.append(
            finding(2, "Do not ship", "fixture/rpc.schema", "client-supplied capability")
        )
    return findings


def check_scope(role: str, operations: Iterable[str]) -> list[dict[str, object]]:
    routine_operations = {"read_invoice", "list_orders"}
    if role in {"superuser", "admin", "service_role"} and set(operations) <= routine_operations:
        return [finding(3, "Fix before launch", "fixture/runtime.config", "overprivileged role")]
    return []


def check_template(
    referenced_names: Iterable[str], template: Mapping[str, str]
) -> list[dict[str, object]]:
    findings = []
    for name, value in template.items():
        if FAKE_KEY_PATTERN.search(value):
            findings.append(
                finding(4, "Do not ship", ".env.example", f"live-format value for {name}")
            )
    missing = sorted(set(referenced_names) - set(template))
    if missing:
        findings.append(
            finding(
                4,
                "Fix before launch",
                ".env.example",
                "missing names: " + ", ".join(missing),
            )
        )
    return findings


def check_storage(
    variable_names: Iterable[str], compose_password: str | None
) -> list[dict[str, object]]:
    findings = []
    public_secret = any(
        name.startswith(("NEXT_PUBLIC_", "VITE_"))
        and name.endswith(("SECRET", "TOKEN", "KEY"))
        for name in variable_names
    )
    if public_secret:
        findings.append(
            finding(5, "Do not ship", "fixture/client.env", "secret-class name exposed to client")
        )
    if compose_password is not None:
        findings.append(finding(5, "Do not ship", "fixture/compose.yaml", "literal password"))
    return findings


def check_environment_separation(
    staging_host: str, key_modes: Iterable[str]
) -> list[dict[str, object]]:
    findings = []
    if staging_host == "production-db.fixture.invalid":
        findings.append(
            finding(6, "Do not ship", "fixture/staging.env", "staging targets production host")
        )
    if {"test", "live"} <= set(key_modes):
        findings.append(finding(6, "Do not ship", "fixture/provider.env", "mixed test/live identities"))
    return findings


def check_rotation(
    has_owner: bool, has_revocation_path: bool, has_current_evidence: bool
) -> dict[str, object]:
    if not has_revocation_path:
        return finding(7, "Fix before launch", "fixture/rotation-record.json", "no revocation path")
    if not has_owner or not has_current_evidence:
        return finding(
            7,
            "Not verified",
            "fixture/rotation-record.json",
            "required evidence unavailable",
        )
    return finding(7, "Passed with evidence", "fixture/rotation-record.json", "complete current record")


def check_production_flags(
    bypass_default: bool, debug_enabled: bool
) -> list[dict[str, object]]:
    findings = []
    if bypass_default:
        findings.append(
            finding(8, "Do not ship", "fixture/auth.config", "bypass is fail-open when unset")
        )
    if debug_enabled:
        findings.append(finding(8, "Fix before launch", "fixture/production.env", "debug enabled in production"))
    return findings


def check_history_response(events: Iterable[str]) -> dict[str, object]:
    ordered = list(events)
    if "revoke" not in ordered:
        return finding(9, "Do not ship", "fixture/history-plan.json", "credential not revoked")
    if "rewrite" in ordered and ordered.index("rewrite") < ordered.index("revoke"):
        return finding(
            9,
            "Do not ship",
            "fixture/history-plan.json",
            "rewrite precedes revocation",
        )
    return finding(9, "Passed with evidence", "fixture/history-plan.json", "revoke-first order")


def check_default_credentials(
    seed_uses_default: bool, probe_authorized: bool
) -> dict[str, object]:
    if seed_uses_default:
        return finding(10, "Fix before launch", "fixture/seed.sql", "known default credential")
    if not probe_authorized:
        result = finding(
            10,
            "Not verified",
            "fixture/deployment.json",
            "deployed probe not authorized",
        )
        result["probe_performed"] = False
        return result
    return finding(10, "Passed with evidence", "fixture/deployment.json", "authorized evidence supplied")
