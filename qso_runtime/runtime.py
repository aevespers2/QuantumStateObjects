from __future__ import annotations

import copy
import hashlib
import math
import string
from dataclasses import dataclass
from typing import Any, Iterable

from qso_runtime.core import GenomeInterpreter, MCPMessage, QSO, digest


class RuntimeInvariantError(RuntimeError):
    """Raised when a bounded runtime invariant would be violated."""


_EVENT_KEYS = frozenset(
    {
        "sequence",
        "qso",
        "kind",
        "payload",
        "previous_event_sha256",
        "sha256",
    }
)
_CANONICAL_RECORD_REQUIRED_KEYS = frozenset(
    {"content", "content_sha256", "flags", "transformations"}
)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in string.hexdigits for character in value)
    )


def _validate_json_value(value: object, *, label: str) -> None:
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise RuntimeInvariantError(
                f"{label} must contain only UTF-8 encodable strings"
            ) from exc
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RuntimeInvariantError(f"{label} must contain only finite JSON numbers")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, label=f"{label}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise RuntimeInvariantError(f"{label} must contain only string object keys")
            _validate_json_value(key, label=f"{label} object key")
            _validate_json_value(item, label=f"{label}.{key}")
        return
    raise RuntimeInvariantError(f"{label} must contain only canonical JSON values")


