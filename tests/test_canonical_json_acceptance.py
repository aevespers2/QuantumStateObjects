from __future__ import annotations

import copy
import hashlib
import json

import pytest

from qso_runtime.attribution import (
    AttributionJourneyLedger,
    ContributorCredit,
    artifact_reference,
    require_sha256,
)
from qso_runtime.config import (
    ConfigurationError,
    load_runtime_config,
    resolve_local_genomes,
)
from qso_runtime.core import GenomeInterpreter, MCPMessage
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    validate_message,
    verify_event_ledger,
)


def genome() -> dict:
    return {
        "genome_id": "atlas",
        "purpose": "canonical JSON acceptance remediation",
        "immutable": {
            "forbidden_capabilities": sorted(GenomeInterpreter.REQUIRED_FORBIDDEN),
        },
        "mutable": {},
        "resources": {
            "max_records": 3,
            "max_messages": 3,
            "max_events": 30,
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


def permissive_digest(value: object) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def atlas_instance(*, genome_sha256: str | None = None) -> dict:
    genome_reference = {
        "repository": "aevespers2/QSO-GENOMES",
        "path": "genomes/atlas.json",
        "schema_version": 1,
    }
    if genome_sha256 is not None:
        genome_reference["sha256"] = genome_sha256
    return {
        "schema_version": 1,
        "instance_id": "atlas-helix-vespers-0-1-0",
        "declared_name": "Atlas-Helix-Vespers",
        "primary_name": "Atlas",
        "secondary_name": "Helix",
        "lineage_suffix": "Vespers",
        "version": "0.1.0",
        "genome": genome_reference,
        "identity_declaration": {
            "secondary_name_basis": "declared_intent",
            "secondary_focus": "Deterministic canonical JSON acceptance fixture.",
            "chosen_at_freeze_point": True,
            "human_review_required": True,
        },
        "development": {
            "interpretation_enabled": True,
            "self_reflection_enabled": True,
            "self_edit_mode": "proposal_only",
            "immutable_fields_locked": True,
            "proposal_log": "proposals/atlas-helix-vespers.jsonl",
            "max_proposals_per_run": 8,
        },
        "sprite_review": {
            "required": True,
            "sprite": "aequitas",
            "activation_rule": "pending_until_sprite_and_human_review",
        },
        "status": "pending_review",
    }


def test_sent_message_outbox_is_independent_and_deterministic() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    returned_messages = [
        controller.send(
            "nova",
            "proposal",
            {"nested": {"values": [1, 2]}, "finite": 0.5},
        )
        for controller in controllers
    ]
    expected_state = state_sha256(controllers[0].qso)
    expected_events = event_ledger_sha256(controllers[0].qso)
    assert expected_state == state_sha256(controllers[1].qso)
    assert expected_events == event_ledger_sha256(controllers[1].qso)

    returned_messages[0].payload["nested"]["values"].append(3)
    stored = controllers[0].qso.p.outbox[0]
    assert stored.payload == {"nested": {"values": [1, 2]}, "finite": 0.5}
    assert stored is not returned_messages[0]
    validate_message(
        stored,
        allowed_senders={"atlas"},
        allowed_recipients={"nova"},
    )
    assert state_sha256(controllers[0].qso) == expected_state
    assert event_ledger_sha256(controllers[0].qso) == expected_events


@pytest.mark.parametrize(
    "payload",
    [
        {1: "integer-key"},
        {"value": float("nan")},
        {"value": float("inf")},
        {"value": float("-inf")},
    ],
)
def test_rehashed_event_ledgers_reject_noncanonical_payloads(payload: dict) -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    malformed = copy.deepcopy(controller.qso.p.events)
    malformed[0]["payload"] = payload
    malformed[0]["sha256"] = permissive_digest(
        {key: value for key, value in malformed[0].items() if key != "sha256"}
    )

    errors = verify_event_ledger(malformed)
    assert "payload canonical JSON mismatch at 0" in errors


@pytest.mark.parametrize(
    "payload",
    [
        {1: "integer-key"},
        {"value": float("nan")},
        {"value": float("inf")},
        {"value": {"not-json"}},
    ],
)
def test_message_payloads_fail_before_build_send_receive_or_mutation(payload: dict) -> None:
    with pytest.raises(ValueError, match="message payload"):
        MCPMessage.build("atlas", "nova", "proposal", payload)

    sender = RuntimeController.instantiate(genome(), identity())
    sender_state = state_sha256(sender.qso)
    sender_events = event_ledger_sha256(sender.qso)
    with pytest.raises((RuntimeInvariantError, ValueError), match="message payload"):
        sender.send("nova", "proposal", payload)
    assert sender.qso.p.outbox == []
    assert state_sha256(sender.qso) == sender_state
    assert event_ledger_sha256(sender.qso) == sender_events

    receiver = RuntimeController.instantiate(genome(), identity())
    receiver_state = state_sha256(receiver.qso)
    receiver_events = event_ledger_sha256(receiver.qso)
    malformed = MCPMessage(
        sender="nova",
        recipient="atlas",
        kind="annotation",
        payload=copy.deepcopy(payload),
        sha256="0" * 64,
    )
    with pytest.raises(RuntimeInvariantError, match="message payload"):
        receiver.receive(malformed)
    assert receiver.qso.p.inbox == []
    assert state_sha256(receiver.qso) == receiver_state
    assert event_ledger_sha256(receiver.qso) == receiver_events


def test_lowercase_attribution_state_and_artifact_hashes_are_required() -> None:
    require_sha256("a" * 64, "state")
    artifact = artifact_reference(
        "fixture",
        "test-evidence",
        "b" * 64,
        "created",
    )
    assert artifact["sha256"] == "b" * 64

    with pytest.raises(ValueError, match="lowercase SHA-256"):
        require_sha256("A" * 64, "state")
    with pytest.raises(ValueError, match="lowercase SHA-256"):
        artifact_reference("fixture", "test-evidence", "B" * 64, "created")

    credit = ContributorCredit(
        contributor_id="fixture-1",
        credit_name="Synthetic Fixture",
        credit_mode="public_pseudonymous",
        contribution_classes=("test_fixture",),
        description="Deterministic local test input.",
    )
    ledger = AttributionJourneyLedger("atlas-test")
    with pytest.raises(ValueError, match="lowercase SHA-256"):
        ledger.append(
            event_type="state_transition",
            contributors=[credit],
            state_before_sha256="A" * 64,
            state_after_sha256="b" * 64,
            timestamp_utc="2026-07-18T00:00:00+00:00",
        )


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_configuration_parser_rejects_nonstandard_json_constants(
    tmp_path,
    constant: str,
) -> None:
    valid_path = tmp_path / "valid.json"
    valid_path.write_text(
        json.dumps({"instances": [atlas_instance()]}),
        encoding="utf-8",
    )
    assert load_runtime_config(valid_path).instances[0].primary_name == "Atlas"

    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(
        '{"instances":[' + json.dumps(atlas_instance()) + f'],"probe":{constant}}}',
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        load_runtime_config(invalid_path)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_hash_pinned_genome_parser_rejects_nonstandard_json_constants_atomically(
    tmp_path,
    constant: str,
) -> None:
    genome_root = tmp_path / "genome-root"
    genome_path = genome_root / "genomes" / "atlas.json"
    genome_path.parent.mkdir(parents=True)
    genome_bytes = f'{{"schema_version":1,"probe":{constant}}}'.encode("utf-8")
    genome_path.write_bytes(genome_bytes)
    genome_hash = hashlib.sha256(genome_bytes).hexdigest()

    config_path = tmp_path / "runtime.json"
    config_path.write_text(
        json.dumps({"instances": [atlas_instance(genome_sha256=genome_hash)]}),
        encoding="utf-8",
    )
    config = load_runtime_config(config_path)
    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        resolve_local_genomes(config, genome_root)

    assert genome_path.read_bytes() == genome_bytes
    assert config.instances[0].genome.sha256 == genome_hash


def test_valid_hash_pinned_genome_resolution_remains_deterministic(tmp_path) -> None:
    genome_root = tmp_path / "genome-root"
    genome_path = genome_root / "genomes" / "atlas.json"
    genome_path.parent.mkdir(parents=True)
    genome_bytes = b'{"probe":0.5,"schema_version":1}'
    genome_path.write_bytes(genome_bytes)
    genome_hash = hashlib.sha256(genome_bytes).hexdigest()

    config_path = tmp_path / "runtime.json"
    config_path.write_text(
        json.dumps({"instances": [atlas_instance(genome_sha256=genome_hash)]}),
        encoding="utf-8",
    )
    config = load_runtime_config(config_path)
    first = resolve_local_genomes(config, genome_root)
    second = resolve_local_genomes(config, genome_root)
    assert first == second == {"atlas-helix-vespers-0-1-0": genome_hash}
