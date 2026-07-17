# Release Plan

## Current Decision

Status: `BLOCKED — CLEAN EXACT-HEAD CANDIDATE UNDER CI; LOCAL RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #6 is the clean bounded P0 candidate rebuilt from current `main`. It restores `qso_runtime.cli:main`, adds four deterministic CLI tests, constrains setuptools discovery to `qso_runtime*`, and adds least-privilege Python 3.11/3.13 CI with exact submitted-head checkout and assertion.

PR #6 retains the checked-out SHA, Python version, deterministic CLI JSON, CLI version, wheel, and SHA-256 manifest for 30 days. Independent reconstructed verification passed four tests, source/test compilation, workflow YAML parsing, wheel construction, and checksum generation; the reconstructed wheel SHA-256 was `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`. Latest-head GitHub-hosted matrix completion and artifact inspection remain required before canonical acceptance.

Earlier PR #4 passed functional matrix checks but used a synthetic merge ref and retained no artifact. PR #5 has reconstructed local evidence but no attached workflow. Neither older candidate is accepted while PR #6 is under exact-head verification. PR #2 is superseded and closed. Draft PR #3 remains deferred outside P0 and outside the first release.

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

PR #6 is selected for review as the clean P0 CLI/test/CI slice. It includes deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four focused tests, constrained package discovery, two-version CI, exact-head checkout/assertion, checksummed wheel evidence, and retained artifacts. It remains a candidate until latest-head CI passes and artifacts are inspected.

PR #4 and PR #5 are pending supersession only after PR #6 is accepted. PR #2 is superseded and closed. PR #3 is not selected for the first release.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | IN PROGRESS | PR #6 latest submitted head passes exact-head Python 3.11/3.13 CI and retained artifacts are inspected; then PR #4 and PR #5 are dispositioned. |
| Runnable package/CLI | PARTIAL | Independent reconstructed install/test/build evidence passes; GitHub-hosted exact-head clean build/install and `qso-run` smoke must pass at the accepted PR head and later merged head. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Four deterministic CLI tests pass in reconstructed verification; full runtime tests, invalid configuration fixtures, repeated seeded canonical hashes, and retained final-head reports remain. |
| Local configuration/runtime | FAIL | Instance loading, validation, message/ledger/attribution behavior, resource limits, and deterministic local fixtures are independently verified. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | REVIEW | PR #3 remains excluded; duplicate candidates do not silently replace the canonical path; no future capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI uses read-only permissions and no persisted checkout credentials; complete parser, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture/policy documents and candidate CLI output exist; verified configuration, operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR #6 records exact-head controls and retained artifact contents; final hosted logs/artifacts, complete inputs/tools, SBOM, attestations, and rollback evidence remain pending. |
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

- Latest-head GitHub-hosted CI and retained artifact inspection remain pending for PR #6.
- PR #4 and PR #5 must be explicitly dispositioned after PR #6 acceptance.
- Local configuration loading, complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted SBOM, complete security/privacy review, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation, then closed it as superseded when it no longer represented the current canonical path.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Recorded PR #4 functional matrix evidence but rejected it as exact-head acceptance because checkout used a synthetic merge ref and retained no artifact.
- 2026-07-17: Recorded PR #5 as a duplicate local-replay candidate without attached CI.
- 2026-07-17: Opened clean PR #6 from current `main` with the bounded CLI/tests/package repair and exact-head retained-evidence workflow; reconstructed verification passed while final hosted matrix evidence remains pending.
