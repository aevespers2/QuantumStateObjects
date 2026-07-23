#!/usr/bin/env python3
"""Validate the documentation-only QSO interface compatibility profile."""

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
    "producer_corpus",
    "consumer_candidate",
    "interfaces",
    "payload_contract_gaps",
    "required_gluing_witnesses",
    "denied_inferences",
    "skill_tree_mapping",
    "proposed_subdivisions",
    "decisions_required",
    "authority_effect",
}

EXPECTED_SOURCE = {
    "repository": "aevespers2/QSO-FABRIC",
    "pull_request": 21,
    "head_sha": "25036a5cfcea79e204a4660ddd1af09c054935b1",
    "fixture_path": "fixtures/qso-interface-compatibility-v1.json",
    "fixture_git_blob": "143b80448cb4623682669ab8e6a9599239dd5847",
    "contract_id": "QSO-INTERFACE-COMPATIBILITY-001",
    "contract_version": "1.0.0",
    "workflow_run": 29986841042,
    "artifact_id": 8555344357,
    "artifact_digest": "sha256:09be1df24f4ab8b08708dd521c6720f4c95195d3e4379cecaad6d1a4b026a238",
    "evidence_expires_at": "2026-10-21T06:59:56Z",
}

EXPECTED_REASON_ORDER = [
    "STALE_SOURCE_TUPLE",
    "UNKNOWN_INTERFACE",
    "INTERFACE_NAME_MISMATCH",
    "PRODUCER_ROLE_INVALID",
    "CONSUMER_ROLE_INVALID",
    "PROTOCOL_MISMATCH",
    "SCHEMA_VERSION_MISMATCH",
    "IDEMPOTENCY_MISMATCH",
    "RETRY_POLICY_MISMATCH",
    "DEFAULT_DENY_NOT_PRESERVED",
    "CORRECTION_SEMANTICS_MISSING",
    "ROLLBACK_SEMANTICS_MISSING",
    "EVIDENCE_NOT_BOUND",
    "AUTHORITY_PROMOTION_DETECTED",
]

EXPECTED_INTERFACES = {
    "qso-event-ledger": {
        "protocol": "append-only-json",
        "schema_version": "1.0.0",
        "idempotent": True,
        "retry_limit": 0,
        "payload_contract_status": "not_accepted",
        "obstruction": "ROLE_NAMESPACE_AND_PAYLOAD_COLLISION",
    },
    "qso-runtime-report": {
        "protocol": "json-file",
        "schema_version": "1.0.0",
        "idempotent": True,
        "retry_limit": 0,
        "payload_contract_status": "not_accepted",
        "obstruction": "ROLE_SEMANTIC_CLASS_AND_PAYLOAD_COLLISION",
    },
}

EXPECTED_CONSUMER = {
    "repository": "aevespers2/QuantumStateObjects",
    "branch": "docs/pages-architecture-onboarding",
    "source_tuple_path": "contracts/qso-interface-source-tuple-v1.json",
    "fixture_path": "fixtures/qso-interface-compatibility-v1.json",
    "planned_validator_path": "tools/validate_fabric_interface_compatibility.py",
    "planned_test_path": "tests/test_fabric_interface_compatibility.py",
    "planned_workflow_path": ".github/workflows/fabric-interface-compatibility.yml",
    "implementation_status": "not_implemented",
    "documentation_profile_path": "docs/ecosystem-interface-compatibility-v0.json",
    "documentation_validator_path": "scripts/check_ecosystem_interface_compatibility.py",
}

REQUIRED_CATEGORIES = {
    "CAT-012": {"012-A", "012-B", "012-D", "012-E"},
    "CAT-017": {"017-C", "017-E"},
    "CAT-031": {"031-A", "031-D", "031-E"},
    "CAT-040": {"040-D", "040-E"},
    "CAT-054": {"054-A", "054-E"},
    "CAT-059": {"059-B", "059-E"},
}

EXPECTED_DENIALS = {
    "producer corpus availability is not independent consumer completion",
    "synthetic compatibility is not payload schema acceptance",
    "byte identity is not semantic ownership",
    "schema version equality is not namespace agreement",
    "runtime or Fabric success is not Repository 1 canonical acceptance",
    "transport or display is not authority",
    "documentation validation grants no merge release publication deployment or operational authority",
}


class StrictJSONError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise StrictJSONError(f"non-finite JSON number is forbidden: {value}")


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise StrictJSONError("non-finite JSON number is forbidden")
    if isinstance(value, dict):
        for item in value.values():
            _reject_nonfinite(item)
    elif isinstance(value, list):
        for item in value:
            _reject_nonfinite(item)


def strict_load(path: Path) -> dict[str, Any]:
    try:
        text = path.read_bytes().decode("utf-8", errors="strict")
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
    _reject_nonfinite(value)
    return value


def _exact_keys(value: Any, expected: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} unknown fields: {', '.join(extra)}")


def _exact_typed_mapping(value: Any, expected: dict[str, Any], label: str, errors: list[str]) -> None:
    _exact_keys(value, set(expected), label, errors)
    if not isinstance(value, dict):
        return
    for key, expected_value in expected.items():
        actual = value.get(key)
        if type(actual) is not type(expected_value) or actual != expected_value:
            errors.append(f"{label}.{key} does not match the recorded immutable value")


