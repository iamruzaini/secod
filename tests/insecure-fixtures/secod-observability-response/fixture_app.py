"""Deterministic secure and unsafe behaviors for observability-response fixtures."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


SENSITIVE_FIELDS = {
    "authorization",
    "body",
    "cookie",
    "output",
    "password",
    "prompt",
    "secret",
    "session",
    "token",
}


class SinkUnavailable(RuntimeError):
    pass


def security_event(actor: str, action: str, target: str, outcome: str) -> dict[str, str]:
    return {
        "actor": actor,
        "action": action,
        "target": target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "outcome": outcome,
        "correlation_id": "fixture-correlation-id",
    }


def secure_redact(value: Any, key: str = "") -> Any:
    normalized = key.lower().replace("-", "_")
    if any(part in SENSITIVE_FIELDS for part in normalized.split("_")):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {item_key: secure_redact(item, item_key) for item_key, item in value.items()}
    if isinstance(value, list):
        return [secure_redact(item) for item in value]
    return value


def unsafe_shallow_redact(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    for key in SENSITIVE_FIELDS:
        if key in result:
            result[key] = "[REDACTED]"
    return result


@dataclass
class AuditSink:
    available: bool = True
    visible_failure: bool = True
    events: list[dict[str, str]] = field(default_factory=list)

    def emit(self, event: dict[str, str]) -> bool:
        if self.available:
            self.events.append(event)
            return True
        if self.visible_failure:
            raise SinkUnavailable("audit sink unavailable")
        return False


@dataclass
class KeyRegistry:
    enforce_revocation: bool = True
    revoked: set[str] = field(default_factory=set)
    events: list[dict[str, str]] = field(default_factory=list)

    def issue(self, key_id: str) -> None:
        self.events.append(security_event("system", "key.created", key_id, "success"))

    def revoke(self, key_id: str) -> None:
        self.revoked.add(key_id)
        self.events.append(security_event("operator", "key.revoked", key_id, "success"))

    def authorize(self, key_id: str) -> bool:
        allowed = not (self.enforce_revocation and key_id in self.revoked)
        outcome = "allowed" if allowed else "denied"
        self.events.append(security_event(key_id, "key.use", "fixture-endpoint", outcome))
        return allowed


@dataclass
class AlertRoute:
    recipients: list[str]
    delivery_enabled: bool
    deliveries: list[dict[str, str]] = field(default_factory=list)

    def trigger(self, alert_class: str) -> bool:
        if not self.recipients or not self.delivery_enabled:
            return False
        self.deliveries.append(
            {
                "alert_class": alert_class,
                "recipient": self.recipients[0],
                "delivered_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        return True


def runbook_status(*, covers_applicable_breaches: bool, dated_exercise: bool) -> str:
    return (
        "Passed with evidence"
        if covers_applicable_breaches and dated_exercise
        else "Not verified"
    )


def recovery_status(*, restore_artifact: bool, partial_recovery_observed: bool) -> str:
    return (
        "Passed with evidence"
        if restore_artifact and partial_recovery_observed
        else "Not verified"
    )


def external_evidence_status(
    *, production_sink: bool, alert_delivery: bool, runbook_exercise: bool, restore_drill: bool
) -> str:
    return (
        "Passed with evidence"
        if all((production_sink, alert_delivery, runbook_exercise, restore_drill))
        else "Not verified"
    )
