from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable

BIDI_CLASSES = {"RLE", "LRE", "RLO", "LRO", "PDF", "RLI", "LRI", "FSI", "PDI"}
INVISIBLE_CODEPOINTS = {
    0x00AD, 0x034F, 0x061C, 0x180E, 0x200B, 0x200C, 0x200D,
    0x2060, 0xFEFF,
}
LINE_SEPARATORS = {"\r", "\u0085", "\u2028", "\u2029"}


@dataclass(frozen=True)
class GlyphLockPolicy:
    field_type: str = "natural_language"
    allow_newline: bool = True
    allow_tab: bool = False
    allow_emoji: bool = False
    allow_combining_marks: bool = True
    allowed_scripts: tuple[str, ...] = ()
    normalization: str = "NFC"
    max_codepoints: int = 1_000_000


@dataclass(frozen=True)
class ScanFinding:
    code: str
    offset: int
    codepoint: str
    name: str
    severity: str = "high"


@dataclass(frozen=True)
class ScanResult:
    raw_sha256: str
    canonical_sha256: str
    accepted: bool
    disposition: str
    tainted: bool
    normalization: str
    findings: tuple[ScanFinding, ...] = field(default_factory=tuple)


def _script_hint(character: str) -> str:
    name = unicodedata.name(character, "UNKNOWN")
    return name.split(" ", 1)[0]


def _finding(code: str, offset: int, character: str, severity: str = "high") -> ScanFinding:
    return ScanFinding(
        code=code,
        offset=offset,
        codepoint=f"U+{ord(character):04X}",
        name=unicodedata.name(character, "UNNAMED"),
        severity=severity,
    )


def scan_bytes(raw: bytes, policy: GlyphLockPolicy | None = None) -> ScanResult:
    selected = policy or GlyphLockPolicy()
    raw_hash = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        finding = ScanFinding("invalid_utf8", 0, "N/A", "INVALID UTF-8")
        return ScanResult(raw_hash, raw_hash, False, "reject", True, selected.normalization, (finding,))
    return scan_text(text, selected, raw_sha256=raw_hash)


def scan_text(text: str, policy: GlyphLockPolicy | None = None, *, raw_sha256: str | None = None) -> ScanResult:
    selected = policy or GlyphLockPolicy()
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    raw = text.encode("utf-8", errors="strict")
    raw_hash = raw_sha256 or hashlib.sha256(raw).hexdigest()
    findings: list[ScanFinding] = []
    if len(text) > selected.max_codepoints:
        findings.append(ScanFinding("length_limit", selected.max_codepoints, "N/A", "LENGTH LIMIT"))

    canonical = unicodedata.normalize(selected.normalization, text)
    if canonical != text:
        findings.append(ScanFinding("normalization_drift", 0, "N/A", "NORMALIZATION DRIFT"))

    scripts: set[str] = set()
    for offset, character in enumerate(text):
        category = unicodedata.category(character)
        combining = unicodedata.combining(character)
        bidi = unicodedata.bidirectional(character)
        codepoint = ord(character)

        if character in LINE_SEPARATORS:
            findings.append(_finding("noncanonical_line_separator", offset, character))
        elif character == "\n" and not selected.allow_newline:
            findings.append(_finding("newline_forbidden", offset, character))
        elif character == "\t" and not selected.allow_tab:
            findings.append(_finding("tab_forbidden", offset, character))
        elif category.startswith("C") or codepoint in INVISIBLE_CODEPOINTS:
            findings.append(_finding("invisible_or_control", offset, character))

        if bidi in BIDI_CLASSES:
            findings.append(_finding("bidi_control", offset, character))
        if category in {"Mn", "Mc", "Me"} and not selected.allow_combining_marks:
            findings.append(_finding("combining_mark_forbidden", offset, character))
        if combining and offset and unicodedata.combining(text[offset - 1]):
            findings.append(_finding("stacked_combining_mark", offset, character))
        if 0xFE00 <= codepoint <= 0xFE0F or 0xE0100 <= codepoint <= 0xE01EF:
            findings.append(_finding("variation_selector", offset, character))
        if category == "So" and not selected.allow_emoji:
            findings.append(_finding("symbol_or_emoji_forbidden", offset, character))

        if character.isalpha():
            scripts.add(_script_hint(character))

    if selected.field_type in {"identifier", "path", "protocol", "schema_key", "hash", "command"}:
        for offset, character in enumerate(text):
            if ord(character) > 0x7F:
                findings.append(_finding("non_ascii_machine_field", offset, character))
    elif selected.allowed_scripts:
        unexpected = sorted(scripts.difference(selected.allowed_scripts))
        if unexpected:
            findings.append(ScanFinding("mixed_or_unexpected_script", 0, "N/A", ",".join(unexpected)))

    canonical_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    accepted = not findings
    disposition = "accept" if accepted else "quarantine"
    return ScanResult(raw_hash, canonical_hash, accepted, disposition, not accepted, selected.normalization, tuple(findings))
