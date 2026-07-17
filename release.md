# Release Plan

## Current Decision

Status: `BLOCKED — CONFIGURATION CONTRACT HARDENING UNDER EXACT-HEAD CI; RUNTIME, UPSTREAM CONTRACTS, AND PUBLICATION BOUNDARIES REQUIRED`

QuantumStateObjects has an accepted canonical CLI/package baseline on PR #6. Exact-head workflow run `29607170551` passed Python 3.11 and 3.13 at `9389d5322f535f59bd5db386dffe7ca2c9b052cf`, including checkout assertion, installation, compilation, four deterministic tests, installed `qso-run`, version output, wheel construction, SHA-256 generation, and retained evidence. PR #4 and PR #5 were closed as superseded while preserving their histories.

The initial local-configuration slice passed exact-head workflow run `29610600428` on Python 3.11 and 3.13 at `6e382853e6746f8eb18e97c64481dccfe6684652`. `qso_runtime/config.py` loads bounded local JSON, validates the Atlas/Nova/Orion/Lyra set, unique identities, supported schema versions, normalized relative JSON paths, optional lowercase SHA-256 pins, non-symlink regular files, and file-size limits. `qso-run --config` exposes validation without resolving or executing upstream material. `--genome-root` permits only explicit local, hash-pinned genome JSON files beneath the chosen directory.

The current hardening slice closes three review findings before runtime work proceeds: it requires exact canonical QSO name casing, restricts genome references to `aevespers2/QSO-GENOMES`, enforces each QSO's canonical `genomes/<name>.json` path, and updates the published instance schema to permit the optional SHA-256 field required by resolution. Four new regression tests raise the reconstructed total to 15 passing tests; final hosted exact-head CI and retained-artifact inspection remain pending.

The current Atlas declaration still points to `genomes/atlas.json` without an accepted SHA-256. The resolver rejects that reference before file execution, network access, or cross-repository import. Broader runtime/ledger/resource/freeze/rollback fixtures remain incomplete. QSO-GENOMES has not yet supplied accepted hash-pinned genome contracts, QSO-SEEKER has not supplied an accepted canonical-record contract, and public privacy/confidentiality/license/attribution approval is absent.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate should be `0.1.0-alpha.1` until runnable, contract, test, and publication gates pass.
- Instance, message, ledger, attribution, freeze/rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible changes require migrations and coordinated upstream contract versions.
- Experimenter object-model work requires a separately approved later scope/version after the runnable baseline and upstream contracts are accepted.

## Release Scope

- Working package/CLI with validated local configuration loading.
- Local runtime, instance, message, ledger, attribution, resource-limit, freeze, rollback, and deterministic evidence baseline.
- Real unit/smoke tests and CI with exact-head assertion, malformed/missing/duplicate/mismatched-contract negative paths, and retained evidence.
- Later version/hash validation of QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible package/source artifacts, security checks, documentation, SBOM where applicable, checksums, provenance, and rollback.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Duplicate CLI branches after the canonical path was accepted.
- Materialized placeholder trees presented as implemented capability.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, or production orchestration.

## Selected Candidate Work

PR #6 remains the canonical branch. The accepted baseline includes deterministic JSON self-check output, `--pretty`, `--version`, explicit data-only/no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, constrained package discovery, exact-head two-version CI, and retained checksummed artifacts.

The active extension includes:

