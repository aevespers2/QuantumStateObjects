from __future__ import annotations

import copy
import hashlib

import pytest

from qso_runtime.attribution import AttributionJourneyLedger, ContributorCredit
from qso_runtime.core import GenomeInterpreter, MCPMessage
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    validate_message,
    verify_event_ledger,
)


def genome(*, max_records: int = 3, max_messages: int = 2, max_events: int = 30) -> dict:
    return {
        "genome_id": "atlas",
        "purpose": "deterministic runtime primitive verification",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": max_records,
            "max_messages": max_messages,
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


def test_instance_lifecycle_is_active_and_invalid_genome_fails_closed() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    assert controller.status == "active"
    assert [event["kind"] for event in controller.qso.p.events] == ["instantiated"]
    assert verify_event_ledger(controller.qso.p.events) == []

    invalid = genome()
    invalid.pop("freeze")
    with pytest.raises(ValueError, match="missing genome fields"):
        RuntimeController.instantiate(invalid, identity())


def test_message_validation_accepts_canonical_and_rejects_tampering() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    message = controller.send("nova", "proposal", {"claim": "bounded"})
    validate_message(
        message,
        allowed_senders={"atlas"},
        allowed_recipients={"nova"},
    )

    tampered = MCPMessage(
        sender=message.sender,
        recipient=message.recipient,
        kind=message.kind,
        payload={"claim": "changed"},
        sha256=message.sha256,
    )
    with pytest.raises(RuntimeInvariantError, match="integrity"):
        validate_message(tampered)

    unauthorized = MCPMessage.build("unknown", "atlas", "annotation", {"x": 1})
    with pytest.raises(RuntimeInvariantError, match="sender"):
        controller.receive(unauthorized)


def test_event_ledger_is_hash_linked_and_tamper_evident() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("one"))
    assert verify_event_ledger(controller.qso.p.events) == []
    original_hash = event_ledger_sha256(controller.qso)

    tampered = copy.deepcopy(controller.qso.p.events)
    tampered[1]["payload"]["sha256"] = "0" * 64
    errors = verify_event_ledger(tampered)
    assert "event hash mismatch at 1" in errors
    assert event_ledger_sha256(controller.qso) == original_hash


def test_attribution_ledger_is_deterministic_chained_and_tamper_evident() -> None:
    credit = ContributorCredit(
        contributor_id="fixture-1",
        credit_name="Synthetic Fixture",
        credit_mode="public_pseudonymous",
        contribution_classes=("test_fixture",),
        description="Deterministic local test input.",
    )
    before = "1" * 64
    after = "2" * 64

    ledgers = [AttributionJourneyLedger("atlas-test") for _ in range(2)]
    for ledger in ledgers:
        ledger.append(
            event_type="state_transition",
            contributors=[credit],
            state_before_sha256=before,
            state_after_sha256=after,
            timestamp_utc="2026-07-17T00:00:00+00:00",
        )
        ledger.append(
            event_type="freeze",
            contributors=[credit],
            state_before_sha256=after,
            state_after_sha256=after,
            timestamp_utc="2026-07-17T00:00:01+00:00",
        )

    assert ledgers[0].verify() == []
    assert ledgers[0].certificate()["journey_sha256"] == ledgers[1].certificate()["journey_sha256"]
    ledgers[0].entries[0]["event_type"] = "tampered"
    assert "entry hash mismatch at 0" in ledgers[0].verify()

    with pytest.raises(ValueError, match="SHA-256 hex"):
        ledgers[1].append(
            event_type="invalid",
            contributors=[credit],
            state_before_sha256="z" * 64,
            state_after_sha256=after,
            timestamp_utc="2026-07-17T00:00:02+00:00",
        )


def test_resource_limits_reject_without_partial_mutation() -> None:
    controller = RuntimeController.instantiate(genome(max_records=1, max_messages=1), identity())
    controller.ingest(record("one"))
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError, match="record limit"):
        controller.ingest(record("two"))
    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before

    controller.send("nova", "proposal", {"sequence": 1})
    outbox_before = copy.deepcopy(controller.qso.p.outbox)
    with pytest.raises(RuntimeInvariantError, match="outbox"):
        controller.send("nova", "proposal", {"sequence": 2})
    assert controller.qso.p.outbox == outbox_before


def test_freeze_interruption_recovery_and_rollback_preserve_evidence() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("checkpoint"))
    frozen = controller.freeze([])
    assert frozen["decision"] == "frozen_pending_external_commit"
    assert controller.status == "frozen"
    checkpoint_hash = controller.checkpoint.state_sha256

    controller.resume()
    controller.ingest(record("transient"))
    controller.interrupt("synthetic interruption")
    with pytest.raises(RuntimeInvariantError, match="status"):
        controller.ingest(record("blocked"))
    controller.recover()

    assert controller.status == "active"
    assert [item["content"] for item in controller.qso.p.records] == ["synthetic:checkpoint"]
    assert state_sha256(controller.qso) == checkpoint_hash
    assert {"freeze", "resumed", "interrupted", "recovered"}.issubset(
        {event["kind"] for event in controller.qso.p.events}
    )

    event_count = len(controller.qso.p.events)
    controller.ingest(record("rollback-target"))
    controller.rollback()
    assert [item["content"] for item in controller.qso.p.records] == ["synthetic:checkpoint"]
    assert len(controller.qso.p.events) == event_count + 2
    assert controller.qso.p.events[-1]["kind"] == "rollback"
    assert verify_event_ledger(controller.qso.p.events) == []


def test_canonical_state_and_event_hashes_repeat_across_identical_runs() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    for controller in controllers:
        controller.ingest(record("one"))
        controller.freeze([])
        controller.resume()
        controller.interrupt("deterministic stop")
        controller.recover()

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)
    assert controllers[0].evidence() == controllers[1].evidence()
