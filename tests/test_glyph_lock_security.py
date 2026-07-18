import pytest

from qso_runtime.attribution import AttributionJourneyLedger
from qso_runtime.glyph_lock import GlyphLockPolicy, scan_bytes, scan_text

SHA = "0" * 64


def test_artifacts_falsy_non_list_is_rejected_without_mutation():
    ledger = AttributionJourneyLedger("atlas")
    for invalid in ({}, "", 0, False):
        with pytest.raises(ValueError, match="artifacts must be a list"):
            ledger.append(
                event_type="test",
                contributors=[],
                state_before_sha256=SHA,
                state_after_sha256=SHA,
                artifacts=invalid,  # type: ignore[arg-type]
            )
        assert ledger.entries == []


def test_none_artifacts_remains_valid_empty_list():
    ledger = AttributionJourneyLedger("atlas")
    entry = ledger.append(
        event_type="test",
        contributors=[],
        state_before_sha256=SHA,
        state_after_sha256=SHA,
        artifacts=None,
        timestamp_utc="2026-07-17T00:00:00+00:00",
    )
    assert entry["artifacts"] == []


def test_strict_utf8_rejects_invalid_bytes():
    result = scan_bytes(b"safe\xfftext")
    assert result.accepted is False
    assert result.disposition == "reject"
    assert result.findings[0].code == "invalid_utf8"


def test_accent_catch_detects_decomposed_normalization_drift():
    result = scan_text("cafe\u0301")
    assert result.accepted is False
    assert "normalization_drift" in {item.code for item in result.findings}


def test_machine_fields_reject_accented_and_non_ascii_glyphs():
    policy = GlyphLockPolicy(field_type="identifier", allow_combining_marks=False)
    result = scan_text("admín", policy)
    assert "non_ascii_machine_field" in {item.code for item in result.findings}


def test_invisible_bidi_and_variation_selectors_are_quarantined():
    result = scan_text("safe\u200b\u202e\ufe0f")
    codes = {item.code for item in result.findings}
    assert {"invisible_or_control", "bidi_control", "variation_selector"}.issubset(codes)
    assert result.disposition == "quarantine"
