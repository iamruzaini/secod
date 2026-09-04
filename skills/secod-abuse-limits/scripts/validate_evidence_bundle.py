"""Validate abuse-limits evidence bundle structure without asserting control passage."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any


REQUIRED_KINDS: dict[str, set[str]] = {
    "PROVISIONAL-ABUSE-01": {
        "deployed_limiter_config",
        "shared_store_consistency",
        "burst_test",
    },
    "PROVISIONAL-ABUSE-02": {"auth_throttle_test", "recovery_uniformity_test"},
    "PROVISIONAL-ABUSE-03": {"deployed_idempotency_config", "duplicate_delivery_test"},
    "PROVISIONAL-ABUSE-04": {"atomicity_config", "concurrency_test"},
    "PROVISIONAL-ABUSE-05": {"retry_config", "failure_injection_test"},
    "PROVISIONAL-ABUSE-06": {"business_ceiling_config", "identity_bypass_test"},
    "PROVISIONAL-ABUSE-07": {"job_cap_config", "timeout_cancellation_test"},
    "PROVISIONAL-ABUSE-08": {
        "concurrency_config",
        "shedding_test",
        "provider_spend_control",
    },
}
KNOWN_KINDS = set().union(*REQUIRED_KINDS.values())
PROBE_KINDS = {kind for kind in KNOWN_KINDS if kind.endswith("_test")}
REQUIRED_FIELDS = {
    "id",
    "kind",
    "control_ids",
    "environment",
    "deployment_id",
    "source",
    "captured_by",
    "captured_at",
    "expires_at",
    "path",
    "sha256",
    "redacted",
    "authorized",
}
SPEND_FIELDS = {
    "provider",
    "account",
    "control_mode",
    "amount",
    "currency",
    "reset_period",
    "alert_recipients",
}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
MAX_EVIDENCE_AGE = timedelta(days=90)
MAX_EVIDENCE_VALIDITY = timedelta(days=90)


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


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_json_constant(value: str) -> None:
    raise ValueError("non-finite JSON number: " + value)


def validate_bundle(manifest_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeError, ValueError) as error:
        return {
            "bundle": str(manifest_path),
            "valid": False,
            "errors": [f"manifest unreadable: {error}"],
            "controls": {},
            "readiness_verdict": "not_issued",
            "verdict_owner": "secod-ship-check",
        }

    if not isinstance(manifest, dict):
        return {
            "bundle": str(manifest_path),
            "valid": False,
            "errors": ["manifest root must be an object"],
            "controls": {},
            "readiness_verdict": "not_issued",
            "verdict_owner": "secod-ship-check",
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

    deployment_scopes: set[tuple[str, str]] = set()
    reviewed_deployments = manifest.get("reviewed_deployments")
    if applicable_controls:
        if not isinstance(reviewed_deployments, list) or not reviewed_deployments:
            errors.append("reviewed_deployments must be a non-empty list")
            reviewed_deployments = []
        for index, deployment in enumerate(reviewed_deployments):
            prefix = f"reviewed_deployments[{index}]"
            if not isinstance(deployment, dict):
                errors.append(prefix + " must be an object")
                continue
            environment = deployment.get("environment")
            deployment_id = deployment.get("deployment_id")
            if not isinstance(environment, str) or not environment.strip():
                errors.append(prefix + ".environment must be a non-empty string")
            if not isinstance(deployment_id, str) or not deployment_id.strip():
                errors.append(prefix + ".deployment_id must be a non-empty string")
            if isinstance(environment, str) and isinstance(deployment_id, str):
                scope = (environment, deployment_id)
                if scope in deployment_scopes:
                    errors.append(prefix + " duplicates environment/deployment_id")
                else:
                    deployment_scopes.add(scope)

    topology_inventory: dict[tuple[str, str, str], dict[str, Any]] = {}
    if "PROVISIONAL-ABUSE-01" in applicable_controls:
        topologies = manifest.get("deployment_topologies")
        if not isinstance(topologies, list) or not topologies:
            errors.append("deployment_topologies must be a non-empty list for PROVISIONAL-ABUSE-01")
            topologies = []
        for index, topology in enumerate(topologies):
            prefix = f"deployment_topologies[{index}]"
            if not isinstance(topology, dict):
                errors.append(prefix + " must be an object")
                continue
            environment = topology.get("environment")
            deployment_id = topology.get("deployment_id")
            topology_class = topology.get("topology_class")
            regions = topology.get("regions")
            instance_ids = topology.get("instance_ids")
            store_id = topology.get("store_id")
            multi_instance = topology.get("multi_instance")
            if not isinstance(environment, str) or not environment.strip():
                errors.append(prefix + ".environment must be a non-empty string")
            if not isinstance(deployment_id, str) or not deployment_id.strip():
                errors.append(prefix + ".deployment_id must be a non-empty string")
            if not isinstance(topology_class, str) or not topology_class.strip():
                errors.append(prefix + ".topology_class must be a non-empty string")
            if (
                not isinstance(regions, list)
                or not regions
                or any(not isinstance(value, str) or not value.strip() for value in regions)
            ):
                errors.append(prefix + ".regions must be a non-empty string list")
            if not isinstance(multi_instance, bool):
                errors.append(prefix + ".multi_instance must be boolean")
            minimum_instances = 2 if multi_instance is True else 1
            if (
                not isinstance(instance_ids, list)
                or any(not isinstance(value, str) or not value.strip() for value in instance_ids)
                or len(set(instance_ids)) < minimum_instances
            ):
                errors.append(
                    prefix + f".instance_ids must identify at least {minimum_instances} instance(s)"
                )
            if not isinstance(store_id, str) or not store_id.strip():
                errors.append(prefix + ".store_id must be a non-empty string")
            if (
                isinstance(environment, str)
                and isinstance(deployment_id, str)
                and isinstance(topology_class, str)
            ):
                if (environment, deployment_id) not in deployment_scopes:
                    errors.append(prefix + " references undeclared reviewed deployment")
                key = (environment, deployment_id, topology_class)
                if key in topology_inventory:
                    errors.append(prefix + " duplicates environment/deployment/topology_class")
                else:
                    topology_inventory[key] = topology

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("artifacts must be a list")
        artifacts = []

    bundle_root = manifest_path.resolve().parent
    seen_ids: set[str] = set()
    supplied: dict[tuple[str, str, str], set[str]] = {
        (control_id, environment, deployment_id): set()
        for control_id in applicable_controls
        for environment, deployment_id in deployment_scopes
    }
    covered_topologies: set[tuple[str, str, str]] = set()

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
        if not isinstance(kind, str) or kind not in KNOWN_KINDS:
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
                elif control_id not in REQUIRED_KINDS:
                    artifact_errors.append(
                        prefix + f" references unknown control {control_id!r}"
                    )
                elif not isinstance(kind, str) or kind not in REQUIRED_KINDS[control_id]:
                    artifact_errors.append(
                        prefix + f" kind {kind!r} is not evidence for {control_id}"
                    )

        for field in ("environment", "deployment_id", "source", "captured_by"):
            value = artifact.get(field)
            if not isinstance(value, str) or not value.strip():
                artifact_errors.append(prefix + f".{field} must be a non-empty string")
        artifact_environment = artifact.get("environment")
        artifact_deployment = artifact.get("deployment_id")
        artifact_scope = (
            (artifact_environment, artifact_deployment)
            if isinstance(artifact_environment, str) and isinstance(artifact_deployment, str)
            else None
        )
        if artifact_scope is not None and artifact_scope not in deployment_scopes:
            artifact_errors.append(prefix + " references undeclared reviewed deployment")

        captured = _timestamp(artifact.get("captured_at"))
        expires = _timestamp(artifact.get("expires_at"))
        if captured is None:
            artifact_errors.append(prefix + ".captured_at must be an ISO-8601 timestamp with timezone")
        if expires is None:
            artifact_errors.append(prefix + ".expires_at must be an ISO-8601 timestamp with timezone")
        if captured is not None and expires is not None and expires <= captured:
            artifact_errors.append(prefix + ".expires_at must be later than captured_at")
        now = datetime.now(timezone.utc)
        if captured is not None and captured > now + timedelta(minutes=5):
            artifact_errors.append(prefix + ".captured_at is in the future")
        if captured is not None and captured < now - MAX_EVIDENCE_AGE:
            artifact_errors.append(prefix + ".captured_at exceeds maximum evidence age")
        if (
            captured is not None
            and expires is not None
            and expires - captured > MAX_EVIDENCE_VALIDITY
        ):
            artifact_errors.append(prefix + ".evidence validity exceeds 90 days")
        if expires is not None and expires <= now:
            artifact_errors.append(prefix + ".expires_at is stale")
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

        if kind == "shared_store_consistency":
            topology_class = artifact.get("topology_class")
            regions = artifact.get("regions")
            store_id = artifact.get("store_id")
            instance_ids = artifact.get("instance_ids")
            environment = artifact.get("environment")
            deployment_id = artifact.get("deployment_id")
            topology_key = (
                (environment, deployment_id, topology_class)
                if (
                    isinstance(environment, str)
                    and isinstance(deployment_id, str)
                    and isinstance(topology_class, str)
                )
                else None
            )
            declared = topology_inventory.get(topology_key) if topology_key is not None else None
            if not isinstance(topology_class, str) or not topology_class.strip():
                artifact_errors.append(prefix + ".topology_class must be a non-empty string")
            if declared is None:
                artifact_errors.append(prefix + ".topology_class is not declared for this environment")
            if (
                not isinstance(regions, list)
                or not regions
                or any(not isinstance(value, str) or not value.strip() for value in regions)
            ):
                artifact_errors.append(prefix + ".regions must be a non-empty string list")
            if not isinstance(store_id, str) or not store_id.strip():
                artifact_errors.append(prefix + ".store_id must be a non-empty string")
            minimum_instances = 2
            if (
                not isinstance(instance_ids, list)
                or any(not isinstance(value, str) or not value.strip() for value in instance_ids)
                or len(set(instance_ids)) < minimum_instances
            ):
                artifact_errors.append(
                    prefix + f".instance_ids must identify at least {minimum_instances} instance(s)"
                )
            if declared is not None:
                if store_id != declared.get("store_id"):
                    artifact_errors.append(prefix + ".store_id does not match topology inventory")
                declared_regions = declared.get("regions")
                declared_instances = declared.get("instance_ids")
                if (
                    isinstance(regions, list)
                    and all(isinstance(value, str) for value in regions)
                    and isinstance(declared_regions, list)
                    and all(isinstance(value, str) for value in declared_regions)
                    and not set(declared_regions) <= set(regions)
                ):
                    artifact_errors.append(prefix + ".regions do not cover topology inventory")
                if (
                    isinstance(instance_ids, list)
                    and all(isinstance(value, str) for value in instance_ids)
                    and isinstance(declared_instances, list)
                    and all(isinstance(value, str) for value in declared_instances)
                    and not set(declared_instances) <= set(instance_ids)
                ):
                    artifact_errors.append(prefix + ".instance_ids do not cover topology inventory")
        if isinstance(kind, str) and kind in PROBE_KINDS:
            command = artifact.get("command")
            thresholds = artifact.get("thresholds")
            responses = artifact.get("responses")
            side_effect_count = artifact.get("side_effect_count")
            cleanup_status = artifact.get("cleanup_status")
            execution_status = artifact.get("execution_status")
            if not isinstance(command, str) or not command.strip():
                artifact_errors.append(prefix + ".command must be a non-empty string")
            if not isinstance(thresholds, dict) or not thresholds:
                artifact_errors.append(prefix + ".thresholds must be a non-empty object")
            if not isinstance(responses, list) or not responses:
                artifact_errors.append(prefix + ".responses must be a non-empty list")
            if (
                isinstance(side_effect_count, bool)
                or not isinstance(side_effect_count, int)
                or side_effect_count < 0
            ):
                artifact_errors.append(prefix + ".side_effect_count must be a non-negative integer")
            if not isinstance(cleanup_status, str) or cleanup_status not in {
                "completed",
                "not_required",
                "failed",
            }:
                artifact_errors.append(
                    prefix + ".cleanup_status must be completed, not_required, or failed"
                )
            if not isinstance(execution_status, str) or execution_status not in {
                "passed",
                "failed",
                "blocked",
            }:
                artifact_errors.append(
                    prefix + ".execution_status must be passed, failed, or blocked"
                )
        if kind == "provider_spend_control":
            missing_spend = sorted(SPEND_FIELDS - artifact.keys())
            if missing_spend:
                artifact_errors.append(
                    prefix + " missing provider spend fields: " + ", ".join(missing_spend)
                )
            control_mode = artifact.get("control_mode")
            if not isinstance(control_mode, str) or control_mode not in {
                "hard_ceiling",
                "billing_alert",
                "both",
            }:
                artifact_errors.append(
                    prefix + ".control_mode must be hard_ceiling, billing_alert, or both"
                )
            for field in ("provider", "account", "currency", "reset_period"):
                value = artifact.get(field)
                if not isinstance(value, str) or not value.strip():
                    artifact_errors.append(prefix + f".{field} must be a non-empty string")
            amount = artifact.get("amount")
            if (
                isinstance(amount, bool)
                or not isinstance(amount, (int, float))
                or not math.isfinite(amount)
                or amount <= 0
            ):
                artifact_errors.append(prefix + ".amount must be positive")
            recipients = artifact.get("alert_recipients")
            if (
                not isinstance(recipients, list)
                or not recipients
                or any(not isinstance(value, str) or not value.strip() for value in recipients)
            ):
                artifact_errors.append(prefix + ".alert_recipients must be a non-empty list")

        errors.extend(artifact_errors)
        if not artifact_errors and isinstance(kind, str):
            for control_id in control_ids:
                supplied.setdefault(
                    (control_id, artifact["environment"], artifact["deployment_id"]),
                    set(),
                ).add(kind)
            if kind == "shared_store_consistency":
                covered_topologies.add(
                    (
                        artifact["environment"],
                        artifact["deployment_id"],
                        artifact["topology_class"],
                    )
                )

    for topology_key in sorted(set(topology_inventory) - covered_topologies):
        errors.append(
            "missing shared_store_consistency artifact for "
            + topology_key[0]
            + "/"
            + topology_key[1]
            + "/"
            + topology_key[2]
        )

    controls: dict[str, dict[str, Any]] = {}
    for control_id in applicable_controls:
        if control_id not in REQUIRED_KINDS:
            continue
        deployment_results: list[dict[str, Any]] = []
        aggregate_missing: set[str] = set()
        for environment, deployment_id in sorted(deployment_scopes):
            missing = sorted(
                REQUIRED_KINDS[control_id]
                - supplied.get((control_id, environment, deployment_id), set())
            )
            deployment_results.append({
                "environment": environment,
                "deployment_id": deployment_id,
                "intake_status": "Structurally complete" if not missing else "Not verified",
                "missing_artifact_kinds": missing,
            })
            aggregate_missing.update(missing)
            if missing:
                errors.append(
                    control_id
                    + " "
                    + environment
                    + "/"
                    + deployment_id
                    + " missing artifact kinds: "
                    + ", ".join(missing)
                )
        if not deployment_scopes:
            aggregate_missing.update(REQUIRED_KINDS[control_id])
        missing_kinds = sorted(aggregate_missing)
        controls[control_id] = {
            "intake_status": "Structurally complete" if not missing_kinds else "Not verified",
            "missing_artifact_kinds": missing_kinds,
            "deployments": deployment_results,
        }
        if missing_kinds and not deployment_scopes:
            errors.append(control_id + " missing artifact kinds: " + ", ".join(missing_kinds))

    return {
        "bundle": str(manifest_path),
        "valid": not errors,
        "errors": errors,
        "controls": controls,
        "limitation": "Structural completeness only; inspect artifact contents before control status.",
        "readiness_verdict": "not_issued",
        "verdict_owner": "secod-ship-check",
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
