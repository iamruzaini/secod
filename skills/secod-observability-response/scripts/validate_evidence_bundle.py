"""Validate observability-response evidence bundle structure without asserting control passage."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any


REQUIRED_KINDS: dict[str, set[str]] = {
    "SECOD-OBS-01": {"production_sink", "emitted_security_event"},
    "SECOD-OBS-02": {"redaction_marker_test", "retention_access_decision"},
    "SECOD-OBS-03": {"revoked_key_replay", "key_lifecycle_events"},
    "SECOD-OBS-04": {"alert_definition", "alert_delivery"},
    "SECOD-OBS-05": {"runbook", "runbook_exercise"},
    "SECOD-OBS-06": {"evidence_store_controls", "exercised_export"},
    "SECOD-OBS-07": {"restore_drill", "partial_operation_recovery"},
}
KNOWN_KINDS = set().union(*REQUIRED_KINDS.values())
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
REQUIRED_FIELDS = {
    "id",
    "kind",
    "control_ids",
    "environment",
    "deployment_id",
    "source",
    "captured_at",
    "path",
    "sha256",
    "redacted",
    "authorized",
}


def _inside(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def _timestamp_has_timezone(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_bundle(manifest_path: Path) -> dict[str, Any]:
    errors: list[str] = []
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
                errors.append(f"unknown applicable control: {control_id}")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("artifacts must be a list")
        artifacts = []

    bundle_root = manifest_path.resolve().parent
    seen_ids: set[str] = set()
    supplied: dict[str, set[str]] = {control_id: set() for control_id in applicable_controls}

    for index, artifact in enumerate(artifacts):
        prefix = f"artifacts[{index}]"
        artifact_errors: list[str] = []
        if not isinstance(artifact, dict):
            errors.append(prefix + " must be an object")
            continue

        missing_fields = sorted(REQUIRED_FIELDS - artifact.keys())
        if missing_fields:
            artifact_errors.append(prefix + " missing fields: " + ", ".join(missing_fields))

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

        for field in ("environment", "deployment_id", "source"):
            value = artifact.get(field)
            if not isinstance(value, str) or not value.strip():
                artifact_errors.append(prefix + f".{field} must be a non-empty string")

        if kind == "production_sink" and artifact.get("environment") != "production":
            artifact_errors.append(prefix + ".production_sink must identify environment production")
        if not _timestamp_has_timezone(artifact.get("captured_at")):
            artifact_errors.append(prefix + ".captured_at must be an ISO-8601 timestamp with timezone")
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

        errors.extend(artifact_errors)
        if not artifact_errors and isinstance(kind, str):
            for control_id in control_ids:
                supplied.setdefault(control_id, set()).add(kind)

    controls: dict[str, dict[str, Any]] = {}
    for control_id in applicable_controls:
        if control_id not in REQUIRED_KINDS:
            continue
        missing_kinds = sorted(REQUIRED_KINDS[control_id] - supplied.get(control_id, set()))
        controls[control_id] = {
            "intake_status": "Bundle complete" if not missing_kinds else "Not verified",
            "missing_artifact_kinds": missing_kinds,
        }
        if missing_kinds:
            errors.append(control_id + " missing artifact kinds: " + ", ".join(missing_kinds))

    return {
        "bundle": str(manifest_path),
        "valid": not errors,
        "errors": errors,
        "controls": controls,
        "limitation": "Structural completeness only; inspect artifact contents before control status.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    result = validate_bundle(args.manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
