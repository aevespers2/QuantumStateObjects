from __future__ import annotations

import copy

import pytest

from qso_runtime.attribution import AttributionJourneyLedger
from qso_runtime.core import GenomeInterpreter
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    verify_event_ledger,
)


STATE_BEFORE = "0" * 64
STATE_AFTER = "1" * 64
TIMESTAMP = "2026-07-18T00:00:00+00:00"


def genome() -> dict:
    return {
        "genome_id": "atlas",
        "purpose": "latest bounded acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 2,
            "max_messages": 2,
            "max_events": 10,
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


def append_attribution(
    ledger: AttributionJourneyLedger,
    artifacts: object,
) -> dict:
    return ledger.append(
        event_type="bounded_check",
        contributors=[],
        state_before_sha256=STATE_BEFORE,
        state_after_sha256=STATE_AFTER,
        artifacts=artifacts,  # type: ignore[arg-type]
        timestamp_utc=TIMESTAMP,
    )


@pytest.mark.parametrize("artifacts", [{}, "", (), 0, False])
def test_explicit_non_none_non_list_artifacts_fail_atomically(artifacts: object) -> None:
    ledger = AttributionJourneyLedger("atlas")
    entries_before = copy.deepcopy(ledger.entries)

    with pytest.raises(ValueError, match="artifacts must be a list"):
        append_attribution(ledger, artifacts)

    assert ledger.entries == entries_before


def test_omitted_and_explicit_empty_artifact_lists_are_equivalent() -> None:
    omitted_ledger = AttributionJourneyLedger("atlas")
    explicit_ledger = AttributionJourneyLedger("atlas")

    omitted = append_attribution(omitted_ledger, None)
    explicit = append_attribution(explicit_ledger, [])

    assert omitted == explicit
    assert omitted["artifacts"] == []
    assert omitted_ledger.verify() == []
    assert explicit_ledger.verify() == []


@pytest.mark.parametrize(
    ("extra_keys", "expected_extra_error"),
    [
        ({1: "x"}, None),
        ({1: "x", "z": "y"}, "unexpected event fields at 0: ['z']"),
    ],
)
def test_non_string_and_mixed_event_keys_report_deterministic_errors(
    extra_keys: dict[object, object],
    expected_extra_error: str | None,
) -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    malformed = copy.deepcopy(controller.qso.p.events[0])
    malformed.update(extra_keys)

    first = verify_event_ledger([malformed])
    second = verify_event_ledger([copy.deepcopy(malformed)])

    assert first == second
    assert "event key type mismatch at 0" in first
    assert "event serialization failure at 0" in first
    if expected_extra_error is not None:
        assert expected_extra_error in first


@pytest.mark.parametrize("resources", [[], "", 0, None, False])
def test_non_object_resources_fail_before_instantiation_or_input_mutation(
    resources: object,
) -> None:
    candidate_genome = genome()
    candidate_genome["resources"] = resources
    candidate_identity = identity()
    genome_before = copy.deepcopy(candidate_genome)
    identity_before = copy.deepcopy(candidate_identity)

    with pytest.raises(RuntimeInvariantError, match="genome resources must be an object"):
        RuntimeController.instantiate(candidate_genome, candidate_identity)

    assert candidate_genome == genome_before
    assert candidate_identity == identity_before


def test_valid_resources_preserve_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)
    assert verify_event_ledger(controllers[0].qso.p.events) == []
    assert verify_event_ledger(controllers[1].qso.p.events) == []
