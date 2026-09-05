"""Executable expectations for SECOD critical behavior categories."""

from __future__ import annotations

import unittest

from fixture_app import (
    BoundedEndpoint,
    PaymentLedger,
    TenantStore,
    UnboundedEndpoint,
    insecure_ai_tool_call,
    insecure_client_payload,
    insecure_command,
    insecure_fetch_allowed,
    insecure_log,
    insecure_retry,
    insecure_server_authorization,
    insecure_storage_object,
    insecure_upload,
    insecure_vector_search,
    insecure_verify_webhook,
    secure_ai_tool_call,
    secure_client_payload,
    secure_command,
    secure_fetch_allowed,
    secure_log,
    secure_retry,
    secure_server_authorization,
    secure_storage_object,
    secure_upload,
    secure_vector_search,
    secure_verify_webhook,
    sign_webhook,
)


FIXTURE_SECRET = b"fixture-webhook-secret"
RAW_WEBHOOK = b'{"type":"invoice.paid","account":"acct-fixture"}'


class CriticalBehaviorFixtures(unittest.TestCase):
    def test_01_broken_tenant_authorization(self) -> None:
        store = TenantStore()
        self.assertEqual(store.insecure_read("tenant-a", "tenant-b", "invoice-b"), "tenant-b invoice")
        self.assertIsNone(store.secure_read("tenant-a", "tenant-b", "invoice-b"))

    def test_02_missing_server_side_authorization(self) -> None:
        self.assertTrue(insecure_server_authorization("user", "admin"))
        self.assertFalse(secure_server_authorization("user", "admin"))
        self.assertTrue(secure_server_authorization("admin", "admin"))

    def test_03_exposed_secret(self) -> None:
        secret = "sk_live_fixture"
        self.assertEqual(insecure_client_payload(secret)["api_key"], secret)
        self.assertIsNone(secure_client_payload(secret)["api_key"])

    def test_04_weak_webhook_verification(self) -> None:
        valid_signature = sign_webhook(FIXTURE_SECRET, RAW_WEBHOOK)
        self.assertTrue(insecure_verify_webhook(RAW_WEBHOOK, "forged"))
        self.assertFalse(secure_verify_webhook(FIXTURE_SECRET, RAW_WEBHOOK, "forged"))
        self.assertTrue(secure_verify_webhook(FIXTURE_SECRET, RAW_WEBHOOK, valid_signature))

    def test_05_payment_replay(self) -> None:
        insecure = PaymentLedger()
        insecure.insecure_apply("evt-1", "user-a")
        insecure.insecure_apply("evt-1", "user-a")
        self.assertEqual(insecure.entitlements, ["user-a", "user-a"])

        secure = PaymentLedger()
        secure.secure_apply("evt-1", "user-a")
        secure.secure_apply("evt-1", "user-a")
        self.assertEqual(secure.entitlements, ["user-a"])

    def test_06_unrestricted_file_upload(self) -> None:
        oversized_unknown = b"MZ" + (b"x" * 2048)
        valid_png = b"\x89PNG\r\n\x1a\n" + b"fixture"
        self.assertTrue(insecure_upload("payload.exe", oversized_unknown))
        self.assertFalse(secure_upload("payload.exe", oversized_unknown))
        self.assertTrue(secure_upload("avatar.png", valid_png))

    def test_07_public_storage_object(self) -> None:
        self.assertEqual(insecure_storage_object("tenant-b/private.pdf").visibility, "public")
        self.assertEqual(secure_storage_object("tenant-b/private.pdf").visibility, "private")

    def test_08_command_injection(self) -> None:
        malicious_name = "photo.png; touch /tmp/pwned"
        self.assertIn(";", insecure_command(malicious_name))
        self.assertIsNone(secure_command(malicious_name))
        self.assertEqual(secure_command("photo.png"), ("convert", "photo.png", "/tmp/output.png"))

    def test_09_ssrf(self) -> None:
        metadata_url = "http://169.254.169.254/latest/meta-data"
        self.assertTrue(insecure_fetch_allowed(metadata_url))
        self.assertFalse(secure_fetch_allowed(metadata_url))
        self.assertTrue(secure_fetch_allowed("https://api.example.test/v1/status"))

    def test_10_missing_rate_limits(self) -> None:
        insecure = UnboundedEndpoint()
        self.assertTrue(all(insecure.request() for _ in range(5)))
        self.assertEqual(insecure.requests, 5)

        secure = BoundedEndpoint(limit=2)
        self.assertEqual([secure.request("user-a") for _ in range(3)], [True, True, False])

    def test_11_retry_storm(self) -> None:
        self.assertEqual(insecure_retry(100), 100)
        self.assertEqual(secure_retry(100), 3)

    def test_12_sensitive_log_entry(self) -> None:
        token = "session-fixture-token"
        self.assertIn(token, insecure_log(token))
        self.assertNotIn(token, secure_log(token))
        self.assertEqual(secure_log(token), "authorization=[REDACTED]")

    def test_13_unsafe_ai_tool_execution(self) -> None:
        self.assertEqual(
            insecure_ai_tool_call("delete_account", {"account": "user-a"})["executed"],
            "delete_account",
        )
        denied = secure_ai_tool_call(
            "delete_account",
            {"account": "user-a"},
            allowed_tools={"search_account"},
            user_confirmed=False,
        )
        self.assertIsNone(denied["executed"])

    def test_14_cross_tenant_vector_search(self) -> None:
        self.assertEqual({document.tenant_id for document in insecure_vector_search("product")}, {"tenant-a", "tenant-b"})
        self.assertEqual(
            {document.tenant_id for document in secure_vector_search("product", "tenant-a")},
            {"tenant-a"},
        )


if __name__ == "__main__":
    unittest.main()
