"""Executable identity and authorization expectations."""

from __future__ import annotations

import unittest

from fixture_app import (
    Record,
    Session,
    secure_authorize_role,
    secure_read_record,
    unsafe_authorize_role,
    unsafe_read_record,
)


class IdentityAccessFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.records = {
            ("tenant-a", "record-a"): Record("record-a", "tenant-a", "user-a", "A"),
            ("tenant-b", "record-b"): Record("record-b", "tenant-b", "user-b", "B"),
        }
        self.user_a = Session("user-a", "tenant-a", frozenset({"member"}))

    def test_cross_tenant_request_is_exposed_by_unsafe_boundary(self) -> None:
        self.assertEqual(
            unsafe_read_record(
                self.records,
                requested_tenant="tenant-b",
                requested_record="record-b",
            ),
            (200, "B"),
        )
        self.assertEqual(secure_read_record(self.records, self.user_a, record_id="record-b"), (404, None))

    def test_owner_can_read_record_in_own_tenant(self) -> None:
        self.assertEqual(secure_read_record(self.records, self.user_a, record_id="record-a"), (200, "A"))

    def test_same_tenant_non_owner_is_denied(self) -> None:
        other_user = Session("user-other", "tenant-a", frozenset({"member"}))
        self.assertEqual(secure_read_record(self.records, other_user, record_id="record-a"), (403, None))

    def test_unauthenticated_request_is_denied(self) -> None:
        anonymous = Session("anonymous", "tenant-a", frozenset(), authenticated=False)
        self.assertEqual(secure_read_record(self.records, anonymous, record_id="record-a"), (401, None))

    def test_client_role_forgery_does_not_define_secure_authorization(self) -> None:
        self.assertTrue(unsafe_authorize_role(requested_role="admin", required_role="admin"))
        self.assertFalse(secure_authorize_role(self.user_a, required_role="tenant-admin"))

    def test_verified_tenant_admin_can_read_tenant_record(self) -> None:
        admin = Session("user-admin", "tenant-a", frozenset({"tenant-admin"}))
        self.assertEqual(secure_read_record(self.records, admin, record_id="record-a"), (200, "A"))


if __name__ == "__main__":
    unittest.main()
