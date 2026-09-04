"""Executable expectations for crypto-data-protection evidence intake."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


SECOD_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_ROOT = SECOD_ROOT / "skills" / "secod-crypto-data-protection" / "scripts"
sys.path.insert(0, str(VALIDATOR_ROOT))

from validate_evidence_bundle import validate_bundle


REVIEW_TIME = datetime.fromisoformat("2026-08-28T12:00:00+05:30")


class CryptoEvidenceFixtures(unittest.TestCase):
    def _bundle(self, root: Path) -> tuple[Path, dict[str, object]]:
        controls = ["SECOD-CDP-01", "SECOD-CDP-04", "SECOD-CDP-08", "SECOD-CDP-09"]

        def artifact(
            artifact_id: str, kind: str, control_id: str, fields: dict[str, object]
        ) -> dict[str, object]:
            path = root / f"{artifact_id}.json"
            path.write_text(json.dumps({"fixture": artifact_id}), encoding="utf-8")
            return {
                "id": artifact_id,
                "kind": kind,
                "control_ids": [control_id],
                "environment": "production",
                "deployment_id": "deploy-fixture",
                "source": "authorized fixture export",
                "captured_at": "2026-08-27T09:30:00+05:30",
                "valid_until": "2026-09-30T23:59:59+05:30",
                "path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "redacted": True,
                "authorized": True,
                **fields,
            }

        artifacts = [
            artifact(
                "tls",
                "deployed_tls_posture",
                "SECOD-CDP-01",
                {
                    "endpoints": ["api.example.test:443"],
                    "minimum_protocol": "TLSv1.2",
                    "certificate_validation": True,
                },
            ),
            artifact(
                "encryption",
                "managed_service_encryption_at_rest",
                "SECOD-CDP-04",
                {
                    "resource_ids": ["database/primary"],
                    "encryption_at_rest": True,
                    "key_management": "customer_managed",
                },
            ),
            artifact(
                "deletion",
                "provider_deletion_outcome",
                "SECOD-CDP-08",
                {
                    "store_ids": ["database/primary", "search/main"],
                    "deletion_event_id": "delete-fixture-1",
                    "outcome": "confirmed_deleted",
                },
            ),
            artifact(
                "backup",
                "backup_encryption_at_rest",
                "SECOD-CDP-09",
                {
                    "backup_ids": ["backup-fixture-1"],
                    "encrypted": True,
                    "key_separated_from_primary": True,
                },
            ),
            artifact(
                "restore",
                "restore_test_result",
                "SECOD-CDP-09",
                {
                    "restore_tested_at": "2026-08-26T11:00:00+05:30",
                    "policy_max_age_days": 60,
                    "restored_backup_id": "backup-fixture-1",
                    "successful": True,
                    "integrity_verified": True,
                    "deletion_policy_reapplied": True,
                },
            ),
        ]
        manifest: dict[str, object] = {
            "schema_version": 1,
            "applicable_controls": controls,
            "expected_tls_endpoints": ["api.example.test:443"],
            "expected_managed_resource_ids": ["database/primary"],
            "expected_deletion_store_ids": ["database/primary", "search/main"],
            "expected_backup_ids": ["backup-fixture-1"],
            "artifacts": artifacts,
        }
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path, manifest

    def test_complete_bundle_is_reviewable_not_passed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, _ = self._bundle(Path(directory))
            result = validate_bundle(path, as_of=REVIEW_TIME)
            self.assertTrue(result["valid"])
            self.assertEqual(result["readiness_verdict"], "not_issued")
            self.assertTrue(
                all(
                    control["intake_status"] == "Bundle complete"
                    for control in result["controls"].values()
                )
            )

    def test_missing_provider_deletion_stays_not_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, manifest = self._bundle(Path(directory))
            manifest["artifacts"] = [
                artifact
                for artifact in manifest["artifacts"]
                if artifact["kind"] != "provider_deletion_outcome"
            ]
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_bundle(path, as_of=REVIEW_TIME)
            self.assertFalse(result["valid"])
            self.assertEqual(result["controls"]["SECOD-CDP-08"]["intake_status"], "Not verified")

    def test_stale_restore_test_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, manifest = self._bundle(Path(directory))
            restore = next(
                artifact
                for artifact in manifest["artifacts"]
                if artifact["kind"] == "restore_test_result"
            )
            restore["valid_until"] = "2026-08-28T00:00:00+05:30"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_bundle(path, as_of=REVIEW_TIME)
            self.assertFalse(result["valid"])
            self.assertTrue(any("valid_until is stale" in error for error in result["errors"]))

    def test_hash_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = self._bundle(root)
            (root / "tls.json").write_text('{"fixture":"changed"}', encoding="utf-8")
            result = validate_bundle(path, as_of=REVIEW_TIME)
            self.assertFalse(result["valid"])
            self.assertTrue(any("SHA-256 mismatch" in error for error in result["errors"]))

    def test_kind_cannot_prove_wrong_control(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, manifest = self._bundle(Path(directory))
            backup = next(
                artifact
                for artifact in manifest["artifacts"]
                if artifact["kind"] == "backup_encryption_at_rest"
            )
            backup["control_ids"] = ["SECOD-CDP-01"]
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_bundle(path, as_of=REVIEW_TIME)
            self.assertFalse(result["valid"])
            self.assertTrue(any("is not evidence for SECOD-CDP-01" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