def _string_list(value: Any, label: str, errors: list[str], minimum: int) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{label} must contain at least {minimum} entries")
        return
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label} entries must be non-empty strings")
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _exact_keys(profile, EXPECTED_TOP_LEVEL, "profile", errors)

    expected_scalars = {
        "profile_id": "QSO-INTERFACE-COMPATIBILITY-DOCUMENTATION-001",
        "profile_version": "0.2.0",
        "status": "PRODUCER_CORPUS_BOUND_CONSUMER_AND_PAYLOAD_PENDING",
        "scope": "documentation-and-synthetic-validation-only",
        "authority_effect": "none",
    }
    for key, expected in expected_scalars.items():
        if profile.get(key) != expected:
            errors.append(f"{key} must be {expected}")

    _exact_typed_mapping(profile.get("producer_source"), EXPECTED_SOURCE, "producer_source", errors)
    _exact_typed_mapping(profile.get("consumer_candidate"), EXPECTED_CONSUMER, "consumer_candidate", errors)

    corpus = profile.get("producer_corpus")
    corpus_fields = {
        "case_count",
        "fact_count",
        "reason_count",
        "positive_disposition",
        "negative_disposition",
        "reason_order",
    }
    _exact_keys(corpus, corpus_fields, "producer_corpus", errors)
    if isinstance(corpus, dict):
        for key, expected in (("case_count", 17), ("fact_count", 14), ("reason_count", 14)):
            actual = corpus.get(key)
            if type(actual) is not int or actual != expected:
                errors.append(f"producer_corpus.{key} must be integer {expected}")
        if corpus.get("positive_disposition") != "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL":
            errors.append("producer_corpus positive disposition drifted")
        if corpus.get("negative_disposition") != "BLOCKED":
            errors.append("producer_corpus negative disposition drifted")
        if corpus.get("reason_order") != EXPECTED_REASON_ORDER:
            errors.append("producer_corpus reason order drifted")

    interfaces = profile.get("interfaces")
    fields = {
        "name",
        "protocol",
        "schema_version",
        "idempotent",
        "retry_limit",
        "local_semantic_overlap",
        "payload_contract_status",
        "obstruction",
    }
    if not isinstance(interfaces, list) or len(interfaces) != 2:
        errors.append("interfaces must contain exactly two entries")
    else:
        seen: set[str] = set()
        for index, interface in enumerate(interfaces):
            _exact_keys(interface, fields, f"interfaces[{index}]", errors)
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
                    errors.append(f"{name}.{key} drifted")
            overlap = interface.get("local_semantic_overlap")
            if not isinstance(overlap, str) or not overlap.strip():
                errors.append(f"{name}.local_semantic_overlap must be non-empty")
        if seen != set(EXPECTED_INTERFACES):
            errors.append("interface set is incomplete")

    _string_list(profile.get("payload_contract_gaps"), "payload_contract_gaps", errors, 7)
    _string_list(profile.get("required_gluing_witnesses"), "required_gluing_witnesses", errors, 6)
    _string_list(profile.get("denied_inferences"), "denied_inferences", errors, 7)
    if isinstance(profile.get("denied_inferences"), list) and set(profile["denied_inferences"]) != EXPECTED_DENIALS:
        errors.append("denied_inferences must exactly preserve the authority boundary")

    mappings = profile.get("skill_tree_mapping")
    fields = {"category_id", "subdivision_ids", "application"}
    observed: dict[str, set[str]] = {}
    if not isinstance(mappings, list) or len(mappings) != len(REQUIRED_CATEGORIES):
        errors.append("skill_tree_mapping must contain exactly six categories")
    else:
        for index, mapping in enumerate(mappings):
            _exact_keys(mapping, fields, f"skill_tree_mapping[{index}]", errors)
            if not isinstance(mapping, dict):
                continue
            category = mapping.get("category_id")
            subdivisions = mapping.get("subdivision_ids")
            if not isinstance(category, str):
                errors.append(f"skill_tree_mapping[{index}].category_id must be a string")
                continue
            if category in observed:
                errors.append(f"duplicate skill-tree category: {category}")
            if not isinstance(subdivisions, list) or any(not isinstance(item, str) for item in subdivisions):
                errors.append(f"{category}.subdivision_ids must be a string list")
                observed[category] = set()
            else:
                observed[category] = set(subdivisions)
                if len(subdivisions) != len(set(subdivisions)):
                    errors.append(f"{category}.subdivision_ids contains duplicates")
            if not isinstance(mapping.get("application"), str) or not mapping["application"].strip():
                errors.append(f"{category}.application must be non-empty")
        if set(observed) != set(REQUIRED_CATEGORIES):
            errors.append("skill-tree category set is incomplete")
        for category, expected in REQUIRED_CATEGORIES.items():
            if observed.get(category) != expected:
                errors.append(f"{category} subdivision mapping drifted")

    _string_list(profile.get("proposed_subdivisions"), "proposed_subdivisions", errors, 5)
    _string_list(profile.get("decisions_required"), "decisions_required", errors, 7)

    status = profile.get("status", "")
    if isinstance(status, str) and "ACCEPTED" in status:
        errors.append("status must not imply acceptance")
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
        "producer_case_count": profile.get("producer_corpus", {}).get("case_count") if isinstance(profile, dict) else None,
        "consumer_implementation_status": profile.get("consumer_candidate", {}).get("implementation_status") if isinstance(profile, dict) else None,
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
