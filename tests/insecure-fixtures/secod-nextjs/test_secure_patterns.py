"""Executable Next.js boundary expectations."""

from __future__ import annotations

import unittest

from fixture_app import (
    Record,
    Session,
    secure_cache_key,
    secure_client_config,
    secure_server_action,
    unsafe_cache_key,
    unsafe_client_config,
    unsafe_server_action,
)


class NextjsFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.records = {
            ("tenant-a", "record-a"): Record("record-a", "tenant-a", "user-a", "A"),
            ("tenant-b", "record-b"): Record("record-b", "tenant-b", "user-b", "B"),
        }
        self.user_a = Session("user-a", "tenant-a", frozenset({"member"}))

    def test_direct_action_invocation_cannot_cross_tenant(self) -> None:
        forged_request = {
            "tenant_id": "tenant-b",
            "record_id": "record-b",
            "role": "tenant-admin",
        }
        self.assertEqual(unsafe_server_action(self.records, forged_request), (200, "B"))
        self.assertEqual(
            secure_server_action(self.records, self.user_a, record_id="record-b", cache={}),
            (404, None),
        )

    def test_owner_can_use_server_action(self) -> None:
        self.assertEqual(
            secure_server_action(self.records, self.user_a, record_id="record-a", cache={}),
            (200, "A"),
        )

    def test_unauthenticated_direct_action_is_rejected(self) -> None:
        anonymous = Session("anonymous", "tenant-a", frozenset(), authenticated=False)
        self.assertEqual(
            secure_server_action(self.records, anonymous, record_id="record-a", cache={}),
            (401, None),
        )

    def test_server_secret_stays_out_of_client_configuration(self) -> None:
        environment = {
            "DATABASE_URL": "server-only",
            "NEXT_PUBLIC_APP_NAME": "fixture",
        }
        self.assertEqual(unsafe_client_config(environment), environment)
        self.assertEqual(secure_client_config(environment), {"NEXT_PUBLIC_APP_NAME": "fixture"})

    def test_cache_key_is_scoped_to_trusted_identity(self) -> None:
        user_b = Session("user-b", "tenant-b", frozenset({"member"}))
        self.assertEqual(unsafe_cache_key("dashboard"), unsafe_cache_key("dashboard"))
        self.assertNotEqual(
            secure_cache_key(self.user_a, "dashboard"),
            secure_cache_key(user_b, "dashboard"),
        )
        cache: dict[str, str] = {}
        secure_server_action(self.records, self.user_a, record_id="record-a", cache=cache)
        self.assertEqual(cache, {secure_cache_key(self.user_a, "record-a"): "A"})


if __name__ == "__main__":
    unittest.main()
