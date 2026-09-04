"""Deterministic package-delivery evidence and unsafe-pattern fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re


CONTROL_IDS = tuple(f"PROVISIONAL-packages-{number}" for number in range(1, 13))
EXTERNAL_EVIDENCE_CONTROLS = frozenset(
    {
        "PROVISIONAL-packages-2",
        "PROVISIONAL-packages-3",
        "PROVISIONAL-packages-4",
        "PROVISIONAL-packages-7",
        "PROVISIONAL-packages-8",
        "PROVISIONAL-packages-9",
        "PROVISIONAL-packages-10",
        "PROVISIONAL-packages-11",
    }
)
ISSUE_OUTCOMES = {
    "missing-lockfile": ("PROVISIONAL-packages-1", "Fix before launch"),
    "no-supported-version-policy": ("PROVISIONAL-packages-2", "Fix before launch"),
    "untrusted-registry-and-scripts": ("PROVISIONAL-packages-3", "Fix before launch"),
    "workflow-write-all": ("PROVISIONAL-packages-4", "Fix before launch"),
    "privileged-pr-checkout": ("PROVISIONAL-packages-5", "Do not ship"),
    "short-sha-with-digest-check": ("PROVISIONAL-packages-5", "Recommended hardening"),
    "unpinned-build-fetch": ("PROVISIONAL-packages-6", "Fix before launch"),
    "ungated-production": ("PROVISIONAL-packages-7", "Fix before launch"),
    "mutable-production-tag": ("PROVISIONAL-packages-8", "Fix before launch"),
    "attestation-not-verified": ("PROVISIONAL-packages-9", "Fix before launch"),
    "signing-key-in-repository": ("PROVISIONAL-packages-10", "Do not ship"),
    "no-rollback-path": ("PROVISIONAL-packages-11", "Fix before launch"),
    "stale-primary-source": ("PROVISIONAL-packages-12", "Not verified"),
}
STATUS_PRIORITY = {
    "Passed with evidence": 0,
    "Not verified": 1,
    "Recommended hardening": 2,
    "Fix before launch": 3,
    "Do not ship": 4,
}


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    direct_url: str
    reviewed: date
    expires: date
    status: str
    fingerprint: str


@dataclass(frozen=True)
class ReviewEvidence:
    repository_controls: frozenset[str]
    external_controls: frozenset[str]
    negative_test_controls: frozenset[str]
    issues: frozenset[str]
    sources: tuple[SourceRecord, ...]
    reviewed_on: date


def parse_source_register(path: Path) -> tuple[SourceRecord, ...]:
    records: list[SourceRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| PKG-S"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 10:
            raise ValueError(f"source row needs 10 cells: {line}")
        records.append(
            SourceRecord(
                source_id=cells[0],
                direct_url=cells[2],
                reviewed=date.fromisoformat(cells[4]),
                expires=date.fromisoformat(cells[5][:10]),
                status=cells[6],
                fingerprint=cells[9],
            )
        )
    return tuple(records)


def source_register_ready(records: tuple[SourceRecord, ...], reviewed_on: date) -> bool:
    expected_ids = {f"PKG-S{number}" for number in range(1, 9)}
    if {record.source_id for record in records} != expected_ids:
        return False
    return all(
        record.direct_url.startswith("https://")
        and record.status == "Reviewed"
        and record.reviewed <= reviewed_on <= record.expires
        and re.search(r"[0-9a-f]{64}", record.fingerprint) is not None
        for record in records
    )


def evaluate(evidence: ReviewEvidence) -> dict[str, str]:
    sources_ready = source_register_ready(evidence.sources, evidence.reviewed_on)
    outcomes = {control_id: "Passed with evidence" for control_id in CONTROL_IDS}
    for issue in evidence.issues:
        control_id, status = ISSUE_OUTCOMES[issue]
        if STATUS_PRIORITY[status] > STATUS_PRIORITY[outcomes[control_id]]:
            outcomes[control_id] = status
    for control_id in CONTROL_IDS:
        if outcomes[control_id] != "Passed with evidence":
            continue
        if not sources_ready:
            outcomes[control_id] = "Not verified"
        elif control_id not in evidence.repository_controls:
            outcomes[control_id] = "Not verified"
        elif control_id not in evidence.negative_test_controls:
            outcomes[control_id] = "Not verified"
        elif (
            control_id in EXTERNAL_EVIDENCE_CONTROLS
            and control_id not in evidence.external_controls
        ):
            outcomes[control_id] = "Not verified"
    return outcomes


def complete_evidence(
    sources: tuple[SourceRecord, ...], reviewed_on: date
) -> ReviewEvidence:
    all_controls = frozenset(CONTROL_IDS)
    return ReviewEvidence(
        repository_controls=all_controls,
        external_controls=EXTERNAL_EVIDENCE_CONTROLS,
        negative_test_controls=all_controls,
        issues=frozenset(),
        sources=sources,
        reviewed_on=reviewed_on,
    )


def action_ref_is_full_sha(reference: str) -> bool:
    return re.fullmatch(r"[^@\s]+@[0-9a-fA-F]{40}", reference) is not None


def privileged_pr_flow_is_safe(
    *, trigger: str, checkout_pr_head: bool, privileged_credentials: bool
) -> bool:
    privileged_trigger = trigger in {"pull_request_target", "workflow_run"}
    return not (privileged_trigger and checkout_pr_head and privileged_credentials)


def artifact_ref_is_immutable(reference: str) -> bool:
    return re.fullmatch(r"[^@\s]+@sha256:[0-9a-fA-F]{64}", reference) is not None


def verification_fails_closed(command: str) -> bool:
    normalized = " ".join(command.lower().split())
    return "verify" in normalized and "|| true" not in normalized and "continue-on-error" not in normalized
