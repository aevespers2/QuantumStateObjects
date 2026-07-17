# Release Plan

## Current Decision

Status: `BLOCKED — PR #6 EXACT-HEAD CI PASSED; CONFIGURATION CORRECTNESS, MERGED-HEAD, RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #6 is now the single canonical bounded P0 candidate. It supersedes the closed, unmerged PR #4 and PR #5 CLI branches while preserving their evidence, restores `qso_runtime.cli:main`, adds deterministic CLI behavior, constrains setuptools discovery to `qso_runtime*`, and advances into fail-closed local configuration validation.

Workflow run `29610600428` checked out and asserted exact submitted head `6e382853e6746f8eb18e97c64481dccfe6684652`. Python 3.11 and 3.13 jobs passed installation, compilation, all 11 unit/smoke tests, installed `qso-run` smoke and boundary validation, version output, wheel construction, SHA-256 generation, and retained-artifact upload. The retained artifact digests are `505be6dae69827c150c72161ed348a752cf623a9589b29045c70000ff7aa2422` for Python 3.11 and `f44653928b2974f10f76822aebdac89fd31cdedf485f3ee9b5758be2766ae5f1` for Python 3.13; wheel SHA-256 values are `9c1a1fe0209864d1e614d491da881f004792fac288b14a98596e021de2abf7f2` and `be85a103430e911974c28073a2e3bb283c7fdc9d30812b5b8ef9f0fd49e5a225`.

PR #6 remains unaccepted because three current P2 review threads identify configuration-contract defects: the published instance schema does not permit the new required `genome.sha256` field; the resolver can accept hash-matching genome references outside the declared `aevespers2/QSO-GENOMES` repository/path contract; and case-folded name comparison accepts non-canonical lowercase QSO names. These findings must be repaired at a new immutable head, re-reviewed, and reverified before merge or release consideration.

Atlas correctly fails closed while its QSO-GENOMES reference lacks an accepted SHA-256, but upstream QSO-GENOMES PR #2 remains unaccepted with unresolved correctness, provenance, workflow, and contract-review findings. QSO-SEEKER has not published an accepted canonical-record contract. Message/ledger/attribution behavior, deterministic runtime hashes, resource limits, interruption, freeze, recovery, rollback, and public privacy/confidentiality/license/attribution approval remain incomplete.

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
- Superseded CLI branches PR #2, PR #4, and PR #5.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #6 is selected as the sole canonical P0 candidate. It includes deterministic default JSON, `--pretty`, `--version`, `--config`, optional explicit `--genome-root`, data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four CLI tests, seven configuration tests, constrained package discovery, exact-head two-version CI, retained artifacts, and Atlas fail-closed behavior when no accepted genome hash exists.

The candidate remains in review until the schema/hash-pin mismatch, repository/path contract bypass, and canonical-name-casing findings are repaired; the final PR head passes exact-head CI and retained-artifact inspection; all material review threads are resolved; and a merged-head clean build/install and smoke verification succeeds. PR #3 remains deferred and outside the first release.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local configuration loader, runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, canonical repository/path/name enforcement, inert proposals, input isolation, credential/network/repository-write boundaries, exact-head workflow controls, and privacy review.
- `Fixed`: accepted missing CLI remediation, package discovery, schema/hash-pin agreement, local configuration contract enforcement, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work and superseded CLI paths from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | PR #6 is the sole selected path; resolve its three current correctness threads and verify the final immutable head. |
| Runnable package/CLI | PARTIAL | Exact-head run `29610600428` passed on Python 3.11/3.13 with retained artifacts; merged-head clean build/install and smoke remain required. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Eleven CLI/configuration tests passed exact-head matrix CI; full runtime, resource-limit, freeze/rollback, repeated seeded canonical-hash, and adversarial fixtures remain. |
| Local configuration/runtime | REVIEW | Loader and negative fixtures exist, but schema/hash-pin agreement, fixed repository/path contract, canonical case-sensitive QSO names, message/ledger/attribution behavior, and deterministic local runtime remain unaccepted. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | PASS | PR #3 remains draft and excluded; superseded CLI branches are closed; no future capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI uses read-only permissions, exact-head checkout, no persisted credentials, and inert local data; complete parser, contract, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture/policy documents and candidate CLI/configuration behavior exist; verified operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR/head/run/job/artifact identities and wheel hashes are recorded; final-head review disposition, merged-head evidence, source archive/sdist, SBOM, attestations, complete inputs/tools, and rollback evidence remain absent. |
| Deployment readiness | BLOCKED | `deploy.md` gates environment, permissions, artifacts, configuration, health, observability, rollback, and post-validation; none are approved. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive from the accepted immutable head.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head and merged-head clean-checkout build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Invalid-configuration, mismatched-hash, wrong-repository/path, non-canonical-name, interruption, rollback, and generated-content-inertness fixtures.
- Retained CI evidence with checked-out SHA, Python/tool versions, command results, artifact hashes, and expiry policy.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Deployment Readiness

No deployment is authorized. The first permitted target is a disposable local or CI verification environment using no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, and no sensitive data. Health, observability, rollback, and post-deployment checks are defined in `deploy.md` and remain blocked until the release gates pass.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, candidate identity becomes ambiguous, the schema and loader disagree, repository/path/name/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI/configuration smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- PR #6 has three unresolved P2 review threads: schema omission of `genome.sha256`, acceptance of references outside the declared QSO-GENOMES repository/path contract, and acceptance of non-canonical QSO name casing.
- The final repaired PR #6 head and any merged head require exact-head/merged-head CI, artifact retention, and review disposition.
- Complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-GENOMES PR #2 retains unresolved P1/P2 correctness and provenance findings, and QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted source archive/sdist checksum set, SBOM, complete security review, privacy/license approval, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation, then closed it as superseded when it no longer represented the current canonical path.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Recorded PR #4 as the preferred CLI/test/CI candidate, then corrected its exact-head claim after logs proved the synthetic merge ref was tested; PR #5 was classified as a duplicate local-replay candidate.
- 2026-07-17: PR #6 superseded PR #4 and PR #5 as the sole exact-head candidate. Run `29610600428` passed 11 tests and retained Python 3.11/3.13 artifacts at head `6e382853e6746f8eb18e97c64481dccfe6684652`. Three unresolved configuration-contract review findings keep the candidate and release blocked.