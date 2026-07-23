from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_interface_compatibility_consumer import (
    FACT_ORDER,
    REASON_ORDER,
    ValidationError,
    parse_bytes,
    validate_document,
)

INTERFACES = ["qso-event-ledger", "qso-runtime-report"]


def good_facts():
    return {name: True for name in FACT_ORDER}


def make_corpus():
    cases = []
    for interface in INTERFACES:
        cases.append({
            "case_id": interface + "-compatible",
            "interface": interface,
            "facts": good_facts(),
            "expected": {
                "disposition": "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL",
                "reasons": [],
            },
        })

    for index, (fact, reason) in enumerate(zip(FACT_ORDER, REASON_ORDER, strict=True)):
        facts = good_facts()
        facts[fact] = False
        interface = "qso-unknown-interface" if fact == "known_interface" else INTERFACES[index % 2]
        cases.append({
            "case_id": "blocked-" + fact.replace("_", "-"),
            "interface": interface,
            "facts": facts,
            "expected": {"disposition": "BLOCKED", "reasons": [reason]},
        })

    facts = good_facts()
    for fact in [
        "source_tuple_current",
        "protocol_match",
        "schema_version_match",
        "evidence_bound",
        "authority_promotion_absent",
    ]:
        facts[fact] = False
    cases.append({
        "case_id": "multi-obstruction-order",
        "interface": "qso-runtime-report",
        "facts": facts,
        "expected": {
            "disposition": "BLOCKED",
            "reasons": [
                "STALE_SOURCE_TUPLE",
                "PROTOCOL_MISMATCH",
                "SCHEMA_VERSION_MISMATCH",
                "EVIDENCE_NOT_BOUND",
                "AUTHORITY_PROMOTION_DETECTED",
            ],
        },
    })

    return {
        "contract_id": "QSO-INTERFACE-COMPATIBILITY-001",
        "version": "1.0.0",
        "fact_order": FACT_ORDER,
        "reason_order": REASON_ORDER,
        "cases": cases,
    }


class ConsumerTests(unittest.TestCase):
    def test_semantic_profile_validates(self):
        self.assertTrue(validate_document(make_corpus())["valid"])

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValidationError):
            parse_bytes(b'{"a":1,"a":2}')

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValidationError):
            parse_bytes(b'{"a":NaN}')

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(ValidationError):
            parse_bytes(b'\xff')

    def test_unknown_top_field_rejected(self):
        corpus = make_corpus()
        corpus["extra"] = True
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_nonboolean_fact_rejected(self):
        corpus = make_corpus()
        corpus["cases"][0]["facts"][FACT_ORDER[0]] = 1
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_fact_order_drift_rejected(self):
        corpus = make_corpus()
        corpus["fact_order"] = list(reversed(FACT_ORDER))
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_reason_order_drift_rejected(self):
        corpus = make_corpus()
        corpus["reason_order"] = list(reversed(REASON_ORDER))
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_duplicate_case_rejected(self):
        corpus = make_corpus()
        corpus["cases"][1]["case_id"] = corpus["cases"][0]["case_id"]
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_known_interface_consistency_rejected(self):
        corpus = make_corpus()
        corpus["cases"][0]["facts"]["known_interface"] = False
        corpus["cases"][0]["expected"] = {
            "disposition": "BLOCKED",
            "reasons": ["UNKNOWN_INTERFACE"],
        }
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_disposition_drift_rejected(self):
        corpus = make_corpus()
        corpus["cases"][0]["expected"]["disposition"] = "BLOCKED"
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_reason_order_within_case_rejected(self):
        corpus = make_corpus()
        corpus["cases"][-1]["expected"]["reasons"].reverse()
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_missing_reason_coverage_rejected(self):
        corpus = make_corpus()
        corpus["cases"].pop(-2)
        with self.assertRaises(ValidationError):
            validate_document(corpus)

    def test_wrong_source_hash_rejected_before_semantics(self):
        from tools.validate_interface_compatibility_consumer import validate_path

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(make_corpus()), encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate_path(path, "0" * 64)


if __name__ == "__main__":
    unittest.main()