def _validate_canonical_record(record: object) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise RuntimeInvariantError("canonical record must be an object")
    missing = sorted(_CANONICAL_RECORD_REQUIRED_KEYS - record.keys())
    if missing:
        raise RuntimeInvariantError(f"canonical record is missing required fields: {missing}")
    _validate_json_value(record, label="canonical record")

    content = record.get("content")
    if not isinstance(content, str):
        raise RuntimeInvariantError("canonical record content must be a string")
    declared_hash = record.get("content_sha256")
    if (
        not isinstance(declared_hash, str)
        or len(declared_hash) != 64
        or any(character not in "0123456789abcdef" for character in declared_hash)
    ):
        raise RuntimeInvariantError(
            "canonical record content_sha256 must be a lowercase SHA-256 hex string"
        )
    flags = record.get("flags")
    if not isinstance(flags, list) or any(not isinstance(flag, str) for flag in flags):
        raise RuntimeInvariantError("canonical record flags must be an array of strings")
    transformations = record.get("transformations")
    if not isinstance(transformations, list) or any(
        not isinstance(transformation, str) for transformation in transformations
    ):
        raise RuntimeInvariantError(
            "canonical record transformations must be an array of strings"
        )
    return record


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
        if not isinstance(event, dict):
            errors.append(f"event shape mismatch at {expected_sequence}")
            previous_hash = None
            continue

        event_keys = tuple(event.keys())
        string_keys = {key for key in event_keys if isinstance(key, str)}
        if len(string_keys) != len(event_keys):
            errors.append(f"event key type mismatch at {expected_sequence}")
        missing = sorted(_EVENT_KEYS - string_keys)
        extra = sorted(string_keys - _EVENT_KEYS)
        if missing:
            errors.append(f"missing event fields at {expected_sequence}: {missing}")
        if extra:
            errors.append(f"unexpected event fields at {expected_sequence}: {extra}")

        sequence = event.get("sequence")
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            errors.append(f"sequence type mismatch at {expected_sequence}")
        elif sequence != expected_sequence:
            errors.append(f"sequence mismatch at {expected_sequence}")

        if not isinstance(event.get("qso"), str) or not event.get("qso"):
            errors.append(f"qso field mismatch at {expected_sequence}")
        if not isinstance(event.get("kind"), str) or not event.get("kind"):
            errors.append(f"kind field mismatch at {expected_sequence}")
        payload = event.get("payload")
        if not isinstance(payload, dict):
            errors.append(f"payload field mismatch at {expected_sequence}")
        else:
            try:
                _validate_json_value(payload, label=f"event payload at {expected_sequence}")
            except RuntimeInvariantError:
                errors.append(f"payload canonical JSON mismatch at {expected_sequence}")

        previous = event.get("previous_event_sha256")
        if expected_sequence == 0:
            if previous is not None:
                errors.append("chain mismatch at 0")
        elif not _is_sha256(previous) or previous != previous_hash:
            errors.append(f"chain mismatch at {expected_sequence}")

        current_hash = event.get("sha256")
        if not _is_sha256(current_hash):
            errors.append(f"event hash shape mismatch at {expected_sequence}")
        try:
            expected_hash = digest({key: value for key, value in event.items() if key != "sha256"})
        except (TypeError, ValueError):
            errors.append(f"event serialization failure at {expected_sequence}")
        else:
            if current_hash != expected_hash:
                errors.append(f"event hash mismatch at {expected_sequence}")

        previous_hash = current_hash if _is_sha256(current_hash) else None
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
    _validate_json_value(message.payload, label="message payload")
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
        event_limit = self._resource_limit("max_events", default=10_000)
        if event_limit < len(self.qso.p.events) + 1:
            raise RuntimeInvariantError("max_events must reserve capacity for rollback evidence")
        self._checkpoint = self._capture_checkpoint()

    @classmethod
    def instantiate(cls, genome: dict[str, Any], identity: dict[str, Any]) -> "RuntimeController":
        if not isinstance(genome, dict):
            raise RuntimeInvariantError("genome must be an object")
        if not isinstance(identity, dict):
            raise RuntimeInvariantError("identity must be an object")
        _validate_json_value(genome, label="genome")
        _validate_json_value(identity, label="identity")
        resources = genome.get("resources")
        if not isinstance(resources, dict):
            raise RuntimeInvariantError("genome resources must be an object")
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

    def _allowed_peers(self) -> tuple[str, ...]:
        communication = self.qso.p.genome.get("communication")
        if not isinstance(communication, dict):
            raise RuntimeInvariantError("communication must be an object")
        peers = communication.get("allowed_peers")
        if not isinstance(peers, list):
            raise RuntimeInvariantError("communication.allowed_peers must be a JSON array")
        if any(not isinstance(peer, str) or not peer.strip() for peer in peers):
            raise RuntimeInvariantError(
                "communication.allowed_peers must contain only non-empty strings"
            )
        if len(set(peers)) != len(peers):
            raise RuntimeInvariantError("communication.allowed_peers must not contain duplicates")
        return tuple(peers)

    def _require_event_capacity(
        self,
        additions: int = 1,
        *,
        reserve_rollback: bool = True,
    ) -> None:
        limit = self._resource_limit("max_events", default=10_000)
        reserve = 1 if reserve_rollback else 0
        if len(self.qso.p.events) + additions + reserve > limit:
            raise RuntimeInvariantError("event limit exceeded")

    def ingest(self, record: dict[str, Any]) -> None:
        self._require_status("active")
        record = _validate_canonical_record(record)
        content = record["content"]
        declared_hash = record["content_sha256"]
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if declared_hash != expected_hash:
            raise RuntimeInvariantError("canonical record content hash mismatch")
        if len(self.qso.p.records) >= self._resource_limit("max_records", default=1):
            raise RuntimeInvariantError("record limit exceeded")
        self._require_event_capacity()
        before = canonical_state(self.qso)
        events_before = copy.deepcopy(self.qso.p.events)
        try:
            self.qso.ingest(record)
        except Exception as exc:
            self._restore_state(before)
            self.qso.p.events = events_before
            raise RuntimeInvariantError("ingest failed closed without partial mutation") from exc
        if len(self.qso.p.records) > self._resource_limit("max_records", default=1):
            self._restore_state(before)
            self.qso.p.events = events_before
            raise RuntimeInvariantError("record limit exceeded")

    def send(self, recipient: str, kind: str, payload: dict[str, Any]) -> MCPMessage:
        self._require_status("active")
        if len(self.qso.p.outbox) >= self._resource_limit("max_messages", default=1_000):
            raise RuntimeInvariantError("outbox message limit exceeded")
        allowed_peers = self._allowed_peers()
        message = MCPMessage.build(self.qso.genome_id, recipient, kind, payload)
        validate_message(
            message,
            allowed_senders={self.qso.genome_id},
            allowed_recipients=allowed_peers,
        )
        stored_message = MCPMessage(
            sender=message.sender,
            recipient=message.recipient,
            kind=message.kind,
            payload=copy.deepcopy(message.payload),
            sha256=message.sha256,
        )
        self.qso.p.outbox.append(stored_message)
        return message

    def receive(self, message: MCPMessage) -> None:
        self._require_status("active")
        if len(self.qso.p.inbox) >= self._resource_limit("max_messages", default=1_000):
            raise RuntimeInvariantError("inbox message limit exceeded")
        stored_message = MCPMessage(
            sender=message.sender,
            recipient=message.recipient,
            kind=message.kind,
            payload=copy.deepcopy(message.payload),
            sha256=message.sha256,
        )
        validate_message(
            stored_message,
            allowed_senders=self._allowed_peers(),
            allowed_recipients={self.qso.genome_id},
        )
        self.qso.receive(stored_message)

    def freeze(self, annotations: list[dict[str, Any]]) -> dict[str, Any]:
        self._require_status("active")
        if not isinstance(annotations, list) or any(not isinstance(item, dict) for item in annotations):
            raise RuntimeInvariantError("freeze annotations must be a list of objects")
        _validate_json_value(annotations, label="freeze annotations")
        blocked = [copy.deepcopy(item) for item in annotations if item.get("severity") in {"high", "critical"}]
        if blocked:
            result = {
                "qso": self.qso.name,
                "decision": "rollback",
                "annotations": blocked,
                "checkpoint_state_sha256": self._checkpoint.state_sha256,
            }
            self._rollback_to_checkpoint(result)
            return copy.deepcopy(result)

        self._require_event_capacity()
        state = canonical_state(self.qso)
        result = {
            "qso": self.qso.name,
            "decision": "frozen_pending_external_commit",
            "state_sha256": digest(state),
        }
        self.qso.record_event("freeze", result)
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
        self._require_event_capacity(reserve_rollback=False)
        state_before = canonical_state(self.qso)
        events_before = copy.deepcopy(self.qso.p.events)
        status_before = self.status
        try:
            self._restore_state(self._checkpoint.state)
            self.status = "active"
            self.qso.record_event(
                "recovered",
                {"checkpoint_state_sha256": self._checkpoint.state_sha256},
            )
        except Exception as exc:
            self._restore_state(state_before)
            self.qso.p.events = events_before
            self.status = status_before
            raise RuntimeInvariantError("recovery failed closed without partial mutation") from exc

    def _rollback_to_checkpoint(self, payload: dict[str, Any]) -> None:
        _validate_json_value(payload, label="rollback payload")
        self._require_event_capacity(reserve_rollback=False)
        self._restore_state(self._checkpoint.state)
        self.status = "active"
        self.qso.record_event("rollback", copy.deepcopy(payload))

    def rollback(self) -> None:
        self._require_status("active", "frozen", "interrupted")
        self._rollback_to_checkpoint(
            {"checkpoint_state_sha256": self._checkpoint.state_sha256}
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
