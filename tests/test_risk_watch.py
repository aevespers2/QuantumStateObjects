from qso_runtime.mutation_audit import MutationAuditLedger
from qso_runtime.risk_watch import RiskPolicy, RiskWatch, public_disclosure

SHA0 = "0" * 64
SHA1 = "1" * 64


def _critical_ledger():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    intent = ledger.append_intent(
        operation="remove_pull_request_reviewers",
        target={"pull_request": 9, "reviewers": ["reviewer-a"]},
        requested_by_type="ai",
        requested_by_id="assistant-session",
        reason="Explicit repository-owner instruction",
        instruction_source={"type": "human_message", "message_sha256": SHA0},
        before_state_sha256=SHA0,
        timestamp_utc="2026-07-18T00:00:00+00:00",
    )
    ledger.append_completion(
        intent_entry_sha256=intent["entry_sha256"],
        result="succeeded",
        after_state_sha256=SHA1,
        provider_receipt={"provider": "github", "request_id": "receipt-1"},
        performed_by_type="ai",
        performed_by_id="assistant-session",
        timestamp_utc="2026-07-18T00:00:01+00:00",
    )
    return ledger


def test_critical_mutations_trigger_review_and_public_summary():
    ledger = _critical_ledger()
    assessment = RiskWatch().assess(ledger.entries)
    assert assessment.require_human_review is True
    assert assessment.public_summary["critical_mutation_count"] == 1


def test_orphaned_intents_raise_risk():
    ledger = MutationAuditLedger("aevespers2/QuantumStateObjects")
    ledger.append_intent(
        operation="update_ref",
        target={"branch": "main"},
        requested_by_type="service",
        requested_by_id="automation",
        reason="release operation",
        instruction_source={"type": "policy", "policy_sha256": SHA0},
        before_state_sha256=SHA0,
        timestamp_utc="2026-07-18T00:00:00+00:00",
    )
    assessment = RiskWatch().assess(ledger.entries)
    assert assessment.public_summary["orphaned_intent_count"] == 1
    assert assessment.require_human_review is True


def test_high_risk_produces_nonautomatic_rollback_proposal():
    ledger = _critical_ledger()
    policy = RiskPolicy(rollback_score_threshold=1, freeze_score_threshold=20)
    watch = RiskWatch(policy)
    assessment = watch.assess(ledger.entries)
    plan = watch.rollback_plan(assessment, SHA0)
    assert plan["action"] == "propose_rollback"
    assert plan["execute_automatically"] is False
    assert plan["requires_authorization"] is True


def test_missing_checkpoint_freezes_instead_of_guessing():
    ledger = _critical_ledger()
    policy = RiskPolicy(rollback_score_threshold=1)
    watch = RiskWatch(policy)
    plan = watch.rollback_plan(watch.assess(ledger.entries), None)
    assert plan["action"] == "freeze_and_investigate"


def test_public_disclosure_redacts_actor_identity_and_target_values():
    ledger = _critical_ledger()
    public = public_disclosure(ledger.entries)
    assert public[0]["actor_type"] == "ai"
    assert "requested_by" not in public[0]
    assert "reviewers" not in public[0]
    assert public[0]["target_type"] == "pull_request"
