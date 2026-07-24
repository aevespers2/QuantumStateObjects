from __future__ import annotations

import hashlib
import json
import math
import re
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

_INSTANCE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,127}$")
_SECONDARY_NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]{1,31}$")
_VERSION_PATTERN = re.compile(r"^0\.[0-9]+\.[0-9]+$")
_PROPOSAL_LOG_PATTERN = re.compile(r"^proposals/[a-z0-9-]+\.jsonl$")

_INSTANCE_KEYS = frozenset(
    {
        "schema_version",
        "instance_id",
        "declared_name",
        "primary_name",
        "secondary_name",
        "lineage_suffix",
        "version",
        "genome",
        "identity_declaration",
        "development",
        "sprite_review",
        "status",
    }
)
_GENOME_KEYS = frozenset({"repository", "path", "schema_version", "sha256"})
_IDENTITY_DECLARATION_KEYS = frozenset(
    {
        "secondary_name_basis",
        "secondary_focus",
        "chosen_at_freeze_point",
        "human_review_required",
    }
)
_DEVELOPMENT_KEYS = frozenset(
    {
        "interpretation_enabled",
        "self_reflection_enabled",
        "self_edit_mode",
        "immutable_fields_locked",
        "proposal_log",
        "max_proposals_per_run",
    }
)
_SPRITE_REVIEW_KEYS = frozenset({"required", "sprite", "activation_rule"})


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
    """Read a bounded regular file while normalizing filesystem failures."""
    try:
        if not path.exists():
            raise ConfigurationError(f"{label} is missing: {path}")
        if path.is_symlink():
            raise ConfigurationError(f"{label} must not be a symbolic link: {path}")
        if not path.is_file():
            raise ConfigurationError(f"{label} is not a regular file: {path}")
        if path.stat().st_size > max_bytes:
            raise ConfigurationError(f"{label} exceeds the {max_bytes}-byte limit: {path}")
        return path.read_bytes()
    except ConfigurationError:
        raise
    except OSError as exc:
        raise ConfigurationError(f"{label} could not be read safely: {path}") from exc


def _reject_nonstandard_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant: {value}")


def _reject_duplicate_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _parse_finite_json_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"JSON number exceeds finite range: {value}")
    return parsed


def _decode_json(payload: bytes, *, label: str) -> object:
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ConfigurationError(f"{label} is not valid UTF-8 JSON") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_object_pairs,
            parse_constant=_reject_nonstandard_json_constant,
            parse_float=_parse_finite_json_float,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise ConfigurationError(f"{label} is not valid UTF-8 JSON") from exc


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"{label} must be a JSON object")
    return value


def _require_exact_keys(
    value: Mapping[str, object],
    *,
    required: frozenset[str],
    allowed: frozenset[str],
    label: str,
) -> None:
    keys = set(value)
    missing = sorted(required - keys)
    extra = sorted(keys - allowed)
    if missing:
        raise ConfigurationError(f"{label} is missing required fields: {missing}")
    if extra:
        raise ConfigurationError(f"{label} has unexpected fields: {extra}")


