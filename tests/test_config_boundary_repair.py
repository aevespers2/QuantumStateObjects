from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from qso_runtime.config import (
    REQUIRED_QSOS,
    ConfigurationError,
    load_runtime_config,
    resolve_local_genomes,
)


def _repository_document() -> dict[str, object]:
    return json.loads(Path("config/instances.json").read_text(encoding="utf-8"))


def _write_document(tmp_path: Path, document: dict[str, object]) -> Path:
    path = tmp_path / "instances.json"
    path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("identity_declaration", "secondary_name_basis"), ["declared_intent"]),
        (("development", "self_edit_mode"), {"mode": "proposal_only"}),
        (("sprite_review", "sprite"), ["aequitas"]),
        (
            ("sprite_review", "activation_rule"),
            {"rule": "pending_until_sprite_and_human_review"},
        ),
        (("status",), ["pending_review"]),
    ],
    ids=[
        "secondary-name-basis",
        "self-edit-mode",
        "sprite",
        "activation-rule",
        "status",
    ],
)
def test_structured_config_enums_fail_as_configuration_errors(
    tmp_path: Path,
    path: tuple[str, ...],
    value: object,
) -> None:
    document = _repository_document()
    instances = document["instances"]
    assert isinstance(instances, list)
    target = instances[0]
    assert isinstance(target, dict)
    for key in path[:-1]:
        target = target[key]
        assert isinstance(target, dict)
    target[path[-1]] = value

    config_path = _write_document(tmp_path, document)
    with pytest.raises(ConfigurationError, match=r"(must be a string|unsupported)"):
        load_runtime_config(config_path, expected_primary_names=REQUIRED_QSOS)


def test_configuration_read_oserror_is_normalized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = _write_document(tmp_path, _repository_document())
    original_read_bytes = Path.read_bytes

    def unreadable(path: Path) -> bytes:
        if path == config_path:
            raise PermissionError("synthetic denied")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", unreadable)

    with pytest.raises(ConfigurationError, match="could not be read safely"):
        load_runtime_config(config_path, expected_primary_names=REQUIRED_QSOS)


def test_hash_pinned_genome_read_oserror_is_normalized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    genome_payload = json.dumps(
        {"schema_version": 1, "kind": "bounded-fixture"},
        sort_keys=True,
    ).encode("utf-8")
    genome_hash = hashlib.sha256(genome_payload).hexdigest()

    document = _repository_document()
    instances = document["instances"]
    assert isinstance(instances, list)
    for instance in instances:
        assert isinstance(instance, dict)
        genome = instance["genome"]
        assert isinstance(genome, dict)
        genome["sha256"] = genome_hash

    config_path = _write_document(tmp_path, document)
    genome_root = tmp_path / "QSO-GENOMES"
    target_paths: set[Path] = set()
    for name in REQUIRED_QSOS:
        genome_path = genome_root / "genomes" / f"{name.lower()}.json"
        genome_path.parent.mkdir(parents=True, exist_ok=True)
        genome_path.write_bytes(genome_payload)
        target_paths.add(genome_path)

    config = load_runtime_config(
        config_path,
        expected_primary_names=REQUIRED_QSOS,
    )
    original_read_bytes = Path.read_bytes

    def unreadable(path: Path) -> bytes:
        if path in target_paths:
            raise OSError("synthetic I/O failure")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", unreadable)

    with pytest.raises(ConfigurationError, match="could not be read safely"):
        resolve_local_genomes(config, genome_root)
