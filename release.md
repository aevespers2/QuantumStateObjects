# Release Plan

## Current Decision

Status: `BLOCKED — EXACT-HEAD WORKFLOW REPAIRED; FINAL HOSTED EVIDENCE, LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #4 remains the preferred bounded P0 candidate because it restores `qso_runtime.cli:main`, adds deterministic CLI tests, constrains setuptools discovery to `qso_runtime*`, disables checkout credential persistence, installs declared build tooling, and covers Python 3.11 and 3.13.

Earlier workflow run `29599534913` passed package installation, compilation, four tests, installed `qso-run` smoke, boundary JSON validation, version output, and wheel construction. It did not satisfy the exact-head gate because checkout used a synthetic merge ref and retained no artifacts.

Commit `e9ba8736a00b7f356c352a81a1e7bf409c38c18e` repaired the workflow to check out `${{ github.event.pull_request.head.sha || github.sha }}`, assert the checked-out SHA, retain the SHA and Python version, preserve deterministic CLI output and version, build a wheel plus SHA-256 manifest, and upload per-Python evidence for 30 days. Independent reconstructed verification passed four tests, source/test compilation, workflow YAML parsing, and wheel construction; the reconstructed wheel SHA-256 was `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`. Final GitHub-hosted verification for the latest PR head remains required.

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

PR #4 is selected for architectural review as the preferred P0 CLI/test/CI slice. It includes deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four focused tests, constrained package discovery, two-version CI, exact-head checkout/assertion, checksummed wheel evidence, and retained artifacts. It remains a candidate until final latest-head CI passes, material review threads are resolved, and duplicate PR #5 is explicitly dispositioned.

PR #5 remains a duplicate candidate and is not selected. PR #2 is superseded and closed. PR #3 is not selected for the first release.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | Final latest-head PR #4 CI passes, review threads are resolved, and PR #5 is explicitly dispositioned. |
| Runnable package/CLI | PARTIAL | Local reconstructed verification passes; final GitHub-hosted exact-head clean build/install and `qso-run` smoke must pass at the accepted head and later merged head. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Four CLI tests pass locally and in the earlier matrix run; full runtime tests, invalid configuration fixtures, repeated seeded canonical hashes, and retained final-head reports remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains excluded; PR #5 does not silently replace the canonical path; no future capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI is read-only and does not persist checkout credentials; complete parser, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | CLI boundary and workflow evidence are documented; verified configuration, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | Workflow now records checked-out SHA, Python version, CLI output, wheel, and checksums; final hosted artifacts, complete tools/inputs, SBOM, attestation, review disposition, and rollback bundle remain absent. |
| Deployment readiness | BLOCKED | No deployment is authorized before all release gates pass. |
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

No deployment is authorized. The first permitted target is a disposable local or CI verification environment using no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, and no sensitive data.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, multiple candidates become ambiguous, schema/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- Final GitHub-hosted exact-head CI and retained artifacts are not yet recorded for the latest PR #4 head.
- PR #4 review-thread disposition and explicit PR #5 disposition remain open.
- Local configuration loading, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted SBOM, complete security/privacy review, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation, then closed it as superseded when it no longer represented the current canonical path.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Recorded PR #4 as the preferred CLI/test/CI candidate. Earlier matrix CI passed but used a synthetic merge ref and retained no artifacts.
- 2026-07-17: Repaired PR #4 exact-head checkout/assertion and evidence retention; reconstructed tests, compilation, workflow parsing, wheel construction, and checksum verification passed. Final hosted latest-head evidence remains required.
