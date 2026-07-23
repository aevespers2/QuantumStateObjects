#!/usr/bin/env python3
"""Validate the documentation-only ecosystem interface compatibility profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

PROFILE_PATH = Path("docs/ecosystem-interface-compatibility-v0.json")

EXPECTED_TOP_LEVEL = {
    "profile_id",
    "profile_version",
    "status",
    "scope",
    "producer_source",
    "consumer_context",
    "interfaces",
    "compatibility_invariants",
    "gluing_witnesses",
    "denied_inferences",
    "skill_tree_mapping",
    "proposed_subdivisions",
    "decisions_required",
    "authority_effect",
}

EXPECTED_SOURCE = {
    "repository": "aevespers2/QSO-FABRIC",
    "commit": "738cf25aec9b2bae0b71c50374585bab36934ef3",
    "path": "qso.manifest.json",
    "git_blob_sha1": "5070ac6615b8127b14a9f230678f58a081c6c2c4",
    "sha256": "c5e6d2e42fdbe9703d9f28c7f65ffff02208bff52fa96ee7090bfcbcb5dea728",
    "size_bytes": 1564,
}

EXPECTED_INTERFACES = {
    "qso-event-ledger": {
        "manifest_role": "producer",
        "protocol": "append-only-json",
        "schema_version": "1.0.0",
        "idempotent": True,
        "retry_limit": 0,
        "obstruction": "ROLE_AND_NAMESPACE_COLLISION",
    },
    "qso-runtime-report": {
        "manifest_role": "producer",
        "protocol": "json-file",
        "schema_version": "1.0.0",
        "idempotent": True,
        "retry_limit": 0,
        "obstruction": "ROLE_AND_SEMANTIC_CLASS_COLLISION",
    },
}

REQUIRED_CATEGORIES = {
    "CAT-012": {"012-A", "012-B", "012-D", "012-E"},
    "CAT-017": {"017-C", "017-E"},
    "CAT-031": {"031-A", "031-D", "031-E"},
    "CAT-040": {"040-D", "040-E"},
    "CAT-054": {"054-A", "054-E"},
    "CAT-059": {"059-B", "059-E"},
}

REQUIRED_DENIALS = {
    "documentation is not contract acceptance",
    "byte identity is not semantic compatibility",
    "schema version equality is not namespace agreement",
    "successful validation is not ecosystem admission",
    "transport or display is not canonical status",
    "runtime or Fabric success is not authority",
    "this profile grants no merge release publication or deployment approval",
}


class StrictJSONError(ValueError):
    """Raised when JSON is ambiguous or contains forbidden values."""


def _reject_constant(value: str) -> None:
    raise StrictJSONError(f"non-finite JSON number is forbidden: {value}")


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise StrictJSONError(f"profile is not strict UTF-8: {exc}") from exc

    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, StrictJSONError) as exc:
        raise StrictJSONError(str(exc)) from exc

    if not isinstance(value, dict):
        raise StrictJSONError("profile root must be an object")
    _reject_nonfinite_recursive(value)
    return value


def _reject_nonfinite_recursive(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise StrictJSONError("non-finite number found")
    if isinstance(value, list):
        for item in value:
            _reject_nonfinite_recursive(item)
    if isinstance(value, dict):
        for item in value.values():
            _reject_nonfinite_recursive(item)


def _require_exact_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} unknown fields: {', '.join(extra)}")


def _require_nonempty_string_list(value: Any, label: str, errors: list[str], minimum: int = 1) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{label} must contain at least {minimum} entries")
        return
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label} entries must be non-empty strings")
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _require_exact_keys(profile, EXPECTED_TOP_LEVEL, "profile", errors)

    if profile.get("profile_id") != "QSO-INTERFACE-COMPATIBILITY-001":
        errors.append("unexpected profile_id")
    if profile.get("profile_version") != "0.1.0":
        errors.append("unexpected profile_version")
    if profile.get("status") != "BLOCKED_ROLE_COLLISION":
        errors.append("status must remain BLOCKED_ROLE_COLLISION pending architecture approval")
    if profile.get("scope") != "documentation-and-synthetic-validation-only":
        errors.append("scope must remain documentation-and-synthetic-validation-only")
    if profile.get("authority_effect") != "none":
        errors.append("authority_effect must be none")

    source = profile.get("producer_source")
    _require_exact_keys(source, set(EXPECTED_SOURCE), "producer_source", errors)
    if isinstance(source, dict):
        for key, expected in EXPECTED_SOURCE.items():
            actual = source.get(key)
            if type(actual) is not type(expected) or actual != expected:
                errors.append(f"producer_source.{key} does not match the immutable source tuple")

    context = profile.get("consumer_context")
    context_fields = {"repository", "branch", "role", "exact_head_binding"}
    _require_exact_keys(context, context_fields, "consumer_context", errors)
    if isinstance(context, dict):
        expected_context = {
            "repository": "aevespers2/QuantumStateObjects",
            "branch": "docs/pages-architecture-onboarding",
            "role": "bounded-local-runtime-and-evidence-subsystem",
            "exact_head_binding": "workflow-runtime",
        }
        for key, expected in expected_context.items():
            if context.get(key) != expected:
                errors.append(f"consumer_context.{key} is unexpected")

    interfaces = profile.get("interfaces")
    interface_fields = {
        "name",
        "manifest_role",
        "protocol",
        "schema_version",
        "idempotent",
        "retry_limit",
        "local_semantic_overlap",
        "obstruction",
        "required_resolution",
    }
    if not isinstance(interfaces, list) or len(interfaces) != 2:
        errors.append("interfaces must contain exactly two entries")
    else:
        seen: set[str] = set()
        for index, interface in enumerate(interfaces):
            _require_exact_keys(interface, interface_fields, f"interfaces[{index}]", errors)
            if not isinstance(interface, dict):
                continue
            name = interface.get("name")
            if not isinstance(name, str):
                errors.append(f"interfaces[{index}].name must be a string")
                continue
            if name in seen:
                errors.append(f"duplicate interface name: {name}")
            seen.add(name)
            expected = EXPECTED_INTERFACES.get(name)
            if expected is None:
                errors.append(f"unexpected interface: {name}")
                continue
            for key, expected_value in expected.items():
                actual = interface.get(key)
                if type(actual) is not type(expected_value) or actual != expected_value:
                    errors.append(f"{name}.{key} does not match the observed manifest boundary")
            overlap = interface.get("local_semantic_overlap")
            if not isinstance(overlap, str) or not overlap.strip():
                errors.append(f"{name}.local_semantic_overlap must be a non-empty string")
            _require_nonempty_string_list(
                interface.get("required_resolution"),
                f"{name}.required_resolution",
                errors,
                minimum=5,
            )
        if seen != set(EXPECTED_INTERFACES):
            errors.append("interface set is incomplete")

    _require_nonempty_string_list(
        profile.get("compatibility_invariants"),
        "compatibility_invariants",
        errors,
        minimum=10,
    )
    _require_nonempty_string_list(
        profile.get("gluing_witnesses"),
        "gluing_witnesses",
        errors,
        minimum=5,
    )
    _require_nonempty_string_list(
        profile.get("denied_inferences"),
        "denied_inferences",
        errors,
        minimum=len(REQUIRED_DENIALS),
    )
    denied = profile.get("denied_inferences")
    if isinstance(denied, list) and set(denied) != REQUIRED_DENIALS:
        errors.append("denied_inferences must exactly preserve the authority boundary")

    mappings = profile.get("skill_tree_mapping")
    mapping_fields = {"category_id", "subdivision_ids", "application"}
    observed_categories: dict[str, set[str]] = {}
    if not isinstance(mappings, list) or len(mappings) != len(REQUIRED_CATEGORIES):
        errors.append("skill_tree_mapping must contain the six selected categories")
    else:
        for index, mapping in enumerate(mappings):
            _require_exact_keys(mapping, mapping_fields, f"skill_tree_mapping[{index}]", errors)
            if not isinstance(mapping, dict):
                continue
            category_id = mapping.get("category_id")
            subdivisions = mapping.get("subdivision_ids")
            application = mapping.get("application")
            if not isinstance(category_id, str):
                errors.append(f"skill_tree_mapping[{index}].category_id must be a string")
                continue
            if category_id in observed_categories:
                errors.append(f"duplicate skill-tree category: {category_id}")
            if not isinstance(subdivisions, list) or any(not isinstance(item, str) for item in subdivisions):
                errors.append(f"{category_id}.subdivision_ids must be a string list")
                observed_categories[category_id] = set()
            else:
                observed_categories[category_id] = set(subdivisions)
                if len(subdivisions) != len(set(subdivisions)):
                    errors.append(f"{category_id}.subdivision_ids contains duplicates")
            if not isinstance(application, str) or not application.strip():
                errors.append(f"{category_id}.application must be a non-empty string")
        if set(observed_categories) != set(REQUIRED_CATEGORIES):
            errors.append("skill-tree category set is incomplete")
        for category_id, expected_subdivisions in REQUIRED_CATEGORIES.items():
            if observed_categories.get(category_id) != expected_subdivisions:
                errors.append(f"{category_id} subdivision mapping drifted")

    _require_nonempty_string_list(
        profile.get("proposed_subdivisions"),
        "proposed_subdivisions",
        errors,
        minimum=5,
    )
    _require_nonempty_string_list(
        profile.get("decisions_required"),
        "decisions_required",
        errors,
        minimum=7,
    )

    serialized = json.dumps(profile, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    if "accepted" in profile.get("status", "").lower():
        errors.append("profile status must not imply acceptance")
    if '"authority_effect":"none"' not in serialized:
        errors.append("canonical profile must preserve authority_effect none")

    return errors


def build_report(path: Path, profile: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "profile_path": path.as_posix(),
        "profile_sha256": hashlib.sha256(raw).hexdigest(),
        "profile_size_bytes": len(raw),
        "validation_status": "passed" if not errors else "failed",
        "error_count": len(errors),
        "errors": errors,
        "interface_count": len(profile.get("interfaces", [])) if isinstance(profile, dict) else 0,
        "disposition": profile.get("status") if isinstance(profile, dict) else None,
        "authority_effect": profile.get("authority_effect") if isinstance(profile, dict) else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(PROFILE_PATH))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    path = Path(args.path)
    try:
        profile = strict_load(path)
        errors = validate_profile(profile)
    except (OSError, StrictJSONError) as exc:
        profile = {}
        errors = [str(exc)]

    report = build_report(path, profile, errors)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
