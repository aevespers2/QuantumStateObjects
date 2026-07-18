import copy

import pytest

from qso_runtime.mutation_audit import MutationAuditLedger

SHA0 = "0" * 64
SHA1 = "1" * 64


def test_reviewer_removal_requires_full_attribution_and_reason():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    with pytest.raises(ValueError, match="reason must be a non-empty string"):
        ledger.append_intent(
            operation="remove_pull_request_reviewers",
            target={"pull_request": 9, "reviewers": ["reviewer-a"]},
            requested_by_type="ai",
            requested_by_id="assistant-session",
            reason="",
            instruction_source={"type": "human_message", "message_sha256": SHA0},
            before_state_sha256=SHA0,
        )
    assert ledger.entries == []


def test_reviewer_removal_records_ai_and_human_instruction_source():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    intent = ledger.append_intent(
        operation="remove_pull_request_reviewers",
        target={"pull_request": 9, "reviewers": ["reviewer-a"], "teams": []},
        requested_by_type="ai",
        requested_by_id="assistant-session",
        reason="User explicitly revoked the review request",
        instruction_source={
            "type": "human_message",
            "authorized_by": "repository-owner",
            "message_sha256": SHA0,
        },
        before_state_sha256=SHA0,
        timestamp_utc="2026-07-18T00:00:00+00:00",
    )
    completion = ledger.append_completion(
        intent_entry_sha256=intent["entry_sha256"],
        result="succeeded",
        after_state_sha256=SHA1,
        provider_receipt={"provider": "github", "request_id": "receipt-1"},
        performed_by_type="ai",
        performed_by_id="assistant-session",
        timestamp_utc="2026-07-18T00:00:01+00:00",
    )
    assert completion["intent_entry_sha256"] == intent["entry_sha256"]
    assert ledger.verify() == []


def test_tampering_is_detected_and_original_copy_remains_verifiable():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    intent = ledger.append_intent(
        operation="remove_pull_request_reviewers",
        target={"pull_request": 9, "reviewers": ["reviewer-a"]},
        requested_by_type="human",
        requested_by_id="repository-owner",
        reason="Reviewer requested removal",
        instruction_source={"type": "signed_request", "request_sha256": SHA0},
        before_state_sha256=SHA0,
        timestamp_utc="2026-07-18T00:00:00+00:00",
    )
    pristine = copy.deepcopy(ledger)
    ledger.entries[0]["reason"] = "altered"
    assert "entry hash mismatch at 0" in ledger.verify()
    assert pristine.verify() == []
    assert intent["reason"] == "Reviewer requested removal"


def test_completion_without_intent_is_rejected():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    with pytest.raises(ValueError, match="intent_entry_sha256"):
        ledger.append_completion(
            intent_entry_sha256=SHA0,
            result="succeeded",
            after_state_sha256=SHA1,
            provider_receipt={"provider": "github", "request_id": "receipt-1"},
            performed_by_type="service",
            performed_by_id="github-app",
        )


def test_anchor_manifest_requires_independent_anchors():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    manifest = ledger.anchor_manifest()
    assert manifest["required_external_anchors"] == [
        "protected repository artifact",
        "independent append-only transparency log",
    ]
