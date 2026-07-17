# Release Plan

## Current Decision

Status: `BLOCKED — CLI CANDIDATE VERIFIED BY FILE REPLAY; EXACT-HEAD CI, LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #5 now provides the first bounded P0 slice on a fresh branch from current `main`: the previously missing `qso_runtime.cli:main` entry point plus five focused unit, smoke, and fail-closed tests. The code/test commit is `1ec3e6b25ac359d2711626e23ec5da8e3efc8af0`.

A reconstructed exact-file replay passed five tests, bytecode compilation, no-isolation wheel construction, isolated installation, `qso-run`, and `qso-run --version`; the resulting wheel SHA-256 was `8562d17728721c7f2ba4f4ad0fc0ec262ed0e1bc0bc853f4a2643518ba55f14f`. This is bounded candidate evidence, not complete-tree or attached CI evidence: the execution environment could not resolve `github.com`, local configuration loading and broader runtime/ledger/freeze/rollback fixtures remain incomplete, Atlas still depends on an unaccepted QSO-GENOMES contract, QSO-SEEKER has not published an accepted canonical-record contract, and public privacy/confidentiality/license/attribution approval is absent.

PR #2 is superseded by PR #5 because its earlier branch no longer merged cleanly with current `main`. Draft PR #3 remains a deferred Experimenter-QSO roadmap scaffold outside P0 and outside the first release candidate.

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

PR #5 is selected for review as the bounded P0 CLI-and-tests slice. It adds `qso_runtime/cli.py`, deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credentials/no-network/no-repository-write/no-generated-code-execution boundaries, and five tests. Reconstructed exact-file replay passed; no release task is `DONE` until an exact-head workflow and independent complete-tree checkout reproduce the accepted tree.

PR #2 is superseded and should not be merged. PR #3 is not selected for the first release and remains deferred pending P0 acceptance, upstream contract publication, approved architecture ownership, implementation evidence, security review, and separate exact-head CI.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, and privacy review.
- `Fixed`: accepted missing CLI remediation, local configuration loading, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | REVIEW | PR #5 supplies the entry point and five focused tests; exact-head CI and an independent complete-tree clean build/install plus `qso-run` smoke must pass. |
| Task completion | FAIL | P0 is `DONE`; included later tasks have linked evidence. |
| Tests/determinism | PARTIAL | Five CLI tests and reconstructed build/install smoke pass; full runtime tests, attached CI, invalid configuration fixtures, and repeated seeded canonical hashes remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains draft and excluded; no scaffold or future Experimenter capability enters P0 without separate approval and evidence. |
| Security | PARTIAL | PR #5 declares bounded no-credentials/no-network/no-write/no-generated-code-execution behavior; complete parser, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Planning evidence and candidate CLI output exist; verified install, configuration, operations, limitations, and recovery remain incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR #5 records code/test commit, commands, results, and wheel hash; attached CI logs, complete inputs/tools, SBOM, attestations, and rollback evidence remain absent. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head clean-checkout build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Invalid-configuration, mismatched-hash, interruption, rollback, and generated-content-inertness fixtures.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, schema/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted PR changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- PR #5 has reconstructed exact-file evidence but no attached exact-head workflow or independent complete-tree clean-checkout replay.
- Local configuration loading, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold with no attached workflow evidence and must remain outside P0.
- P0 and the broader quality gates remain incomplete.
- No accepted package checksum bundle, SBOM, security, privacy/license, provenance, attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as an initial bounded CLI attempt; it was later superseded because the branch no longer merged cleanly with current `main`.
- 2026-07-17: Selected PR #5 as the fresh P0 CLI-and-tests candidate. Reconstructed exact-file replay passed five tests, compilation, wheel build, isolated installation, CLI smoke, and version smoke; exact-head CI and complete-tree verification remain required.
