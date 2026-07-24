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
        "purpose": "interruption reason atomicity acceptance remediation",
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


def test_canonical_interruption_reason_is_stripped_recorded_and_status_linked() -> None:
    controller = RuntimeController.instantiate(genome(), identity())

    controller.interrupt("  bounded operator interruption  ")

    assert controller.status == "interrupted"
    assert controller.qso.p.events[-1]["kind"] == "interrupted"
    assert controller.qso.p.events[-1]["payload"] == {
        "reason": "bounded operator interruption"
    }
    assert verify_event_ledger(controller.qso.p.events) == []


@pytest.mark.parametrize(
    "invalid_reason",
    [
        pytest.param(None, id="null"),
        pytest.param(True, id="boolean-true"),
        pytest.param(False, id="boolean-false"),
        pytest.param(0, id="integer-zero"),
        pytest.param(7, id="integer-positive"),
        pytest.param(-2.5, id="float"),
        pytest.param([], id="list"),
        pytest.param({}, id="object"),
        pytest.param({"reason"}, id="set"),
        pytest.param(("reason",), id="tuple"),
        pytest.param(object(), id="opaque-object"),
        pytest.param("", id="empty-string"),
        pytest.param(" \t\n ", id="whitespace-string"),
        pytest.param("\ud800", id="high-lone-surrogate"),
        pytest.param("\udfff", id="low-lone-surrogate"),
    ],
)
def test_invalid_interruption_reasons_raise_runtime_invariant_error(
    invalid_reason: object,
) -> None:
    controller = RuntimeController.instantiate(genome(), identity())

    with pytest.raises(RuntimeInvariantError, match="interruption reason"):
        controller.interrupt(invalid_reason)  # type: ignore[arg-type]


def test_invalid_reason_is_atomic_and_preserves_active_status() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("atomicity"))
    state_before = copy.deepcopy(canonical_state(controller.qso))
    events_before = copy.deepcopy(controller.qso.p.events)
    checkpoint_before = controller.checkpoint
    status_before = controller.status

    with pytest.raises(RuntimeInvariantError):
        controller.interrupt("\ud800")

    assert canonical_state(controller.qso) == state_before
    assert controller.qso.p.events == events_before
    assert controller.checkpoint == checkpoint_before
    assert controller.status == status_before == "active"


def test_invalid_reason_preserves_freeze_checkpoint_and_transient_state() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("checkpoint"))
    controller.freeze([])
    checkpoint_before = controller.checkpoint
    controller.resume()
    controller.ingest(record("transient"))
    transient_state_before = copy.deepcopy(canonical_state(controller.qso))
    events_before = copy.deepcopy(controller.qso.p.events)

    with pytest.raises(RuntimeInvariantError):
        controller.interrupt("\udfff")

    assert controller.status == "active"
    assert controller.checkpoint == checkpoint_before
    assert canonical_state(controller.qso) == transient_state_before
    assert controller.qso.p.events == events_before
    assert [item["content"] for item in controller.qso.p.records] == [
        "synthetic:checkpoint",
        "synthetic:transient",
    ]


def test_invalid_reason_does_not_append_or_rewrite_event_ledger() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("ledger"))
    events_before = copy.deepcopy(controller.qso.p.events)
    ledger_hash_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError):
        controller.interrupt("\ud800")

    assert controller.qso.p.events == events_before
    assert event_ledger_sha256(controller.qso) == ledger_hash_before
    assert verify_event_ledger(controller.qso.p.events) == []


def test_invalid_reason_failures_preserve_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    state_hashes_before = [state_sha256(controller.qso) for controller in controllers]
    event_hashes_before = [event_ledger_sha256(controller.qso) for controller in controllers]
    errors: list[str] = []

    for controller in controllers:
        with pytest.raises(RuntimeInvariantError) as exc_info:
            controller.interrupt("\ud800")
        errors.append(str(exc_info.value))

    assert errors == [
        "interruption reason must contain only UTF-8 encodable strings",
        "interruption reason must contain only UTF-8 encodable strings",
    ]
    assert [state_sha256(controller.qso) for controller in controllers] == state_hashes_before
    assert [event_ledger_sha256(controller.qso) for controller in controllers] == event_hashes_before
    assert state_hashes_before[0] == state_hashes_before[1]
    assert event_hashes_before[0] == event_hashes_before[1]


def test_valid_reason_produces_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]

    for controller in controllers:
        controller.interrupt("  deterministic interruption  ")

    assert [controller.status for controller in controllers] == [
        "interrupted",
        "interrupted",
    ]
    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(
        controllers[1].qso
    )
    assert controllers[0].qso.p.events[-1]["payload"] == {
        "reason": "deterministic interruption"
    }
    assert verify_event_ledger(controllers[0].qso.p.events) == []
    assert verify_event_ledger(controllers[1].qso.p.events) == []
