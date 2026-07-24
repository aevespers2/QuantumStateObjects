from __future__ import annotations

import pytest

from qso_runtime.preflight import (
    PreflightContext,
    PreflightRejected,
    canonical_json_bytes,
    run_preflight,
    strict_json_loads,
)


VALID_DIGEST = "a" * 64
VALID_HEAD = "b" * 40


def ready_context() -> PreflightContext:
    return PreflightContext(
        console_scripts={"qso-run": "qso_runtime.cli:main"},
        importable_targets=frozenset({"qso_runtime.cli:main"}),
        documents={
            "instance": {
                "identity": {
                    "primary_name": "Atlas",
                    "secondary_name": "Atlas-Prime",
                    "declared_name": "Atlas",
                }
            }
        },
        raw_utf8_documents={"config": b'{"schema_version":1}'},
        required_artifacts={"genome": VALID_DIGEST},
        accepted_artifacts={"genome": VALID_DIGEST},
        exact_head_sha=VALID_HEAD,
        evidence_head_sha=VALID_HEAD,
    )


def test_ready_report_is_deterministic_and_hash_bound() -> None:
    first = run_preflight(ready_context())
    second = run_preflight(ready_context())

    assert first.ready is True
    assert first.canonical_dict() == second.canonical_dict()
    assert first.sha256 == second.sha256
    first.require_ready()


def test_missing_console_target_fails_before_pip() -> None:
    context = ready_context()
    context = PreflightContext(
        **{
            **context.__dict__,
            "importable_targets": frozenset(),
        }
    )

    report = run_preflight(context)

    assert report.ready is False
    with pytest.raises(PreflightRejected, match="PKG.CONSOLE_TARGETS"):
        report.require_ready()


def test_duplicate_json_keys_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate JSON key"):
        strict_json_loads(b'{"value":1,"value":2}')


def test_invalid_utf8_is_rejected() -> None:
    with pytest.raises(UnicodeDecodeError):
        strict_json_loads(b'{"value":"\xff"}')


def test_nonstandard_and_overflow_numbers_are_rejected() -> None:
    with pytest.raises(ValueError):
        strict_json_loads(b'{"value":NaN}')
    with pytest.raises(ValueError, match="non-finite numeric value"):
        strict_json_loads(b'{"value":1e999}')


def test_lone_surrogate_is_rejected() -> None:
    with pytest.raises(UnicodeEncodeError):
        canonical_json_bytes({"value": "\ud800"})


def test_non_string_json_keys_are_rejected() -> None:
    with pytest.raises(ValueError, match="keys must be strings"):
        canonical_json_bytes({1: "invalid"})


def test_noncanonical_identity_fails_before_construction() -> None:
    context = ready_context()
    context = PreflightContext(
        **{
            **context.__dict__,
            "documents": {
                "instance": {
                    "identity": {
                        "primary_name": "atlas",
                        "declared_name": "atlas",
                    }
                }
            },
        }
    )

    report = run_preflight(context)

    assert report.ready is False
    failure = next(
        result for result in report.results if result.rule_id == "SCHEMA.CANONICAL_IDENTITY"
    )
    assert failure.passed is False


def test_unaccepted_or_mismatched_artifact_is_rejected() -> None:
    context = ready_context()
    context = PreflightContext(
        **{
            **context.__dict__,
            "accepted_artifacts": {"genome": "c" * 64},
        }
    )

    report = run_preflight(context)

    assert report.ready is False
    failure = next(
        result for result in report.results if result.rule_id == "PROV.ACCEPTED_HASHES"
    )
    assert failure.passed is False


def test_unresolved_review_or_stale_evidence_blocks_acceptance() -> None:
    context = ready_context()
    context = PreflightContext(
        **{
            **context.__dict__,
            "unresolved_findings": ("P2 canonical identity mismatch",),
            "evidence_head_sha": "d" * 40,
        }
    )

    report = run_preflight(context)

    assert report.ready is False
    failure = next(
        result for result in report.results
        if result.rule_id == "EVIDENCE.EXACT_HEAD_READY"
    )
    assert failure.passed is False
    assert len(failure.details["failures"]) == 2
