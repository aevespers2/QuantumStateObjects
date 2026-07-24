"""Fail-closed preventive assurance for QuantumStateObjects.

This module is intentionally side-effect free. It evaluates known failure classes
before package installation, controller construction, state mutation, or runtime
execution and emits a deterministic, hash-bound report.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re
from typing import Any, Callable, Iterable, Mapping, Sequence


class PreflightBoundary(str, Enum):
    REPOSITORY = "repository"
    PACKAGING = "packaging"
    PARSING = "parsing"
    SCHEMA = "schema"
    PROVENANCE = "provenance"
    CONSTRUCTION = "construction"
    LEDGER = "ledger"
    SAFETY = "safety"
    EVIDENCE = "evidence"


@dataclass(frozen=True)
class InsightResult:
    rule_id: str
    boundary: PreflightBoundary
    passed: bool
    summary: str
    remediation: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "boundary": self.boundary.value,
            "details": canonicalize(self.details),
            "passed": self.passed,
            "remediation": self.remediation,
            "rule_id": self.rule_id,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class InsightRule:
    rule_id: str
    boundary: PreflightBoundary
    description: str
    validator: Callable[["PreflightContext"], InsightResult]
    required: bool = True

    def evaluate(self, context: "PreflightContext") -> InsightResult:
        result = self.validator(context)
        if result.rule_id != self.rule_id or result.boundary != self.boundary:
            raise ValueError(f"validator returned mismatched identity for {self.rule_id}")
        return result


@dataclass(frozen=True)
class PreflightContext:
    repository_files: frozenset[str] = frozenset()
    pyproject: Mapping[str, Any] | None = None
    console_scripts: Mapping[str, str] = field(default_factory=dict)
    importable_targets: frozenset[str] = frozenset()
    documents: Mapping[str, Any] = field(default_factory=dict)
    raw_utf8_documents: Mapping[str, bytes] = field(default_factory=dict)
    accepted_artifacts: Mapping[str, str] = field(default_factory=dict)
    required_artifacts: Mapping[str, str] = field(default_factory=dict)
    unresolved_findings: tuple[str, ...] = ()
    exact_head_sha: str | None = None
    evidence_head_sha: str | None = None


@dataclass(frozen=True)
class PreflightReport:
    results: tuple[InsightResult, ...]
    required_rule_ids: tuple[str, ...]

    @property
    def ready(self) -> bool:
        required = set(self.required_rule_ids)
        return all(result.passed for result in self.results if result.rule_id in required)

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "required_rule_ids": list(self.required_rule_ids),
            "results": [result.canonical_dict() for result in self.results],
        }

    @property
    def sha256(self) -> str:
        return hashlib.sha256(canonical_json_bytes(self.canonical_dict())).hexdigest()

    def require_ready(self) -> None:
        if self.ready:
            return
        failures = [
            f"{result.rule_id}: {result.summary}"
            for result in self.results
            if result.rule_id in set(self.required_rule_ids) and not result.passed
        ]
        raise PreflightRejected("; ".join(failures), report=self)


class PreflightRejected(RuntimeError):
    def __init__(self, message: str, *, report: PreflightReport) -> None:
        super().__init__(message)
        self.report = report


_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*(?:-[A-Z][A-Za-z0-9]*)*$")


def canonicalize(value: Any) -> Any:
    """Return a JSON-safe canonical value or fail closed."""
    if value is None or isinstance(value, (bool, str)):
        if isinstance(value, str):
            value.encode("utf-8", "strict")
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("non-finite numeric value")
        return value
    if isinstance(value, list):
        return [canonicalize(item) for item in value]
    if isinstance(value, tuple):
        return [canonicalize(item) for item in value]
    if isinstance(value, Mapping):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("JSON object keys must be strings")
            key.encode("utf-8", "strict")
            output[key] = canonicalize(item)
        return output
    raise ValueError(f"unsupported canonical value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    canonical = canonicalize(value)
    return json.dumps(
        canonical,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8", "strict")


def strict_json_loads(raw: bytes) -> Any:
    text = raw.decode("utf-8", "strict")

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    def reject_duplicate_pairs(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    value = json.loads(
        text,
        parse_constant=reject_constant,
        object_pairs_hook=reject_duplicate_pairs,
    )
    return canonicalize(value)


def _result(
    rule_id: str,
    boundary: PreflightBoundary,
    passed: bool,
    summary: str,
    remediation: str = "",
    **details: Any,
) -> InsightResult:
    return InsightResult(
        rule_id=rule_id,
        boundary=boundary,
        passed=passed,
        summary=summary,
        remediation=remediation,
        details=details,
    )


def validate_console_scripts(context: PreflightContext) -> InsightResult:
    missing: list[str] = []
    malformed: list[str] = []
    for name, target in sorted(context.console_scripts.items()):
        if ":" not in target:
            malformed.append(name)
            continue
        module, callable_name = target.split(":", 1)
        normalized = f"{module}:{callable_name}"
        if normalized not in context.importable_targets:
            missing.append(f"{name}={normalized}")
    passed = not missing and not malformed
    return _result(
        "PKG.CONSOLE_TARGETS",
        PreflightBoundary.PACKAGING,
        passed,
        "all console-script targets resolve" if passed else "console-script target is missing or malformed",
        "Create the module/callable and verify importability before invoking pip.",
        missing=missing,
        malformed=malformed,
    )


def validate_documents(context: PreflightContext) -> InsightResult:
    failures: dict[str, str] = {}
    for name, value in sorted(context.documents.items()):
        try:
            canonical_json_bytes(value)
        except (TypeError, ValueError, UnicodeError) as exc:
            failures[name] = str(exc)
    for name, raw in sorted(context.raw_utf8_documents.items()):
        try:
            strict_json_loads(raw)
        except (TypeError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
            failures[name] = str(exc)
    passed = not failures
    return _result(
        "DATA.CANONICAL_JSON",
        PreflightBoundary.PARSING,
        passed,
        "all documents are canonical UTF-8 JSON" if passed else "noncanonical document rejected",
        "Reject duplicate keys, invalid UTF-8, non-finite values, surrogates, and unsupported shapes.",
        failures=failures,
    )


def validate_artifacts(context: PreflightContext) -> InsightResult:
    failures: dict[str, str] = {}
    for name, expected in sorted(context.required_artifacts.items()):
        actual = context.accepted_artifacts.get(name)
        if not _HEX_64.fullmatch(expected):
            failures[name] = "required digest is not lowercase SHA-256"
        elif actual is None:
            failures[name] = "accepted artifact is absent"
        elif actual != expected:
            failures[name] = "accepted artifact digest does not match required digest"
    passed = not failures
    return _result(
        "PROV.ACCEPTED_HASHES",
        PreflightBoundary.PROVENANCE,
        passed,
        "all required artifacts are accepted and hash-pinned" if passed else "artifact acceptance gate failed",
        "Accept immutable upstream artifacts and require exact lowercase SHA-256 matches.",
        failures=failures,
    )


def validate_identity_names(context: PreflightContext) -> InsightResult:
    failures: dict[str, str] = {}
    for document_name, document in sorted(context.documents.items()):
        if not isinstance(document, Mapping):
            continue
        identity = document.get("identity")
        if identity is None:
            continue
        if not isinstance(identity, Mapping):
            failures[document_name] = "identity must be an object"
            continue
        names = {
            key: identity.get(key)
            for key in ("primary_name", "secondary_name", "declared_name")
            if key in identity
        }
        for key, value in names.items():
            if not isinstance(value, str) or not _CANONICAL_NAME.fullmatch(value):
                failures[f"{document_name}.{key}"] = "noncanonical identity name"
    passed = not failures
    return _result(
        "SCHEMA.CANONICAL_IDENTITY",
        PreflightBoundary.SCHEMA,
        passed,
        "identity names satisfy the canonical contract" if passed else "identity contract rejected",
        "Validate identity names before RuntimeController construction.",
        failures=failures,
    )


def validate_review_and_evidence(context: PreflightContext) -> InsightResult:
    failures: list[str] = list(context.unresolved_findings)
    if not context.exact_head_sha:
        failures.append("exact head SHA is absent")
    if context.exact_head_sha != context.evidence_head_sha:
        failures.append("evidence is not bound to the exact head SHA")
    passed = not failures
    return _result(
        "EVIDENCE.EXACT_HEAD_READY",
        PreflightBoundary.EVIDENCE,
        passed,
        "review and exact-head evidence gates pass" if passed else "acceptance evidence gate failed",
        "Resolve findings and retain evidence bound to the immutable submitted head.",
        failures=failures,
    )


def default_rules() -> tuple[InsightRule, ...]:
    return (
        InsightRule(
            "PKG.CONSOLE_TARGETS",
            PreflightBoundary.PACKAGING,
            "Verify entry points before pip or build execution.",
            validate_console_scripts,
        ),
        InsightRule(
            "DATA.CANONICAL_JSON",
            PreflightBoundary.PARSING,
            "Reject noncanonical bytes and values before schema evaluation.",
            validate_documents,
        ),
        InsightRule(
            "SCHEMA.CANONICAL_IDENTITY",
            PreflightBoundary.SCHEMA,
            "Reject noncanonical in-memory identities before construction.",
            validate_identity_names,
        ),
        InsightRule(
            "PROV.ACCEPTED_HASHES",
            PreflightBoundary.PROVENANCE,
            "Require accepted immutable dependency hashes.",
            validate_artifacts,
        ),
        InsightRule(
            "EVIDENCE.EXACT_HEAD_READY",
            PreflightBoundary.EVIDENCE,
            "Require resolved findings and exact-head evidence.",
            validate_review_and_evidence,
        ),
    )


def run_preflight(
    context: PreflightContext,
    rules: Iterable[InsightRule] | None = None,
) -> PreflightReport:
    selected = tuple(rules or default_rules())
    results = tuple(rule.evaluate(context) for rule in selected)
    required = tuple(rule.rule_id for rule in selected if rule.required)
    return PreflightReport(results=results, required_rule_ids=required)
