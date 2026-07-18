from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EPIGRAPH = (
    "What hands have shaped, let faithful records show; "
    "That every seed may share the fruit it grows."
)


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def require_sha256(value: str, field_name: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{field_name} must be a lowercase SHA-256 hex string")


def _validated_artifacts(artifacts: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if artifacts is None:
        return []
    if not isinstance(artifacts, list):
        raise ValueError("artifacts must be a list")
    artifact_entries = copy.deepcopy(artifacts)
    for index, artifact in enumerate(artifact_entries):
        if not isinstance(artifact, dict):
            raise ValueError(f"artifacts[{index}] must be an object")
        require_sha256(artifact.get("sha256"), f"artifacts[{index}].sha256")
    return artifact_entries


@dataclass(frozen=True)
class ContributorCredit:
    contributor_id: str
    credit_name: str
    credit_mode: str
    contribution_classes: tuple[str, ...]
    description: str
    consent: str = "confirmed"
    influence_estimate: float | None = None
    influence_estimate_note: str | None = None

    def as_dict(self) -> dict[str, Any]:
        if self.credit_mode not in {
            "public_named", "public_pseudonymous", "private_escrowed", "anonymous_with_attestation"
        }:
            raise ValueError("unsupported credit mode")
        if not self.contribution_classes:
            raise ValueError("at least one contribution class is required")
        if self.influence_estimate is not None and not 0 <= self.influence_estimate <= 1:
            raise ValueError("influence estimate must be between zero and one")
        return {
            "contributor_id": self.contributor_id,
            "credit_name": self.credit_name,
            "credit_mode": self.credit_mode,
            "contribution_classes": list(self.contribution_classes),
            "description": self.description,
            "consent": self.consent,
            "influence_estimate": self.influence_estimate,
            "influence_estimate_note": self.influence_estimate_note,
        }


@dataclass
class AttributionJourneyLedger:
    qso_instance: str
    entries: list[dict[str, Any]] = field(default_factory=list)

    def append(self, *, event_type: str, contributors: list[ContributorCredit], state_before_sha256: str,
               state_after_sha256: str, artifacts: list[dict[str, Any]] | None = None,
               attribution_required: bool = True, ownership_claimed: bool = False,
               license_reference: str | None = None, benefit_sharing_reference: str | None = None,
               sprite_reviewed: bool = False, human_review_required: bool = True,
               dispute_status: str = "none", timestamp_utc: str | None = None) -> dict[str, Any]:
        require_sha256(state_before_sha256, "state_before_sha256")
        require_sha256(state_after_sha256, "state_after_sha256")
        artifact_entries = _validated_artifacts(artifacts)
        previous_hash = self.entries[-1]["entry_sha256"] if self.entries else None
        sequence = len(self.entries)
        timestamp = timestamp_utc or datetime.now(timezone.utc).isoformat()
        body = {
            "schema_version": 1, "qso_instance": self.qso_instance, "sequence": sequence,
            "timestamp_utc": timestamp, "event_type": event_type,
            "contributors": [credit.as_dict() for credit in contributors],
            "state_before_sha256": state_before_sha256, "state_after_sha256": state_after_sha256,
            "previous_entry_sha256": previous_hash, "artifacts": artifact_entries,
            "terms": {"attribution_required": attribution_required, "ownership_claimed": ownership_claimed,
                      "benefit_sharing_defined": benefit_sharing_reference is not None,
                      "license_reference": license_reference, "benefit_sharing_reference": benefit_sharing_reference},
            "review": {"sprite_reviewed": sprite_reviewed, "human_review_required": human_review_required,
                       "dispute_status": dispute_status},
        }
        entry_hash = canonical_sha256(body)
        body["entry_id"] = f"attr-{entry_hash[:24]}"
        body["entry_sha256"] = canonical_sha256({k: v for k, v in body.items() if k != "entry_sha256"})
        self.entries.append(body)
        return copy.deepcopy(body)

    def verify(self) -> list[str]:
        errors: list[str] = []
        previous_hash: str | None = None
        for expected_sequence, entry in enumerate(self.entries):
            if entry.get("sequence") != expected_sequence:
                errors.append(f"sequence mismatch at {expected_sequence}")
            if entry.get("previous_entry_sha256") != previous_hash:
                errors.append(f"chain mismatch at {expected_sequence}")
            expected_hash = canonical_sha256({k: v for k, v in entry.items() if k != "entry_sha256"})
            if entry.get("entry_sha256") != expected_hash:
                errors.append(f"entry hash mismatch at {expected_sequence}")
            previous_hash = entry.get("entry_sha256")
        return errors

    def certificate(self) -> dict[str, Any]:
        return {"certificate_type": "QSO_ATTRIBUTION_STATE_CERTIFICATE", "qso_instance": self.qso_instance,
                "entry_count": len(self.entries),
                "latest_entry_sha256": self.entries[-1]["entry_sha256"] if self.entries else None,
                "journey_sha256": canonical_sha256(self.entries), "epigraph": EPIGRAPH,
                "verification_errors": self.verify()}

    def write(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "attribution-journey.jsonl").write_text(
            "".join(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n" for entry in self.entries), encoding="utf-8")
        (directory / "attribution-certificate.json").write_text(
            json.dumps(self.certificate(), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def artifact_reference(artifact_id: str, kind: str, sha256: str, relationship: str,
                       uri: str | None = None) -> dict[str, Any]:
    if relationship not in {"input", "created", "derived", "referenced", "licensed"}:
        raise ValueError("unsupported artifact relationship")
    require_sha256(sha256, "artifact hash")
    return {"artifact_id": artifact_id, "kind": kind, "sha256": sha256,
            "relationship": relationship, "uri": uri}
