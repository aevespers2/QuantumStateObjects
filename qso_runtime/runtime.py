from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Iterable

from qso_runtime.core import GenomeInterpreter, MCPMessage, QSO, digest


class RuntimeInvariantError(RuntimeError):
    """Raised when a bounded runtime invariant would be violated."""


def _message_dict(message: MCPMessage) -> dict[str, Any]:
    return {
        "sender": message.sender,
        "recipient": message.recipient,
        "kind": message.kind,
        "payload": copy.deepcopy(message.payload),
        "sha256": message.sha256,
    }


def canonical_state(qso: QSO) -> dict[str, Any]:
    """Return the complete mutable partition state without the event ledger."""
    return {
        "identity": copy.deepcopy(qso.p.identity),
        "genome": copy.deepcopy(qso.p.genome),
        "records": copy.deepcopy(qso.p.records),
        "inbox": [_message_dict(message) for message in qso.p.inbox],
        "outbox": [_message_dict(message) for message in qso.p.outbox],
        "proposals": copy.deepcopy(qso.p.proposals),
    }


def state_sha256(qso: QSO) -> str:
    return digest(canonical_state(qso))


def event_ledger_sha256(qso: QSO) -> str:
    return digest(qso.p.events)


def verify_event_ledger(events: Iterable[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    previous_hash: str | None = None
    for expected_sequence, event in enumerate(events):
        if event.get("sequence") != expected_sequence:
            errors.append(f"sequence mismatch at {expected_sequence}")
        if event.get("previous_event_sha256") != previous_hash:
            errors.append(f"chain mismatch at {expected_sequence}")
        expected_hash = digest({key: value for key, value in event.items() if key != "sha256"})
        if event.get("sha256") != expected_hash:
            errors.append(f"event hash mismatch at {expected_sequence}")
        previous_hash = event.get("sha256")
    return errors


def validate_message(
    message: MCPMessage,
    *,
    allowed_senders: Iterable[str] | None = None,
    allowed_recipients: Iterable[str] | None = None,
) -> None:
    if not isinstance(message.sender, str) or not message.sender:
        raise RuntimeInvariantError("message sender must be a non-empty string")
    if not isinstance(message.recipient, str) or not message.recipient:
        raise RuntimeInvariantError("message recipient must be a non-empty string")
    if message.kind not in {"proposal", "critique", "annotation", "vote"}:
        raise RuntimeInvariantError("unsupported message kind")
    if not isinstance(message.payload, dict):
        raise RuntimeInvariantError("message payload must be an object")
    if allowed_senders is not None and message.sender not in set(allowed_senders):
        raise RuntimeInvariantError("message sender is outside the allowed set")
    if allowed_recipients is not None and message.recipient not in set(allowed_recipients):
        raise RuntimeInvariantError("message recipient is outside the allowed set")
    expected = digest(
        {
            "sender": message.sender,
            "recipient": message.recipient,
            "kind": message.kind,
            "payload": message.payload,
        }
    )
    if message.sha256 != expected:
        raise RuntimeInvariantError("message integrity failure")


@dataclass
class RuntimeCheckpoint:
    state: dict[str, Any]
    state_sha256: str
    event_ledger_sha256: str


class RuntimeController:
    """Small, deterministic lifecycle wrapper around one isolated QSO partition."""

    def __init__(self, qso: QSO):
        self.qso = qso
        self.status = "active"
        self._checkpoint = self._capture_checkpoint()

    @classmethod
    def instantiate(cls, genome: dict[str, Any], identity: dict[str, Any]) -> "RuntimeController":
        return cls(GenomeInterpreter().instantiate(genome, identity))

    @property
    def checkpoint(self) -> RuntimeCheckpoint:
        return copy.deepcopy(self._checkpoint)

    def _capture_checkpoint(self) -> RuntimeCheckpoint:
        state = canonical_state(self.qso)
        return RuntimeCheckpoint(
            state=state,
            state_sha256=digest(state),
            event_ledger_sha256=event_ledger_sha256(self.qso),
        )

    def _require_status(self, *allowed: str) -> None:
        if self.status not in allowed:
            raise RuntimeInvariantError(
                f"operation requires status in {sorted(allowed)}, current status is {self.status}"
            )

    def _resource_limit(self, name: str, *, default: int) -> int:
        value = self.qso.p.genome.get("resources", {}).get(name, default)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise RuntimeInvariantError(f"resource limit {name} must be a positive integer")
        return value

    def _require_event_capacity(self, additions: int = 1) -> None:
        limit = self._resource_limit("max_events", default=10_000)
        if len(self.qso.p.events) + additions > limit:
            raise RuntimeInvariantError("event limit exceeded")

    def ingest(self, record: dict[str, Any]) -> None:
        self._require_status("active")
        if len(self.qso.p.records) >= self._resource_limit("max_records", default=1):
            raise RuntimeInvariantError("record limit exceeded")
        self._require_event_capacity()
        before = canonical_state(self.qso)
        self.qso.ingest(record)
        if len(self.qso.p.records) > self._resource_limit("max_records", default=1):
            self._restore_state(before)
            raise RuntimeInvariantError("record limit exceeded")

    def send(self, recipient: str, kind: str, payload: dict[str, Any]) -> MCPMessage:
        self._require_status("active")
        if len(self.qso.p.outbox) >= self._resource_limit("max_messages", default=1_000):
            raise RuntimeInvariantError("outbox message limit exceeded")
        message = MCPMessage.build(self.qso.genome_id, recipient, kind, payload)
        validate_message(
            message,
            allowed_senders={self.qso.genome_id},
            allowed_recipients=self.qso.p.genome["communication"]["allowed_peers"],
        )
        self.qso.p.outbox.append(message)
        return message

    def receive(self, message: MCPMessage) -> None:
        self._require_status("active")
        if len(self.qso.p.inbox) >= self._resource_limit("max_messages", default=1_000):
            raise RuntimeInvariantError("inbox message limit exceeded")
        validate_message(
            message,
            allowed_senders=self.qso.p.genome["communication"]["allowed_peers"],
            allowed_recipients={self.qso.genome_id},
        )
        self.qso.receive(message)

    def freeze(self, annotations: list[dict[str, Any]]) -> dict[str, Any]:
        self._require_status("active")
        self._require_event_capacity()
        result = self.qso.freeze(annotations)
        if result["decision"] == "rollback":
            self.status = "active"
        else:
            self.status = "frozen"
            self._checkpoint = self._capture_checkpoint()
        return copy.deepcopy(result)

    def resume(self) -> None:
        self._require_status("frozen")
        self._require_event_capacity()
        self.status = "active"
        self.qso.record_event("resumed", {"checkpoint_state_sha256": self._checkpoint.state_sha256})

    def interrupt(self, reason: str) -> None:
        self._require_status("active")
        if not isinstance(reason, str) or not reason.strip():
            raise RuntimeInvariantError("interruption reason must be non-empty")
        self._require_event_capacity()
        self.status = "interrupted"
        self.qso.record_event("interrupted", {"reason": reason.strip()})

    def recover(self) -> None:
        self._require_status("interrupted")
        self._require_event_capacity()
        self._restore_state(self._checkpoint.state)
        self.status = "active"
        self.qso.record_event(
            "recovered",
            {"checkpoint_state_sha256": self._checkpoint.state_sha256},
        )

    def rollback(self) -> None:
        self._require_status("active", "frozen", "interrupted")
        self._require_event_capacity()
        self._restore_state(self._checkpoint.state)
        self.status = "active"
        self.qso.record_event(
            "rollback",
            {"checkpoint_state_sha256": self._checkpoint.state_sha256},
        )

    def _restore_state(self, state: dict[str, Any]) -> None:
        self.qso.p.identity = copy.deepcopy(state["identity"])
        self.qso.p.genome = copy.deepcopy(state["genome"])
        self.qso.p.records = copy.deepcopy(state["records"])
        self.qso.p.inbox = [MCPMessage(**copy.deepcopy(item)) for item in state["inbox"]]
        self.qso.p.outbox = [MCPMessage(**copy.deepcopy(item)) for item in state["outbox"]]
        self.qso.p.proposals = copy.deepcopy(state["proposals"])
        self.qso._snapshot = self.qso.snapshot()

    def evidence(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "state_sha256": state_sha256(self.qso),
            "event_ledger_sha256": event_ledger_sha256(self.qso),
            "event_verification_errors": verify_event_ledger(self.qso.p.events),
            "checkpoint_state_sha256": self._checkpoint.state_sha256,
            "record_count": len(self.qso.p.records),
            "inbox_count": len(self.qso.p.inbox),
            "outbox_count": len(self.qso.p.outbox),
        }
