"""Validate crypto-data-protection evidence intake without asserting control passage."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any


REQUIRED_KINDS: dict[str, set[str]] = {
    "SECOD-CDP-01": {"deployed_tls_posture"},
    "SECOD-CDP-04": {"managed_service_encryption_at_rest"},
    "SECOD-CDP-08": {"provider_deletion_outcome"},
    "SECOD-CDP-09": {"backup_encryption_at_rest", "restore_test_result"},
}
KNOWN_KINDS = set().union(*REQUIRED_KINDS.values())
SCOPE_FIELDS = {
    "SECOD-CDP-01": "expected_tls_endpoints",
    "SECOD-CDP-04": "expected_managed_resource_ids",
    "SECOD-CDP-08": "expected_deletion_store_ids",
    "SECOD-CDP-09": "expected_backup_ids",
}
REQUIRED_FIELDS = {
    "id",
    "kind",
    "control_ids",
    "environment",
    "deployment_id",
    "source",
    "captured_at",
    "valid_until",
    "path",
    "sha256",
    "redacted",
    "authorized",
}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


def _inside(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _non_empty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
        and len(value) == len(set(value))
    )


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _kind_fields(prefix: str, artifact: dict[str, Any], errors: list[str]) -> None:
    kind = artifact.get("kind")
    if kind == "deployed_tls_posture":
        if not _non_empty_strings(artifact.get("endpoints")):
            errors.append(prefix + ".endpoints must be a non-empty unique string list")
        if artifact.get("minimum_protocol") not in {"TLSv1.2", "TLSv1.3"}:
            errors.append(prefix + ".minimum_protocol must be TLSv1.2 or TLSv1.3")
        if artifact.get("certificate_validation") is not True:
            errors.append(prefix + ".certificate_validation must be true")
    elif kind == "managed_service_encryption_at_rest":
        if not _non_empty_strings(artifact.get("resource_ids")):
            errors.append(prefix + ".resource_ids must be a non-empty unique string list")
        if artifact.get("encryption_at_rest") is not True:
            errors.append(prefix + ".encryption_at_rest must be true")
        if artifact.get("key_management") not in {"provider_managed", "customer_managed"}:
            errors.append(
                prefix + ".key_management must be provider_managed or customer_managed"
            )
    elif kind == "provider_deletion_outcome":
        if not _non_empty_strings(artifact.get("store_ids")):
            errors.append(prefix + ".store_ids must be a non-empty unique string list")
        if not isinstance(artifact.get("deletion_event_id"), str) or not artifact[
            "deletion_event_id"
        ].strip():
            errors.append(prefix + ".deletion_event_id must be a non-empty string")
        if artifact.get("outcome") not in {"confirmed_deleted", "policy_bounded"}:
            errors.append(prefix + ".outcome must be confirmed_deleted or policy_bounded")
        if artifact.get("outcome") == "policy_bounded":
            residual_until = _timestamp(artifact.get("residual_until"))
            captured_at = _timestamp(artifact.get("captured_at"))
            if residual_until is None:
                errors.append(prefix + ".residual_until must bound policy_bounded residuals")
            elif captured_at is not None and residual_until <= captured_at:
                errors.append(prefix + ".residual_until must be later than captured_at")
    elif kind == "backup_encryption_at_rest":
        if not _non_empty_strings(artifact.get("backup_ids")):
            errors.append(prefix + ".backup_ids must be a non-empty unique string list")
        if artifact.get("encrypted") is not True:
            errors.append(prefix + ".encrypted must be true")
        if artifact.get("key_separated_from_primary") is not True:
            errors.append(prefix + ".key_separated_from_primary must be true")
    elif kind == "restore_test_result":
        tested_at = _timestamp(artifact.get("restore_tested_at"))
        captured_at = _timestamp(artifact.get("captured_at"))
        valid_until = _timestamp(artifact.get("valid_until"))
        if tested_at is None:
            errors.append(prefix + ".restore_tested_at must include an ISO-8601 timezone")
        elif captured_at is not None and tested_at > captured_at:
            errors.append(prefix + ".restore_tested_at cannot be after captured_at")
        max_age = artifact.get("policy_max_age_days")
        if not isinstance(max_age, int) or isinstance(max_age, bool) or max_age <= 0:
            errors.append(prefix + ".policy_max_age_days must be a positive integer")
        elif tested_at is not None and valid_until is not None:
            if valid_until > tested_at + timedelta(days=max_age):
                errors.append(prefix + ".valid_until exceeds restore-test policy age")
        if not isinstance(artifact.get("restored_backup_id"), str) or not artifact[
            "restored_backup_id"
        ].strip():
            errors.append(prefix + ".restored_backup_id must be a non-empty string")
        for field in ("successful", "integrity_verified", "deletion_policy_reapplied"):
            if artifact.get(field) is not True:
                errors.append(prefix + f".{field} must be true")


def validate_bundle(
    manifest_path: Path, as_of: datetime | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    review_time = as_of or datetime.now(timezone.utc)
    if review_time.tzinfo is None or review_time.utcoffset() is None:
        raise ValueError("as_of must include a timezone")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {
            "bundle": str(manifest_path),
            "valid": False,
            "errors": [f"manifest unreadable: {error}"],
            "controls": {},
        }
    if not isinstance(manifest, dict):
        return {
            "bundle": str(manifest_path),
            "valid": False,
            "errors": ["manifest root must be an object"],
            "controls": {},
        }
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must equal 1")

    applicable = manifest.get("applicable_controls")
    if not isinstance(applicable, list) or not applicable:
        errors.append("applicable_controls must be a non-empty list")
        applicable_controls: list[str] = []
    else:
        applicable_controls = [value for value in applicable if isinstance(value, str)]
        if len(applicable_controls) != len(applicable):
            errors.append("applicable_controls values must be strings")
        if len(applicable_controls) != len(set(applicable_controls)):
            errors.append("applicable_controls contains duplicates")
        for control_id in applicable_controls:
            if control_id not in REQUIRED_KINDS:
                errors.append(f"control has no external evidence contract: {control_id}")

    expected_scope: dict[str, set[str]] = {}
    for control_id in applicable_controls:
        field = SCOPE_FIELDS.get(control_id)
        if field is None:
            continue
        values = manifest.get(field)
        if not _non_empty_strings(values):
            errors.append(field + " must be a non-empty unique string list")
            expected_scope[control_id] = set()
        else:
            expected_scope[control_id] = set(values)

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("artifacts must be a list")
        artifacts = []

    bundle_root = manifest_path.resolve().parent
    seen_ids: set[str] = set()
    supplied: dict[str, set[str]] = {control_id: set() for control_id in applicable_controls}
    observed_scope: dict[str, set[str]] = {control_id: set() for control_id in applicable_controls}

    for index, artifact in enumerate(artifacts):
        prefix = f"artifacts[{index}]"
        artifact_errors: list[str] = []
        if not isinstance(artifact, dict):
            errors.append(prefix + " must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - artifact.keys())
        if missing:
            artifact_errors.append(prefix + " missing fields: " + ", ".join(missing))

        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            artifact_errors.append(prefix + ".id must be a non-empty string")
        elif artifact_id in seen_ids:
            artifact_errors.append(prefix + f" duplicates artifact id {artifact_id}")
        else:
            seen_ids.add(artifact_id)

        kind = artifact.get("kind")
        if kind not in KNOWN_KINDS:
            artifact_errors.append(prefix + f" has unknown kind {kind!r}")

        control_ids = artifact.get("control_ids")
        if not isinstance(control_ids, list) or not control_ids:
            artifact_errors.append(prefix + ".control_ids must be a non-empty list")
            control_ids = []
        else:
            for control_id in control_ids:
                if control_id not in applicable_controls:
                    artifact_errors.append(
                        prefix + f" references undeclared or unknown control {control_id!r}"
                    )
                elif kind not in REQUIRED_KINDS.get(control_id, set()):
                    artifact_errors.append(
                        prefix + f" kind {kind!r} is not evidence for {control_id}"
                    )

        for field in ("environment", "deployment_id", "source"):
            value = artifact.get(field)
            if not isinstance(value, str) or not value.strip():
                artifact_errors.append(prefix + f".{field} must be a non-empty string")

        captured = _timestamp(artifact.get("captured_at"))
        valid_until = _timestamp(artifact.get("valid_until"))
        if captured is None:
            artifact_errors.append(prefix + ".captured_at must include an ISO-8601 timezone")
        if valid_until is None:
            artifact_errors.append(prefix + ".valid_until must include an ISO-8601 timezone")
        if captured is not None and captured > review_time:
            artifact_errors.append(prefix + ".captured_at cannot be after review time")
        if captured is not None and valid_until is not None and valid_until <= captured:
            artifact_errors.append(prefix + ".valid_until must be later than captured_at")
        if valid_until is not None and valid_until <= review_time:
            artifact_errors.append(prefix + ".valid_until is stale at review time")
        if artifact.get("redacted") is not True:
            artifact_errors.append(prefix + ".redacted must be true")
        if artifact.get("authorized") is not True:
            artifact_errors.append(prefix + ".authorized must be true")

        relative_path = artifact.get("path")
        target: Path | None = None
        if not isinstance(relative_path, str) or not relative_path.strip():
            artifact_errors.append(prefix + ".path must be a non-empty relative path")
        else:
            candidate = Path(relative_path)
            target = (bundle_root / candidate).resolve()
            if candidate.is_absolute() or not _inside(bundle_root, target):
                artifact_errors.append(prefix + ".path must stay inside bundle directory")
            elif not target.is_file():
                artifact_errors.append(prefix + f" file is missing: {relative_path}")
            elif target.stat().st_size == 0:
                artifact_errors.append(prefix + f" file is empty: {relative_path}")

        expected_hash = artifact.get("sha256")
        if not isinstance(expected_hash, str) or not SHA256_PATTERN.fullmatch(expected_hash):
            artifact_errors.append(prefix + ".sha256 must be 64 lowercase hexadecimal characters")
        elif target is not None and target.is_file() and target.stat().st_size > 0:
            if _file_hash(target) != expected_hash:
                artifact_errors.append(prefix + f" SHA-256 mismatch for {relative_path}")

        _kind_fields(prefix, artifact, artifact_errors)
        if kind == "restore_test_result" and artifact.get("restored_backup_id") not in (
            expected_scope.get("SECOD-CDP-09", set())
        ):
            artifact_errors.append(prefix + ".restored_backup_id is outside expected_backup_ids")
        errors.extend(artifact_errors)
        if not artifact_errors and isinstance(kind, str):
            for control_id in control_ids:
                supplied.setdefault(control_id, set()).add(kind)
                if kind == "deployed_tls_posture":
                    observed_scope.setdefault(control_id, set()).update(artifact["endpoints"])
                elif kind == "managed_service_encryption_at_rest":
                    observed_scope.setdefault(control_id, set()).update(artifact["resource_ids"])
                elif kind == "provider_deletion_outcome":
                    observed_scope.setdefault(control_id, set()).update(artifact["store_ids"])
                elif kind == "backup_encryption_at_rest":
                    observed_scope.setdefault(control_id, set()).update(artifact["backup_ids"])

    controls: dict[str, dict[str, Any]] = {}
    for control_id in applicable_controls:
        if control_id not in REQUIRED_KINDS:
            continue
        missing_kinds = sorted(REQUIRED_KINDS[control_id] - supplied.get(control_id, set()))
        missing_scope = sorted(
            expected_scope.get(control_id, set()) - observed_scope.get(control_id, set())
        )
        controls[control_id] = {
            "intake_status": (
                "Bundle complete" if not missing_kinds and not missing_scope else "Not verified"
            ),
            "missing_artifact_kinds": missing_kinds,
            "missing_scope_ids": missing_scope,
        }
        if missing_kinds:
            errors.append(control_id + " missing artifact kinds: " + ", ".join(missing_kinds))
        if missing_scope:
            errors.append(control_id + " missing scoped evidence: " + ", ".join(missing_scope))

    return {
        "bundle": str(manifest_path),
        "valid": not errors,
        "errors": errors,
        "controls": controls,
        "reviewed_as_of": review_time.isoformat(),
        "limitation": "Structural completeness only; inspect content before assigning status.",
        "readiness_verdict": "not_issued",
        "verdict_owner": "secod-ship-check",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--as-of", type=str, help="ISO-8601 review time; defaults to now")
    args = parser.parse_args()
    as_of = _timestamp(args.as_of) if args.as_of else None
    if args.as_of and as_of is None:
        parser.error("--as-of must be an ISO-8601 timestamp with timezone")
    result = validate_bundle(args.manifest, as_of=as_of)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
