from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_ecosystem_interface_compatibility.py"
SPEC = importlib.util.spec_from_file_location("interface_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

PROFILE_PATH = Path(__file__).resolve().parents[1] / "docs" / "ecosystem-interface-compatibility-v0.json"


class InterfaceCompatibilityProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = validator.strict_load(PROFILE_PATH)

    def validate(self, profile: dict) -> list[str]:
        return validator.validate_profile(profile)

    def test_current_profile_passes(self) -> None:
        self.assertEqual(self.validate(copy.deepcopy(self.profile)), [])

    def test_source_digest_drift_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["producer_source"]["sha256"] = "0" * 64
        self.assertTrue(any("sha256" in error for error in self.validate(profile)))

    def test_boolean_does_not_satisfy_retry_limit(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["interfaces"][0]["retry_limit"] = False
        self.assertTrue(any("retry_limit" in error for error in self.validate(profile)))

    def test_missing_interface_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["interfaces"].pop()
        self.assertTrue(any("exactly two" in error for error in self.validate(profile)))

    def test_duplicate_interface_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["interfaces"][1] = copy.deepcopy(profile["interfaces"][0])
        errors = self.validate(profile)
        self.assertTrue(any("duplicate interface" in error for error in errors))

    def test_authority_promotion_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["authority_effect"] = "ecosystem-admission"
        self.assertTrue(any("authority_effect" in error for error in self.validate(profile)))

    def test_status_promotion_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["status"] = "ACCEPTED"
        self.assertTrue(any("BLOCKED_ROLE_COLLISION" in error for error in self.validate(profile)))

    def test_unknown_field_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["unexpected"] = True
        self.assertTrue(any("unknown fields" in error for error in self.validate(profile)))

    def test_skill_mapping_drift_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["skill_tree_mapping"][0]["subdivision_ids"].remove("012-D")
        self.assertTrue(any("CAT-012" in error for error in self.validate(profile)))

    def test_denied_inference_removal_fails(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["denied_inferences"].pop()
        errors = self.validate(profile)
        self.assertTrue(any("denied_inferences" in error for error in errors))

    def test_duplicate_json_key_is_rejected(self) -> None:
        text = PROFILE_PATH.read_text(encoding="utf-8")
        hostile = text.replace(
            '"profile_id": "QSO-INTERFACE-COMPATIBILITY-001",',
            '"profile_id": "QSO-INTERFACE-COMPATIBILITY-001",\n  "profile_id": "duplicate",',
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(hostile, encoding="utf-8")
            with self.assertRaises(validator.StrictJSONError):
                validator.strict_load(path)

    def test_nonfinite_json_number_is_rejected(self) -> None:
        text = PROFILE_PATH.read_text(encoding="utf-8")
        hostile = text.replace('"size_bytes": 1564', '"size_bytes": NaN', 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(hostile, encoding="utf-8")
            with self.assertRaises(validator.StrictJSONError):
                validator.strict_load(path)

    def test_invalid_utf8_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_bytes(b'{"profile_id":"x"}\xff')
            with self.assertRaises(validator.StrictJSONError):
                validator.strict_load(path)

    def test_report_is_deterministic_for_same_source(self) -> None:
        profile = copy.deepcopy(self.profile)
        first = validator.build_report(PROFILE_PATH, profile, [])
        second = validator.build_report(PROFILE_PATH, profile, [])
        self.assertEqual(first, second)
        self.assertEqual(first["validation_status"], "passed")
        self.assertEqual(first["disposition"], "BLOCKED_ROLE_COLLISION")
        self.assertEqual(first["authority_effect"], "none")


if __name__ == "__main__":
    unittest.main()
