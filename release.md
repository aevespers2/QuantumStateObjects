# Release Plan

## Current Decision

Status: `BLOCKED — PR #7 CURRENT-MAIN CONFIGURATION REPAIR REQUIRES EXACT-HEAD CI; RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REMAIN`

QuantumStateObjects contains runtime modules, schemas, four instance declarations, attribution/ledger primitives, and package metadata at version `0.1.0`, but no runtime release is eligible. Earlier PR #6 established a useful exact-head CLI/configuration baseline in workflow run `29610600428`, then diverged five planning commits behind `main` and could no longer provide a current mergeable verification head. PR #7 rebuilds that candidate from current `main` commit `dd455b52beb0c257d2f11abc994da6b94085c2c3`.

PR #7 restores `qso_runtime.cli:main`, bounded local configuration loading, deterministic CLI behavior, constrained setuptools discovery, and least-privilege Python 3.11/3.13 exact-head CI. It also closes all three configuration-contract defects identified on PR #6: the published schema now permits the optional lowercase `genome.sha256` field required by resolution; the loader accepts only `aevespers2/QSO-GENOMES` and each QSO's exact canonical `genomes/<name>.json` path; and primary names must exactly match case-sensitive Atlas, Nova, Orion, and Lyra.

Reconstructed verification passed source/test compilation, all 15 unit/smoke tests, and `python -m qso_runtime.cli --config config/instances.json`. The run executed no generated snippets, accessed no credentials, consumed no network inputs, and made no external-repository writes. PR #7 still requires hosted exact-head CI, retained-artifact inspection, review disposition, and mergeability confirmation before PR #6 can be closed as superseded or the runtime inventory can proceed.

Atlas correctly fails closed while its QSO-GENOMES reference lacks an accepted SHA-256. QSO-GENOMES PR #2 remains unaccepted, QSO-SEEKER has not published an accepted canonical-record contract, and message/ledger/attribution behavior, deterministic runtime hashes, resource limits, interruption, freeze, recovery, rollback, and public privacy/confidentiality/license/attribution approval remain incomplete.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.
- Experimenter object-model work requires a separately approved later scope/version after the runnable baseline and upstream contracts are accepted.

## Release Scope

- Working package/CLI with validated local configuration loading.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke tests and CI with exact-head assertion, invalid-configuration and mismatched-contract negative paths, and retained evidence.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Superseded CLI branches PR #2, PR #4, and PR #5.
- PR #6 after PR #7 independently passes and preserves its prior evidence.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #7 is the current P0 candidate. It includes deterministic default JSON, `--pretty`, `--version`, `--config`, optional explicit `--genome-root`, data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, four CLI tests, eleven configuration tests, constrained package discovery, exact-head two-version CI, configuration CLI evidence, and Atlas fail-closed behavior when no accepted genome hash exists.

The candidate remains in review until its final head passes exact-head CI and retained-artifact inspection, review confirms the three PR #6 defects remain closed, the diff remains mergeable against current `main`, and a merged-head clean build/install and smoke verification succeeds. PR #3 remains deferred and outside the first release.

## Planned Changelog Entries

- `Added`: accepted working CLI, verified local configuration loader, runtime baseline, tests/CI, deterministic evidence formats, and later contract validators.
- `Security`: resource caps, fail-closed schemas/hashes, canonical repository/path/name enforcement, inert proposals, input isolation, credential/network/repository-write boundaries, exact-head workflow controls, and privacy review.
- `Fixed`: missing CLI remediation, package discovery, schema/hash-pin agreement, local configuration contract enforcement, Atlas reference, and any message/ledger/freeze/rollback/ordering/attribution defects.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, commands, privacy/license model, limitations, and recovery.
- `Release`: sdist/wheel/source artifacts, reports, SBOM, checksums, provenance, and approval.
- `Excluded`: unaccepted Experimenter scaffold/materialization work and superseded CLI paths from the first runnable baseline.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | PR #7 is based on current `main`; require exact-head CI, review, mergeability, and preserved disposition of PR #6. |
| Runnable package/CLI | PARTIAL | Reconstructed build/import and default/configuration CLI behavior pass; hosted exact-head and merged-head clean build/install remain required. |
| Task completion | FAIL | P0-A and P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Fifteen CLI/configuration tests pass reconstructed verification; hosted exact-head, full runtime, resource-limit, freeze/rollback, repeated seeded canonical-hash, and adversarial fixtures remain. |
| Local configuration/runtime | REVIEW | Schema/hash-pin, repository/path, and canonical-name rules are repaired; hosted acceptance plus message/ledger/attribution behavior and deterministic local runtime remain. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | PASS | PR #3 remains draft and excluded; generated snippets, credentials, network inputs, and external repository writes remain outside the candidate. |
| Security | PARTIAL | CI is least privilege and the loader rejects symbolic links, traversal, oversized files, malformed JSON, duplicate identities, noncanonical names, unaccepted repositories, path mismatches, unsupported schemas, missing pins during resolution, and mismatched hashes; complete dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Planning and candidate behavior are documented; verified operations, limitations, and recovery are incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | Earlier PR #6 evidence is retained and PR #7's base plus local verification are recorded; final exact-head artifacts, merged-head evidence, source archive/sdist, SBOM, attestations, and rollback evidence remain absent. |
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

- PR #7 final exact-head CI, retained artifacts, review, and mergeability confirmation are pending.
- PR #6 remains open only to preserve evidence until PR #7 independently passes; its branch is five planning commits behind current `main`.
- Complete runtime tests, deterministic fixtures, resource-limit behavior, freeze/rollback, event/attribution evidence, and accepted CI remain incomplete.
- Atlas depends on an unaccepted QSO-GENOMES artifact set; QSO-GENOMES PR #2 remains unaccepted, and QSO-SEEKER's versioned canonical-record contract is unpublished or unaccepted.
- PR #3 is an unaccepted draft scaffold and must remain outside P0.
- No accepted source archive/sdist checksum set, SBOM, complete security review, privacy/license approval, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-17: PR #6 established the initial exact-head CLI/configuration baseline in run `29610600428` with 11 tests and retained Python 3.11/3.13 artifacts.
- 2026-07-17: PR #6 review identified schema/hash-pin disagreement, uncontracted repository/path acceptance, and noncanonical QSO casing.
- 2026-07-17: Created PR #7 from current `main`, ported the verified bounded runtime/configuration path, closed all three contract defects, added four regression tests for 15 total, and passed reconstructed compilation plus configuration CLI verification without generated-code execution, credentials, network access, or external-repository writes.