def _require_nonempty_string(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{label} must be a non-empty string")
    return value


def _require_enum_string(
    value: object,
    *,
    allowed: frozenset[str],
    label: str,
) -> str:
    if not isinstance(value, str):
        raise ConfigurationError(f"{label} must be a string")
    if value not in allowed:
        raise ConfigurationError(f"{label} is unsupported")
    return value


def _require_exact_version(value: object, *, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value != 1:
        raise ConfigurationError(f"{label} must equal integer 1")
    return value


def _require_true(value: object, *, label: str) -> None:
    if value is not True:
        raise ConfigurationError(f"{label} must equal true")


def _validate_sha256(value: object, *, label: str, required: bool) -> str | None:
    if value is None and not required:
        return None
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
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


def _validate_instance_contract(
    instance: Mapping[str, object],
    *,
    label: str,
) -> tuple[str, str, int, str, GenomeReference]:
    _require_exact_keys(instance, required=_INSTANCE_KEYS, allowed=_INSTANCE_KEYS, label=label)

    instance_id = _require_nonempty_string(
        instance.get("instance_id"), label=f"{label}.instance_id"
    )
    if _INSTANCE_ID_PATTERN.fullmatch(instance_id) is None:
        raise ConfigurationError(
            f"{label}.instance_id must match ^[a-z][a-z0-9-]{{2,127}}$"
        )

    primary_name = _require_nonempty_string(
        instance.get("primary_name"), label=f"{label}.primary_name"
    )
    if primary_name not in REQUIRED_QSOS:
        raise ConfigurationError(
            f"{label}.primary_name must be one of the canonical names: "
            + ", ".join(REQUIRED_QSOS)
        )

    secondary_name = _require_nonempty_string(
        instance.get("secondary_name"), label=f"{label}.secondary_name"
    )
    if _SECONDARY_NAME_PATTERN.fullmatch(secondary_name) is None:
        raise ConfigurationError(
            f"{label}.secondary_name does not match the published schema"
        )

    declared_name = _require_nonempty_string(
        instance.get("declared_name"), label=f"{label}.declared_name"
    )
    expected_declared_name = f"{primary_name}-{secondary_name}-Vespers"
    if declared_name != expected_declared_name:
        raise ConfigurationError(
            f"{label}.declared_name must equal {expected_declared_name}"
        )
    if instance.get("lineage_suffix") != "Vespers":
        raise ConfigurationError(f"{label}.lineage_suffix must equal Vespers")

    schema_version = _require_exact_version(
        instance.get("schema_version"), label=f"{label}.schema_version"
    )
    version = _require_nonempty_string(instance.get("version"), label=f"{label}.version")
    if _VERSION_PATTERN.fullmatch(version) is None:
        raise ConfigurationError(f"{label}.version does not match the published schema")

    genome_value = _require_mapping(instance.get("genome"), label=f"{label}.genome")
    _require_exact_keys(
        genome_value,
        required=frozenset({"repository", "path", "schema_version"}),
        allowed=_GENOME_KEYS,
        label=f"{label}.genome",
    )
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
    genome_schema_version = _require_exact_version(
        genome_value.get("schema_version"), label=f"{label}.genome.schema_version"
    )
    expected_hash = (
        _validate_sha256(
            genome_value["sha256"],
            label=f"{label}.genome.sha256",
            required=True,
        )
        if "sha256" in genome_value
        else None
    )

    identity_declaration = _require_mapping(
        instance.get("identity_declaration"), label=f"{label}.identity_declaration"
    )
    _require_exact_keys(
        identity_declaration,
        required=_IDENTITY_DECLARATION_KEYS,
        allowed=_IDENTITY_DECLARATION_KEYS,
        label=f"{label}.identity_declaration",
    )
    _require_enum_string(
        identity_declaration.get("secondary_name_basis"),
        allowed=frozenset(
            {
                "declared_intent",
                "secondary_focus",
                "demonstrated_specialization",
            }
        ),
        label=f"{label}.identity_declaration.secondary_name_basis",
    )
    secondary_focus = _require_nonempty_string(
        identity_declaration.get("secondary_focus"),
        label=f"{label}.identity_declaration.secondary_focus",
    )
    if not 3 <= len(secondary_focus) <= 300:
        raise ConfigurationError(
            f"{label}.identity_declaration.secondary_focus must contain 3 to 300 characters"
        )
    _require_true(
        identity_declaration.get("chosen_at_freeze_point"),
        label=f"{label}.identity_declaration.chosen_at_freeze_point",
    )
    _require_true(
        identity_declaration.get("human_review_required"),
        label=f"{label}.identity_declaration.human_review_required",
    )

    development = _require_mapping(
        instance.get("development"), label=f"{label}.development"
    )
    _require_exact_keys(
        development,
        required=_DEVELOPMENT_KEYS,
        allowed=_DEVELOPMENT_KEYS,
        label=f"{label}.development",
    )
    for field in (
        "interpretation_enabled",
        "self_reflection_enabled",
        "immutable_fields_locked",
    ):
        _require_true(development.get(field), label=f"{label}.development.{field}")
    _require_enum_string(
        development.get("self_edit_mode"),
        allowed=frozenset({"proposal_only"}),
        label=f"{label}.development.self_edit_mode",
    )
    proposal_log = _require_nonempty_string(
        development.get("proposal_log"),
        label=f"{label}.development.proposal_log",
    )
    if _PROPOSAL_LOG_PATTERN.fullmatch(proposal_log) is None:
        raise ConfigurationError(
            f"{label}.development.proposal_log does not match the published schema"
        )
    max_proposals = development.get("max_proposals_per_run")
    if (
        isinstance(max_proposals, bool)
        or not isinstance(max_proposals, int)
        or not 1 <= max_proposals <= 20
    ):
        raise ConfigurationError(
            f"{label}.development.max_proposals_per_run must be an integer from 1 to 20"
        )

    sprite_review = _require_mapping(
        instance.get("sprite_review"), label=f"{label}.sprite_review"
    )
    _require_exact_keys(
        sprite_review,
        required=_SPRITE_REVIEW_KEYS,
        allowed=_SPRITE_REVIEW_KEYS,
        label=f"{label}.sprite_review",
    )
    _require_true(
        sprite_review.get("required"), label=f"{label}.sprite_review.required"
    )
    _require_enum_string(
        sprite_review.get("sprite"),
        allowed=frozenset({"aequitas"}),
        label=f"{label}.sprite_review.sprite",
    )
    _require_enum_string(
        sprite_review.get("activation_rule"),
        allowed=frozenset({"pending_until_sprite_and_human_review"}),
        label=f"{label}.sprite_review.activation_rule",
    )
    _require_enum_string(
        instance.get("status"),
        allowed=frozenset({"draft", "pending_review", "active", "frozen", "retired"}),
        label=f"{label}.status",
    )

    return (
        instance_id,
        primary_name,
        schema_version,
        version,
        GenomeReference(
            repository=repository,
            path=genome_path,
            schema_version=genome_schema_version,
            sha256=expected_hash,
        ),
    )


def load_runtime_config(
    path: str | Path,
    *,
    expected_primary_names: Iterable[str] | None = None,
) -> RuntimeConfig:
    """Load and structurally validate local instance metadata without resolving genomes."""
    source = Path(path)
    payload = _read_bounded_file(
        source,
        max_bytes=MAX_CONFIG_BYTES,
        label="configuration file",
    )
    document = _decode_json(payload, label=f"configuration file: {source}")
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
        (
            instance_id,
            primary_name,
            schema_version,
            version,
            genome,
        ) = _validate_instance_contract(instance, label=label)
        if instance_id in instance_ids:
            raise ConfigurationError(f"duplicate instance_id: {instance_id}")
        if primary_name in primary_names:
            raise ConfigurationError(f"duplicate primary_name: {primary_name}")
        instance_ids.add(instance_id)
        primary_names.add(primary_name)
        instances.append(
            InstanceManifest(
                instance_id=instance_id,
                primary_name=primary_name,
                schema_version=schema_version,
                version=version,
                genome=genome,
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

    return RuntimeConfig(
        source=source,
        sha256=_sha256_bytes(payload),
        instances=tuple(instances),
    )


def resolve_local_genomes(
    config: RuntimeConfig,
    genome_root: str | Path,
) -> dict[str, str]:
    """Resolve only hash-pinned local genome JSON files and fail closed on any mismatch."""
    root = Path(genome_root)
    try:
        if not root.exists() or not root.is_dir() or root.is_symlink():
            raise ConfigurationError(
                f"genome root must be an existing non-symlink directory: {root}"
            )
        root_resolved = root.resolve()
    except ConfigurationError:
        raise
    except OSError as exc:
        raise ConfigurationError(
            f"genome root could not be inspected safely: {root}"
        ) from exc

    resolved: dict[str, str] = {}
    for instance in config.instances:
        reference = instance.genome
        expected_hash = _validate_sha256(
            reference.sha256,
            label=f"{instance.primary_name} genome sha256",
            required=True,
        )
        candidate = root / Path(*PurePosixPath(reference.path).parts)
        try:
            candidate_resolved = candidate.resolve(strict=False)
        except OSError as exc:
            raise ConfigurationError(
                f"{instance.primary_name} genome path could not be resolved safely"
            ) from exc
        if (
            candidate_resolved != root_resolved
            and root_resolved not in candidate_resolved.parents
        ):
            raise ConfigurationError(
                f"{instance.primary_name} genome escapes the configured root"
            )
        payload = _read_bounded_file(
            candidate,
            max_bytes=MAX_GENOME_BYTES,
            label=f"{instance.primary_name} genome",
        )
        actual_hash = _sha256_bytes(payload)
        if actual_hash != expected_hash:
            raise ConfigurationError(
                f"{instance.primary_name} genome hash mismatch: "
                f"expected {expected_hash}, got {actual_hash}"
            )
        genome_document = _decode_json(
            payload,
            label=f"{instance.primary_name} genome",
        )
        genome_object = _require_mapping(
            genome_document,
            label=f"{instance.primary_name} genome",
        )
        genome_schema_version = _require_exact_version(
            genome_object.get("schema_version"),
            label=f"{instance.primary_name} genome.schema_version",
        )
        if genome_schema_version != reference.schema_version:
            raise ConfigurationError(
                f"{instance.primary_name} genome schema_version "
                "does not match its reference"
            )
        resolved[instance.instance_id] = actual_hash

    return resolved
