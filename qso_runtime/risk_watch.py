from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True)
class RiskPolicy:
    critical_operations: tuple[str, ...] = (
        "delete_file",
        "update_ref",
        "merge_pull_request",
        "remove_pull_request_reviewers",
    )
    high_risk_results: tuple[str, ...] = ("failed", "denied")
    repeated_operation_threshold: int = 3
    review_window_entries: int = 20
    rollback_score_threshold: int = 7
    freeze_score_threshold: int = 10


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    reasons: tuple[str, ...]
    recommend_rollback: bool
    recommend_freeze: bool
    require_human_review: bool
    public_summary: dict[str, Any]


@dataclass
class RiskWatch:
    policy: RiskPolicy = field(default_factory=RiskPolicy)

    def assess(self, entries: Iterable[dict[str, Any]]) -> RiskAssessment:
        records = copy.deepcopy(list(entries))
        score = 0
        reasons: list[str] = []
        recent = records[-self.policy.review_window_entries :]

        critical_successes = [
            entry
            for entry in recent
            if entry.get("operation") in self.policy.critical_operations
            and entry.get("result") == "succeeded"
        ]
        if critical_successes:
            score += min(6, len(critical_successes) * 2)
            reasons.append(f"{len(critical_successes)} successful critical mutation(s) in review window")

        failed_or_denied = [
            entry for entry in recent if entry.get("result") in self.policy.high_risk_results
        ]
        if failed_or_denied:
            score += min(4, len(failed_or_denied))
            reasons.append(f"{len(failed_or_denied)} failed or denied mutation(s)")

        pending_intents = {
            entry.get("entry_sha256")
            for entry in recent
            if entry.get("phase") == "intent"
        }
        completed_intents = {
            entry.get("intent_entry_sha256")
            for entry in recent
            if entry.get("phase") == "completion"
        }
        orphaned = pending_intents.difference(completed_intents)
        if orphaned:
            score += min(5, len(orphaned) * 2)
            reasons.append(f"{len(orphaned)} privileged intent(s) without completion")

        operation_counts: dict[str, int] = {}
        for entry in recent:
            operation = entry.get("operation")
            if isinstance(operation, str):
                operation_counts[operation] = operation_counts.get(operation, 0) + 1
        repeated = {
            operation: count
            for operation, count in operation_counts.items()
            if count >= self.policy.repeated_operation_threshold
        }
        if repeated:
            score += min(4, sum(repeated.values()) // self.policy.repeated_operation_threshold)
            reasons.append(f"repeated privileged operations detected: {dict(sorted(repeated.items()))}")

        tamper_indicators = [
            entry for entry in recent if entry.get("verification_errors")
        ]
        if tamper_indicators:
            score += 10
            reasons.append("tamper or verification errors present")

        level = _level(score)
        rollback = score >= self.policy.rollback_score_threshold
        freeze = score >= self.policy.freeze_score_threshold
        return RiskAssessment(
            score=score,
            level=level,
            reasons=tuple(reasons),
            recommend_rollback=rollback,
            recommend_freeze=freeze,
            require_human_review=score > 0,
            public_summary={
                "risk_level": level,
                "risk_score": score,
                "critical_mutation_count": len(critical_successes),
                "failed_or_denied_count": len(failed_or_denied),
                "orphaned_intent_count": len(orphaned),
                "repeated_operations": dict(sorted(repeated.items())),
                "rollback_recommended": rollback,
                "freeze_recommended": freeze,
            },
        )

    def rollback_plan(self, assessment: RiskAssessment, checkpoint_sha256: str | None) -> dict[str, Any]:
        if not assessment.recommend_rollback:
            return {
                "action": "continue_with_observation",
                "requires_authorization": False,
                "reason": "risk score below rollback threshold",
            }
        if not isinstance(checkpoint_sha256, str) or len(checkpoint_sha256) != 64:
            return {
                "action": "freeze_and_investigate",
                "requires_authorization": True,
                "reason": "rollback recommended but no valid checkpoint is available",
            }
        return {
            "action": "propose_rollback",
            "checkpoint_sha256": checkpoint_sha256,
            "requires_authorization": True,
            "reason": "; ".join(assessment.reasons),
            "execute_automatically": False,
        }


def public_disclosure(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    disclosed: list[dict[str, Any]] = []
    for entry in entries:
        actor = entry.get("requested_by") or entry.get("performed_by") or {}
        target = entry.get("target") or {}
        disclosed.append(
            {
                "entry_sha256": entry.get("entry_sha256"),
                "timestamp_utc": entry.get("timestamp_utc"),
                "phase": entry.get("phase"),
                "operation": entry.get("operation"),
                "result": entry.get("result"),
                "actor_type": actor.get("type"),
                "repository": entry.get("repository"),
                "target_type": _target_type(target),
            }
        )
    return disclosed


def _target_type(target: dict[str, Any]) -> str:
    for key in ("pull_request", "issue", "path", "branch", "comment"):
        if key in target:
            return key
    return "other"


def _level(score: int) -> str:
    if score >= 10:
        return "critical"
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    if score > 0:
        return "low"
    return "none"
