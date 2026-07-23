#!/usr/bin/env python3
"""Independent fail-closed consumer for QSO-INTERFACE-COMPATIBILITY-001."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

FACT_ORDER = [
    "source_tuple_current", "known_interface", "interface_name_match",
    "producer_role_valid", "consumer_role_valid", "protocol_match",
    "schema_version_match", "idempotency_match", "retry_policy_match",
    "default_deny_preserved", "correction_supported", "rollback_supported",
    "evidence_bound", "authority_promotion_absent",
]
REASON_ORDER = [
    "STALE_SOURCE_TUPLE", "UNKNOWN_INTERFACE", "INTERFACE_NAME_MISMATCH",
    "PRODUCER_ROLE_INVALID", "CONSUMER_ROLE_INVALID", "PROTOCOL_MISMATCH",
    "SCHEMA_VERSION_MISMATCH", "IDEMPOTENCY_MISMATCH", "RETRY_POLICY_MISMATCH",
    "DEFAULT_DENY_NOT_PRESERVED", "CORRECTION_SEMANTICS_MISSING",
    "ROLLBACK_SEMANTICS_MISSING", "EVIDENCE_NOT_BOUND",
    "AUTHORITY_PROMOTION_DETECTED",
]
FACT_TO_REASON = dict(zip(FACT_ORDER, REASON_ORDER, strict=True))
KNOWN_INTERFACES = {"qso-event-ledger", "qso-runtime-report"}
TOP_FIELDS = {"contract_id", "version", "fact_order", "reason_order", "cases"}
CASE_FIELDS = {"case_id", "interface", "facts", "expected"}
EXPECTED_FIELDS = {"disposition", "reasons"}
EXPECTED_SHA256 = "baac67caaa6b213e5a50019c8cad011be1e1906699c7903391313b11677ac5d4"


class ValidationError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValidationError(f"non-finite number: {value}")


def parse_bytes(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValidationError("invalid UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValidationError(str(exc)) from exc
    _reject_nonfinite(value)
    return value


def _reject_nonfinite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("non-finite number")
    if isinstance(value, dict):
        for child in value.values():
            _reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            _reject_nonfinite(child)


def _closed(obj: dict[str, Any], allowed: set[str], context: str) -> None:
    unknown = set(obj) - allowed
    if unknown:
        raise ValidationError(f"{context}: unknown fields: {sorted(unknown)}")


def evaluate(facts: dict[str, bool]) -> tuple[str, list[str]]:
    reasons = [FACT_TO_REASON[name] for name in FACT_ORDER if facts[name] is False]
    return ("BLOCKED", reasons) if reasons else (
        "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL", []
    )


def validate_document(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ValidationError("top level must be an object")
    _closed(document, TOP_FIELDS, "top level")
    if set(document) != TOP_FIELDS:
        raise ValidationError("top level is incomplete")
    if document["contract_id"] != "QSO-INTERFACE-COMPATIBILITY-001":
        raise ValidationError("contract_id drift")
    if document["version"] != "1.0.0":
        raise ValidationError("version drift")
    if document["fact_order"] != FACT_ORDER:
        raise ValidationError("fact_order drift")
    if document["reason_order"] != REASON_ORDER:
        raise ValidationError("reason_order drift")
    cases = document["cases"]
    if not isinstance(cases, list) or len(cases) != 17:
        raise ValidationError("expected exactly 17 cases")

    ids: set[str] = set()
    reason_coverage: set[str] = set()
    compatible_interfaces: set[str] = set()
    results: list[dict[str, Any]] = []

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValidationError(f"case {index}: must be an object")
        _closed(case, CASE_FIELDS, f"case {index}")
        if set(case) != CASE_FIELDS:
            raise ValidationError(f"case {index}: incomplete")
        case_id = case["case_id"]
        interface = case["interface"]
        if not isinstance(case_id, str) or not case_id:
            raise ValidationError(f"case {index}: invalid case_id")
        if case_id in ids:
            raise ValidationError(f"duplicate case_id: {case_id}")
        ids.add(case_id)
        if not isinstance(interface, str) or not interface:
            raise ValidationError(f"{case_id}: invalid interface")

        facts = case["facts"]
        if not isinstance(facts, dict) or list(facts) != FACT_ORDER:
            raise ValidationError(f"{case_id}: fact fields/order drift")
        if any(type(facts[name]) is not bool for name in FACT_ORDER):
            raise ValidationError(f"{case_id}: every fact must be Boolean")
        if facts["known_interface"] != (interface in KNOWN_INTERFACES):
            raise ValidationError(f"{case_id}: known_interface is inconsistent")

        expected = case["expected"]
        if not isinstance(expected, dict):
            raise ValidationError(f"{case_id}: expected must be object")
        _closed(expected, EXPECTED_FIELDS, f"{case_id}.expected")
        if set(expected) != EXPECTED_FIELDS:
            raise ValidationError(f"{case_id}: expected is incomplete")

        disposition, reasons = evaluate(facts)
        if expected["disposition"] != disposition or expected["reasons"] != reasons:
            raise ValidationError(f"{case_id}: disposition/reason drift")
        reason_coverage.update(reasons)
        if not reasons:
            compatible_interfaces.add(interface)
        results.append({
            "case_id": case_id,
            "interface": interface,
            "disposition": disposition,
            "reasons": reasons,
        })

    if reason_coverage != set(REASON_ORDER):
        raise ValidationError("reason coverage is incomplete")
    if compatible_interfaces != KNOWN_INTERFACES:
        raise ValidationError("positive interface coverage is incomplete")

    return {
        "valid": True,
        "contract_id": document["contract_id"],
        "version": document["version"],
        "case_count": len(cases),
        "results": results,
        "authority_effect": "none",
    }


def validate_path(path: Path, expected_sha256: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValidationError(f"source SHA-256 mismatch: {digest}")
    result = validate_document(parse_bytes(raw))
    result["source_sha256"] = digest
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-sha256", default=EXPECTED_SHA256)
    args = parser.parse_args(argv)
    try:
        result = validate_path(args.path, args.expected_sha256)
    except (OSError, ValidationError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
