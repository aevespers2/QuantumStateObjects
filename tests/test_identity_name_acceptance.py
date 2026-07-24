from __future__ import annotations

import copy

import pytest

from qso_runtime.config import REQUIRED_QSOS
from qso_runtime.core import GenomeInterpreter, QSO
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    verify_event_ledger,
)


def genome(primary_name: str = "Atlas") -> dict:
    genome_id = primary_name.lower()
    peers = [name.lower() for name in REQUIRED_QSOS if name != primary_name]
    return {
        "genome_id": genome_id,
        "purpose": "canonical identity acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 2,
            "max_messages": 4,
            "max_events": 10,
        },
        "freeze": {"human_review_required": True},
        "communication": {"allowed_peers": peers},
        "learning": {"input_boundary": "qso_seeker_canonical_records_only"},
    }


def identity(
    primary_name: str = "Atlas",
    secondary_name: str = "Helix",
    declared_name: str | None = None,
) -> dict:
    return {
        "primary_name": primary_name,
        "secondary_name": secondary_name,
        "declared_name": declared_name
        if declared_name is not None
        else f"{primary_name}-{secondary_name}-Vespers",
    }


@pytest.mark.parametrize("primary_name", REQUIRED_QSOS)
def test_published_canonical_identity_names_instantiate(primary_name: str) -> None:
    controller = RuntimeController.instantiate(genome(primary_name), identity(primary_name))

    assert controller.qso.name == f"{primary_name}-Helix-Vespers"
    assert controller.qso.p.identity == identity(primary_name)
    assert verify_event_ledger(controller.qso.p.events) == []


def test_lowercase_primary_name_fails_before_qso_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    qso_constructed = False

    def unexpected_qso_init(self: QSO, partition: object) -> None:
        nonlocal qso_constructed
        qso_constructed = True
        raise AssertionError("QSO construction must not begin for a noncanonical identity")

    monkeypatch.setattr(QSO, "__init__", unexpected_qso_init)

    with pytest.raises(RuntimeInvariantError, match="genome and identity contract is invalid"):
        RuntimeController.instantiate(
            genome("Atlas"),
            identity("atlas", declared_name="atlas-Helix-Vespers"),
        )

    assert qso_constructed is False


@pytest.mark.parametrize(
    "secondary_name",
    ["helix", "H", "Helix-Prime", "A" * 33],
    ids=["lowercase", "too-short", "hyphenated", "too-long"],
)
def test_schema_invalid_secondary_names_fail_closed(secondary_name: str) -> None:
    candidate_genome = genome()
    candidate_identity = identity(secondary_name=secondary_name)

    with pytest.raises(RuntimeInvariantError, match="genome and identity contract is invalid"):
        RuntimeController.instantiate(candidate_genome, candidate_identity)


def test_declared_name_must_match_primary_secondary_and_lineage() -> None:
    with pytest.raises(RuntimeInvariantError, match="genome and identity contract is invalid"):
        RuntimeController.instantiate(
            genome(),
            identity(declared_name="Atlas-Talon-Vespers"),
        )


def test_rejected_identity_is_atomic_and_does_not_mutate_inputs_or_append_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate_genome = genome()
    candidate_identity = identity(primary_name="atlas")
    genome_before = copy.deepcopy(candidate_genome)
    identity_before = copy.deepcopy(candidate_identity)
    event_append_attempted = False

    def unexpected_record_event(self: QSO, kind: str, payload: dict) -> None:
        nonlocal event_append_attempted
        event_append_attempted = True
        raise AssertionError("no evidence event may be appended for a rejected identity")

    monkeypatch.setattr(QSO, "record_event", unexpected_record_event)

    with pytest.raises(RuntimeInvariantError, match="genome and identity contract is invalid"):
        RuntimeController.instantiate(candidate_genome, candidate_identity)

    assert candidate_genome == genome_before
    assert candidate_identity == identity_before
    assert event_append_attempted is False


def test_canonical_identity_produces_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(
        controllers[1].qso
    )
    assert verify_event_ledger(controllers[0].qso.p.events) == []
    assert verify_event_ledger(controllers[1].qso.p.events) == []
