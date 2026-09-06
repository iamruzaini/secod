"""Executable secure-pattern tests for crypto and data protection."""

from __future__ import annotations

import unittest

from fixture_app import hash_password, public_response, validate_key_source, verify_password


class CryptoDataProtectionFixtures(unittest.TestCase):
    def test_password_hash_uses_random_salt(self) -> None:
        first = hash_password("fixture-password")
        second = hash_password("fixture-password")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("fixture-password", *first))
        self.assertFalse(verify_password("wrong-password", *first))

    def test_secret_never_enters_public_response(self) -> None:
        secret = "fixture-secret"
        self.assertNotIn(secret, public_response(secret).values())

    def test_key_source_rejects_repository_literal(self) -> None:
        self.assertTrue(validate_key_source("workload-identity"))
        self.assertTrue(validate_key_source("secret-manager"))
        self.assertFalse(validate_key_source("repository-literal"))
