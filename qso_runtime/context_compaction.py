from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable


PROTECTED_KEYS = {
    "entry_sha256",
    "previous_entry_sha256",
    "intent_entry_sha256",
    "before_state_sha256",
    "after_state_sha256",
    "raw_sha256",
    "canonical_sha256",
    "ledger_sha256",
    "repository",
    "operation",
    "phase",
    "result",
    "timestamp_utc",
    "reason",
    "requested_by",
    "performed_by",
    "instruction_source",
    "provider_receipt",
    "verification_errors",
}


@dataclass(frozen=True)
class CompactionPolicy:
    max_visible_chars: int = 12_000
    max_items_per_section: int = 20
    preserve_protected_keys: bool = True
    include_provenance_pointers: bool = True
    token_char_ratio: float = 4.0


@dataclass(frozen=True)
class CompactionResult:
    compacted: dict[str, Any]
    source_sha256: str
    compacted_sha256: str
    source_char_count: int
    compacted_char_count: int
    estimated_source_tokens: int
    estimated_compacted_tokens: int
    omitted_item_count: int
    provenance_pointers: tuple[str, ...]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8", errors="strict")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _estimate_tokens(char_count: int, ratio: float) -> int:
    if ratio <= 0:
        raise ValueError("token_char_ratio must be positive")
    return max(1, int(round(char_count / ratio))) if char_count else 0


def compact_context(
    sections: dict[str, Iterable[dict[str, Any]] | dict[str, Any] | str],
    policy: CompactionPolicy | None = None,
) -> CompactionResult:
    selected = policy or CompactionPolicy()
    if not isinstance(sections, dict):
        raise TypeError("sections must be an object")
    source = copy.deepcopy(sections)
    source_bytes = _canonical_bytes(source)
    output: dict[str, Any] = {}
    pointers: list[str] = []
    omitted = 0

    for section_name in sorted(source):
        value = source[section_name]
        if isinstance(value, list):
            retained = []
            for item in value[: selected.max_items_per_section]:
                retained.append(_compact_value(item, selected, pointers))
            omitted += max(0, len(value) - len(retained))
            output[section_name] = retained
        else:
            output[section_name] = _compact_value(value, selected, pointers)

    compacted_bytes = _canonical_bytes(output)
    if len(compacted_bytes.decode("utf-8")) > selected.max_visible_chars:
        output = _truncate_sections(output, selected.max_visible_chars, pointers)
        compacted_bytes = _canonical_bytes(output)

    source_chars = len(source_bytes.decode("utf-8"))
    compacted_chars = len(compacted_bytes.decode("utf-8"))
    return CompactionResult(
        compacted=output,
        source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        compacted_sha256=hashlib.sha256(compacted_bytes).hexdigest(),
        source_char_count=source_chars,
        compacted_char_count=compacted_chars,
        estimated_source_tokens=_estimate_tokens(source_chars, selected.token_char_ratio),
        estimated_compacted_tokens=_estimate_tokens(compacted_chars, selected.token_char_ratio),
        omitted_item_count=omitted,
        provenance_pointers=tuple(sorted(set(pointers))),
    )


def _compact_value(value: Any, policy: CompactionPolicy, pointers: list[str]) -> Any:
    if isinstance(value, dict):
        compacted: dict[str, Any] = {}
        for key in sorted(value):
            item = value[key]
            if key in PROTECTED_KEYS and policy.preserve_protected_keys:
                compacted[key] = copy.deepcopy(item)
                if policy.include_provenance_pointers and isinstance(item, str) and key.endswith("sha256"):
                    pointers.append(item)
            elif item in (None, "", [], {}, False):
                continue
            elif isinstance(item, (dict, list)):
                compacted[key] = _compact_value(item, policy, pointers)
            elif isinstance(item, str):
                compacted[key] = _collapse_text(item)
            else:
                compacted[key] = copy.deepcopy(item)
        return compacted
    if isinstance(value, list):
        return [_compact_value(item, policy, pointers) for item in value[: policy.max_items_per_section]]
    if isinstance(value, str):
        return _collapse_text(value)
    return copy.deepcopy(value)


def _collapse_text(value: str) -> str:
    return " ".join(value.split())


def _truncate_sections(output: dict[str, Any], max_chars: int, pointers: list[str]) -> dict[str, Any]:
    retained: dict[str, Any] = {}
    for key in sorted(output):
        candidate = {**retained, key: output[key]}
        if len(_canonical_bytes(candidate).decode("utf-8")) <= max_chars:
            retained[key] = output[key]
        else:
            retained["compaction_notice"] = {
                "truncated_before_display": True,
                "last_retained_section": next(reversed(retained), None),
                "provenance_pointer_count": len(set(pointers)),
            }
            break
    return retained
