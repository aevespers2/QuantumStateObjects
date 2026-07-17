# Release Plan

## Current Decision

Status: `BLOCKED — PR #7 EXACT-HEAD CI PASSED; THREE PARSER/SCHEMA FINDINGS, MERGED-HEAD, RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. PR #7 is now the sole canonical bounded P0 candidate. It rebuilds the verified CLI/configuration slice from current `main`, closes PR #6's earlier hash-pin, repository/path, and canonical-name findings, and preserves fail-closed Atlas behavior.

Workflow run `29614395650` checked out and asserted exact submitted head `80e0546a53c139b26e956bce8f20c41e907739a6`. Python 3.11 and 3.13 jobs passed installation, compilation, all 15 unit/smoke tests, installed default and configuration `qso-run` smoke, wheel construction, SHA-256 generation, and retained-artifact upload. Retained artifact digests are `cdfd6817c3d0e0c07b41613072443c4fdd5aa0952ea68e4969ccee362ed7470a` and `221cfa42111ed0a6ac42c0311934d812f437f9eeeaa80d3f5cb574d155cde7ed`; wheel SHA-256 values are `99fa4f424f4c1ca12ece6d0971e887708e7083275934904d264ace80ecac1790` and `7afba2f01fc3d9481989ea68302b79a8e671c7121572899c374e6c8f6a606dfd`.

PR #7 remains unaccepted because three current P2 review threads identify parser/schema-enforcement defects: raw bytes can allow UTF-16/UTF-32 configuration or genome JSON despite the declared strict UTF-8 contract; manifests missing schema-required identity/development/review/status blocks can be accepted by the CLI and fail later during instantiation; and JSON booleans can pass equality checks for numeric schema version `1`. These findings require repair at a new immutable head, negative fixtures, re-review, and exact-head re-verification.

Atlas correctly fails closed while its QSO-GENOMES reference lacks an accepted SHA-256. QSO-GENOMES PR #2 remains unaccepted and non-mergeable with unresolved correctness, provenance, workflow, and contract-review findings. QSO-SEEKER has not published an accepted canonical-record contract. Message/ledger/attribution behavior, deterministic runtime hashes, resource limits, interruption, freeze, recovery, rollback, and public privacy/confidentiality/license/attribution approval remain incomplete.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.
- Experimenter object-model work requires a separately approved later scope/version after the runnable baseline and upstream contracts are accepted.

## Release Scope

- Working package/CLI with validated strict-UTF-8 local configuration loading.
- Schema-parity enforcement for all required runtime identity/development/review/status fields and integer-only schema versions.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke/adversarial tests and CI with exact-head assertion, invalid-configuration and mismatched-hash negative paths, and retained evidence.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Superseded PR #2, PR #4, PR #5, and PR #6 branches.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #7 is selected as the sole canonical P0 candidate. It includes deterministic default JSON, `--pretty`, `--version`, `--config`, optional explicit `--genome-root`, data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, 15 tests, constrained package discovery, exact-head two-version CI, retained artifacts, canonical QSO source/path/name checks, schema support for the optional genome hash pin, and Atlas fail-closed behavior when no accepted genome hash exists.

The candidate remains in review until strict UTF-8 decoding, complete schema-required manifest enforcement, and integer-only schema-version checks are repaired; the final PR head passes exact-head CI and retained-artifact inspection; all material review threads are resolved; and a merged-head clean build/install and smoke verification succeeds. PR #3 remains deferred and outside the first release.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local configuration loader, runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, strict UTF-8 parsing, fail-closed schemas/hashes, canonical repository/path/name enforcement, integer schema versions, inert proposals, input isolation, credential/network/repository-write boundaries, exact-head workflow controls, and privacy review.
- `Fixed`: accepted missing CLI remediation, package discovery, schema/hash-pin agreement, full schema parity, local configuration contract enforcement, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work and superseded branches from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | PR #7 is the sole selected path; resolve its three current P2 correctness threads and verify the final immutable head. |
| Runnable package/CLI | PARTIAL | Exact-head run `29614395650` passed on Python 3.11/3.13 with retained artifacts; repaired final-head and merged-head clean build/install and smoke remain required. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Fifteen CLI/configuration tests passed exact-head matrix CI; strict-UTF-8, missing-required-block, boolean-version, full runtime, resource-limit, freeze/rollback, repeated seeded canonical-hash, and adversarial fixtures remain. |
| Local configuration/runtime | REVIEW | Earlier hash-pin/source/name findings are fixed, but strict UTF-8, complete schema parity, integer-only versions, message/ledger/attribution behavior, and deterministic local runtime remain unaccepted. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | PASS | PR #3 remains draft and excluded; superseded branches are closed; no future capability enters P0 without a separate approval and evidence cycle. |
| Security | PARTIAL | CI uses read-only permissions, exact-head checkout, no persisted credentials, and inert local data; complete parser, contract, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture/policy documents and candidate CLI/configuration behavior exist; verified operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | PR/head/run/job/artifact identities and wheel hashes are recorded; repaired final-head review disposition, merged-head evidence, source archive/sdist, SBOM, attestations, complete inputs/tools, and rollback evidence remain absent. |
| Deployment readiness | BLOCKED | `deploy.md` gates environment, permissions, artifacts, configuration, health, observability, rollback, and post-validation; none are approved. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive from the accepted immutable head.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head and merged-head clean-checkout build, CLI smoke, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Strict-UTF-8, missing-required-block, boolean-schema-version, invalid-configuration, mismatched-hash, wrong-repository/path, non-canonical-name, interruption, rollback, and generated-content-inertness fixtures.
- Retained CI evidence with checked-out SHA, Python/tool versions, command results, artifact hashes, and expiry policy.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Deployment Readiness

No deployment is authorized. The first permitted target is a disposable local or CI verification environment using no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, and no sensitive data. Health, observability, rollback, and post-deployment checks are defined in `deploy.md` and remain blocked until the release gates pass.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, candidate identity becomes ambiguous, non-UTF-8 JSON is accepted, required schema fields are bypassed, booleans pass as numeric schema versions, repository/path/name/hash checks can be bypassed, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, scaffold material is mistaken for implemented capability, or artifact hashes differ. Revert the unaccepted changes, restore the last reviewed state, preserve failed-candidate inputs/reports/hashes, and rerun clean installation, CLI/configuration smoke, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- PR #7 has three unresolved P2 review threads: strict UTF-8 decoding for configuration and genome files, complete enforcement of schema-required instance blocks, and integer-only schema versions.
- The final repaired PR #7 head and any merged head require exact-head/merged-head CI, artifact retention, and review disposition.
- Complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-GENOMES PR #2 remains non-mergeable with unresolved correctness and provenance findings, and QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted source archive/sdist checksum set, SBOM, complete security review, privacy/license approval, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-16: Aligned the candidate with the runnable local-package priority; release remained blocked by the missing CLI/tests, upstream contracts, and publication-boundary approval.
- 2026-07-17: Recorded PR #2 as bounded CLI remediation, then closed it as superseded when it no longer represented the current canonical path.
- 2026-07-17: Classified draft PR #3 as a deferred Experimenter object-model roadmap proposal outside the first runnable baseline.
- 2026-07-17: Recorded PR #4 as the preferred CLI/test/CI candidate, then corrected its exact-head claim after logs proved the synthetic merge ref was tested; PR #5 was classified as a duplicate local-replay candidate.
- 2026-07-17: PR #6 became the first exact-head configuration candidate, passed 11 tests with retained artifacts, then was closed without merge after its earlier three review findings were fixed in a current-main rebuild.
- 2026-07-17: PR #7 became the sole canonical candidate. Exact-head run `29614395650` passed 15 tests and retained Python 3.11/3.13 evidence at `80e0546a53c139b26e956bce8f20c41e907739a6`; three new parser/schema-enforcement findings keep the candidate and release blocked.
