from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from qso_runtime.cli import main
from qso_runtime.config import REQUIRED_QSOS, ConfigurationError, load_runtime_config, resolve_local_genomes


def _instance(name: str, *, path: str | None = None, sha256: str | None = None) -> dict[str, object]:
    genome: dict[str, object] = {
        "repository": "aevespers2/QSO-GENOMES",
        "path": path or f"genomes/{name.lower()}.json",
        "schema_version": 1,
    }
    if sha256 is not None:
        genome["sha256"] = sha256
    return {
        "schema_version": 1,
        "instance_id": f"{name.lower()}-0-1-0",
        "primary_name": name,
        "version": "0.1.0",
        "genome": genome,
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


def test_duplicate_instance_id_fails_closed(tmp_path: Path) -> None:
    document = _document()
    instances = document["instances"]
    assert isinstance(instances, list)
    instances[1]["instance_id"] = instances[0]["instance_id"]
    path = tmp_path / "instances.json"
    _write_json(path, document)
    with pytest.raises(ConfigurationError, match="duplicate instance_id"):
        load_runtime_config(path)


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


def test_hash_pinned_local_genomes_resolve_deterministically(tmp_path: Path) -> None:
    genome_payload = json.dumps({"schema_version": 1, "kind": "bounded-fixture"}, sort_keys=True).encode()
    digest = hashlib.sha256(genome_payload).hexdigest()
    path = tmp_path / "instances.json"
    _write_json(path, _document(sha256=digest))
    genome_root = tmp_path / "QSO-GENOMES"
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
    config = load_runtime_config(path, expected_primary_names=REQUIRED_QSOS)
    first = resolve_local_genomes(config, genome_root)
    second = resolve_local_genomes(config, genome_root)
    assert first == second
    assert set(first.values()) == {digest}
