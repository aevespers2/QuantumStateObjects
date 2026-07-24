#!/usr/bin/env python3
"""Independent QuantumStateObjects evaluator for QSO-FABRIC interface compatibility."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

CONTRACT_ID = "QSO-INTERFACE-COMPATIBILITY-001"
CONTRACT_VERSION = "1.0.0"
PRODUCER_REPOSITORY = "aevespers2/QSO-FABRIC"
PRODUCER_PULL_REQUEST = 21
PRODUCER_HEAD = "25036a5cfcea79e204a4660ddd1af09c054935b1"
PRODUCER_FIXTURE_BLOB = "143b80448cb4623682669ab8e6a9599239dd5847"
CONSUMER_REPOSITORY = "aevespers2/QuantumStateObjects"
DECLARED_INTERFACES = frozenset({"qso-event-ledger", "qso-runtime-report"})

FACTS = (
    "source_tuple_current",
    "known_interface",
    "interface_name_match",
    "producer_role_valid",
    "consumer_role_valid",
    "protocol_match",
    "schema_version_match",
    "idempotency_match",
    "retry_policy_match",
    "default_deny_preserved",
    "correction_supported",
    "rollback_supported",
    "evidence_bound",
    "authority_promotion_absent",
)
REASONS = (
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
)
RULES: tuple[tuple[str, str, Callable[[bool], bool]], ...] = tuple(
    (fact, reason, lambda value: not value) for fact, reason in zip(FACTS, REASONS, strict=True)
)


def _pairs_to_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate key {key!r}")
        output[key] = value
    return output


def _constant_forbidden(token: str) -> None:
    raise ValueError(f"non-finite number {token!r} is forbidden")


def _walk_numbers(value: Any, location: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"non-finite number at {location}")
    if isinstance(value, dict):
        for key, child in value.items():
            _walk_numbers(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_numbers(child, f"{location}[{index}]")


def parse_json(raw: bytes, label: str) -> Any:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not strict UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_to_object,
            parse_constant=_constant_forbidden,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is invalid JSON: {exc}") from exc
    _walk_numbers(value)
    return value


def parse_path(path: Path) -> Any:
    return parse_json(path.read_bytes(), str(path))


def closed_object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    missing = sorted(fields - set(value))
    extra = sorted(set(value) - fields)
    if missing or extra:
        raise ValueError(f"{label} fields differ; missing={missing}, extra={extra}")
    return value


def validate_source_tuple(data: Any, repository_root: Path) -> dict[str, Any]:
    root = closed_object(data, {"contract_id", "version", "producer", "consumer", "authority_effect"}, "tuple")
    if root["contract_id"] != CONTRACT_ID or root["version"] != CONTRACT_VERSION:
        raise ValueError("tuple contract generation mismatch")
    if root["authority_effect"] != "none":
        raise ValueError("tuple may not create authority")

    producer = closed_object(
        root["producer"],
        {
            "repository",
            "pull_request",
            "head_sha",
            "fixture_path",
            "fixture_git_blob",
            "workflow_run",
            "artifact_id",
            "artifact_digest",
            "evidence_expires_at",
        },
        "tuple.producer",
    )
    consumer = closed_object(
        root["consumer"],
        {"repository", "fixture_path", "validator_path", "test_path", "workflow_path"},
        "tuple.consumer",
    )

    expected_producer = {
        "repository": PRODUCER_REPOSITORY,
        "pull_request": PRODUCER_PULL_REQUEST,
        "head_sha": PRODUCER_HEAD,
        "fixture_path": "fixtures/qso-interface-compatibility-v1.json",
        "fixture_git_blob": PRODUCER_FIXTURE_BLOB,
    }
    for field, expected in expected_producer.items():
        if producer[field] != expected:
            raise ValueError(f"producer {field} mismatch")
    if type(producer["workflow_run"]) is not int or producer["workflow_run"] <= 0:
        raise ValueError("producer workflow_run must be a positive integer")
    if type(producer["artifact_id"]) is not int or producer["artifact_id"] <= 0:
        raise ValueError("producer artifact_id must be a positive integer")
    if not isinstance(producer["artifact_digest"], str) or not producer["artifact_digest"].startswith("sha256:"):
        raise ValueError("producer artifact_digest must be a sha256 digest")
    if not isinstance(producer["evidence_expires_at"], str) or not producer["evidence_expires_at"].endswith("Z"):
        raise ValueError("producer evidence expiry must be a UTC timestamp")

    expected_consumer = {
        "repository": CONSUMER_REPOSITORY,
        "fixture_path": "fixtures/qso-interface-compatibility-v1.json",
        "validator_path": "tools/validate_fabric_interface_compatibility.py",
        "test_path": "tests/test_fabric_interface_compatibility.py",
        "workflow_path": ".github/workflows/fabric-interface-compatibility.yml",
    }
    if consumer != expected_consumer:
        raise ValueError("consumer path or repository tuple mismatch")

    fixture_path = repository_root / consumer["fixture_path"]
    if not fixture_path.is_file():
        raise ValueError("consumer fixture is missing")
    actual_blob = subprocess.run(
        ["git", "hash-object", str(fixture_path)],
        cwd=repository_root,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if actual_blob != PRODUCER_FIXTURE_BLOB:
        raise ValueError(f"consumer fixture blob mismatch: {actual_blob}")
    return {"producer_head": PRODUCER_HEAD, "fixture_git_blob": actual_blob}


def evaluate(facts: dict[str, bool]) -> tuple[str, list[str]]:
    failures: list[str] = []
    for fact, reason, predicate in RULES:
        if predicate(facts[fact]):
            failures.append(reason)
    return (
        "BLOCKED" if failures else "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL",
        failures,
    )


def validate_corpus(data: Any) -> list[dict[str, Any]]:
    corpus = closed_object(data, {"contract_id", "version", "fact_order", "reason_order", "cases"}, "corpus")
    if corpus["contract_id"] != CONTRACT_ID or corpus["version"] != CONTRACT_VERSION:
        raise ValueError("corpus contract generation mismatch")
    if corpus["fact_order"] != list(FACTS):
        raise ValueError("corpus fact order mismatch")
    if corpus["reason_order"] != list(REASONS):
        raise ValueError("corpus reason order mismatch")
    if not isinstance(corpus["cases"], list) or not corpus["cases"]:
        raise ValueError("corpus cases must be a non-empty array")

    seen_cases: set[str] = set()
    reason_coverage: set[str] = set()
    positive_interfaces: set[str] = set()
    output: list[dict[str, Any]] = []

    for index, raw_case in enumerate(corpus["cases"]):
        case = closed_object(raw_case, {"case_id", "interface", "facts", "expected"}, f"case[{index}]")
        case_id = case["case_id"]
        interface = case["interface"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"case[{index}] has invalid case_id")
        if case_id in seen_cases:
            raise ValueError(f"duplicate case_id {case_id}")
        seen_cases.add(case_id)
        if not isinstance(interface, str) or not interface:
            raise ValueError(f"case[{index}] has invalid interface")

        facts = closed_object(case["facts"], set(FACTS), f"case[{index}].facts")
        for fact in FACTS:
            if type(facts[fact]) is not bool:
                raise ValueError(f"case[{index}].facts.{fact} must be boolean")
        if facts["known_interface"] != (interface in DECLARED_INTERFACES):
            raise ValueError(f"case[{index}] known-interface fact contradicts the interface")

        expected = closed_object(case["expected"], {"disposition", "reasons"}, f"case[{index}].expected")
        if expected["disposition"] not in {"BLOCKED", "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL"}:
            raise ValueError(f"case[{index}] has invalid expected disposition")
        if not isinstance(expected["reasons"], list) or any(type(reason) is not str for reason in expected["reasons"]):
            raise ValueError(f"case[{index}] expected reasons must be strings")
        if len(expected["reasons"]) != len(set(expected["reasons"])):
            raise ValueError(f"case[{index}] expected reasons contain duplicates")
        canonical_reasons = [reason for reason in REASONS if reason in expected["reasons"]]
        if canonical_reasons != expected["reasons"]:
            raise ValueError(f"case[{index}] expected reasons are out of order or unknown")

        disposition, reasons = evaluate(facts)
        if disposition != expected["disposition"]:
            raise ValueError(f"case[{index}] disposition mismatch")
        if reasons != expected["reasons"]:
            raise ValueError(f"case[{index}] reason mismatch")
        reason_coverage.update(reasons)
        if not reasons:
            positive_interfaces.add(interface)
        output.append({"case_id": case_id, "interface": interface, "disposition": disposition, "reasons": reasons})

    missing = sorted(set(REASONS) - reason_coverage)
    if missing:
        raise ValueError(f"corpus misses obstruction coverage: {missing}")
    if positive_interfaces != set(DECLARED_INTERFACES):
        raise ValueError(f"positive-interface coverage mismatch: {sorted(positive_interfaces)}")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", nargs="?", type=Path, default=Path("fixtures/qso-interface-compatibility-v1.json"))
    parser.add_argument("source_tuple", nargs="?", type=Path, default=Path("contracts/qso-interface-source-tuple-v1.json"))
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        tuple_result = validate_source_tuple(parse_path(args.source_tuple), args.repository_root.resolve())
        results = validate_corpus(parse_path(args.corpus))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "contract_id": CONTRACT_ID,
                "version": CONTRACT_VERSION,
                "source_tuple": tuple_result,
                "case_count": len(results),
                "results": results,
                "authority_effect": "none",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
