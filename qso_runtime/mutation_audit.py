from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


PRIVILEGED_MUTATIONS = {
    "remove_pull_request_reviewers",
    "update_pull_request",
    "update_issue",
    "update_issue_comment",
    "update_review_comment",
    "resolve_review_thread",
    "unresolve_review_thread",
    "remove_issue_assignees",
    "remove_issue_label",
    "delete_file",
    "update_file",
    "update_ref",
    "merge_pull_request",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8", errors="strict")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _require_nonempty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


@dataclass
class MutationAuditLedger:
    repository: str
    entries: list[dict[str, Any]] = field(default_factory=list)

    def append_intent(
        self,
        *,
        operation: str,
        target: dict[str, Any],
        requested_by_type: str,
        requested_by_id: str,
        reason: str,
        instruction_source: dict[str, Any],
        before_state_sha256: str,
        timestamp_utc: str | None = None,
    ) -> dict[str, Any]:
        if operation not in PRIVILEGED_MUTATIONS:
            raise ValueError("operation is not registered as a privileged mutation")
        if requested_by_type not in {"human", "ai", "service"}:
            raise ValueError("requested_by_type must be human, ai, or service")
        _require_nonempty_string(requested_by_id, "requested_by_id")
        _require_nonempty_string(reason, "reason")
        if not isinstance(target, dict) or not target:
            raise ValueError("target must be a non-empty object")
        if not isinstance(instruction_source, dict) or not instruction_source:
            raise ValueError("instruction_source must be a non-empty object")
        if not isinstance(before_state_sha256, str) or len(before_state_sha256) != 64:
            raise ValueError("before_state_sha256 must be a SHA-256 hex string")

        previous_hash = self.entries[-1]["entry_sha256"] if self.entries else None
        body = {
            "schema_version": 1,
            "repository": self.repository,
            "sequence": len(self.entries),
            "phase": "intent",
            "operation": operation,
            "target": copy.deepcopy(target),
            "requested_by": {
                "type": requested_by_type,
                "id": requested_by_id,
            },
            "reason": reason,
            "instruction_source": copy.deepcopy(instruction_source),
            "before_state_sha256": before_state_sha256,
            "after_state_sha256": None,
            "result": "pending",
            "timestamp_utc": timestamp_utc or datetime.now(timezone.utc).isoformat(),
            "previous_entry_sha256": previous_hash,
        }
        body["entry_sha256"] = canonical_sha256(body)
        self.entries.append(body)
        return copy.deepcopy(body)

    def append_completion(
        self,
        *,
        intent_entry_sha256: str,
        result: str,
        after_state_sha256: str,
        provider_receipt: dict[str, Any],
        performed_by_type: str,
        performed_by_id: str,
        timestamp_utc: str | None = None,
    ) -> dict[str, Any]:
        if result not in {"succeeded", "failed", "denied"}:
            raise ValueError("result must be succeeded, failed, or denied")
        if performed_by_type not in {"human", "ai", "service"}:
            raise ValueError("performed_by_type must be human, ai, or service")
        _require_nonempty_string(performed_by_id, "performed_by_id")
        if not isinstance(provider_receipt, dict) or not provider_receipt:
            raise ValueError("provider_receipt must be a non-empty object")
        matching = [entry for entry in self.entries if entry["entry_sha256"] == intent_entry_sha256]
        if len(matching) != 1 or matching[0]["phase"] != "intent":
            raise ValueError("intent_entry_sha256 must identify exactly one intent entry")
        if not isinstance(after_state_sha256, str) or len(after_state_sha256) != 64:
            raise ValueError("after_state_sha256 must be a SHA-256 hex string")

        previous_hash = self.entries[-1]["entry_sha256"]
        body = {
            "schema_version": 1,
            "repository": self.repository,
            "sequence": len(self.entries),
            "phase": "completion",
            "operation": matching[0]["operation"],
            "target": copy.deepcopy(matching[0]["target"]),
            "intent_entry_sha256": intent_entry_sha256,
            "performed_by": {
                "type": performed_by_type,
                "id": performed_by_id,
            },
            "before_state_sha256": matching[0]["before_state_sha256"],
            "after_state_sha256": after_state_sha256,
            "result": result,
            "provider_receipt": copy.deepcopy(provider_receipt),
            "timestamp_utc": timestamp_utc or datetime.now(timezone.utc).isoformat(),
            "previous_entry_sha256": previous_hash,
        }
        body["entry_sha256"] = canonical_sha256(body)
        self.entries.append(body)
        return copy.deepcopy(body)

    def verify(self) -> list[str]:
        errors: list[str] = []
        previous_hash: str | None = None
        seen_intents: set[str] = set()
        completed_intents: set[str] = set()
        for expected_sequence, entry in enumerate(self.entries):
            if entry.get("sequence") != expected_sequence:
                errors.append(f"sequence mismatch at {expected_sequence}")
            if entry.get("previous_entry_sha256") != previous_hash:
                errors.append(f"chain mismatch at {expected_sequence}")
            expected_hash = canonical_sha256({k: v for k, v in entry.items() if k != "entry_sha256"})
            if entry.get("entry_sha256") != expected_hash:
                errors.append(f"entry hash mismatch at {expected_sequence}")
            if entry.get("phase") == "intent":
                seen_intents.add(entry.get("entry_sha256"))
            elif entry.get("phase") == "completion":
                intent_hash = entry.get("intent_entry_sha256")
                if intent_hash not in seen_intents:
                    errors.append(f"completion without prior intent at {expected_sequence}")
                if intent_hash in completed_intents:
                    errors.append(f"duplicate completion at {expected_sequence}")
                completed_intents.add(intent_hash)
            previous_hash = entry.get("entry_sha256")
        return errors

    def anchor_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "repository": self.repository,
            "entry_count": len(self.entries),
            "latest_entry_sha256": self.entries[-1]["entry_sha256"] if self.entries else None,
            "ledger_sha256": canonical_sha256(self.entries),
            "verification_errors": self.verify(),
            "required_external_anchors": [
                "protected repository artifact",
                "independent append-only transparency log",
            ],
        }
