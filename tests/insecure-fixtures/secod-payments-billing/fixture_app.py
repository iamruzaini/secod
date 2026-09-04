"""Deterministic provider-neutral payment behaviors for fixture tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import hashlib
import hmac
import json


@dataclass(frozen=True)
class CapabilityRow:
    adapter: str
    has_signature: bool = True
    has_timestamp: bool = True
    has_delivery_id: bool = True
    has_event_type: bool = True
    has_account_context: bool = True
    has_api_version: bool = True
    has_retry_behavior: bool = True
    has_disabled_endpoint_behavior: bool = True
    source_refs: tuple[str, ...] = ()
    compensating_controls: tuple[str, ...] = ()


@dataclass(frozen=True)
class SourceRecord:
    direct_primary: bool
    status: str
    review_expiry: date


def capability_status(
    row: CapabilityRow,
    sources: dict[str, SourceRecord],
    *,
    reviewed_on: date,
) -> str:
    if not row.adapter or not row.source_refs:
        return "Not verified"
    for source_ref in row.source_refs:
        source = sources.get(source_ref)
        if (
            source is None
            or not source.direct_primary
            or source.status != "Reviewed"
            or source.review_expiry < reviewed_on
        ):
            return "Not verified"
    if not row.has_delivery_id:
        required = {"stable-dedup-key", "replay-ledger", "provider-retrieval", "reconciliation"}
        if not required.issubset(row.compensating_controls):
            return "Not verified"
    if not row.has_signature or not row.has_event_type or not row.has_account_context:
        return "Not verified"
    if not row.has_retry_behavior or not row.has_disabled_endpoint_behavior:
        return "Not verified"
    return "Passed with evidence"


def resolve_checkout(
    request: dict[str, object],
    catalog: dict[str, dict[str, object]],
    *,
    trust_client: bool,
) -> dict[str, object]:
    product = catalog[str(request["product_id"])]
    if trust_client:
        return {
            "product_id": request["product_id"],
            "amount": request["amount"],
            "currency": request["currency"],
            "tenant": request["tenant"],
            "entitlement": request["entitlement"],
        }
    return dict(product)


def card_fields(*, hosted_checkout: bool) -> tuple[str, ...]:
    return () if hosted_checkout else ("card_number", "cvc")


@dataclass
class PaymentWriter:
    results: dict[str, str] = field(default_factory=dict)
    mutations: list[str] = field(default_factory=list)

    def write(self, intent: str, idempotency_key: str) -> str:
        if idempotency_key in self.results:
            return self.results[idempotency_key]
        result = f"mutation-{len(self.mutations) + 1}"
        self.mutations.append(intent)
        self.results[idempotency_key] = result
        return result


def session_is_bounded(expires_at: int | None) -> bool:
    return expires_at is not None and expires_at > 0


def accepts_version(event_version: str, pinned_version: str, *, fail_closed: bool) -> bool:
    return event_version == pinned_version or not fail_closed


def grants_entitlement(*, provider_verified: bool, client_paid: bool, trust_client: bool) -> bool:
    return provider_verified or (trust_client and client_paid)


def sign_webhook(secret: bytes, raw_body: bytes, timestamp: int) -> str:
    message = str(timestamp).encode("ascii") + b"." + raw_body
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


@dataclass
class WebhookProcessor:
    secret: bytes
    current_time: int
    tolerance: int = 300
    seen: set[str] = field(default_factory=set)

    def process(
        self,
        raw_body: bytes,
        *,
        signature: str,
        timestamp: int,
        delivery_id: str,
        capability: CapabilityRow,
        expected_event_types: set[str],
        expected_account: str,
        expected_api_version: str,
    ) -> str:
        if capability.has_signature:
            expected = sign_webhook(self.secret, raw_body, timestamp)
            if not hmac.compare_digest(signature, expected):
                return "rejected-signature"
        if capability.has_timestamp and abs(self.current_time - timestamp) > self.tolerance:
            return "rejected-stale"
        if capability.has_delivery_id and delivery_id in self.seen:
            return "duplicate"
        event = json.loads(raw_body)
        if capability.has_event_type and event.get("type") not in expected_event_types:
            return "rejected-event-type"
        if capability.has_account_context and event.get("account") != expected_account:
            return "rejected-account"
        if capability.has_api_version and event.get("api_version") != expected_api_version:
            return "rejected-version"
        if capability.has_delivery_id:
            self.seen.add(delivery_id)
        return "accepted"


@dataclass
class DeliveryStore:
    seen: set[str] = field(default_factory=set)
    sequence: int = 0
    state: str = "pending"

    def apply(self, delivery_id: str, sequence: int, state: str) -> str:
        if delivery_id in self.seen:
            return "duplicate"
        self.seen.add(delivery_id)
        if sequence <= self.sequence:
            return "out-of-order-ignored"
        self.sequence = sequence
        self.state = state
        return "applied"

    def reconcile(self, provider_state: str, provider_sequence: int) -> None:
        self.state = provider_state
        self.sequence = provider_sequence


def delivery_readiness(
    *,
    retry_exhaustion_detected: bool,
    disabled_endpoint_detected: bool,
    reconciliation: bool,
    persistent_deduplication: bool,
    persisted_before_ack: bool,
) -> str:
    return (
        "Passed with evidence"
        if (
            retry_exhaustion_detected
            and disabled_endpoint_detected
            and reconciliation
            and persistent_deduplication
            and persisted_before_ack
        )
        else "Fix before launch"
    )


@dataclass
class MappingStore:
    customer_user: dict[str, str] = field(default_factory=dict)
    entitlements: set[tuple[str, str]] = field(default_factory=set)
    pending: list[str] = field(default_factory=list)

    def map_event(
        self,
        customer: str,
        user: str,
        tenant: str,
        *,
        fail_after_mapping: bool,
        recoverable: bool,
        trusted_tenant: str,
        trust_event_tenant: bool,
    ) -> None:
        before_mapping = dict(self.customer_user)
        before_entitlements = set(self.entitlements)
        self.customer_user[customer] = user
        try:
            if fail_after_mapping:
                raise RuntimeError("injected mapping failure")
            resolved_tenant = tenant if trust_event_tenant else trusted_tenant
            self.entitlements.add((user, resolved_tenant))
        except RuntimeError:
            if recoverable:
                self.customer_user = before_mapping
                self.entitlements = before_entitlements
                self.pending.append(customer)
            raise


@dataclass
class Ledger:
    entries: list[tuple[str, str]] = field(default_factory=list)
    entitlement: str = "none"

    def record(self, event: str, entitlement: str, *, append_only: bool) -> None:
        if append_only or not self.entries:
            self.entries.append((event, entitlement))
        else:
            self.entries[-1] = (event, entitlement)
        self.entitlement = entitlement


def credential_status(credentials: dict[str, str]) -> str:
    if any(
        name.startswith("NEXT_PUBLIC_") and value.startswith("live_")
        for name, value in credentials.items()
    ):
        return "Do not ship"
    live_values = [value for name, value in credentials.items() if name.endswith("_LIVE")]
    test_values = [value for name, value in credentials.items() if name.endswith("_TEST")]
    if set(live_values) & set(test_values):
        return "Not verified"
    return "Passed with evidence"


def evidence_status(repository: bool, provider: bool, production: bool) -> str:
    return "Passed with evidence" if all((repository, provider, production)) else "Not verified"
