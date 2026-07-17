# Release Plan

## Current Decision

Status: `BLOCKED — CLI MATRIX CI PASSED ON MERGE REF; EXACT-HEAD, LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #4 is the preferred bounded P0 candidate because it restores `qso_runtime.cli:main`, adds deterministic CLI tests, constrains setuptools discovery to `qso_runtime*`, disables checkout credential persistence, installs declared build tooling, and adds Python 3.11/3.13 CI.

Workflow run `29599534913` completed successfully in both matrix jobs and passed package installation, compilation, four tests, installed `qso-run` smoke, explicit boundary JSON validation, version output, and wheel construction. The run did **not** satisfy the exact-head gate: checkout fetched synthetic merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701` rather than submitted head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`, and the workflow retained no artifacts. PR #4 also has unresolved review threads; the current diff appears to repair package discovery, build dependencies, and credential persistence, while exact-head checkout remains unresolved.

PR #5 duplicates the CLI slice on another branch. Its reconstructed exact-file replay reports five tests, compilation, wheel construction, isolated installation, CLI smoke, version output, and wheel SHA-256 `8562d17728721c7f2ba4f4ad0fc0ec262ed0e1bc0bc853f4a2643518ba55f14f`, but it has no attached workflow and no independent complete-tree clone evidence. PR #5 is not selected while PR #4 remains the stronger evidence path. PR #2 is closed as superseded. Draft PR #3 remains deferred outside P0 and outside the first release.

Local configuration loading and broader runtime/ledger/freeze/rollback fixtures remain incomplete. Atlas still depends on an unaccepted QSO-GENOMES compatibility set, QSO-SEEKER has not published an accepted canonical-record contract, and public privacy/confidentiality/license/attribution approval is absent.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.
- Experimenter object-model work requires a separately approved later scope/version after the runnable baseline and upstream contracts are accepted.

## Release Scope

- Working package/CLI with validated local configuration loading.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke tests and CI with exact-head assertion, invalid-configuration and mismatched-hash negative paths, and retained evidence.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Duplicate CLI branches after one canonical path is accepted.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #4 is selected for architectural review as the preferred P0 CLI/test/CI slice. It includes deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four focused tests, constrained package discovery, and two-version CI. It remains a candidate until its workflow checks out and asserts the immutable PR head, all material review threads are resolved, evidence artifacts are retained, and final-head verification passes.

PR #5 is a duplicate candidate and is not selected. PR #2 is superseded and closed. PR #3 is not selected for the first release.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, inert proposals, input isolation, credential/network/repository-write boundaries, exact-head workflow controls, and privacy review.
- `Fixed`: accepted missing CLI remediation, package discovery, local configuration loading, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work and duplicate CLI paths from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | Explicitly select PR #4 or another single immutable path and disposition PR #5 without losing evidence. |
| Runnable package/CLI | PARTIAL | Run `29599534913` passed on the synthetic merge ref; exact-head clean build/install and `qso-run` smoke must pass at the accepted PR head and merged head. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Four CLI tests passed in matrix CI; full runtime tests, invalid configuration fixtures, repeated seeded canonical hashes, and retained reports remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains draft and excluded; PR #5 does not silently replace the canonical path; no future capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI uses read-only permissions and no persisted checkout credentials; complete parser, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture/policy documents and candidate CLI output exist; verified configuration, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR, head, merge-ref, workflow, commands, and one duplicate wheel hash are recorded; accepted exact-head logs, retained artifacts, complete inputs/tools, SBOM, attestations, and rollback evidence remain absent. |
| Deployment readiness | BLOCKED | `deploy.md` gates environment, permissions, artifacts, configuration, health, observability, rollback, and post-validation; none are approved. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive from the accepted immutable head.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head and merged-head clean-checkout build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Invalid-configuration, mismatched-hash, interruption, rollback, and generated-content-inertness fixtures.
- Retained CI evidence with checked-out SHA, Python/tool versions, command results, artifact hashes, and expiry policy.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Deployment Readiness

No deployment is authorized. The first permitted target is a disposable local or CI verification environment using no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, and no sensitive data. Health, observability, rollback, and post-deployment checks are defined in `deploy.md` and remain blocked until the release gates pass.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, multiple candidates become ambiguous, schema/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- PR #4 workflow run `29599534913` checked out merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701`, not submitted head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`.
- PR #4 has unresolved review threads and retained no workflow artifacts.
- PR #5 duplicates the CLI candidate and has no attached workflow; canonical disposition is required.
- Local configuration loading, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted package checksum, SBOM, security, privacy/license, provenance, attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation, then closed it as superseded when it no longer represented the current canonical path.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Recorded PR #4 as the preferred CLI/test/CI candidate. Matrix CI passed, but logs prove checkout used the synthetic merge ref rather than the submitted head; exact-head acceptance, review disposition, retained artifacts, local runtime evidence, and all release/deployment gates remain open.
- 2026-07-17: Recorded PR #5 as a duplicate local-replay candidate without attached CI; it does not supersede PR #4.