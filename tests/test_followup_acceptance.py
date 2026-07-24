from __future__ import annotations

import hashlib
import json

import pytest

from qso_runtime.config import ConfigurationError, REQUIRED_QSOS, load_runtime_config
from qso_runtime.core import GenomeInterpreter, MCPMessage
from qso_runtime.runtime import (
    RuntimeController,
    RuntimeInvariantError,
    event_ledger_sha256,
    state_sha256,
    validate_message,
    verify_event_ledger,
)


def genome(*, max_events: int = 30, allowed_peers: object = None) -> dict:
    if allowed_peers is None:
        allowed_peers = ["nova"]
    return {
        "genome_id": "atlas",
        "purpose": "follow-up acceptance remediation",
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
        "communication": {"allowed_peers": allowed_peers},
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


def test_record_shape_validation_is_positive_atomic_and_deterministic() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    valid = record("canonical")
    valid["repository"] = "local-fixture"
    for controller in controllers:
        controller.ingest(valid)
    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)

    controller = RuntimeController.instantiate(genome(), identity())
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)
    malformed = record("non-json")
    malformed["flags"] = {"not-json"}
    with pytest.raises(RuntimeInvariantError, match="canonical JSON|flags"):
        controller.ingest(malformed)
    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before
    assert controller.qso.p.records == []


@pytest.mark.parametrize(
    "allowed_peers",
    ["nova", {"nova": True}, ["nova", 7], ["nova", "nova"]],
)
def test_malformed_allowed_peer_collections_fail_before_message_mutation(
    allowed_peers: object,
) -> None:
    controller = RuntimeController.instantiate(genome(allowed_peers=allowed_peers), identity())
    state_before = state_sha256(controller.qso)
    with pytest.raises(RuntimeInvariantError, match="allowed_peers"):
        controller.send("nova", "proposal", {"claim": "bounded"})
    assert state_sha256(controller.qso) == state_before
    assert controller.qso.p.outbox == []


def test_recovery_consumes_reserved_safety_slot_and_is_deterministic() -> None:
    controllers = [RuntimeController.instantiate(genome(max_events=7), identity()) for _ in range(2)]
    for controller in controllers:
        controller.ingest(record("checkpoint"))
        controller.freeze([])
        controller.resume()
        controller.ingest(record("transient"))
        controller.interrupt("synthetic interruption")
        controller.recover()
        assert controller.status == "active"
        assert [item["content"] for item in controller.qso.p.records] == ["synthetic:checkpoint"]
        assert len(controller.qso.p.events) == 7
        assert controller.qso.p.events[-1]["kind"] == "recovered"
        assert verify_event_ledger(controller.qso.p.events) == []
    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)
    assert event_ledger_sha256(controllers[0].qso) == event_ledger_sha256(controllers[1].qso)


def test_high_severity_annotation_validation_precedes_rollback_mutation() -> None:
    controller = RuntimeController.instantiate(genome(), identity())
    controller.ingest(record("checkpoint"))
    controller.freeze([])
    controller.resume()
    controller.ingest(record("transient"))
    state_before = state_sha256(controller.qso)
    events_before = event_ledger_sha256(controller.qso)

    with pytest.raises(RuntimeInvariantError, match="canonical JSON"):
        controller.freeze([{"severity": "high", "evidence": {"not-json"}}])

    assert controller.status == "active"
    assert state_sha256(controller.qso) == state_before
    assert event_ledger_sha256(controller.qso) == events_before
    assert [item["content"] for item in controller.qso.p.records] == [
        "synthetic:checkpoint",
        "synthetic:transient",
    ]


def test_received_message_is_defensively_copied_and_remains_valid() -> None:
    controllers = [RuntimeController.instantiate(genome(), identity()) for _ in range(2)]
    messages = [
        MCPMessage.build(
            "nova",
            "atlas",
            "annotation",
            {"nested": {"value": [1, 2]}},
        )
        for _ in range(2)
    ]
    for controller, message in zip(controllers, messages):
        controller.receive(message)
        message.payload["nested"]["value"].append(3)
        stored = controller.qso.p.inbox[0]
        assert stored.payload == {"nested": {"value": [1, 2]}}
        validate_message(
            stored,
            allowed_senders={"nova"},
            allowed_recipients={"atlas"},
        )
    assert state_sha256(controllers[0].qso) == state_sha256(controllers[1].qso)


def _instance_document(*, genome_hash_marker: object = "omitted") -> dict:
    secondary_names = {
        "Atlas": "Helix",
        "Nova": "Talon",
        "Orion": "Keystone",
        "Lyra": "Cadence",
    }
    instances = []
    for name, secondary_name in secondary_names.items():
        genome_reference = {
            "repository": "aevespers2/QSO-GENOMES",
            "path": f"genomes/{name.lower()}.json",
            "schema_version": 1,
        }
        if genome_hash_marker != "omitted":
            genome_reference["sha256"] = genome_hash_marker
        instances.append(
            {
                "schema_version": 1,
                "instance_id": f"{name.lower()}-{secondary_name.lower()}-vespers-0-1-0",
                "declared_name": f"{name}-{secondary_name}-Vespers",
                "primary_name": name,
                "secondary_name": secondary_name,
                "lineage_suffix": "Vespers",
                "version": "0.1.0",
                "genome": genome_reference,
                "identity_declaration": {
                    "secondary_name_basis": "declared_intent",
                    "secondary_focus": f"Synthetic deterministic focus for {name}.",
                    "chosen_at_freeze_point": True,
                    "human_review_required": True,
                },
                "development": {
                    "interpretation_enabled": True,
                    "self_reflection_enabled": True,
                    "self_edit_mode": "proposal_only",
                    "immutable_fields_locked": True,
                    "proposal_log": f"proposals/{name.lower()}-{secondary_name.lower()}-vespers.jsonl",
                    "max_proposals_per_run": 8,
                },
                "sprite_review": {
                    "required": True,
                    "sprite": "aequitas",
                    "activation_rule": "pending_until_sprite_and_human_review",
                },
                "status": "pending_review",
            }
        )
    return {"instances": instances}


def test_omitted_optional_genome_hash_is_accepted_but_explicit_null_is_rejected(
    tmp_path,
) -> None:
    omitted_path = tmp_path / "omitted.json"
    omitted_path.write_text(json.dumps(_instance_document()), encoding="utf-8")
    config = load_runtime_config(omitted_path, expected_primary_names=REQUIRED_QSOS)
    assert all(instance.genome.sha256 is None for instance in config.instances)

    null_path = tmp_path / "null.json"
    null_path.write_text(
        json.dumps(_instance_document(genome_hash_marker=None)),
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError, match="genome.sha256"):
        load_runtime_config(null_path, expected_primary_names=REQUIRED_QSOS)
