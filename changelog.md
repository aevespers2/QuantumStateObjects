# Changelog

All notable product, architecture, implementation, documentation, release, and deployment changes are recorded here. Entries describe evidence at named states; they do not imply release or deployment unless stated explicitly.

## Unreleased

### Product

- 2026-07-16 — Set the immediate objective to a runnable, locally verifiable QuantumStateObjects package before cross-repository or four-QSO claims.
- 2026-07-17 — Selected PR #7 as the sole canonical CLI/configuration/runtime candidate and kept Experimenter work outside P0.
- 2026-07-17 — Advanced P0 from configuration-only evidence to one bounded runtime-primitives slice while retaining fail-closed review gates.
- 2026-07-19 — Preserved the same bounded implementation scope while adding a complete documentation and Pages-readiness foundation.

### Architecture

- The accepted dependency order remains: reconciled and accepted PR #7 runtime → accepted QSO-GENOMES contract → accepted QSO-SEEKER contract → local cross-repository validation → bounded four-QSO experiment.
- Configuration, runtime state, messages, events, attribution, checkpoints, freeze, interruption, recovery, and rollback must share explicit versioned canonicalization and integrity rules.
- Atlas, Nova, Orion, and Lyra may not be described as running without authorized append-only runtime evidence.
- 2026-07-19 — Added component, sequence, lifecycle, trust-zone, failure-boundary, and cross-repository dependency diagrams without changing runtime behavior.

### Added

- Draft PR #7 provides the candidate installable package, `qso-run` CLI, strict local configuration, genome-file resolution, runtime controller, messages, event and attribution evidence, checkpoints, freeze, interruption, recovery, rollback, and deterministic hashes.
- 2026-07-18 — Accepted `main` gained the repaired repository-wide policy validator, exact submitted-source controls, pinned workflow actions, focused regression tests, and retained evidence.
- 2026-07-19 — Added `mkdocs.yml` and a pinned documentation toolchain.
- 2026-07-19 — Added Pages-ready project overview, architecture, design contracts, developer guide, security guide, operations/recovery runbook, and release-status guide.

### Changed

- 2026-07-18 — PR #7 became stale against accepted `main` after the policy-control repair merged; it requires normal reconciliation and fresh exact-head evidence.
- 2026-07-19 — Expanded the root README with evidence-qualified status, repository responsibilities, architecture, documentation navigation, candidate verification, and contribution boundaries.
- 2026-07-19 — Updated `taskchain.md` and `release.md` to reflect the accepted policy-control base, the current PR #7 pre-reconciliation state, open candidate findings, and documentation publication gates.

### Documentation

- 2026-07-19 — Documented the distinction between accepted `main`, draft PR #7, accepted upstream contracts, proposed experiment behavior, release, and deployment.
- 2026-07-19 — Documented identity, genome, configuration, canonical record, message, proposal, event, attribution, resource, checkpoint, freeze, interruption, recovery, rollback, determinism, and compatibility contracts.
- 2026-07-19 — Added isolated developer onboarding, test matrices, exact-head evidence guidance, pull-request requirements, and architectural stop conditions.
- 2026-07-19 — Added hostile-input and prompt-injection threat modeling, least-privilege rules, security evidence requirements, and vulnerability response guidance.
- 2026-07-19 — Added local verification, health, observability, incident, cleanup, recovery, rollback, Pages publication, and release stop procedures.

### Verification

- Historical PR #7 exact-head runs remain evidence for their recorded commits only. The latest candidate description reports a successful Python 3.11/3.13 matrix with 150 tests at a prior immutable head.
- Accepted `main` policy-control repair passed its exact-head focused tests and repository-wide validator before merge.
- Documentation strict build, rendered-diagram review, link checking, accessibility review, site artifact hashing, and Pages deployment validation remain pending.

### Review findings

Current PR #7 work includes:

- removal of retired runtime review identity dependencies and binding to accepted human final approval;
- canonical repository-field shape;
- singleton message allowlists;
- correct limit/default and exact-type handling;
- complete configuration enum guards;
- message-kind and outgoing-recipient validation;
- atomic malformed incoming-message rejection;
- consistent bounded file-read error behavior;
- atomic delegated ingest failure;
- one canonical message-inclusive checkpoint for freeze and recovery;
- rollback at a full event ceiling;
- strict persisted-event validation;
- hostile-input issue #8 acceptance;
- accepted hash-fixed upstream contracts;
- complete review-thread, exact-head, and merged-head acceptance.

### Security

- Candidate CI uses read-only contents permission, exact submitted-head checkout/assertion, and disabled checkout credential persistence; the accepted policy workflow additionally pins actions by commit.
- Runtime and documentation examples remain local, synthetic, credential-free, network-independent, and non-deploying.
- Complete parser, identity, message, state-atomicity, checkpoint, rollback-capacity, persisted-evidence, dependency, secret, workflow, hostile-input, and adversarial review remains required.

### Release

- The first eligible package version remains `0.1.0-alpha.1`.
- Runtime release remains blocked by reconciliation, open findings, fresh exact-head and merged-head evidence, accepted upstream contracts, source/sdist/wheel/SBOM/provenance, privacy/licensing, rollback drill, and approval.
- Documentation publication remains blocked by strict build, content review, link/accessibility checks, privacy/license review, site provenance, publication approval, deployment validation, and rollback evidence.

### Deployment

- No runtime, package publication, Pages publication, scheduled execution, four-QSO experiment, external integration, financial path, or production deployment is authorized.
- The only initial target remains a disposable credential-free, network-independent local/CI verification environment after applicable gates pass.

## Entry format

- Date
- Category: Product / Architecture / Added / Changed / Fixed / Documentation / Verification / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