- bounded UTF-8 JSON configuration loading;
- duplicate identity and exact canonical QSO-set validation;
- normalized relative genome paths with traversal rejection;
- exact `aevespers2/QSO-GENOMES` repository enforcement;
- canonical per-QSO genome path enforcement;
- optional reference SHA-256 validation aligned with the published schema;
- explicit local-only hash-pinned genome resolution;
- Atlas fail-closed behavior while its accepted genome hash is absent;
- CLI configuration evidence; and
- eleven focused local-configuration tests, for 15 total unit/smoke tests.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | PASS | PR #6 baseline passed exact-head Python 3.11/3.13 CI with retained artifacts; duplicate CLI candidates were superseded. |
| Runnable package/CLI | PASS FOR CONFIGURATION HEAD | Exact-head clean install/build, default `qso-run`, and configuration CLI passed at `6e382853e6746f8eb18e97c64481dccfe6684652`; the hardening head must now pass. |
| Task completion | FAIL | P0-B must be `DONE`; included later tasks must have linked evidence. |
| Tests/determinism | PARTIAL | Initial configuration head passed 11 hosted tests; contract hardening passes 15 reconstructed tests, while exact-head hosted evidence and full runtime deterministic hashes remain. |
| Local configuration/runtime | PARTIAL | Canonical instance/repository/path validation and Atlas fail-closed handling are implemented; message/ledger/attribution behavior, resource limits, and runtime fixtures remain. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, interruption, recovery, and rollback preserve evidence. |
| Upstream contracts | BLOCKED | QSO-GENOMES manifest including Atlas and QSO-SEEKER canonical-record fixtures are accepted, published, and hash-verifiable. |
| Scope integrity | PASS FOR CURRENT SLICE | No generated snippets, credentials, network authority, upstream imports, external repository writes, or future Experimenter capability entered the slice. |
| Security | PARTIAL | Loader rejects symbolic links, traversal, oversized files, malformed JSON, duplicate identities, noncanonical names, unaccepted repositories, path mismatches, unsupported schemas, absent pins during resolution, and mismatched hashes; complete dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Planning and CLI behavior are documented; verified operations, runtime limits, freeze/rollback, and recovery remain incomplete. |
| Privacy/licensing | BLOCKED | Approve the public license/notice model and handling of personal/confidential identifiers before artifact publication. |
| Provenance | PARTIAL | Baseline and initial configuration hosted artifacts and hashes are retained; final hardening-head logs/artifacts, SBOM, attestation, and rollback evidence remain pending. |
| Deployment readiness | BLOCKED | No deployment is authorized before all release gates pass. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Reproducible sdist, wheel, and source archive from the accepted immutable head.
- Versioned schemas, instance manifests, and later fixed upstream fixtures/manifests.
- Exact-head and merged-head clean-checkout build, CLI smoke, configuration validation, unit, deterministic-run, resource-limit, freeze/rollback, security, and documentation reports.
- Append-only sample event/attribution evidence containing no unapproved sensitive data.
- Malformed, missing, duplicate, traversal, repository, path, name-casing, mismatched-hash, interruption, rollback, and generated-content-inertness fixtures.
- Retained CI evidence with checked-out SHA, Python/tool versions, command results, artifact hashes, and expiry policy.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, review disposition, and rollback instructions.

## Deployment Readiness

No deployment is authorized. The first permitted target remains a disposable local or CI verification environment using no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, and no sensitive data.

## Rollback Criteria

Rollback if the entry point fails, CI verifies a different head, local configuration accepts malformed or ambiguous identities, noncanonical names, unaccepted repositories, mismatched per-QSO paths, path traversal or symbolic links, unpinned or mismatched genomes, required upstream artifacts disappear, generated material executes, credentials or network access are introduced, limits fail, freeze/rollback loses evidence, deterministic runs diverge, attribution is inconsistent, privacy/license approval is absent, or artifact hashes differ. Revert the unaccepted changes, restore the last reviewed state, preserve failed inputs/reports/hashes, and rerun clean installation, CLI smoke, configuration, deterministic, freeze/rollback, and security checks.

## Unresolved Blockers

- GitHub-hosted exact-head CI and retained artifact inspection are pending for the configuration contract-hardening head.
- The current Atlas genome reference has no accepted SHA-256 and therefore intentionally fails closed during resolution.
- Local message, ledger, attribution, resource-limit, deterministic runtime, freeze, interruption, recovery, and rollback evidence remain incomplete.
- QSO-GENOMES and QSO-SEEKER contracts remain unpublished or unaccepted for runtime consumption.
- PR #3 remains an unaccepted draft scaffold outside P0.
- No accepted SBOM, complete security/privacy review, provenance attestation, or rollback bundle exists.
- Approval is required for the public privacy/confidentiality/license/attribution notice model.

## Release Log

- 2026-07-17: Accepted PR #6's canonical CLI baseline after exact-head Python 3.11/3.13 CI and retained artifacts passed at `9389d5322f535f59bd5db386dffe7ca2c9b052cf`; closed PR #4 and PR #5 as superseded.
- 2026-07-17: Accepted the initial local configuration candidate after exact-head run `29610600428` passed 11 tests on Python 3.11 and 3.13 at `6e382853e6746f8eb18e97c64481dccfe6684652`.
- 2026-07-17: Hardened the local contract against noncanonical QSO casing, unaccepted genome repositories, and per-QSO path mismatches; aligned the instance schema with optional SHA-256 pins; and added four regression tests. Reconstructed verification passed 15 tests and compilation without generated-code execution, credentials, network access, or external repository writes.
