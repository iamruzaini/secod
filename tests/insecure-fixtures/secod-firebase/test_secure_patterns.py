"""Executable Firebase implementation expectations."""

from __future__ import annotations

import unittest

from fixture_app import (
    Document,
    Request,
    Upload,
    insecure_admin_sdk_call,
    insecure_client_config,
    insecure_firestore_read,
    insecure_storage_write,
    secure_admin_sdk_call,
    secure_client_config,
    secure_firestore_read,
    secure_storage_write,
)


class FirebaseFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.request_a = Request("user-a", "tenant-a")
        self.request_b = Request("user-b", "tenant-b")
        self.document_b = Document("doc-b", "tenant-b", "user-b", "B")
        self.png = Upload("image/png", b"\x89PNG\r\n\x1a\nfixture")

    def test_broad_firestore_rule_exposes_other_tenant_document(self) -> None:
        self.assertTrue(insecure_firestore_read(self.request_a, self.document_b))
        self.assertFalse(secure_firestore_read(self.request_a, self.document_b))

    def test_firestore_owner_and_tenant_admin_are_allowed(self) -> None:
        self.assertTrue(secure_firestore_read(self.request_b, self.document_b))
        admin = Request("admin-a", "tenant-b", frozenset({"tenant-admin"}))
        self.assertTrue(secure_firestore_read(admin, self.document_b))

    def test_firestore_anonymous_request_is_denied(self) -> None:
        self.assertFalse(secure_firestore_read(Request(None, None), self.document_b))

    def test_storage_write_requires_tenant_scoped_path_and_content_checks(self) -> None:
        path = "tenants/tenant-a/users/user-a/avatar.png"
        self.assertTrue(secure_storage_write(self.request_a, path, self.png))
        self.assertTrue(insecure_storage_write(self.request_a, "arbitrary/path", self.png))
        self.assertFalse(secure_storage_write(self.request_a, "tenants/tenant-b/users/user-b/avatar.png", self.png))
        self.assertFalse(secure_storage_write(self.request_a, path, Upload("image/png", b"MZ-not-png")))

    def test_admin_sdk_is_server_only(self) -> None:
        self.assertTrue(insecure_admin_sdk_call("client"))
        self.assertFalse(secure_admin_sdk_call("client"))
        self.assertTrue(secure_admin_sdk_call("server"))

    def test_service_credentials_stay_out_of_client_configuration(self) -> None:
        credentials = {
            "FIREBASE_API_KEY": "public-config",
            "FIREBASE_PROJECT_ID": "fixture-project",
            "FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY": "server-secret",
        }
        self.assertEqual(insecure_client_config(credentials), credentials)
        self.assertNotIn("FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY", secure_client_config(credentials))


if __name__ == "__main__":
    unittest.main()
