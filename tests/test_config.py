from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from qso_runtime.cli import main
from qso_runtime.config import REQUIRED_QSOS, ConfigurationError, load_runtime_config, resolve_local_genomes


def _instance(
    name: str,
    *,
    path: str | None = None,
    repository: str = "aevespers2/QSO-GENOMES",
    sha256: str | None = None,
) -> dict[str, object]:
    secondary_names = {
        "Atlas": "Helix",
        "Nova": "Talon",
        "Orion": "Keystone",
        "Lyra": "Cadence",
    }
    secondary_name = secondary_names[name]
    genome: dict[str, object] = {
        "repository": repository,
        "path": path or f"genomes/{name.lower()}.json",
        "schema_version": 1,
    }
    if sha256 is not None:
        genome["sha256"] = sha256
    return {
        "schema_version": 1,
        "instance_id": f"{name.lower()}-{secondary_name.lower()}-vespers-0-1-0",
        "declared_name": f"{name}-{secondary_name}-Vespers",
        "primary_name": name,
        "secondary_name": secondary_name,
        "lineage_suffix": "Vespers",
        "version": "0.1.0",
        "genome": genome,
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


def _document(*, sha256: str | None = None) -> dict[str, object]:
    return {"instances": [_instance(name, sha256=sha256) for name in REQUIRED_QSOS]}


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def test_repository_configuration_loads_four_unique_instances() -> None:
    config = load_runtime_config(Path("config/instances.json"), expected_primary_names=REQUIRED_QSOS)
    assert [instance.primary_name for instance in config.instances] == list(REQUIRED_QSOS)
    assert len(config.sha256) == 64


def test_cli_validates_local_configuration_without_resolving_upstream(capsys) -> None:
    assert main(["--config", "config/instances.json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["configuration"]["primary_names"] == list(REQUIRED_QSOS)
    assert payload["configuration"]["genomes_resolved"] is False


def test_malformed_configuration_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "instances.json"
    path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="valid UTF-8 JSON"):
        load_runtime_config(path)


def test_non_utf8_configuration_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "instances.json"
    path.write_bytes(json.dumps(_document()).encode("utf-16"))
    with pytest.raises(ConfigurationError, match="not valid UTF-8 JSON"):
        load_runtime_config(path)


def test_duplicate_instance_id_fails_closed(tmp_path: Path) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[1]["instance_id"] = instances[0]["instance_id"]
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="duplicate instance_id"):
        load_runtime_config(path)


def test_noncanonical_primary_name_fails_closed(tmp_path: Path) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0]["primary_name"] = "atlas"
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="canonical names"):
        load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)


@pytest.mark.parametrize(
    "missing_key",
    [
        "declared_name",
        "secondary_name",
        "lineage_suffix",
        "identity_declaration",
        "development",
        "sprite_review",
        "status",
    ],
)
def test_missing_schema_required_instance_blocks_fail_closed(
    tmp_path: Path, missing_key: str
) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0].pop(missing_key)
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="missing required fields"):
        load_runtime_config(path)


@pytest.mark.parametrize(
    ("block", "missing_key"),
    [
        ("identity_declaration", "human_review_required"),
        ("development", "immutable_fields_locked"),
        ("sprite_review", "activation_rule"),
    ],
)
def test_missing_schema_required_nested_fields_fail_closed(
    tmp_path: Path, block: str, missing_key: str
) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0][block].pop(missing_key)
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="missing required fields"):
        load_runtime_config(path)


@pytest.mark.parametrize("location", ["instance", "genome"])
def test_boolean_schema_versions_fail_closed(tmp_path: Path, location: str) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    if location == "instance":
        instances[0]["schema_version"] = True
    else:
        instances[0]["genome"]["schema_version"] = True
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="integer 1"):
        load_runtime_config(path)


@pytest.mark.parametrize("instance_id", ["BAD ID", "ab", "Atlas-valid-looking"])
def test_invalid_instance_id_fails_closed(tmp_path: Path, instance_id: str) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0]["instance_id"] = instance_id
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="instance_id must match"):
        load_runtime_config(path)


def test_uncontracted_genome_repository_fails_closed(tmp_path: Path) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0]["genome"]["repository"] = "example/other-genomes"
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="QSO-GENOMES"):
        load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)


def test_noncanonical_genome_path_fails_closed(tmp_path: Path) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[0]["genome"]["path"] = "fixtures/atlas.json"
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="genomes/atlas.json"):
        load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)


def test_schema_declares_optional_genome_hash_pin() -> None:
    schema = json.loads(Path("schema/qso-instance.schema.json").read_text(encoding="utf-8"))
    genome = schema["properties"]["genome"]
    assert "sha256" in genome["properties"]
    assert "sha256" not in genome["required"]
    assert genome["properties"]["sha256"]["pattern"] == "^[0-9a-f]{64}$"


def test_atlas_missing_hash_fails_closed_before_upstream_resolution(tmp_path: Path) -> None:
    path = tmp_path / "instances.json"
    _write_json(path, _document())
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    genome_root = tmp_path / "QSO-GENOMES"
    genome_root.mkdir()
    with pytest.raises(ConfigurationError, match="Atlas genome sha256"):
        resolve_local_genomes(config, genome_root)


def test_hash_mismatch_fails_closed(tmp_path: Path) -> None:
    genome_payload = json.dumps({"schema_version": 1}, sort_keys=True).encode()
    wrong_hash = "0" * 64
    path = tmp_path / "instances.json"
    _write_json(path, _document(sha256=wrong_hash))
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    with pytest.raises(ConfigurationError, match="Atlas genome hash mismatch"):
        resolve_local_genomes(config, genome_root)


def test_non_utf8_hash_pinned_genome_fails_closed(tmp_path: Path) -> None:
    genome_payload = json.dumps({"schema_version": 1}).encode("utf-16")
    genome_hash = hashlib.sha256(genome_payload).hexdigest()
    path = tmp_path / "instances.json"
    _write_json(path, _document(sha256=genome_hash))
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    with pytest.raises(ConfigurationError, match="Atlas genome is not valid UTF-8 JSON"):
        resolve_local_genomes(config, genome_root)


def test_boolean_genome_document_schema_version_fails_closed(tmp_path: Path) -> None:
    genome_payload = json.dumps({"schema_version": True}, sort_keys=True).encode("utf-8")
    genome_hash = hashlib.sha256(genome_payload).hexdigest()
    path = tmp_path / "instances.json"
    _write_json(path, _document(sha256=genome_hash))
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    with pytest.raises(ConfigurationError, match="integer 1"):
        resolve_local_genomes(config, genome_root)


def test_hash_pinned_local_genomes_resolve_deterministically(tmp_path: Path) -> None:
    genome_payload = json.dumps({"schema_version": 1, "kind": "bounded-fixture"}, sort_keys=True).encode()
    genome_hash = hashlib.sha256(genome_payload).hexdigest()
    path = tmp_path / "instances.json"
    _write_json(path, _document(sha256=genome_hash))
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    first = resolve_local_genomes(config, genome_root)
    second = resolve_local_genomes(config, genome_root)
    assert first == second
    assert set(first.values()) == {genome_hash}
