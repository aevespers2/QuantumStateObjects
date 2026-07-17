from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping

REQUIRED_QSOS = ("Atlas", "Nova", "Orion", "Lyra")
ACCEPTED_GENOME_REPOSITORY = "aevespers2/QSO-GENOMES"
EXPECTED_GENOME_PATHS = {
    "Atlas": "genomes/atlas.json",
    "Nova": "genomes/nova.json",
    "Orion": "genomes/orion.json",
    "Lyra": "genomes/lyra.json",
}
MAX_CONFIG_BYTES = 1_000_000
MAX_GENOME_BYTES = 1_000_000


class ConfigurationError(ValueError):
    """Raised when local configuration cannot be accepted safely."""


@dataclass(frozen=True)
class GenomeReference:
    repository: str
    path: str
    schema_version: int
    sha256: str | None


@dataclass(frozen=True)
class InstanceManifest:
    instance_id: str
    primary_name: str
    schema_version: int
    version: str
    genome: GenomeReference


@dataclass(frozen=True)
class RuntimeConfig:
    source: Path
    sha256: str
    instances: tuple[InstanceManifest, ...]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _read_bounded_file(path: Path, *, max_bytes: int, label: str) -> bytes:
    if not path.exists():
        raise ConfigurationError(f"{label} is missing: {path}")
    if path.is_symlink():
        raise ConfigurationError(f"{label} must not be a symbolic link: {path}")
    if not path.is_file():
        raise ConfigurationError(f"{label} is not a regular file: {path}")
    size = path.stat().st_size
    if size > max_bytes:
        raise ConfigurationError(f"{label} exceeds the {max_bytes}-byte limit: {path}")
    return path.read_bytes()


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"{label} must be a JSON object")
    return value


def _require_nonempty_string(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{label} must be a non-empty string")
    return value


def _validate_sha256(value: object, *, label: str, required: bool) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ConfigurationError(f"{label} must be a lowercase SHA-256 hex string")
    return value


def _validate_relative_json_path(value: object, *, label: str) -> str:
    path = _require_nonempty_string(value, label=label)
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != path:
        raise ConfigurationError(f"{label} must be a normalized relative path")
    if pure.suffix.lower() != ".json":
        raise ConfigurationError(f"{label} must reference a JSON file")
    return path


def load_runtime_config(
    path: str | Path,
    *,
    expected_primary_names: Iterable[str] | None = None,
) -> RuntimeConfig:
    """Load and structurally validate local instance metadata without resolving genomes."""
    source = Path(path)
    payload = _read_bounded_file(source, max_bytes=MAX_CONFIG_BYTES, label="configuration file")
    try:
        document = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"configuration file is not valid UTF-8 JSON: {source}") from exc

    root = _require_mapping(document, label="configuration root")
    raw_instances = root.get("instances")
    if not isinstance(raw_instances, list) or not raw_instances:
        raise ConfigurationError("configuration instances must be a non-empty array")

    instances: list[InstanceManifest] = []
    instance_ids: set[str] = set()
    primary_names: set[str] = set()
    for index, raw_instance in enumerate(raw_instances):
        label = f"instances[{index}]"
        instance = _require_mapping(raw_instance, label=label)
        instance_id = _require_nonempty_string(instance.get("instance_id"), label=f"{label}.instance_id")
        primary_name = _require_nonempty_string(instance.get("primary_name"), label=f"{label}.primary_name")
        if primary_name not in REQUIRED_QSOS:
            raise ConfigurationError(
                f"{label}.primary_name must be one of the canonical names: {', '.join(REQUIRED_QSOS)}"
            )
        schema_version = instance.get("schema_version")
        if schema_version != 1:
            raise ConfigurationError(f"{label}.schema_version must equal 1")
        version = _require_nonempty_string(instance.get("version"), label=f"{label}.version")

        if instance_id in instance_ids:
            raise ConfigurationError(f"duplicate instance_id: {instance_id}")
        if primary_name in primary_names:
            raise ConfigurationError(f"duplicate primary_name: {primary_name}")
        instance_ids.add(instance_id)
        primary_names.add(primary_name)

        genome_value = _require_mapping(instance.get("genome"), label=f"{label}.genome")
        repository = _require_nonempty_string(
            genome_value.get("repository"), label=f"{label}.genome.repository"
        )
        if repository != ACCEPTED_GENOME_REPOSITORY:
            raise ConfigurationError(
                f"{label}.genome.repository must equal {ACCEPTED_GENOME_REPOSITORY}"
            )
        genome_path = _validate_relative_json_path(
            genome_value.get("path"), label=f"{label}.genome.path"
        )
        expected_path = EXPECTED_GENOME_PATHS[primary_name]
        if genome_path != expected_path:
            raise ConfigurationError(
                f"{label}.genome.path must equal {expected_path} for {primary_name}"
            )
        genome_schema_version = genome_value.get("schema_version")
        if genome_schema_version != 1:
            raise ConfigurationError(f"{label}.genome.schema_version must equal 1")
        expected_hash = _validate_sha256(
            genome_value.get("sha256"), label=f"{label}.genome.sha256", required=False
        )
        instances.append(
            InstanceManifest(
                instance_id=instance_id,
                primary_name=primary_name,
                schema_version=schema_version,
                version=version,
                genome=GenomeReference(
                    repository=repository,
                    path=genome_path,
                    schema_version=genome_schema_version,
                    sha256=expected_hash,
                ),
            )
        )

    if expected_primary_names is not None:
        expected = set(expected_primary_names)
        actual = {instance.primary_name for instance in instances}
        if actual != expected:
            missing = sorted(expected - actual)
            unexpected = sorted(actual - expected)
            raise ConfigurationError(
                f"configuration QSO set mismatch; missing={missing}, unexpected={unexpected}"
            )

    return RuntimeConfig(source=source, sha256=_sha256_bytes(payload), instances=tuple(instances))


def resolve_local_genomes(config: RuntimeConfig, genome_root: str | Path) -> dict[str, str]:
    """Resolve only hash-pinned local genome JSON files and fail closed on any mismatch."""
    root = Path(genome_root)
    if not root.exists() or not root.is_dir() or root.is_symlink():
        raise ConfigurationError(f"genome root must be an existing non-symlink directory: {root}")
    root_resolved = root.resolve()
    resolved: dict[str, str] = {}

    for instance in config.instances:
        reference = instance.genome
        expected_hash = _validate_sha256(
            reference.sha256,
            label=f"{instance.primary_name} genome sha256",
            required=True,
        )
        candidate = root / Path(*PurePosixPath(reference.path).parts)
        candidate_resolved = candidate.resolve(strict=False)
        if candidate_resolved != root_resolved and root_resolved not in candidate_resolved.parents:
            raise ConfigurationError(f"{instance.primary_name} genome escapes the configured root")
        payload = _read_bounded_file(
            candidate,
            max_bytes=MAX_GENOME_BYTES,
            label=f"{instance.primary_name} genome",
        )
        actual_hash = _sha256_bytes(payload)
        if actual_hash != expected_hash:
            raise ConfigurationError(
                f"{instance.primary_name} genome hash mismatch: expected {expected_hash}, got {actual_hash}"
            )
        try:
            genome_document = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ConfigurationError(f"{instance.primary_name} genome is not valid UTF-8 JSON") from exc
        genome_object = _require_mapping(genome_document, label=f"{instance.primary_name} genome")
        if genome_object.get("schema_version") != reference.schema_version:
            raise ConfigurationError(
                f"{instance.primary_name} genome schema_version does not match its reference"
            )
        resolved[instance.instance_id] = actual_hash

    return resolved
