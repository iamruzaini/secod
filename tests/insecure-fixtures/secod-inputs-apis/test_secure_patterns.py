"""Executable input and API-boundary expectations."""

from __future__ import annotations

import hashlib
import hmac
import json
import unittest

from fixture_app import (
    safe_command,
    safe_fetch,
    unsafe_command,
    unsafe_fetch,
    unsafe_webhook_event,
    validate_payload,
    verify_webhook,
)


class InputsApisFixtures(unittest.TestCase):
    def test_unsafe_fetch_reaches_private_address_but_safe_fetch_blocks_it(self) -> None:
        calls: list[object] = []

        def requester(target: object) -> str:
            calls.append(target)
            return "response"

        self.assertEqual(unsafe_fetch("http://169.254.169.254/metadata", requester), "response")
        self.assertEqual(
            safe_fetch(
                "https://api.example.test/data",
                requester,
                allowed_hosts={"api.example.test"},
                resolved_ips=["169.254.169.254"],
            ),
            (403, None),
        )
        self.assertEqual(calls, ["http://169.254.169.254/metadata"])

    def test_safe_fetch_rejects_host_not_in_allowlist(self) -> None:
        calls: list[str] = []
        self.assertEqual(
            safe_fetch(
                "https://evil.example.test/data",
                lambda target: calls.append(target) or "response",
                allowed_hosts={"api.example.test"},
                resolved_ips=["203.0.113.10"],
            ),
            (403, None),
        )
        self.assertEqual(calls, [])

    def test_safe_fetch_rechecks_dns_result(self) -> None:
        self.assertEqual(
            safe_fetch(
                "https://api.example.test/data",
                lambda _: "response",
                allowed_hosts={"api.example.test"},
                resolved_ips=["192.0.2.10", "10.0.0.8"],
            ),
            (403, None),
        )

    def test_allowlisted_public_fetch_is_allowed(self) -> None:
        calls: list[str] = []
        self.assertEqual(
            safe_fetch(
                "https://api.example.test/data",
                lambda target: calls.append(target) or "response",
                allowed_hosts={"api.example.test"},
                resolved_ips=["93.184.216.34"],
            ),
            (200, "response"),
        )
        self.assertEqual(calls, ["https://api.example.test/data"])

    def test_webhook_uses_raw_body_authentication(self) -> None:
        raw = json.dumps({"id": "evt-1", "amount": 10}, separators=(",", ":")).encode()
        secret = b"fixture-secret"
        signature = hmac.new(secret, raw, hashlib.sha256).hexdigest()
        self.assertEqual(verify_webhook(raw, signature, secret), {"id": "evt-1", "amount": 10})
        self.assertIsNone(verify_webhook(raw + b" ", signature, secret))
        self.assertEqual(unsafe_webhook_event({"id": "evt-1"}, "forged"), {"id": "evt-1"})

    def test_command_injection_is_not_passed_to_shell(self) -> None:
        unsafe_calls: list[object] = []
        unsafe_result = unsafe_command(
            "example.test; touch /tmp/pwned",
            lambda command: unsafe_calls.append(command) or command,
        )
        self.assertEqual(
            unsafe_result,
            "ping example.test; touch /tmp/pwned",
        )
        self.assertEqual(unsafe_calls, ["ping example.test; touch /tmp/pwned"])
        safe_calls: list[object] = []
        self.assertIsNone(
            safe_command(
                "example.test; touch /tmp/pwned",
                lambda command: safe_calls.append(command),
            )
        )
        self.assertEqual(safe_calls, [])
        self.assertEqual(
            safe_command(
                "example.test",
                lambda command: safe_calls.append(command) or command,
            ),
            ["ping", "--", "example.test"],
        )

    def test_schema_validation_rejects_malformed_payload(self) -> None:
        self.assertEqual(validate_payload({"id": "evt-1", "amount": 2}), (200, {"id": "evt-1", "amount": 2}))
        self.assertEqual(validate_payload({"id": "evt-1", "amount": "2"}), (422, None))
        self.assertEqual(validate_payload({"amount": 2}), (422, None))


if __name__ == "__main__":
    unittest.main()
