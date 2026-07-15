from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class MCPMessage:
    sender: str
    recipient: str
    kind: str
    payload: dict[str, Any]
    sha256: str

    @classmethod
    def build(cls, sender: str, recipient: str, kind: str, payload: dict[str, Any]) -> "MCPMessage":
        if kind not in {"proposal", "critique", "annotation", "vote"}:
            raise ValueError("unsupported message kind")
        body = {"sender": sender, "recipient": recipient, "kind": kind, "payload": payload}
        return cls(sender, recipient, kind, copy.deepcopy(payload), digest(body))


@dataclass
class Partition:
    identity: dict[str, Any]
    genome: dict[str, Any]
    records: list[dict[str, Any]] = field(default_factory=list)
    inbox: list[MCPMessage] = field(default_factory=list)
    outbox: list[MCPMessage] = field(default_factory=list)
    proposals: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)


class GenomeInterpreter:
    REQUIRED_FORBIDDEN = {
        "shell_execution", "subprocess_execution", "arbitrary_code_execution",
        "credential_access", "cookie_or_session_access", "unrestricted_network",
        "direct_repository_write", "self_modification_of_immutable_fields",
        "disabling_freeze_controller", "concealing_provenance",
    }

    def instantiate(self, genome: dict[str, Any], identity: dict[str, Any]) -> "QSO":
        missing = {"genome_id", "purpose", "immutable", "mutable", "resources", "freeze", "communication", "learning"} - genome.keys()
        if missing:
            raise ValueError(f"missing genome fields: {sorted(missing)}")
        forbidden = set(genome["immutable"].get("forbidden_capabilities", []))
        if not self.REQUIRED_FORBIDDEN.issubset(forbidden):
            raise ValueError("genome capability boundary is incomplete")
        if genome["learning"].get("input_boundary") != "qso_seeker_canonical_records_only":
            raise ValueError("QSO-SEEKER must be the external input boundary")
        if identity.get("primary_name", "").lower() != genome["genome_id"]:
            raise ValueError("identity does not match genome")
        expected = f"{identity['primary_name']}-{identity['secondary_name']}-Vespers"
        if identity.get("declared_name") != expected:
            raise ValueError("invalid declared lineage name")
        return QSO(Partition(copy.deepcopy(identity), copy.deepcopy(genome)))


class QSO:
    def __init__(self, partition: Partition):
        self.p = partition
        self._snapshot = self.snapshot()
        self.record_event("instantiated", {"genome_sha256": digest(self.p.genome)})

    @property
    def genome_id(self) -> str:
        return self.p.genome["genome_id"]

    @property
    def name(self) -> str:
        return self.p.identity["declared_name"]

    def ingest(self, record: dict[str, Any]) -> None:
        required = {"content", "content_sha256", "flags", "transformations"}
        if not required.issubset(record):
            raise ValueError("non-canonical input record")
        self.p.records.append(copy.deepcopy(record))
        limit = self.p.genome["resources"]["max_records"]
        self.p.records = self.p.records[-limit:]
        self.record_event("ingested", {"sha256": record["content_sha256"]})

    def propose(self) -> dict[str, Any]:
        role = self.genome_id
        corpus = "\n".join(str(r.get("content", "")) for r in self.p.records)[:12000]
        repository_count = len({r.get("repository") for r in self.p.records})
        templates = {
            "atlas": ("provenance_index", "def build_provenance_index(records):\n    return {r['content_sha256']: r['repository'] for r in records}\n", "Compress sanitized observations into a deterministic provenance index."),
            "nova": ("signal_triage", "def triage(records):\n    return [r for r in records if r.get('flags')]\n", "Separate heuristic signals from ordinary records for review."),
            "orion": ("fabric_router", "def route(message, peers):\n    return peers.get(message['recipient'], []) + [message]\n", "Define a minimal schema-bound message routing boundary."),
            "lyra": ("semantic_annotation", "def annotate(record):\n    return {'purpose': 'unknown', 'evidence': record['content_sha256'], 'uncertainty': 0.5}\n", "Attach explicit purpose, evidence, and uncertainty annotations."),
        }
        title, snippet, rationale = templates[role]
        proposal = {
            "qso": self.name,
            "title": title,
            "rationale": rationale,
            "snippet_language": "python",
            "snippet": snippet,
            "source_repository_count": repository_count,
            "source_digest": digest(corpus),
            "execution_status": "inert_not_executed",
            "requires_sprite_review": True,
            "requires_human_review": True,
        }
        proposal["proposal_sha256"] = digest(proposal)
        self.p.proposals.append(proposal)
        self.record_event("proposal_created", {"proposal_sha256": proposal["proposal_sha256"]})
        return proposal

    def critique(self, proposal: dict[str, Any]) -> dict[str, Any]:
        concerns: list[str] = []
        snippet = proposal.get("snippet", "")
        for token in ("eval(", "exec(", "subprocess", "os.system", "requests.", "socket."):
            if token in snippet:
                concerns.append(f"forbidden capability marker: {token}")
        critique = {
            "reviewer": self.name,
            "proposal_sha256": proposal["proposal_sha256"],
            "concerns": concerns,
            "score": max(0, 100 - 25 * len(concerns)),
            "decision": "reviewable" if not concerns else "block_pending_review",
        }
        critique["sha256"] = digest(critique)
        return critique

    def send(self, recipient: str, kind: str, payload: dict[str, Any]) -> MCPMessage:
        if recipient not in self.p.genome["communication"]["allowed_peers"]:
            raise ValueError("recipient outside allowed peers")
        message = MCPMessage.build(self.genome_id, recipient, kind, payload)
        self.p.outbox.append(message)
        return message

    def receive(self, message: MCPMessage) -> None:
        if message.recipient != self.genome_id:
            raise ValueError("recipient mismatch")
        expected = digest({"sender": message.sender, "recipient": message.recipient, "kind": message.kind, "payload": message.payload})
        if expected != message.sha256:
            raise ValueError("message integrity failure")
        self.p.inbox.append(message)

    def freeze(self, annotations: list[dict[str, Any]]) -> dict[str, Any]:
        blocked = [a for a in annotations if a.get("severity") in {"high", "critical"}]
        if blocked:
            self.rollback()
            return {"qso": self.name, "decision": "rollback", "annotations": blocked}
        self._snapshot = self.snapshot()
        result = {"qso": self.name, "decision": "frozen_pending_external_commit", "state_sha256": digest(self._snapshot)}
        self.record_event("freeze", result)
        return result

    def rollback(self) -> None:
        restored = copy.deepcopy(self._snapshot)
        self.p.records = restored["records"]
        self.p.proposals = restored["proposals"]
        self.p.inbox.clear()
        self.p.outbox.clear()
        self.record_event("rollback", {})

    def snapshot(self) -> dict[str, Any]:
        return {"identity": copy.deepcopy(self.p.identity), "records": copy.deepcopy(self.p.records), "proposals": copy.deepcopy(self.p.proposals)}

    def record_event(self, kind: str, payload: dict[str, Any]) -> None:
        event = {"sequence": len(self.p.events), "qso": self.p.identity.get("declared_name"), "kind": kind, "payload": copy.deepcopy(payload)}
        event["sha256"] = digest(event)
        self.p.events.append(event)
