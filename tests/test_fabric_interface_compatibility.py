from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "validate_fabric_interface_compatibility.py"
CORPUS_PATH = ROOT / "fixtures" / "qso-interface-compatibility-v1.json"
TUPLE_PATH = ROOT / "contracts" / "qso-interface-source-tuple-v1.json"
SPEC = importlib.util.spec_from_file_location("fabric_interface_consumer", MODULE_PATH)
assert SPEC and SPEC.loader
consumer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(consumer)


def corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def source_tuple() -> dict:
    return json.loads(TUPLE_PATH.read_text(encoding="utf-8"))


class FabricInterfaceCompatibilityTests(unittest.TestCase):
    def test_exact_source_tuple_and_corpus_validate(self) -> None:
        tuple_result = consumer.validate_source_tuple(source_tuple(), ROOT)
        results = consumer.validate_corpus(corpus())
        self.assertEqual(tuple_result["fixture_git_blob"], consumer.PRODUCER_FIXTURE_BLOB)
        self.assertEqual(len(results), 17)
        self.assertEqual(
            {item["interface"] for item in results if not item["reasons"]},
            set(consumer.DECLARED_INTERFACES),
        )

    def test_local_fixture_is_byte_identical_to_producer_blob(self) -> None:
        result = subprocess.run(
            ["git", "hash-object", str(CORPUS_PATH)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.stdout.strip(), consumer.PRODUCER_FIXTURE_BLOB)

    def test_duplicate_json_key_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            consumer.parse_json(b'{"a":1,"a":2}', "fixture")

    def test_nonfinite_constant_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-finite"):
            consumer.parse_json(b'{"value":NaN}', "fixture")

    def test_overflowed_number_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-finite"):
            consumer.parse_json(b'{"value":1e999}', "fixture")

    def test_invalid_utf8_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "strict UTF-8"):
            consumer.parse_json(b'{"value":"\xff"}', "fixture")

    def test_unknown_corpus_field_rejected(self) -> None:
        data = corpus()
        data["approval"] = True
        with self.assertRaisesRegex(ValueError, "fields differ"):
            consumer.validate_corpus(data)

    def test_missing_fact_rejected(self) -> None:
        data = corpus()
        del data["cases"][0]["facts"]["correction_supported"]
        with self.assertRaisesRegex(ValueError, "fields differ"):
            consumer.validate_corpus(data)

    def test_boolean_as_integer_rejected(self) -> None:
        data = corpus()
        data["cases"][0]["facts"]["retry_policy_match"] = 1
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            consumer.validate_corpus(data)

    def test_duplicate_case_rejected(self) -> None:
        data = corpus()
        data["cases"].append(deepcopy(data["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            consumer.validate_corpus(data)

    def test_known_interface_contradiction_rejected(self) -> None:
        data = corpus()
        data["cases"][0]["facts"]["known_interface"] = False
        data["cases"][0]["expected"] = {
            "disposition": "BLOCKED",
            "reasons": ["UNKNOWN_INTERFACE"],
        }
        with self.assertRaisesRegex(ValueError, "contradicts"):
            consumer.validate_corpus(data)

    def test_fact_order_drift_rejected(self) -> None:
        data = corpus()
        data["fact_order"] = list(reversed(data["fact_order"]))
        with self.assertRaisesRegex(ValueError, "fact order mismatch"):
            consumer.validate_corpus(data)

    def test_reason_order_drift_rejected(self) -> None:
        data = corpus()
        data["reason_order"] = list(reversed(data["reason_order"]))
        with self.assertRaisesRegex(ValueError, "reason order mismatch"):
            consumer.validate_corpus(data)

    def test_disposition_drift_rejected(self) -> None:
        data = corpus()
        data["cases"][2]["expected"]["disposition"] = "COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL"
        with self.assertRaisesRegex(ValueError, "disposition mismatch"):
            consumer.validate_corpus(data)

    def test_reason_drift_rejected(self) -> None:
        data = corpus()
        data["cases"][2]["expected"]["reasons"] = ["PROTOCOL_MISMATCH"]
        with self.assertRaisesRegex(ValueError, "reason mismatch"):
            consumer.validate_corpus(data)

    def test_reason_order_within_case_rejected(self) -> None:
        data = corpus()
        data["cases"][-1]["expected"]["reasons"] = list(
            reversed(data["cases"][-1]["expected"]["reasons"])
        )
        with self.assertRaisesRegex(ValueError, "out of order"):
            consumer.validate_corpus(data)

    def test_source_tuple_head_drift_rejected(self) -> None:
        data = source_tuple()
        data["producer"]["head_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "head_sha mismatch"):
            consumer.validate_source_tuple(data, ROOT)

    def test_source_tuple_authority_promotion_rejected(self) -> None:
        data = source_tuple()
        data["authority_effect"] = "runtime-admission"
        with self.assertRaisesRegex(ValueError, "may not create authority"):
            consumer.validate_source_tuple(data, ROOT)

    def test_consumer_path_drift_rejected(self) -> None:
        data = source_tuple()
        data["consumer"]["fixture_path"] = "fixtures/other.json"
        with self.assertRaisesRegex(ValueError, "consumer path"):
            consumer.validate_source_tuple(data, ROOT)

    def test_changed_fixture_bytes_rejected_before_semantic_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            fixture = temporary_root / "fixtures" / "qso-interface-compatibility-v1.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_bytes(CORPUS_PATH.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "fixture blob mismatch"):
                consumer.validate_source_tuple(source_tuple(), temporary_root)

    def test_cli_failure_is_structured_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.json"
            bad.write_text('{"version":NaN}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(bad), str(TUPLE_PATH), "--repository-root", str(ROOT)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIs(payload["valid"], False)
        self.assertIn("non-finite", payload["error"])


if __name__ == "__main__":
    unittest.main()
