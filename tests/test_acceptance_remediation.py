from __future__ import annotations

import hashlib

import pytest

from qso_runtime.core import GenomeInterpreter
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
)


def _genome() -> dict:
    return {
        "genome_id": "atlas",
        "purpose": "bounded acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 3,
            "max_messages": 2,
            "max_events": 30,
        },
        "freeze": {"human_review_required": True},
        "communication": {"allowed_peers": ["nova"]},
        "learning": {"input_boundary": "qso_seeker_canonical_records_only"},
    }


def _identity() -> dict:
    return {
        "primary_name": "Atlas",
        "secondary_name": "Helix",
        "declared_name": "Atlas-Helix-Vespers",
    }


def _record(content: str) -> dict:
    return {
        "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "flags": [],
        "transformations": ["synthetic_fixture"],
    }


def test_content_hash_validation_is_positive_atomic_and_deterministic() -> None:
    controllers = [RuntimeController.instantiate(_genome(), _identity()) for _ in range(2)]
    valid = _record("synthetic:unicode:λ")

    for controller in controllers:
        controller.ingest(valid)
        assert controller.qso.p.records == [valid]

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)

    controller = RuntimeController.instantiate(_genome(), _identity())
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)
    invalid = _record("synthetic:tampered")
    invalid["content_sha256"] = "0" * 64

    with pytest.raises(RuntimeInvariantError, match="content hash mismatch"):
        controller.ingest(invalid)

    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before
    assert controller.qso.p.records == []
