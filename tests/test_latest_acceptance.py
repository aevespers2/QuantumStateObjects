from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from qso_runtime.attribution import AttributionJourneyLedger
from qso_runtime.config import (
    REQUIRED_QSOS,
    ConfigurationError,
    load_runtime_config,
    resolve_local_genomes,
)
from qso_runtime.core import GenomeInterpreter, digest
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


def _write_pinned_genome_fixture(tmp_path: Path, payload: bytes):
    document = json.loads(Path("config/instances.json").read_text(encoding="utf-8"))
    genome_hash = hashlib.sha256(payload).hexdigest()
    instances = document["instances"]
    assert isinstance(instances, list)
    for instance in instances:
        instance["genome"]["sha256"] = genome_hash

    config_path = tmp_path / "instances.json"
    config_path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(payload)

    config = load_runtime_config(config_path, expected_primary_names=REQUIRED_QSOS)
    return config, genome_root


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


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("identity_secondary_name", r"identity\.secondary_name"),
        ("forbidden_capabilities_object", "forbidden_capabilities"),
    ],
)
def test_wrong_instantiation_shapes_fail_before_interpreter_and_without_mutation(
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    message: str,
) -> None:
    candidate_genome = genome()
    candidate_identity = identity()
    if case == "identity_secondary_name":
        candidate_identity["secondary_name"] = 123
    else:
        candidate_genome["immutable"]["forbidden_capabilities"] = {
            capability: True for capability in GenomeInterpreter.REQUIRED_FORBIDDEN
        }

    genome_before = copy.deepcopy(candidate_genome)
    identity_before = copy.deepcopy(candidate_identity)
    interpreter_called = False

    def unexpected_interpreter_call(self, genome_value, identity_value):
        nonlocal interpreter_called
        interpreter_called = True
        raise AssertionError("GenomeInterpreter must not receive contract-invalid inputs")

    monkeypatch.setattr(GenomeInterpreter, "instantiate", unexpected_interpreter_call)

    with pytest.raises(RuntimeInvariantError, match=message):
        RuntimeController.instantiate(candidate_genome, candidate_identity)

    assert interpreter_called is False
    assert candidate_genome == genome_before
    assert candidate_identity == identity_before


def test_duplicate_configuration_keys_fail_closed(tmp_path: Path) -> None:
    source = Path("config/instances.json").read_text(encoding="utf-8")
    ambiguous = source.replace(
        '"schema_version": 1,',
        '"schema_version": true, "schema_version": 1,',
        1,
    )
    path = tmp_path / "duplicate-config.json"
    path.write_text(ambiguous, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)


@pytest.mark.parametrize(
    "payload",
    [
        b'{"schema_version": true, "schema_version": 1}',
        b'{"schema_version": 1, "overflow_probe": 1e999}',
    ],
    ids=["duplicate-key", "overflow-number"],
)
def test_hash_pinned_genome_ambiguity_and_overflow_fail_closed(
    tmp_path: Path,
    payload: bytes,
) -> None:
    config, genome_root = _write_pinned_genome_fixture(tmp_path, payload)

    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        resolve_local_genomes(config, genome_root)


def test_configuration_overflow_number_fails_closed(tmp_path: Path) -> None:
    source = Path("config/instances.json").read_text(encoding="utf-8")
    overflowing = source.replace("{", '{"overflow_probe": 1e999,', 1)
    path = tmp_path / "overflow-config.json"
    path.write_text(overflowing, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)


def test_cross_qso_ledger_identity_switch_is_rejected_after_rehashing() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.qso.record_event("bounded_probe", {"accepted": True})
    events = copy.deepcopy(controller.qso.p.events)
    events[1]["qso"] = "Nova-Talon-Vespers"
    events[1]["sha256"] = digest(
        {key: value for key, value in events[1].items() if key != "sha256"}
    )

    first = verify_event_ledger(events)
    second = verify_event_ledger(copy.deepcopy(events))

    assert first == second
    assert "qso identity mismatch at 1" in first
    assert "event hash mismatch at 1" not in first
    assert "chain mismatch at 1" not in first


def test_same_qso_multi_event_ledger_remains_valid() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.qso.record_event("bounded_probe", {"accepted": True})

    assert verify_event_ledger(controller.qso.p.events) == []


def test_valid_resources_preserve_deterministic_state_and_event_hashes() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]

    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)
    assert verify_event_ledger(controllers[0].qso.p.events) == []
    assert verify_event_ledger(controllers[1].qso.p.events) == []
