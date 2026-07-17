# Release Plan

## Current Decision

Status: `BLOCKED — PR #7 EXACT-HEAD RUNTIME SLICE PASSED; EIGHT P2 FINDINGS, MERGED-HEAD, UPSTREAM CONTRACTS, AND PUBLICATION GATES REQUIRED`

QuantumStateObjects contains package metadata at version `0.1.0`, a working candidate CLI/configuration loader, declarative QSO manifests, runtime primitives, event and attribution ledgers, and freeze/rollback controls. No runtime release is eligible. PR #7 remains the sole canonical P0 candidate and is open, unmerged, mergeable, and reconciled with current `main` at normal two-parent head `395915b60510e9a62c53ad128cf23d151e73eb1f` without force-rewriting reviewed history.

Workflow run `29617877793` completed successfully on Python 3.11 and 3.13. Both jobs checked out and asserted the exact submitted head, installed and compiled the package/tests, passed 22 unit and smoke tests with JUnit evidence, ran installed default and configuration CLI smoke, built wheels, generated SHA-256 values, and uploaded retained artifacts. Artifact digests are `c53ecc7692716519be67c92e4e51cc04695187437790c784d8b42f78d70a76fd` and `cf2290f7469b71ebb92cc7b1cb7eb86a64ee9ff56df8b89203fa157bd6b65816`; wheel SHA-256 values are `97c6ec287e2eb1b23776dc232a16641f566202f1aacf792755a992930adf5dc3` and `b074c2328f90585c2fe8fb7a83d023ef34ea7374b6ee9915c57209d589e678cc`.

The bounded runtime-primitives slice now exercises active/frozen/interrupted lifecycle states, message validation, hash-linked event and attribution ledgers, resource-limit prechecks, freeze/resume, interruption/recovery, rollback/checkpoint restoration, and repeatable state/event hashes using synthetic local fixtures. This is candidate test evidence, not evidence that Atlas, Nova, Orion, or Lyra are actively running.

PR #7 remains unaccepted because eight current P2 review threads identify fail-closed defects: non-UTF-8 JSON can bypass the declared contract; manifests missing required identity/development/review/status blocks can be accepted; Booleans can pass as numeric schema versions; invalid instance IDs can bypass the schema pattern; delegated ingest exceptions can leave unledgered partial state; freeze certificates can diverge from controller checkpoints and drop messages; rollback can fail when the event limit is full; and persisted event ledgers can accept malformed entry shapes or Boolean sequences. All require repair, negative fixtures, review disposition, and exact-head reverification.

Atlas continues to fail closed while its QSO-GENOMES reference lacks an accepted SHA-256. QSO-GENOMES PR #2 remains unaccepted and non-mergeable. QSO-SEEKER has no accepted canonical-record/attribution contract. Privacy, confidentiality, licensing, attribution, source artifact, SBOM/provenance, merged-head, rollback-drill, and approval gates remain incomplete.

## Versioning

- Scheme: Semantic Versioning.
- Existing metadata is `0.1.0`; the first eligible candidate remains `0.1.0-alpha.1` until runnable, contract, test, security, provenance, and publication gates pass.
- Instance, message, event-ledger, attribution-ledger, checkpoint, freeze/rollback, evidence, configuration, and upstream-contract versions must be explicit.
- Incompatible schema, canonicalization, state-hash, or rollback changes require migrations and coordinated consumer fixtures.
- Experimenter object-model work requires a separate later scope/version after the runnable baseline is accepted.

## Release Scope

- Working package and CLI with strict-UTF-8, schema-parity, integer-only, canonical-ID/name/repository/path/hash local configuration validation.
- Atomic instance lifecycle and mutation behavior; validated message, event, attribution, limit, freeze, interruption, recovery, rollback, checkpoint, and deterministic-hash primitives.
- Positive, negative, adversarial, and repeated deterministic tests with exact-head and merged-head identity assertions and retained evidence.
- Later hash-fixed validation of accepted QSO-GENOMES and QSO-SEEKER artifacts without importing or executing external code.
- Approved privacy, confidentiality, licensing, attribution, and public-artifact boundaries.
- Reproducible source archive, sdist, wheel, reports, SBOM where applicable, checksums, provenance, rollback bundle, and approval.

### Explicitly excluded from the first candidate

- Draft PR #3 Experimenter object-model scaffold and materializer.
- Superseded PR #2, PR #4, PR #5, and PR #6 branches.
- Materialized placeholder trees presented as implemented capability.
- Atlas/Nova/Orion/Lyra execution claims without authorized append-only runtime evidence.
- Autonomous learning, generated-code execution, network access, credentials, repository mutation, payment authority, scheduled execution, or production orchestration.

## Selected Candidate Work

PR #7 is the sole canonical P0 candidate. Its current head includes the CLI/configuration baseline plus the bounded runtime-primitives test slice and exact-head Python 3.11/3.13 retained evidence. It remains in review until all eight findings are repaired, all material threads are resolved, a new immutable head passes the complete suite, and an explicitly authorized merged head passes clean installation, tests, artifacts, security, provenance, and rollback verification.

## Planned Changelog Entries

