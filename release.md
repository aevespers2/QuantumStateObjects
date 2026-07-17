# Release Plan

## Current Decision

Status: `BLOCKED — RUNNABLE CLI BASELINE VERIFIED; LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #4 provides the current bounded P0 candidate from the latest `main`: it restores `qso_runtime.cli:main`, adds four deterministic CLI tests, constrains setuptools discovery to `qso_runtime*`, and adds least-privilege CI for Python 3.11 and 3.13 with checkout credential persistence disabled.

Candidate head `62bc5784619c1d689694f0d0182692302acf6316` passed GitHub Actions run `29599420796` in both matrix jobs. Package installation, bytecode compilation, four pytest cases, repeated deterministic output, installed `qso-run` boundary validation, version output, and wheel construction all succeeded. Later documentation-only commits must also pass on their exact submitted head before merge.

The verified CLI/test/CI slice does not complete P0. Local configuration loading, invalid-fixture fail-closed behavior, broader runtime/ledger/freeze/rollback fixtures, Atlas's genome reference, QSO-GENOMES and QSO-SEEKER contracts, deterministic four-QSO evidence, and public privacy/confidentiality/license/attribution approval remain incomplete.

Draft PR #3 adds an Experimenter-QSO roadmap scaffold and materializer. It remains deferred and outside the runnable baseline; scaffold presence is not implementation, safety, compatibility, or release evidence.

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

PR #4 is selected for review as the current bounded P0 CLI/test/CI slice. It adds `qso_runtime/cli.py`, deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four focused tests, explicit package discovery, and Python 3.11/3.13 CI. Exact-head run `29599420796` passed at candidate head `62bc5784619c1d689694f0d0182692302acf6316`.

PR #2 is superseded by PR #4 because PR #4 was rebuilt from current `main`, includes CI and packaging repair, and has attached workflow evidence. PR #3 is not selected for the first release.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, and privacy review.
- `Fixed`: accepted missing CLI remediation, package discovery, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Runnable package/CLI | PASS — CANDIDATE | PR #4 exact-head CI installed the package and passed `qso-run`, `qso-run --version`, deterministic output, and wheel construction on Python 3.11 and 3.13. Final merged-head verification remains required. |
| Task completion | FAIL | P0 is `DONE`; included later tasks have linked evidence. |
| Tests/determinism | PARTIAL | Four CLI tests and repeated byte-for-byte output pass; full runtime tests, invalid fixtures, and repeated seeded canonical run hashes remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains excluded; no scaffold or future Experimenter capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI uses read-only permissions and disables checkout credential persistence; the CLI reports no credential/network/write/generated-code authority. Complete parser, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | CLI boundary and CI evidence are documented; configuration, operations, limitations, and recovery remain incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR #4 records base/head and workflow run evidence; package hashes, SBOM, attestations, complete input/tool manifest, and rollback bundle remain absent. |
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

- Local configuration loading, invalid-fixture validation, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, and event/attribution evidence remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- P0 and the broader quality gates remain incomplete.
- No accepted package checksum, SBOM, security review, privacy/license model, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as initial bounded CLI remediation with local-only replay evidence.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Opened PR #4 from current `main`, repaired explicit package discovery after the first CI attempt exposed install failure, hardened checkout credential handling, and obtained passing Python 3.11/3.13 exact-head workflow evidence in run `29599420796`. The runnable CLI/test/CI slice is verified; local runtime and upstream contract gates remain blocked.
