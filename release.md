# Release Plan

## Current Decision

Status: `BLOCKED — CLI CANDIDATE; EXACT-HEAD CI, LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #2 now provides bounded candidate remediation for the previously missing `qso_runtime.cli:main` entry point and adds three focused CLI tests. The PR is open and mergeable at submitted head `38941cb94119850fb3f6102323b534fa4a23f1e9`; its body records a local CPython 3.13.5 replay in which focused pytest, bytecode compilation, no-isolation wheel construction, isolated installation, `qso-run`, and `qso-run --version` passed.

Those claims are candidate evidence only. No pull-request workflow run is attached to the submitted head, the complete current tree has not been independently replayed, local configuration loading and broader runtime/ledger/freeze/rollback fixtures remain incomplete, Atlas still depends on an unaccepted QSO-GENOMES contract, QSO-SEEKER has not published an accepted canonical-record contract, and public privacy/confidentiality/license/attribution approval is absent.

Draft PR #3 adds an Experimenter-QSO roadmap scaffold and materializer. It is open, draft, and mergeable at `7cef9963ee839560ad9e3715abfc9ddf49e0b6ac`, but has no attached pull-request workflow run. Scaffold presence is not implementation, safety, compatibility, or release evidence and must not displace P0.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.
- Experimenter object-model work requires a separately approved later scope/version after the runnable baseline and upstream contracts are accepted.

## Release Scope

- Working package/CLI with validated local configuration loading.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke tests and CI with invalid-configuration and mismatched-hash negative paths.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #2 is selected for review as a bounded P0 CLI slice only. It adds `qso_runtime/cli.py`, deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-network/no-repository-write/no-generated-code-execution boundaries, and three focused tests. Local replay evidence is recorded in the PR, but no release task is `DONE` until an independent clean checkout and attached exact-head workflow reproduce the complete accepted tree.

PR #3 is not selected for the first release. It remains a deferred roadmap proposal pending P0 acceptance, upstream contract publication, approved architecture ownership, implementation evidence, security review, and its own exact-head CI.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, and privacy review.
- `Fixed`: accepted missing CLI remediation, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | REVIEW | PR #2 supplies the entry point and focused tests; an independent exact-head clean build/install and `qso-run` smoke must pass with attached evidence. |
| Task completion | FAIL | P0 is `DONE`; included later tasks have linked evidence. |
| Tests/determinism | PARTIAL | Three focused CLI tests have local candidate evidence; full runtime tests, CI, invalid fixtures, and repeated seeded canonical hashes remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains draft and excluded; no scaffold or future Experimenter capability enters the P0 candidate without a separate approval and evidence cycle. |
| Security | PARTIAL | PR #2 reports bounded no-network/no-write/no-generated-code-execution behavior; complete parser, credential, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture/policy documents and candidate CLI output exist; verified install, configuration, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR #2 identifies submitted head and local commands/results; attached CI logs, complete inputs/tools, package hashes, SBOM, attestations, and rollback evidence remain absent. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head clean-checkout build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Invalid-configuration, mismatched-hash, interruption, rollback, and generated-content-inertness fixtures.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, schema/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted PR changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- PR #2 head `38941cb94119850fb3f6102323b534fa4a23f1e9` has no attached pull-request workflow run or independent complete-tree clean-checkout replay.
- Local configuration loading, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold with no attached workflow evidence and must remain outside P0.
- P0 and the broader quality gates remain incomplete.
- No accepted package checksum, SBOM, security, privacy/license, provenance, attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation. The missing entry point and three focused tests have local replay evidence at `38941cb94119850fb3f6102323b534fa4a23f1e9`, but no attached exact-head workflow or complete runtime evidence exists.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline. It has no attached workflow run and cannot change P0 priority or release scope.
