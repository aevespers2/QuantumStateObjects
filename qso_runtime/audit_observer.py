from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable


@dataclass(frozen=True)
class AuditQuery:
    operations: tuple[str, ...] = ()
    actor_types: tuple[str, ...] = ()
    results: tuple[str, ...] = ()
    phases: tuple[str, ...] = ()
    target_contains: tuple[tuple[str, Any], ...] = ()
    since_utc: str | None = None
    until_utc: str | None = None
    limit: int = 100


@dataclass(frozen=True)
class NotificationRule:
    rule_id: str
    operations: tuple[str, ...] = ()
    results: tuple[str, ...] = ()
    actor_types: tuple[str, ...] = ()
    minimum_severity: str = "medium"
    recipients: tuple[str, ...] = ()
    require_human_review: bool = True


@dataclass(frozen=True)
class AuditNotification:
    rule_id: str
    entry_sha256: str
    severity: str
    recipients: tuple[str, ...]
    summary: str
    require_human_review: bool


@dataclass
class AuditObserver:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def ingest_verified(self, entries: Iterable[dict[str, Any]], verification_errors: list[str]) -> None:
        if verification_errors:
            raise ValueError("cannot ingest an unverified audit ledger")
        candidate = copy.deepcopy(list(entries))
        for index, entry in enumerate(candidate):
            if not isinstance(entry, dict):
                raise ValueError(f"entries[{index}] must be an object")
            if not isinstance(entry.get("entry_sha256"), str):
                raise ValueError(f"entries[{index}].entry_sha256 is required")
        self.entries = candidate

    def query(self, request: AuditQuery) -> list[dict[str, Any]]:
        if not isinstance(request.limit, int) or isinstance(request.limit, bool) or request.limit < 1 or request.limit > 1000:
            raise ValueError("limit must be an integer between 1 and 1000")
        since = _parse_time(request.since_utc)
        until = _parse_time(request.until_utc)
        results: list[dict[str, Any]] = []
        for entry in reversed(self.entries):
            actor = entry.get("requested_by") or entry.get("performed_by") or {}
            timestamp = _parse_time(entry.get("timestamp_utc"))
            if request.operations and entry.get("operation") not in request.operations:
                continue
            if request.actor_types and actor.get("type") not in request.actor_types:
                continue
            if request.results and entry.get("result") not in request.results:
                continue
            if request.phases and entry.get("phase") not in request.phases:
                continue
            if since is not None and (timestamp is None or timestamp < since):
                continue
            if until is not None and (timestamp is None or timestamp > until):
                continue
            target = entry.get("target") or {}
            if any(target.get(key) != value for key, value in request.target_contains):
                continue
            results.append(copy.deepcopy(entry))
            if len(results) >= request.limit:
                break
        return results

    def notifications(self, rules: Iterable[NotificationRule]) -> list[AuditNotification]:
        output: list[AuditNotification] = []
        for entry in self.entries:
            actor = entry.get("requested_by") or entry.get("performed_by") or {}
            for rule in rules:
                if rule.operations and entry.get("operation") not in rule.operations:
                    continue
                if rule.results and entry.get("result") not in rule.results:
                    continue
                if rule.actor_types and actor.get("type") not in rule.actor_types:
                    continue
                severity = classify_severity(entry)
                if _severity_rank(severity) < _severity_rank(rule.minimum_severity):
                    continue
                output.append(
                    AuditNotification(
                        rule_id=rule.rule_id,
                        entry_sha256=entry["entry_sha256"],
                        severity=severity,
                        recipients=rule.recipients,
                        summary=_summary(entry),
                        require_human_review=rule.require_human_review,
                    )
                )
        return output

    def review_queue(self) -> list[dict[str, Any]]:
        pending: list[dict[str, Any]] = []
        completed_intents = {
            entry.get("intent_entry_sha256")
            for entry in self.entries
            if entry.get("phase") == "completion"
        }
        for entry in self.entries:
            severity = classify_severity(entry)
            needs_review = (
                entry.get("phase") == "intent" and entry.get("entry_sha256") not in completed_intents
            ) or entry.get("result") in {"failed", "denied"} or severity in {"high", "critical"}
            if needs_review:
                item = copy.deepcopy(entry)
                item["observer_severity"] = severity
                pending.append(item)
        return pending

    def decision_survey(self) -> dict[str, Any]:
        operations: dict[str, int] = {}
        outcomes: dict[str, int] = {}
        actors: dict[str, int] = {}
        for entry in self.entries:
            operations[entry.get("operation", "unknown")] = operations.get(entry.get("operation", "unknown"), 0) + 1
            outcomes[entry.get("result", "unknown")] = outcomes.get(entry.get("result", "unknown"), 0) + 1
            actor = entry.get("requested_by") or entry.get("performed_by") or {}
            actor_type = actor.get("type", "unknown")
            actors[actor_type] = actors.get(actor_type, 0) + 1
        return {
            "entry_count": len(self.entries),
            "operations": dict(sorted(operations.items())),
            "outcomes": dict(sorted(outcomes.items())),
            "actor_types": dict(sorted(actors.items())),
            "open_review_count": len(self.review_queue()),
        }


def classify_severity(entry: dict[str, Any]) -> str:
    operation = entry.get("operation")
    result = entry.get("result")
    if operation in {"delete_file", "update_ref", "merge_pull_request", "remove_pull_request_reviewers"}:
        return "critical" if result == "succeeded" else "high"
    if result in {"failed", "denied"}:
        return "high"
    if entry.get("phase") == "intent":
        return "medium"
    return "low"


def _summary(entry: dict[str, Any]) -> str:
    actor = entry.get("requested_by") or entry.get("performed_by") or {}
    return (
        f"{entry.get('operation')} {entry.get('phase')} {entry.get('result')} "
        f"by {actor.get('type')}:{actor.get('id')}"
    )


def _severity_rank(value: str) -> int:
    ranks = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    if value not in ranks:
        raise ValueError("unknown severity")
    return ranks[value]


def _parse_time(value: Any) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be ISO-8601") from exc
