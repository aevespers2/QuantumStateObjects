# Release Plan

## Current Decision
Status: `BLOCKED — NON-RUNNABLE CANDIDATE`

No QuantumStateObjects runtime is eligible for release. The repository contains runtime modules, schemas, four instance declarations, an attribution ledger implementation, and package metadata at version `0.1.0`, but the declared console entry point `qso-run = qso_runtime.cli:main` refers to a missing `qso_runtime/cli.py`. `pyproject.toml` declares `tests` as the pytest path, yet no test files or CI workflow are present. The Atlas instance also references `QSO-GENOMES/genomes/atlas.json`, which is absent upstream. P0 remains `READY`, all punch-list items are unchecked, privacy/licensing publication approval is unresolved, and no current build/test/security/provenance evidence is attached to reviewed head `d290fb637387c5197dea9bd720bd6a07eded4d58`.

## Versioning
- Scheme: Semantic Versioning.
- Existing package metadata identifies version `0.1.0`; the first eligible published candidate should be a clearly marked pre-release such as `0.1.0-alpha.1` until the entry point, contracts, tests, and publication boundaries pass.
- Schema, instance, message, ledger, genome-contract, freeze/rollback, and evidence-format versions must be explicit.
- Incompatible changes require a declared migration and coordinated upstream contract versions.

## Candidate Scope
- Runnable package and CLI with validated configuration loading.
- Current runtime, instance, attribution, ledger, message-integrity, resource-cap, freeze, and rollback baseline.
- Versioned validation of fixed QSO-GENOMES and QSO-SEEKER fixtures by schema version and hash without importing external code.
- Deterministic four-instance configuration and bounded experiment evidence after upstream gates pass.
- Inert proposal handling with Sprite plus human authorization.
- Approved privacy, confidentiality, licensing, attribution, and public-evidence boundaries.
- Reproducible tests, security checks, documentation, artifacts, checksums, and provenance.

## Existing Candidate Assets
- `qso_runtime/core.py` and `qso_runtime/attribution.py` implement candidate runtime and ledger primitives.
- Instance and attribution schemas, four instance declarations, constitution/attribution/privacy documents, and package metadata exist.
- Instance status is `pending_review`, and proposal activation remains Sprite/human-review-gated.

These assets are not releasable until the package is runnable, upstream references resolve, tests exist and pass, and publication approval is recorded.

## Selected Completed Work
None. No task is `DONE`, the package entry point is broken, the test/CI baseline is absent, and the required upstream contract set is incomplete.

## Planned Changelog Entries
- `Added`: working CLI/runtime entry point, reproducible baseline, versioned contract validators, deterministic evidence formats, and tests.
- `Security`: resource caps, fail-closed schema/hash checks, inert proposal handling, input isolation, privacy review, and least-privilege boundaries.
- `Fixed`: missing CLI module, unresolved Atlas reference, message/freeze/rollback/ordering/attribution defects found during validation.
- `Documentation`: installation, CLI usage, instance manifests, trust boundaries, exact commands, privacy/licensing, limitations, and recovery.
- `Release`: package/source artifacts, reports, SBOM, checksums, provenance, and approval decision.

## Acceptance Gates
| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | FAIL | `qso_runtime.cli:main` exists; clean install and `qso-run` smoke test succeed. |
| Task completion | FAIL | P0 reaches `DONE`; included P1 work is complete and linked to commits/evidence. |
| Upstream contracts | BLOCKED | Complete versioned/hash-verified QSO-GENOMES and QSO-SEEKER manifests/fixtures exist; Atlas path resolves. |
| Tests/determinism | FAIL | A real test suite and CI workflow exist; full tests and repeated seeded runs reproduce identical hashes. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, recovery, and rollback are tested without state/evidence corruption. |
| Security | NO EVIDENCE | External data fails closed; generated code is not executed; credential/network/repository-write and parser boundaries are reviewed. |
| Documentation | PARTIAL | Architecture and policy documents exist; verified installation, CLI, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve public license/notice model and handling of personal identifiers/confidentiality language before artifacts are published. |
| Provenance | NO EVIDENCE | Candidate/upstream commits, seeds, inputs, Python/tool versions, commands, reports, artifact hashes, SBOM, and attestations recorded. |
| Approval | PENDING | Explicit release approval after all included-scope gates pass. |

## Artifact Requirements
- Reproducible sdist/wheel and source archive for the reviewed commit.
- Versioned schemas, instance manifests, and fixed upstream contract fixtures.
- Complete test, deterministic-run, security, resource-limit, freeze, rollback, and CLI smoke reports.
- Append-only sample event/attribution artifacts containing no unapproved sensitive data.
- SBOM, SHA-256 checksums, provenance manifest, and rollback instructions.

## Rollback Criteria
Rollback if the package entry point fails, schema/hash validation can be bypassed, required upstream artifacts disappear, generated material executes without authorization, resource limits fail, freeze/rollback loses or corrupts evidence, deterministic runs diverge, attribution is inconsistent, or privacy/licensing approval is absent. Restore the last verified tag and preserve the failed candidate's inputs, reports, and hashes.

## Unresolved Blockers
- `qso_runtime/cli.py` is missing although `pyproject.toml` publishes `qso-run = qso_runtime.cli:main`.
- `pyproject.toml` declares `tests`, but no test files or CI workflow are present.
- `config/instances.json` references missing upstream artifact `QSO-GENOMES/genomes/atlas.json`.
- P0 and every punch-list/quality-gate item remain incomplete; required QSO-GENOMES and QSO-SEEKER manifests are unpublished.
- No build, CLI smoke, deterministic, freeze/rollback, security, documentation, artifact, or provenance evidence is recorded.
- Public files contain a personal privacy identifier and confidentiality notice; the public license/notice model requires approval.
- Payment-intent/distribution records remain outside release scope pending an approved declarative policy boundary.

## Release Log
- 2026-07-16: Recorded the missing CLI, absent tests/CI, missing Atlas dependency, and publication-approval blockers; candidate remains `BLOCKED — NON-RUNNABLE CANDIDATE`.