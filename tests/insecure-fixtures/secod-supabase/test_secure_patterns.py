"""Executable Supabase implementation expectations."""

from __future__ import annotations

import unittest

from fixture_app import (
    Row,
    Session,
    StorageObject,
    insecure_browser_config,
    insecure_select,
    insecure_storage_read,
    unsafe_update_owner,
    secure_browser_config,
    secure_select,
    secure_storage_read,
    secure_update_value,
)


class SupabaseFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = [
            Row("row-a", "tenant-a", "user-a", "A"),
            Row("row-b", "tenant-b", "user-b", "B"),
        ]
        self.session_a = Session("user-a", "tenant-a")
        self.session_b = Session("user-b", "tenant-b")
        self.object_b = StorageObject("tenant-b/private.txt", "tenant-b", "user-b", b"B", True)

    def test_missing_rls_exposes_other_tenant_rows(self) -> None:
        self.assertEqual([row.row_id for row in insecure_select(self.rows)], ["row-a", "row-b"])
        self.assertEqual([row.row_id for row in secure_select(self.session_a, self.rows)], ["row-a"])

    def test_anonymous_select_returns_no_rows(self) -> None:
        self.assertEqual(secure_select(Session(None, None, authenticated=False), self.rows), [])

    def test_service_role_key_stays_out_of_browser(self) -> None:
        credentials = {
            "SUPABASE_URL": "https://fixture.supabase.test",
            "SUPABASE_ANON_KEY": "anon-key",
            "SUPABASE_SERVICE_ROLE_KEY": "service-secret",
        }
        self.assertEqual(insecure_browser_config(credentials), credentials)
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", secure_browser_config(credentials))

    def test_private_storage_object_denies_cross_tenant_read(self) -> None:
        self.assertEqual(insecure_storage_read(self.session_a, self.object_b), (200, b"B"))
        self.assertEqual(secure_storage_read(self.session_a, self.object_b), (404, None))
        self.assertEqual(secure_storage_read(self.session_b, self.object_b), (200, b"B"))

    def test_owner_cannot_be_changed_by_request_body(self) -> None:
        changed = unsafe_update_owner(self.rows[0], "user-b")
        self.assertEqual(changed.owner_id, "user-b")
        status, updated = secure_update_value(self.session_a, self.rows[0], "new value")
        self.assertEqual(status, 200)
        assert updated is not None
        self.assertEqual(updated.owner_id, "user-a")
        self.assertEqual(secure_update_value(self.session_b, self.rows[0], "stolen"), (403, None))


if __name__ == "__main__":
    unittest.main()
