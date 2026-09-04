"""Executable expectations for abuse-limits external evidence intake."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "secod-abuse-limits"
    / "scripts"
    / "validate_evidence_bundle.py"
)
SPEC = importlib.util.spec_from_file_location("abuse_evidence_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load abuse-limits evidence validator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def artifact(
    root: Path,
    artifact_id: str,
    kind: object,
    control_id: str,
    **extra: object,
) -> dict[str, object]:
    evidence = root / "evidence.txt"
    evidence.write_text("redacted fixture evidence", encoding="utf-8")
    now = datetime.now(timezone.utc)
    captured = now - timedelta(days=1)
    expires = now + timedelta(days=30)
    payload: dict[str, object] = {
        "id": artifact_id,
        "kind": kind,
        "control_ids": [control_id],
        "environment": "staging",
        "deployment_id": "deploy-1",
        "source": "fixture",
        "captured_by": "fixture-runner",
        "captured_at": captured.isoformat(),
        "expires_at": expires.isoformat(),
        "path": "evidence.txt",
        "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
        "redacted": True,
        "authorized": True,
    }
    if isinstance(kind, str) and kind.endswith("_test"):
        payload.update(
            {
                "command": "fixture probe",
                "thresholds": {"limit": 2},
                "responses": [200, 200, 429],
                "side_effect_count": 2,
                "cleanup_status": "not_required",
                "execution_status": "passed",
            }
        )
    payload.update(extra)
    return payload


def complete_artifact(
    root: Path,
    artifact_id: str,
    kind: str,
    control_id: str,
    environment: str,
    deployment_id: str,
) -> dict[str, object]:
    extra: dict[str, object] = {
        "environment": environment,
        "deployment_id": deployment_id,
    }
    if kind == "shared_store_consistency":
        extra.update(
            {
                "topology_class": environment + "-service",
                "regions": [environment + "-region"],
                "store_id": environment + "-store",
                "instance_ids": [environment + "-instance-a", environment + "-instance-b"],
            }
        )
    if kind == "provider_spend_control":
        extra.update(
            {
                "provider": "provider-a",
                "account": environment + "-account",
                "control_mode": "both",
                "amount": 100,
                "currency": "USD",
                "reset_period": "monthly",
                "alert_recipients": ["security@example.test"],
            }
        )
    return artifact(root, artifact_id, kind, control_id, **extra)


class AbuseEvidenceValidatorFixtures(unittest.TestCase):
    def test_09_complete_limiter_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = []
            for index, kind in enumerate(
                ("deployed_limiter_config", "shared_store_consistency", "burst_test"),
                start=1,
            ):
                artifact_row = artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-01",
                )
                if kind == "shared_store_consistency":
                    artifact_row.update(
                        {
                            "topology_class": "regional-service",
                            "regions": ["region-a"],
                            "store_id": "limiter-store-1",
                            "instance_ids": ["instance-a", "instance-b"],
                        }
                    )
                artifacts.append(artifact_row)
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-01"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "deployment_topologies": [
                            {
                                "environment": "staging",
                                "deployment_id": "deploy-1",
                                "topology_class": "regional-service",
                                "regions": ["region-a"],
                                "instance_ids": ["instance-a", "instance-b"],
                                "store_id": "limiter-store-1",
                                "multi_instance": True,
                            }
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertTrue(result["valid"])
            self.assertEqual(
                result["controls"]["PROVISIONAL-ABUSE-01"]["intake_status"],
                "Structurally complete",
            )
            self.assertEqual(result["readiness_verdict"], "not_issued")

    def test_10_missing_provider_spend_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = Path(temporary_directory) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertIn(
                "provider_spend_control",
                result["controls"]["PROVISIONAL-ABUSE-08"]["missing_artifact_kinds"],
            )

    def test_11_stale_evidence_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-01",
                    expires_at="2021-08-28T10:00:00+05:30",
                    **(
                        {
                            "topology_class": "regional-service",
                            "regions": ["region-a"],
                            "store_id": "limiter-store-1",
                            "instance_ids": ["instance-a", "instance-b"],
                        }
                        if kind == "shared_store_consistency"
                        else {}
                    ),
                )
                for index, kind in enumerate(
                    ("deployed_limiter_config", "shared_store_consistency", "burst_test"),
                    start=1,
                )
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-01"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "deployment_topologies": [
                            {
                                "environment": "staging",
                                "deployment_id": "deploy-1",
                                "topology_class": "regional-service",
                                "regions": ["region-a"],
                                "instance_ids": ["instance-a", "instance-b"],
                                "store_id": "limiter-store-1",
                                "multi_instance": True,
                            }
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("expires_at is stale" in error for error in result["errors"]))

    def test_12_malformed_types_return_structured_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            malformed = artifact(
                root,
                "artifact-1",
                {},
                "PROVISIONAL-ABUSE-01",
                instance_ids=[{"bad": True}],
            )
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-01"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": [malformed],
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertIsInstance(result["errors"], list)
            self.assertTrue(any("unknown kind" in error for error in result["errors"]))

    def test_13_weak_provider_metadata_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                artifact(root, "artifact-1", "concurrency_config", "PROVISIONAL-ABUSE-08"),
                artifact(root, "artifact-2", "shedding_test", "PROVISIONAL-ABUSE-08"),
                artifact(
                    root,
                    "artifact-3",
                    "provider_spend_control",
                    "PROVISIONAL-ABUSE-08",
                    provider="",
                    account="",
                    control_mode="both",
                    amount=True,
                    currency="",
                    reset_period="",
                    alert_recipients=[""],
                ),
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any(".provider must be" in error for error in result["errors"]))
            self.assertTrue(any(".amount must be positive" in error for error in result["errors"]))
            self.assertTrue(any(".alert_recipients" in error for error in result["errors"]))

    def test_14_unknown_control_returns_structured_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            unknown = artifact(
                root,
                "artifact-1",
                "burst_test",
                "PROVISIONAL-ABUSE-99",
            )
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-99"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": [unknown],
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("unknown control" in error for error in result["errors"]))
            self.assertEqual(result["readiness_verdict"], "not_issued")

    def test_15_early_refusals_keep_readiness_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            missing = MODULE.validate_bundle(root / "missing.json")
            self.assertFalse(missing["valid"])
            self.assertEqual(missing["verdict_owner"], "secod-ship-check")
            self.assertEqual(missing["readiness_verdict"], "not_issued")

            non_object = root / "non-object.json"
            non_object.write_text("[]", encoding="utf-8")
            result = MODULE.validate_bundle(non_object)
            self.assertFalse(result["valid"])
            self.assertEqual(result["verdict_owner"], "secod-ship-check")
            self.assertEqual(result["readiness_verdict"], "not_issued")

    def test_16_evidence_is_complete_per_deployment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                artifact(root, "artifact-1", "concurrency_config", "PROVISIONAL-ABUSE-08"),
                artifact(root, "artifact-2", "shedding_test", "PROVISIONAL-ABUSE-08"),
                artifact(
                    root,
                    "artifact-3",
                    "provider_spend_control",
                    "PROVISIONAL-ABUSE-08",
                    provider="provider-a",
                    account="account-a",
                    control_mode="both",
                    amount=100,
                    currency="USD",
                    reset_period="monthly",
                    alert_recipients=["security@example.test"],
                ),
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"},
                            {"environment": "production", "deployment_id": "deploy-2"},
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            control = result["controls"]["PROVISIONAL-ABUSE-08"]
            deployment_results = {
                (row["environment"], row["deployment_id"]): row
                for row in control["deployments"]
            }
            self.assertEqual(
                deployment_results[("staging", "deploy-1")]["intake_status"],
                "Structurally complete",
            )
            self.assertEqual(
                deployment_results[("production", "deploy-2")]["intake_status"],
                "Not verified",
            )

    def test_17_unhashable_membership_values_return_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                artifact(root, "artifact-1", "concurrency_config", "PROVISIONAL-ABUSE-08"),
                artifact(
                    root,
                    "artifact-2",
                    "shedding_test",
                    "PROVISIONAL-ABUSE-08",
                    cleanup_status={},
                    execution_status=[],
                ),
                artifact(
                    root,
                    "artifact-3",
                    "provider_spend_control",
                    "PROVISIONAL-ABUSE-08",
                    provider="provider-a",
                    account="account-a",
                    control_mode=[],
                    amount=100,
                    currency="USD",
                    reset_period="monthly",
                    alert_recipients=["security@example.test"],
                ),
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertIsInstance(result["errors"], list)
            self.assertEqual(result["readiness_verdict"], "not_issued")

            topology_manifest = root / "topology.json"
            topology_manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-01"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "deployment_topologies": [
                            {
                                "environment": "staging",
                                "deployment_id": "deploy-1",
                                "topology_class": "regional-service",
                                "regions": ["region-a"],
                                "instance_ids": ["instance-a"],
                                "store_id": "limiter-store-1",
                                "multi_instance": {},
                            }
                        ],
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            topology_result = MODULE.validate_bundle(topology_manifest)
            self.assertFalse(topology_result["valid"])
            self.assertIsInstance(topology_result["errors"], list)

    def test_18_deployment_result_keys_do_not_collide(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            scopes = (("a", "b/c"), ("a/b", "c"))
            artifacts = []
            for index, (environment, deployment_id) in enumerate(scopes):
                for kind in MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-08"]:
                    artifacts.append(
                        complete_artifact(
                            root,
                            f"artifact-{index}-{kind}",
                            kind,
                            "PROVISIONAL-ABUSE-08",
                            environment,
                            deployment_id,
                        )
                    )
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": environment, "deployment_id": deployment_id}
                            for environment, deployment_id in scopes
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertTrue(result["valid"])
            deployments = result["controls"]["PROVISIONAL-ABUSE-08"]["deployments"]
            self.assertEqual(len(deployments), 2)
            self.assertEqual(
                {(row["environment"], row["deployment_id"]) for row in deployments},
                set(scopes),
            )

    def test_19_future_capture_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = []
            for index, kind in enumerate(MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-08"]):
                row = complete_artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-08",
                    "staging",
                    "deploy-1",
                )
                row["captured_at"] = "2099-08-28T10:00:00+00:00"
                row["expires_at"] = "2100-08-28T10:00:00+00:00"
                artifacts.append(row)
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("captured_at is in the future" in error for error in result["errors"]))

    def test_20_complete_bundle_for_every_control_and_deployment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            scopes = (("staging", "deploy-1"), ("production", "deploy-2"))
            controls = sorted(MODULE.REQUIRED_KINDS)
            artifacts = []
            for control_id in controls:
                for environment, deployment_id in scopes:
                    for kind in MODULE.REQUIRED_KINDS[control_id]:
                        artifacts.append(
                            complete_artifact(
                                root,
                                f"artifact-{len(artifacts)}",
                                kind,
                                control_id,
                                environment,
                                deployment_id,
                            )
                        )
            topologies = [
                {
                    "environment": environment,
                    "deployment_id": deployment_id,
                    "topology_class": environment + "-service",
                    "regions": [environment + "-region"],
                    "instance_ids": [environment + "-instance-a", environment + "-instance-b"],
                    "store_id": environment + "-store",
                    "multi_instance": True,
                }
                for environment, deployment_id in scopes
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": controls,
                        "reviewed_deployments": [
                            {"environment": environment, "deployment_id": deployment_id}
                            for environment, deployment_id in scopes
                        ],
                        "deployment_topologies": topologies,
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertTrue(result["valid"])
            self.assertTrue(
                all(
                    result["controls"][control_id]["intake_status"] == "Structurally complete"
                    for control_id in controls
                )
            )

    def test_21_incomplete_bundle_refused_for_every_control(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            scopes = (("staging", "deploy-1"), ("production", "deploy-2"))
            controls = sorted(MODULE.REQUIRED_KINDS)
            artifacts = []
            omitted_by_control: dict[str, str] = {}
            for control_id in controls:
                omitted = sorted(MODULE.REQUIRED_KINDS[control_id])[0]
                omitted_by_control[control_id] = omitted
                for environment, deployment_id in scopes:
                    for kind in MODULE.REQUIRED_KINDS[control_id]:
                        if environment == "production" and kind == omitted:
                            continue
                        artifacts.append(
                            complete_artifact(
                                root,
                                f"artifact-{len(artifacts)}",
                                kind,
                                control_id,
                                environment,
                                deployment_id,
                            )
                        )
            topologies = [
                {
                    "environment": environment,
                    "deployment_id": deployment_id,
                    "topology_class": environment + "-service",
                    "regions": [environment + "-region"],
                    "instance_ids": [environment + "-instance-a", environment + "-instance-b"],
                    "store_id": environment + "-store",
                    "multi_instance": True,
                }
                for environment, deployment_id in scopes
            ]
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": controls,
                        "reviewed_deployments": [
                            {"environment": environment, "deployment_id": deployment_id}
                            for environment, deployment_id in scopes
                        ],
                        "deployment_topologies": topologies,
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(
                all(
                    result["controls"][control_id]["intake_status"] == "Not verified"
                    for control_id in controls
                )
            )
            for control_id in controls:
                deployments = {
                    (row["environment"], row["deployment_id"]): row
                    for row in result["controls"][control_id]["deployments"]
                }
                self.assertEqual(
                    deployments[("staging", "deploy-1")]["intake_status"],
                    "Structurally complete",
                )
                self.assertEqual(
                    deployments[("production", "deploy-2")]["intake_status"],
                    "Not verified",
                )
                self.assertEqual(
                    deployments[("production", "deploy-2")]["missing_artifact_kinds"],
                    [omitted_by_control[control_id]],
                )

    def test_22_missing_capture_identity_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                complete_artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-08",
                    "staging",
                    "deploy-1",
                )
                for index, kind in enumerate(MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-08"])
            ]
            artifacts[0].pop("captured_by")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("captured_by" in error for error in result["errors"]))

    def test_23_non_finite_spend_amount_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = [
                complete_artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-08",
                    "staging",
                    "deploy-1",
                )
                for index, kind in enumerate(MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-08"])
            ]
            for row in artifacts:
                if row["kind"] == "provider_spend_control":
                    row["amount"] = float("nan")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("non-finite JSON number" in error for error in result["errors"]))
            self.assertEqual(result["readiness_verdict"], "not_issued")

    def test_24_shared_store_probe_requires_two_instances(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifacts = []
            for index, kind in enumerate(MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-01"]):
                row = complete_artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-01",
                    "staging",
                    "deploy-1",
                )
                if kind == "shared_store_consistency":
                    row["instance_ids"] = ["staging-instance-a"]
                artifacts.append(row)
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-01"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "deployment_topologies": [
                            {
                                "environment": "staging",
                                "deployment_id": "deploy-1",
                                "topology_class": "staging-service",
                                "regions": ["staging-region"],
                                "instance_ids": ["staging-instance-a"],
                                "store_id": "staging-store",
                                "multi_instance": False,
                            }
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(any("at least 2 instance" in error for error in result["errors"]))

    def test_25_over_age_unexpired_evidence_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            now = datetime.now(timezone.utc)
            artifacts = [
                complete_artifact(
                    root,
                    f"artifact-{index}",
                    kind,
                    "PROVISIONAL-ABUSE-08",
                    "staging",
                    "deploy-1",
                )
                for index, kind in enumerate(MODULE.REQUIRED_KINDS["PROVISIONAL-ABUSE-08"])
            ]
            for row in artifacts:
                row["captured_at"] = (now - timedelta(days=91)).isoformat()
                row["expires_at"] = (now + timedelta(hours=1)).isoformat()
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "applicable_controls": ["PROVISIONAL-ABUSE-08"],
                        "reviewed_deployments": [
                            {"environment": "staging", "deployment_id": "deploy-1"}
                        ],
                        "artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_bundle(manifest)
            self.assertFalse(result["valid"])
            self.assertTrue(
                any("exceeds maximum evidence age" in error for error in result["errors"])
            )


if __name__ == "__main__":
    unittest.main()
