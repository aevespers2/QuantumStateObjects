# Release Plan

## Current Decision

Status: `BLOCKED — CANDIDATE CLI; FULL TEST/CI AND UPSTREAM CONTRACTS OPEN`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. Builder branch `builder/runnable-cli-baseline-v1` now supplies the previously missing `qso_runtime.cli:main` entry point and three focused CLI tests; this is candidate remediation only. No clean checkout or attached CI run has verified the complete current tree, local configuration loading and broader runtime fixtures remain incomplete, Atlas references a missing QSO-GENOMES artifact, upstream QSO-SEEKER fixtures remain unpublished, P0 is `IN PROGRESS`, and build, deterministic, freeze/rollback, security, documentation, privacy/license, provenance, and release-artifact gates remain open.

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

No release task is `DONE`. The bounded CLI entry point and focused tests are present only as a candidate on `builder/runnable-cli-baseline-v1`; exact-head checkout, complete tests, CI, runtime fixtures, upstream contracts, and all remaining release gates still require acceptance evidence.

## Planned Changelog Entries

- `Added`: working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, and privacy review.
- `Fixed`: missing CLI module, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | CANDIDATE | `qso_runtime.cli:main` exists on the submitted head; clean exact-head build/install and `qso-run` smoke must pass in CI or an independently reproduced checkout. |
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

- The new CLI and focused tests lack exact-head clean-checkout and attached GitHub Actions evidence.
- Local configuration loading, complete runtime tests, deterministic fixtures, and CI workflow coverage remain incomplete.
- Atlas references the missing `QSO-GENOMES/genomes/atlas.json`; Seeker's versioned canonical-record contract is unpublished.
- P0 and all broader quality-gate evidence remain incomplete.
- No accepted determinism, resource, freeze/rollback, security, documentation, package checksum, provenance, or rollback evidence exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remains blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded bounded candidate remediation for the missing CLI entry point and three focused tests. Release remains blocked pending exact-head clean-checkout/CI evidence, broader runtime verification, upstream contracts, and publication-boundary approval.
