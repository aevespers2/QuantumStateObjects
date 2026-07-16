# Release Plan

## Current Decision

Status: `BLOCKED — NON-RUNNABLE PACKAGE AND UPSTREAM CONTRACTS`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. The declared `qso-run = qso_runtime.cli:main` entry point refers to missing `qso_runtime/cli.py`; the configured `tests` path has no test files and no CI workflow; Atlas references a missing QSO-GENOMES artifact; P0 remains `READY`; and candidate head `358218cbd94d998db0259caca1c713c5ea8d34fe` lacks current build, smoke, deterministic, freeze/rollback, security, documentation, privacy/license, provenance, and artifact evidence.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.

## Release Scope

- Working package/CLI with validated local configuration loading.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke tests and CI with invalid-configuration and mismatched-hash negative paths.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

## Selected Completed Work

None. Existing modules and declarative assets are candidate inputs, but no task is `DONE`, the package entry point is broken, tests/CI are absent, and upstream contracts are incomplete.

## Planned Changelog Entries

- `Added`: working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, and privacy review.
- `Fixed`: missing CLI module, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | FAIL | `qso_runtime.cli:main` exists; clean build/install and `qso-run` smoke pass. |
| Task completion | FAIL | P0 is `DONE`; included later tasks have linked evidence. |
| Tests/determinism | FAIL | Real tests and CI exist; full tests and repeated seeded runs reproduce canonical hashes. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest includes Atlas and QSO-SEEKER canonical-record fixtures are published and hash-verifiable. |
| Security | NO EVIDENCE | External data fails closed; generated content does not execute; parser, credential, network, repository-write, dependency, secret, and CI boundaries pass review. |
| Documentation | PARTIAL | Architecture/policy documents exist; verified install, CLI, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | NO EVIDENCE | Candidate/upstream commits, seeds, inputs, tools, commands, reports, artifacts, hashes, SBOM, and attestations are retained. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Complete build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- SBOM where applicable, SHA-256 checksums, provenance manifest, and rollback instructions.

## Rollback Criteria

Rollback if the entry point fails, schema/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, or artifact hashes differ. Restore the last verified state and preserve failed-candidate inputs, reports, and hashes.

## Unresolved Blockers

- `qso_runtime/cli.py` is missing although the package publishes `qso-run`.
- The configured test path has no tests and no CI workflow exists.
- Atlas references the missing `QSO-GENOMES/genomes/atlas.json`; Seeker's versioned canonical-record contract is unpublished.
- P0 and all quality-gate evidence remain incomplete.
- No build, CLI smoke, determinism, resource, freeze/rollback, security, documentation, package, checksum, provenance, or rollback evidence exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remains blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.