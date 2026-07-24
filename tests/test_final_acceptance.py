from __future__ import annotations

import copy
import hashlib

import pytest

from qso_runtime.core import GenomeInterpreter
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    verify_event_ledger,
)


def genome(*, max_events: int = 30) -> dict:
    return {
        "genome_id": "atlas",
        "purpose": "final bounded acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 3,
            "max_messages": 3,
            "max_events": max_events,
        },
        "freeze": {"human_review_required": True},
        "communication": {"allowed_peers": ["nova"]},
        "learning": {"input_boundary": "qso_seeker_canonical_records_only"},
    }


def identity() -> dict:
    return {
        "primary_name": "Atlas",
        "secondary_name": "Helix",
        "declared_name": "Atlas-Helix-Vespers",
    }


def record(label: str) -> dict:
    content = f"synthetic:{label}"
    return {
        "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "flags": [],
        "transformations": ["synthetic_fixture"],
    }


@pytest.mark.parametrize("operation", ["rollback", "high-severity-freeze"])
def test_exhausted_rollback_capacity_preserves_post_checkpoint_messages(operation: str) -> None:
    controller = RuntimeController.instantiate(genome(max_events=2), identity())
    controller.rollback()
    controller.send("nova", "proposal", {"claim": "preserve me"})
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError, match="event limit exceeded"):
        if operation == "rollback":
            controller.rollback()
        else:
            controller.freeze([{"severity": "high", "reason": "synthetic fixture"}])

    assert controller.status == "active"
    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before
    assert controller.qso.p.outbox[0].payload == {"claim": "preserve me"}
    assert verify_event_ledger(controller.qso.p.events) == []


def test_surrogate_record_is_rejected_before_state_or_ledger_mutation() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    malformed = record("surrogate")
    malformed["flags"] = ["\ud800"]
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError, match="UTF-8 encodable"):
        controller.ingest(malformed)

    assert controller.qso.p.records == []
    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before


def test_public_record_event_rejects_noncanonical_payload_atomically() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    events_before = copy.deepcopy(controller.qso.p.events)
    ledger_before = event_ledger_sha256(controller.qso)

    with pytest.raises(ValueError, match="finite JSON"):
        controller.qso.record_event("invalid", {"value": float("nan")})

    assert controller.qso.p.events == events_before
    assert event_ledger_sha256(controller.qso) == ledger_before
    assert verify_event_ledger(controller.qso.p.events) == []


@pytest.mark.parametrize("target", ["genome", "identity"])
def test_noncanonical_instantiation_inputs_fail_at_controller_boundary(target: str) -> None:
    candidate_genome = genome()
    candidate_identity = identity()
    if target == "genome":
        candidate_genome["mutable"]["invalid"] = float("inf")
    else:
        candidate_identity["annotation"] = "\udfff"

    with pytest.raises(RuntimeInvariantError, match="finite JSON|UTF-8 encodable"):
        RuntimeController.instantiate(candidate_genome, candidate_identity)


def test_valid_inputs_and_direct_events_remain_deterministic() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    for controller in controllers:
        controller.qso.record_event("bounded_check", {"sample": [1, "two", None]})
        assert verify_event_ledger(controller.qso.p.events) == []

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)