- `Added`: accepted CLI/configuration loader, runtime controller, message validation, event/attribution ledgers, checkpoints, tests/CI, deterministic evidence formats, and later upstream contract validators.
- `Security`: strict UTF-8, complete schema parity, canonical IDs/sources/hashes, atomic mutation failures, rollback capacity, checkpoint parity, strict persisted-ledger validation, inert proposals, least privilege, and credential/network/repository-write denial.
- `Fixed`: CLI/package discovery, schema/hash-pin agreement, configuration contract enforcement, resource-limit/freeze/rollback/ordering/attribution defects, and accepted Atlas reference behavior.
- `Documentation`: installation, CLI, supported Python versions, trust boundaries, evidence semantics, limitations, privacy/license model, operations, and recovery.
- `Release`: source/sdist/wheel artifacts, reports, SBOM, checksums, provenance, review disposition, rollback evidence, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical candidate | REVIEW | PR #7 is sole selected path, mergeable and current-main reconciled; repair and resolve all eight P2 findings at one final immutable head. |
| Runnable package/CLI | PARTIAL | Run `29617877793` passed exact-head Python 3.11/3.13 installation and smoke with retained artifacts; repaired final-head and merged-head acceptance remain. |
| Runtime primitives | REVIEW | Twenty-two tests cover the bounded slice, but atomic ingest, checkpoint parity, rollback capacity, strict event shape, and complete configuration fail-closed behavior remain unaccepted. |
| Tests/determinism | PARTIAL | Repeatability evidence exists for synthetic fixtures; complete negative/adversarial matrix and accepted-head deterministic reports remain required. |
| Freeze/rollback | PARTIAL | Basic paths are tested; canonical message-inclusive checkpoints and rollback at event capacity must pass. |
| Upstream contracts | BLOCKED | Accepted QSO-GENOMES manifest/hash set and QSO-SEEKER canonical-record/attribution fixtures are required. |
| Scope integrity | PASS | Draft Experimenter work and superseded branches remain excluded; no four-QSO execution claim is made. |
| Security | PARTIAL | Exact-head/read-only/no-persisted-credentials candidate CI exists; complete parser, state-atomicity, persisted-evidence, dependency, secret, workflow, and adversarial review remains. |
| Documentation | PARTIAL | Architecture and candidate behavior are documented; accepted operations, limitations, evidence contracts, and recovery remain incomplete. |
| Privacy/licensing | BLOCKED | Public notice/license and handling of personal/confidential identifiers require approval. |
| Provenance | PARTIAL | PR/head/run/job/artifact/wheel identities are recorded; source/sdist, SBOM, attestation, merged-head, review disposition, and rollback bundle remain absent. |
| Deployment readiness | BLOCKED | `deploy.md` defines the fail-closed target, health, observability, rollback, and post-validation controls; no target is approved. |
| Approval | PENDING | Explicit merge/release approval only after every blocking gate passes. |

## Artifact Requirements

- Reproducible source archive, sdist, and wheel from the accepted immutable and merged heads.
- Versioned schemas, configurations, manifests, event/attribution ledgers, checkpoint/freeze/rollback records, and later fixed upstream fixtures.
- Exact-head and merged-head clean-checkout build, CLI smoke, unit, deterministic, resource-limit, interruption, recovery, freeze/rollback, security, and documentation reports.
- Strict-UTF-8, missing-required-block, Boolean-version, invalid-instance-ID, delegated-ingest-failure, full-event-capacity rollback, message-inclusive-freeze, malformed-ledger, mismatched-hash, wrong-source/path/name, and generated-content-inertness fixtures.
- Retained CI evidence with checked-out SHA, tool versions, commands/results, JUnit, artifact hashes, and expiry.
- SBOM where applicable, checksums, provenance manifest/attestation, review disposition, and tested rollback instructions.

## Deployment Readiness

No deployment is authorized. The first permitted target remains a disposable local or CI verification environment with no credentials, no network-dependent inputs, no external repository writes, no generated-code execution, no sensitive data, bounded resources, explicit human controls, and hash-bound evidence. A successful test run does not authorize package publication, persistent hosting, scheduling, external integration, or a four-QSO experiment.

## Health Checks, Observability, Rollback, and Post-Validation

Health requires exact source/configuration identity, successful startup/shutdown, strict fail-closed input handling, valid canonical ledger/checkpoint heads, deterministic replay, resource compliance, and absence of network, credential, external-write, generated-execution, payment, or sensitive-data activity. Observability must record structured non-secret source/configuration identities, lifecycle transitions, rejections, limits, event/attribution/checkpoint heads, rollback triggers/results, artifact hashes, cleanup, and post-validation. Roll back on any identity/hash/schema/type/atomicity/ledger/checkpoint/determinism/limit/security/privacy failure; preserve failed evidence, restore the last accepted checkpoint or clean disposable state, verify no external mutation, and do not resume without a new accepted head. Post-validation must repeat smoke and deterministic replay, verify final ledger/checkpoint hashes and cleanup, compare resource use with bounds, archive evidence, and return the environment to a known clean state.

## Unresolved Blockers

- Eight unresolved PR #7 P2 findings: strict UTF-8; complete required blocks; integer-only versions; instance-ID pattern; atomic delegated ingest; canonical message-inclusive freeze checkpoint; rollback under a full event ceiling; strict persisted event-entry shape/type validation.
- Final repaired exact head and any merged head require complete retained evidence and review disposition.
- Accepted upstream QSO-GENOMES and QSO-SEEKER contracts remain absent.
- Source/sdist checksum set, SBOM, complete security review, public notice/license approval, provenance attestation, rollback drill, and approval remain absent.

## Release Log

- 2026-07-16 — Aligned the repository with the runnable local-package priority.
- 2026-07-17 — Consolidated superseded CLI candidates into PR #7 and recorded exact-head configuration evidence.
- 2026-07-17 — Reconciled PR #7 with current `main` at head `395915b60510e9a62c53ad128cf23d151e73eb1f`; run `29617877793` passed 22 tests on Python 3.11/3.13 and retained artifacts.
- 2026-07-17 — Advanced the bounded runtime-primitives slice to review, then recorded five new runtime/evidence findings in addition to the three existing configuration findings. Release and deployment remain blocked.
