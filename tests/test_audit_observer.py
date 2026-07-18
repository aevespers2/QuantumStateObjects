from qso_runtime.audit_observer import (
    AuditObserver,
    AuditQuery,
    NotificationRule,
)
from qso_runtime.mutation_audit import MutationAuditLedger

SHA0 = "0" * 64
SHA1 = "1" * 64


def _ledger():
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


def test_observer_only_ingests_verified_ledgers():
    observer = AuditObserver()
    ledger = _ledger()
    observer.ingest_verified(ledger.entries, ledger.verify())
    assert len(observer.entries) == 2


def test_query_filters_by_operation_actor_and_target():
    observer = AuditObserver()
    ledger = _ledger()
    observer.ingest_verified(ledger.entries, ledger.verify())
    results = observer.query(
        AuditQuery(
            operations=("remove_pull_request_reviewers",),
            actor_types=("ai",),
            target_contains=(("pull_request", 9),),
        )
    )
    assert len(results) == 2


def test_notification_rule_surfaces_critical_reviewer_removal():
    observer = AuditObserver()
    ledger = _ledger()
    observer.ingest_verified(ledger.entries, ledger.verify())
    notifications = observer.notifications(
        [
            NotificationRule(
                rule_id="security-reviewer-removal",
                operations=("remove_pull_request_reviewers",),
                minimum_severity="high",
                recipients=("security-specialists", "cybersecurity-researchers", "mcp-auditors"),
            )
        ]
    )
    assert notifications
    assert all(note.require_human_review for note in notifications)
    assert any(note.severity == "critical" for note in notifications)


def test_review_queue_includes_high_impact_decisions():
    observer = AuditObserver()
    ledger = _ledger()
    observer.ingest_verified(ledger.entries, ledger.verify())
    queue = observer.review_queue()
    assert len(queue) == 2
    assert {entry["observer_severity"] for entry in queue} == {"high", "critical"}


def test_decision_survey_supports_retrospective_review():
    observer = AuditObserver()
    ledger = _ledger()
    observer.ingest_verified(ledger.entries, ledger.verify())
    survey = observer.decision_survey()
    assert survey["entry_count"] == 2
    assert survey["operations"]["remove_pull_request_reviewers"] == 2
    assert survey["actor_types"]["ai"] == 2
