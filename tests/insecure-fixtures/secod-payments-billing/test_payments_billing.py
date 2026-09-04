"""Executable expectations for provider-neutral payments-billing fixture cases."""

from __future__ import annotations

from datetime import date
import json
import unittest

from fixture_app import (
    CapabilityRow,
    DeliveryStore,
    Ledger,
    MappingStore,
    PaymentWriter,
    SourceRecord,
    WebhookProcessor,
    accepts_version,
    capability_status,
    card_fields,
    credential_status,
    delivery_readiness,
    evidence_status,
    grants_entitlement,
    resolve_checkout,
    session_is_bounded,
    sign_webhook,
)


CATALOG = {
    "pro": {
        "product_id": "pro",
        "amount": 2500,
        "currency": "USD",
        "tenant": "tenant-a",
        "entitlement": "pro",
    }
}


class PaymentsBillingFixtures(unittest.TestCase):
    def test_01_clean_integration(self) -> None:
        request = {
            "product_id": "pro",
            "amount": 1,
            "currency": "XXX",
            "tenant": "tenant-b",
            "entitlement": "admin",
        }
        self.assertEqual(resolve_checkout(request, CATALOG, trust_client=False), CATALOG["pro"])
        self.assertEqual(card_fields(hosted_checkout=True), ())
        self.assertTrue(
            grants_entitlement(provider_verified=True, client_paid=False, trust_client=False)
        )
        store = MappingStore()
        store.map_event(
            "customer-1",
            "user-1",
            "tenant-a",
            fail_after_mapping=False,
            recoverable=True,
            trusted_tenant="tenant-a",
            trust_event_tenant=False,
        )
        self.assertEqual(store.entitlements, {("user-1", "tenant-a")})

    def test_02_client_price_and_tenant_tampering(self) -> None:
        request = {
            "product_id": "pro",
            "amount": 1,
            "currency": "XXX",
            "tenant": "tenant-b",
            "entitlement": "admin",
        }
        unsafe = resolve_checkout(request, CATALOG, trust_client=True)
        self.assertEqual(
            (unsafe["amount"], unsafe["tenant"], unsafe["entitlement"]),
            (1, "tenant-b", "admin"),
        )

    def test_03_raw_card_collection(self) -> None:
        self.assertEqual(card_fields(hosted_checkout=False), ("card_number", "cvc"))

    def test_04_outbound_idempotency_and_expiration(self) -> None:
        secure = PaymentWriter()
        secure.write("refund-order-1", "refund:order-1")
        secure.write("refund-order-1", "refund:order-1")
        self.assertEqual(len(secure.mutations), 1)

        unsafe = PaymentWriter()
        unsafe.write("refund-order-1", "attempt-1")
        unsafe.write("refund-order-1", "attempt-2")
        self.assertEqual(len(unsafe.mutations), 2)
        self.assertFalse(session_is_bounded(None))

    def test_05_unexpected_api_version(self) -> None:
        self.assertFalse(accepts_version("2026-09", "2026-08", fail_closed=True))
        self.assertTrue(accepts_version("2026-09", "2026-08", fail_closed=False))

    def test_06_client_reported_paid_state(self) -> None:
        self.assertFalse(
            grants_entitlement(provider_verified=False, client_paid=True, trust_client=False)
        )
        self.assertTrue(
            grants_entitlement(provider_verified=False, client_paid=True, trust_client=True)
        )

    def test_07_webhook_authenticity_freshness_and_replay(self) -> None:
        raw = json.dumps(
            {
                "type": "payment.succeeded",
                "account": "acct-1",
                "api_version": "2026-08",
            }
        ).encode()
        row = CapabilityRow(adapter="secod-fixture", source_refs=("ADAPTER-S1",))
        processor = WebhookProcessor(secret=b"fixture-secret", current_time=1000)
        valid = sign_webhook(b"fixture-secret", raw, 1000)
        self.assertEqual(
            processor.process(
                raw,
                signature="forged",
                timestamp=1000,
                delivery_id="evt-1",
                capability=row,
                expected_event_types={"payment.succeeded"},
                expected_account="acct-1",
                expected_api_version="2026-08",
            ),
            "rejected-signature",
        )
        self.assertEqual(
            processor.process(
                raw,
                signature=sign_webhook(b"fixture-secret", raw, 1),
                timestamp=1,
                delivery_id="evt-1",
                capability=row,
                expected_event_types={"payment.succeeded"},
                expected_account="acct-1",
                expected_api_version="2026-08",
            ),
            "rejected-stale",
        )
        self.assertEqual(
            processor.process(
                raw,
                signature=valid,
                timestamp=1000,
                delivery_id="evt-1",
                capability=row,
                expected_event_types={"payment.succeeded"},
                expected_account="acct-1",
                expected_api_version="2026-08",
            ),
            "accepted",
        )
        self.assertEqual(
            processor.process(
                raw,
                signature=valid,
                timestamp=1000,
                delivery_id="evt-1",
                capability=row,
                expected_event_types={"payment.succeeded"},
                expected_account="acct-1",
                expected_api_version="2026-08",
            ),
            "duplicate",
        )
        wrong_context = json.dumps(
            {
                "type": "payment.succeeded",
                "account": "attacker-account",
                "api_version": "2026-08",
            }
        ).encode()
        self.assertEqual(
            processor.process(
                wrong_context,
                signature=sign_webhook(b"fixture-secret", wrong_context, 1000),
                timestamp=1000,
                delivery_id="evt-2",
                capability=row,
                expected_event_types={"payment.succeeded"},
                expected_account="acct-1",
                expected_api_version="2026-08",
            ),
            "rejected-account",
        )

    def test_08_delivery_order_retry_disablement_and_reconciliation(self) -> None:
        store = DeliveryStore()
        self.assertEqual(store.apply("evt-2", 2, "active"), "applied")
        self.assertEqual(store.apply("evt-1", 1, "pending"), "out-of-order-ignored")
        self.assertEqual(store.apply("evt-2", 2, "active"), "duplicate")
        store.reconcile("revoked", 3)
        self.assertEqual((store.state, store.sequence), ("revoked", 3))
        self.assertEqual(
            delivery_readiness(
                retry_exhaustion_detected=False,
                disabled_endpoint_detected=False,
                reconciliation=True,
                persistent_deduplication=False,
                persisted_before_ack=False,
            ),
            "Fix before launch",
        )
        self.assertEqual(
            delivery_readiness(
                retry_exhaustion_detected=True,
                disabled_endpoint_detected=True,
                reconciliation=True,
                persistent_deduplication=True,
                persisted_before_ack=True,
            ),
            "Passed with evidence",
        )

    def test_09_atomic_mapping_and_tenant_binding(self) -> None:
        secure = MappingStore()
        with self.assertRaises(RuntimeError):
            secure.map_event(
                "customer-1",
                "user-1",
                "tenant-a",
                fail_after_mapping=True,
                recoverable=True,
                trusted_tenant="tenant-a",
                trust_event_tenant=False,
            )
        self.assertEqual(secure.customer_user, {})
        self.assertEqual(secure.entitlements, set())
        self.assertEqual(secure.pending, ["customer-1"])

        unsafe = MappingStore()
        with self.assertRaises(RuntimeError):
            unsafe.map_event(
                "customer-1",
                "user-1",
                "attacker-tenant",
                fail_after_mapping=True,
                recoverable=False,
                trusted_tenant="tenant-a",
                trust_event_tenant=True,
            )
        self.assertEqual(unsafe.customer_user, {"customer-1": "user-1"})
        self.assertEqual(unsafe.entitlements, set())

    def test_10_lifecycle_correction_and_append_only_ledger(self) -> None:
        ledger = Ledger()
        ledger.record("payment", "pro", append_only=True)
        ledger.record("renewal-failed", "grace", append_only=True)
        ledger.record("cancellation", "none", append_only=True)
        ledger.record("expiration", "none", append_only=True)
        ledger.record("refund", "none", append_only=True)
        ledger.record("dispute", "revoked", append_only=True)
        ledger.record("chargeback", "revoked", append_only=True)
        self.assertEqual(ledger.entitlement, "revoked")
        self.assertEqual(len(ledger.entries), 7)

        unsafe = Ledger()
        unsafe.record("payment", "pro", append_only=False)
        unsafe.record("refund", "none", append_only=False)
        self.assertEqual(unsafe.entries, [("refund", "none")])

    def test_11_credential_isolation(self) -> None:
        self.assertEqual(
            credential_status(
                {"PAYMENTS_LIVE": "live_prod", "PAYMENTS_TEST": "test_preview"}
            ),
            "Passed with evidence",
        )
        self.assertEqual(
            credential_status({"NEXT_PUBLIC_PAYMENTS_KEY": "live_secret"}),
            "Do not ship",
        )
        self.assertEqual(
            credential_status({"PAYMENTS_LIVE": "same", "PAYMENTS_TEST": "same"}),
            "Not verified",
        )

    def test_12_capability_source_and_adapter_blockers(self) -> None:
        reviewed = {
            "ADAPTER-S1": SourceRecord(True, "Reviewed", date(2027, 2, 27))
        }
        reviewed_on = date(2026, 8, 27)
        self.assertEqual(
            capability_status(
                CapabilityRow(adapter="secod-fixture", source_refs=("ADAPTER-S1",)),
                reviewed,
                reviewed_on=reviewed_on,
            ),
            "Passed with evidence",
        )
        self.assertEqual(
            capability_status(
                CapabilityRow(adapter="", source_refs=("ADAPTER-S1",)),
                reviewed,
                reviewed_on=reviewed_on,
            ),
            "Not verified",
        )
        self.assertEqual(
            capability_status(
                CapabilityRow(adapter="secod-fixture"),
                reviewed,
                reviewed_on=reviewed_on,
            ),
            "Not verified",
        )
        no_id = CapabilityRow(
            adapter="secod-fixture",
            has_delivery_id=False,
            source_refs=("ADAPTER-S1",),
        )
        self.assertEqual(
            capability_status(no_id, reviewed, reviewed_on=reviewed_on),
            "Not verified",
        )

    def test_13_missing_provider_and_production_evidence(self) -> None:
        self.assertEqual(
            evidence_status(repository=True, provider=False, production=False),
            "Not verified",
        )


if __name__ == "__main__":
    unittest.main()
