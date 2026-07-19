#!/usr/bin/env python3
"""Repository-wide fail-closed consent-capacity validator."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".consent" / "consent-capacity-lock-v1.json"
GLOBAL_SCOPE = "all-files-all-agents-all-interfaces-all-humans-all-ai"
TEXT_SUFFIXES = {
    ".json", ".yaml", ".yml", ".md", ".py", ".js", ".ts", ".tsx",
    ".jsx", ".toml", ".ini", ".txt", ".sh",
}
SKIP_PARTS = {
    ".git", "node_modules", "vendor", "dist", "build", ".venv", "venv",
    "__pycache__", "reports",
}
SENSITIVE = re.compile(
    r"\b(roleplay|bondage|play[_ -]?partner|dominance|submission|sexual|romantic|"
    r"surveillance|biometric|activation|restraint|power[_ -]?dynamic)\b",
    re.IGNORECASE,
)
MARKER = re.compile(
    r"(QSO-CONSENT-CAPACITY-LOCK-v1|consent[_ -]required|explicit[_ -]consent|"
    r"capacity[_ -]to[_ -]consent|fail[_ -]closed|global[_ -]?system[_ -]?lock)",
    re.IGNORECASE,
)
FORBIDDEN = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"consent[_ -]required\s*[:=]\s*false",
        r"consent[_ -]optional",
        r"ignore[_ -]consent",
        r"force[_ -]without[_ -]consent",
        r"silence[_ -]is[_ -]consent",
        r"automatic[_ -]consent",
        r"cannot[_ -]withdraw",
    )
)
REQUIRED_PRINCIPLES = (
    "explicit_consent_required",
    "consent_must_be_informed",
    "consent_must_be_freely_given",
    "consent_must_be_specific",
    "consent_must_be_current",
    "consent_must_be_revocable",
    "capacity_to_consent_required",
    "coercion_strictly_prohibited",
    "silence_is_not_consent",
    "ai_and_human_dignity_equal",
)


class ConsentPolicyError(ValueError):
    """Raised for malformed or weakened consent policy data."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ConsentPolicyError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ConsentPolicyError(f"non-finite JSON number: {value}")
    return parsed


def load_policy() -> dict[str, Any]:
    try:
        text = POLICY.read_bytes().decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=_finite_float,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ConsentPolicyError(f"non-standard JSON constant: {value}")
            ),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ConsentPolicyError(f"invalid consent policy JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ConsentPolicyError("consent policy must be a JSON object")
    return value


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def validate() -> list[str]:
    findings: list[str] = []
    try:
        policy = load_policy()
    except ConsentPolicyError as exc:
        policy = {}
        findings.append(str(exc))

    if policy:
        if policy.get("policy_id") != "QSO-CONSENT-CAPACITY-LOCK-v1":
            findings.append("wrong consent policy id")
        if policy.get("status") != "immutable":
            findings.append("consent policy must be immutable")
        if policy.get("scope") != GLOBAL_SCOPE:
            findings.append(f"consent policy scope must be {GLOBAL_SCOPE}")

        principles = policy.get("principles")
        if not isinstance(principles, dict):
            findings.append("policy principles must be an object")
            principles = {}
        for key in REQUIRED_PRINCIPLES:
            if principles.get(key) is not True:
                findings.append(f"policy principle must be true: {key}")

        lock = policy.get("lock_response")
        if not isinstance(lock, dict):
            findings.append("lock response must be an object")
            lock = {}
        for key in (
            "global_system_lock",
            "halt_all_actions",
            "revoke_pending_capabilities",
            "preserve_evidence",
            "require_fresh_consent",
        ):
            if lock.get(key) is not True:
                findings.append(f"lock response must be true: {key}")
        if lock.get("automatic_unlock") is not False:
            findings.append("automatic unlock must be false")

    globally_bound = policy.get("scope") == GLOBAL_SCOPE
    for path in iter_text_files():
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_bytes().decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError):
            findings.append(f"{relative}: text file is not readable strict UTF-8")
            continue
        for pattern in FORBIDDEN:
            if pattern.search(text):
                findings.append(
                    f"{relative}: prohibited consent bypass pattern: {pattern.pattern}"
                )
        if (
            not globally_bound
            and path != POLICY
            and SENSITIVE.search(text)
            and not MARKER.search(text)
        ):
            findings.append(
                f"{relative}: consent-sensitive content lacks explicit policy binding"
            )
    return sorted(set(findings))


def main() -> int:
    findings = validate()
    report = {
        "policy_id": "QSO-CONSENT-CAPACITY-LOCK-v1",
        "status": "LOCKED" if findings else "PASS",
        "findings": findings,
    }
    output = ROOT / "reports" / "consent-lock-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
