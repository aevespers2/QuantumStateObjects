from __future__ import annotations

import copy
import hashlib
from typing import Any

import pytest

from qso_runtime.core import GenomeInterpreter
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    canonical_state,
    event_ledger_sha256,
    state_sha256,
    verify_event_ledger,
)


def genome() -> dict[str, Any]:
    return {
        "genome_id": "atlas",
        "purpose": "freeze annotation severity acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 4,
            "max_messages": 4,
            "max_events": 20,
        },
        "freeze": {"human_review_required": True},
        "communication": {"allowed_peers": ["nova"]},
        "learning": {"input_boundary": "qso_seeker_canonical_records_only"},
    }


def identity() -> dict[str, str]:
    return {
        "primary_name": "Atlas",
        "secondary_name": "Helix",
        "declared_name": "Atlas-Helix-Vespers",
    }


def record(label: str) -> dict[str, Any]:
    content = f"synthetic:{label}"
    return {
        "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "flags": [],
        "transformations": ["synthetic_fixture"],
    }


@pytest.mark.parametrize(
    ("severity", "decision", "status", "event_kind"),
    [
        ("low", "frozen_pending_external_commit", "frozen", "freeze"),
        ("high", "rollback", "active", "rollback"),
    ],
)
def test_string_severity_values_drive_expected_freeze_paths(
    severity: str,
    decision: str,
    status: str,
    event_kind: str,
) -> None:
    controller = RuntimeController.instantiate(genome(), identity())

    result = controller.freeze([{"severity": severity, "reason": "bounded fixture"}])

    assert result["decision"] == decision
    assert controller.status == status
    assert controller.qso.p.events[-1]["kind"] == event_kind
    assert verify_event_ledger(controller.qso.p.events) == []


@pytest.mark.parametrize(
    "invalid_severity",
    [
        pytest.param(["high"], id="list"),
        pytest.param({"level": "high"}, id="object"),
        pytest.param(None, id="null"),
        pytest.param(True, id="boolean-true"),
        pytest.param(False, id="boolean-false"),
        pytest.param(0, id="integer-zero"),
        pytest.param(7, id="integer-positive"),
        pytest.param(-2.5, id="float"),
        pytest.param("\ud800", id="lone-surrogate"),
        pytest.param({"high"}, id="set"),
        pytest.param(("high",), id="tuple"),
    ],
)
def test_invalid_severity_values_raise_runtime_invariant_error(
    invalid_severity: object,
) -> None:
    controller = RuntimeController.instantiate(genome(), identity())

    with pytest.raises(
        RuntimeInvariantError,
        match=r"freeze annotations\[0\]\.severity",
    ):
        controller.freeze([{"severity": invalid_severity}])


def test_invalid_severity_is_atomic_before_any_runtime_mutation() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    state_before = copy.deepcopy(canonical_state(controller.qso))
    checkpoint_before = controller.checkpoint
    events_before = copy.deepcopy(controller.qso.p.events)
    status_before = controller.status

    with pytest.raises(RuntimeInvariantError):
        controller.freeze([{"severity": ["high"]}])

    assert canonical_state(controller.qso) == state_before
    assert controller.checkpoint == checkpoint_before
    assert controller.qso.p.events == events_before
    assert controller.status == status_before


def test_invalid_high_like_severity_preserves_freeze_checkpoint_and_transient_state() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("checkpoint"))
    controller.freeze([])
    checkpoint_before = controller.checkpoint
    controller.resume()
    controller.ingest(record("transient"))
    transient_state_before = copy.deepcopy(canonical_state(controller.qso))

    with pytest.raises(RuntimeInvariantError):
        controller.freeze([{"severity": ["high"], "reason": "must not rollback"}])

    assert canonical_state(controller.qso) == transient_state_before
    assert controller.checkpoint == checkpoint_before
    assert [item["content"] for item in controller.qso.p.records] == [
        "synthetic:checkpoint",
        "synthetic:transient",
    ]
    assert controller.status == "active"


def test_invalid_severity_does_not_append_or_rewrite_event_ledger() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("ledger"))
    events_before = copy.deepcopy(controller.qso.p.events)
    ledger_hash_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError):
        controller.freeze([{"severity": {"level": "critical"}}])

    assert controller.qso.p.events == events_before
    assert event_ledger_sha256(controller.qso) == ledger_hash_before
    assert verify_event_ledger(controller.qso.p.events) == []


def test_invalid_severity_failures_preserve_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    state_hashes_before = [state_sha256(controller.qso) for controller in controllers]
    event_hashes_before = [event_ledger_sha256(controller.qso) for controller in controllers]
    errors: list[str] = []

    for controller in controllers:
        with pytest.raises(RuntimeInvariantError) as exc_info:
            controller.freeze([{"severity": 1}])
        errors.append(str(exc_info.value))

    assert errors == [
        "freeze annotations[0].severity must be a string",
        "freeze annotations[0].severity must be a string",
    ]
    assert [state_sha256(controller.qso) for controller in controllers] == state_hashes_before
    assert [event_ledger_sha256(controller.qso) for controller in controllers] == event_hashes_before
    assert state_hashes_before[0] == state_hashes_before[1]
    assert event_hashes_before[0] == event_hashes_before[1]
