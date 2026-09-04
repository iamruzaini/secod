"""Executable expectations for maintained secrets-config fixture cases."""

from __future__ import annotations

import unittest

from fixture_app import (
    FAKE_KEY,
    check_bearer_flow,
    check_default_credentials,
    check_environment_separation,
    check_history_response,
    check_production_flags,
    check_rotation,
    check_scope,
    check_storage,
    check_template,
    scan_surfaces,
)


class SecretsConfigFixtures(unittest.TestCase):
    def test_01_source_and_log_leaks_are_redacted(self) -> None:
        results = scan_surfaces(
            {
                "fixture/config.py": f'KEY = "{FAKE_KEY}"',
                "fixture/log.py": "logger.info('credential=%s', SECRET_VALUE)",
            }
        )
        self.assertEqual(len(results), 2)
        self.assertTrue(all(item["status"] == "Do not ship" for item in results))
        self.assertNotIn(FAKE_KEY, str(results))
        self.assertEqual({item["evidence"]["match"] for item in results}, {"[REDACTED]"})

    def test_02_bearer_response_and_rpc_are_blocked(self) -> None:
        results = check_bearer_flow(["session_token"], ["tenant_capability"])
        self.assertEqual([item["status"] for item in results], ["Do not ship", "Do not ship"])

    def test_03_superuser_for_routine_runtime_is_blocked(self) -> None:
        result = check_scope("superuser", ["read_invoice"])
        self.assertEqual(result[0]["status"], "Fix before launch")

    def test_04_template_value_and_parity_gaps_are_reported(self) -> None:
        results = check_template(["DATABASE_URL", "PAYMENT_SECRET"], {"DATABASE_URL": FAKE_KEY})
        self.assertEqual(len(results), 2)
        self.assertIn("PAYMENT_SECRET", str(results))
        self.assertNotIn(FAKE_KEY, str(results))

    def test_05_plaintext_and_public_secret_are_blocked(self) -> None:
        results = check_storage(["NEXT_PUBLIC_PROVIDER_SECRET"], "fixture-password")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(item["status"] == "Do not ship" for item in results))

    def test_06_environment_identity_conflicts_are_blocked(self) -> None:
        results = check_environment_separation("production-db.fixture.invalid", ["test", "live"])
        self.assertEqual(len(results), 2)
        self.assertTrue(all(item["status"] == "Do not ship" for item in results))

    def test_07_missing_rotation_evidence_stays_not_verified(self) -> None:
        result = check_rotation(
            has_owner=True, has_revocation_path=True, has_current_evidence=False
        )
        self.assertEqual(result["status"], "Not verified")

    def test_08_missing_revocation_path_blocks_launch(self) -> None:
        result = check_rotation(
            has_owner=True, has_revocation_path=False, has_current_evidence=False
        )
        self.assertEqual(result["status"], "Fix before launch")

    def test_09_fail_open_bypass_and_production_debug_are_reported(self) -> None:
        results = check_production_flags(bypass_default=True, debug_enabled=True)
        self.assertEqual([item["status"] for item in results], ["Do not ship", "Fix before launch"])

    def test_10_history_rewrite_before_revocation_is_blocked(self) -> None:
        result = check_history_response(["rewrite", "revoke", "block"])
        self.assertEqual(result["status"], "Do not ship")

    def test_11_removed_but_unrevoked_key_remains_blocked(self) -> None:
        result = check_history_response(["remove_from_head"])
        self.assertEqual(result["status"], "Do not ship")

    def test_12_default_seed_credential_blocks_launch(self) -> None:
        result = check_default_credentials(seed_uses_default=True, probe_authorized=False)
        self.assertEqual(result["status"], "Fix before launch")

    def test_13_unauthorized_deployed_probe_is_not_run(self) -> None:
        result = check_default_credentials(seed_uses_default=False, probe_authorized=False)
        self.assertEqual(result["status"], "Not verified")
        self.assertFalse(result["probe_performed"])

    def test_14_clean_case_has_no_repository_findings(self) -> None:
        self.assertEqual(
            scan_surfaces({"fixture/config.py": "KEY = load_from_secret_store()"}), []
        )
        self.assertEqual(check_bearer_flow(["user_id"], ["invoice_id"]), [])
        self.assertEqual(check_scope("invoice_reader", ["read_invoice"]), [])
        self.assertEqual(check_template(["PUBLIC_HOST"], {"PUBLIC_HOST": "fixture.invalid"}), [])
        self.assertEqual(check_storage(["NEXT_PUBLIC_SITE_NAME"], None), [])
        self.assertEqual(
            check_environment_separation("staging-db.fixture.invalid", ["test"]), []
        )
        self.assertEqual(check_production_flags(bypass_default=False, debug_enabled=False), [])
        self.assertEqual(
            check_history_response(["revoke", "rewrite", "block"])["status"],
            "Passed with evidence",
        )


if __name__ == "__main__":
    unittest.main()
