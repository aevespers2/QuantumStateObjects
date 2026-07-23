# Release Plan

## Current decision

Status: `BLOCKED — DOCUMENTATION AND SOURCE-BOUND INTERFACE MODEL READY FOR EXACT-HEAD REVIEW; RUNTIME, INDEPENDENT CONSUMER, PAYLOAD CONTRACTS, AND APPROVALS INCOMPLETE`

QuantumStateObjects contains an accepted bounded prototype and repository-wide consent-capacity policy controls on `main`, draft package/runtime candidate PR #7, and a documentation candidate covering runtime admission, ecosystem interface compatibility, operations, recovery, and publication gates. No package release, GitHub Pages publication, experiment activation, Repository `0`/`1` integration, QSO-FABRIC adapter, canonical-state mutation, or deployment is authorized.

Draft PR #7 remains the sole package/configuration/runtime candidate at pre-reconciliation head `40a0c123c271c883356b9315dc213556d4abbb14`. It must be reconciled with current `main` and pass the repaired policy control plus the complete runtime matrix at one new exact head. Historical successful runs remain evidence only for their named immutable sources.

The documentation lineage binds QSO-FABRIC PR #21 head `25036a5cfcea79e204a4660ddd1af09c054935b1`, its exact source tuple, and the byte-identical `QSO-INTERFACE-COMPATIBILITY-001@1.0.0` fixture. This is source and synthetic-case evidence only. The planned independent QuantumStateObjects evaluator and final `qso-event-ledger` / `qso-runtime-report` payload contracts remain unimplemented and unaccepted.

## Versioning

- Scheme: Semantic Versioning.
- Existing package metadata is `0.1.0`; the first eligible candidate remains `0.1.0-alpha.1` until every blocking gate passes.
- Identity, configuration, genome, observation, interpretation, proposal, quarantine, capability, task, admission, message, event, attribution, checkpoint, freeze, interruption, recovery, rollback, correction, revocation, execution receipt, resulting-state evidence, reconciliation, interface source tuple, registry generation, namespace, and payload-schema versions must be explicit.
- Incompatible schema, canonicalization, hash-input, namespace, lifecycle, clock, replay, checkpoint, ledger, report, idempotency, retry, rollback, authority, privacy, or cross-repository changes require migrations and coordinated producer/consumer fixtures.
- Experimenter work, four-QSO execution, autonomous-development integration, device administration, and payment behavior remain separate later scopes.

## First candidate scope

- Installable local package and `qso-run` CLI on supported Python versions.
- Strict, bounded, local-only configuration and artifact validation.
- Canonical local fixture identities for Atlas, Nova, Orion, and Lyra.
- Isolated QSO partitions and inactive generated proposals.
- Atomic canonical-record, admission-envelope, and message handling.
- Versioned local event and attribution evidence.
- Canonical checkpoints, freeze, interruption, recovery, and rollback.
- Deterministic local replay with fixed inputs and recorded hashes.
- Accepted hash-fixed genome, observation, capability, and task-envelope validation without importing or executing producer code.
- Admission decisions and execution receipts distinct from Fabric collaboration and Repository `1` canonical reconciliation.
- Reproducible source, sdist, wheel, checksums, test reports, provenance, rollback bundle, and approved documentation.

### Explicitly excluded

- Autonomous internet learning or background retrieval.
- Host-security collection, device administration, or remote remediation.
- Executing generated or retrieved code.
- Credential, cookie, session, or production-secret access.
- External repository or system writes.
- Scheduled, persistent, remote, concurrent, or distributed execution.
- Production payment, custody, settlement, or investment behavior.
- Portfolio-wide planning, merge, release, deployment, incident, emergency-stop, recovery, capability issuance, or canonical-state authority.
- Claims that Atlas, Nova, Orion, or Lyra are active without authorized append-only runtime evidence.

## Selected candidate work

Before acceptance, PR #7 must:

1. reconcile current accepted `main` without rewriting reviewed history;
2. remove retired review-identity dependencies and preserve explicit human final approval;
3. resolve strict parser, repository-field, schema, identity, limits, enum, message, bounded-file, and canonicalization findings;
4. complete atomic ingestion, message-inclusive checkpoints, freeze parity, rollback at full capacity, and persisted-evidence validation;
5. close hostile-input and prompt-injection issue #8;
6. consume only accepted immutable upstream and Repository `1` contracts;
7. implement or explicitly defer the approved runtime-admission contract without implying that documentation is runtime behavior;
8. resolve every material review thread;
9. pass fresh exact-head and approved merged-head acceptance with retained evidence.

## Documentation and interface candidate

The documentation candidate adds:

- Pages-ready MkDocs configuration and pinned documentation tooling;
- project overview, architecture, design contracts, onboarding, security, operations, recovery, and release guidance;
- an A.L.I.S.T.A.I.R.E. integration model reflecting Repositories `0` and `1`;
- a runtime admission and reconciliation profile separating proposal, quarantine, capability, admission, execution, receipt, transport, review, correction, revocation, and canonical disposition;
- one consolidated QSO-FABRIC interface compatibility page;
- a machine-readable documentation profile, review checklist, ADR, exact producer source tuple, and byte-identical fixture;
- strict documentation-profile validation with hostile regressions and retained exact-head evidence;
- an obstruction ledger, pairwise maps, and required triple-overlap witnesses;
- task-chain, punch-list, README, Pages, and changelog alignment.

Passing documentation workflows proves only that named immutable documentation and evidence inputs satisfy their checks. It does not complete the independent runtime consumer, define accepted payload bytes, select owners, approve privacy/licensing/accessibility, publish Pages, accept PR #7, or authorize release or deployment.

## Interface acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Producer source tuple | SOURCE BOUND | QSO-FABRIC repository, PR, exact head, fixture path/blob, workflow, artifact digest, and expiration are recorded. |
| Fixture identity | SOURCE BOUND | QuantumStateObjects carries the exact producer fixture bytes. |
| Producer corpus | SOURCE BOUND | 17 cases, 14 facts, 14 ordered reasons, and dispositions are documented. |
| Independent consumer | BLOCKED | A separately implemented evaluator derives all outcomes without importing producer validation code. |
| Event-ledger payload | BLOCKED | Identity, sequence, causal order, canonicalization, hash chain, duplicate, replay, conflict, correction, revocation, supersession, withdrawal, and privacy semantics are accepted. |
| Runtime-report payload | BLOCKED | Ledger references, completeness, partial failure, cleanup, uncertainty, resource use, rollback, and authority separation are accepted. |
| Namespace ownership | BLOCKED | Runtime-local and Fabric-level ledger/report classes are separately named or mandatorily partitioned. |
| Migration and rollback | BLOCKED | Mixed-version fixtures, consumer rebinding, correction propagation, cache invalidation, rollback, and restored-state evidence pass. |
| Triple-overlap witnesses | BLOCKED | Runtime/Fabric/Repository `1`, runtime/Bridge/interface, correction/recovery, and migration/rollback paths pass. |
| Architecture approval | PENDING | Human owners approve interfaces, payloads, custody, migration, and authority boundaries. |

## Runtime admission gates

| Gate | Status | Requirement |
|---|---|---|
| Record separation | BLOCKED | Proposal, quarantine, capability, task, admission, execution, receipt, result, reconciliation, correction, revocation, and recovery records have distinct identities. |
| Device/environment binding | BLOCKED | Device identity, enrollment generation, ownership scope, platform profile, and revocation lifecycle are accepted. |
| Workspace/runtime binding | BLOCKED | Repository, base, expected head, sandbox, package, configuration, policy, and pre-state are independently verified. |
| Capability enforcement | BLOCKED | Issuer, requester, executor, action class, paths, tools, network policy, limits, expiry, nonce, replay, revocation, and stop behavior fail closed. |
| Genome and observation admission | BLOCKED | Exact identities, schemas, canonicalization, lineage, provenance, clocks, privacy, correction, and revocation are accepted. |
| Atomic decision | BLOCKED | Validation completes without state mutation and every rejection preserves prior state. |
| Execution receipt | BLOCKED | Receipt binds admission, runtime, device, workspace, capability, task, resources, pre/post/rollback state, artifacts, uncertainty, and cleanup. |
| Reconciliation | BLOCKED | Repository `1` independently dispositions evidence; runtime or Fabric success cannot self-promote. |

## General acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical implementation candidate | REVIEW | PR #7 is the sole path and is normally reconciled with current `main`. |
| Repository-wide policy control | PASS ON MAIN | Accepted consent-capacity controls and retained evidence remain intact. |
| Runnable package and CLI | PARTIAL | Fresh clean install, smoke, build, and error-path evidence at repaired exact and merged heads. |
| Parser/configuration/identity | REVIEW | Strict encoding, exact types, identities, schema, limits, paths, hashes, and negative fixtures. |
| Runtime atomicity/evidence | REVIEW | Message, capacity, delegated failure, ledgers, checkpoints, corrections, revocations, and rollback. |
| Hostile-input security | BLOCKED | Issue #8 adversarial matrix, dependency/workflow review, secret scan, and independent disposition. |
| Semantic ownership | BLOCKED | Kernel, runtime, Fabric, genomes, Seeker, temporal/Digitalis, Bridge, Repository `0`, and Repository `1` responsibilities are approved. |
| Repository `0`/`1` route | BLOCKED | Proposal, quarantine, capability, task, expiry, replay, receipt, revocation, and reconciliation contracts pass. |
| Genome and observation compatibility | BLOCKED | Accepted producer/consumer identities, schemas, policies, lifecycle, corrections, privacy, and fixtures. |
| Fabric/kernel/Bridge/interface gluing | BLOCKED | Pairwise and triple-overlap fixtures preserve local, collaborative, transported, displayed, and canonical states. |
| Emergency stop and recovery | BLOCKED | Runtime freeze, Fabric stop, capability revocation, evidence preservation, interface invalidation, recovery, and bounded restart agree. |
| Determinism and replay | PARTIAL | Repeated fixed-input reports plus clocks, causal order, nonce, expiry, restart, and replay-window evidence. |
| Documentation source/build | REVIEW | Exact-head content alignment, strict build, profile validation, links, and retained evidence. |
| Accessibility | PENDING | Keyboard, headings, landmarks, contrast, reduced motion, tables, code, diagrams, and mobile review. |
| Privacy/confidentiality | BLOCKED | Classification, minimization, redaction, retention, deletion, and public-artifact rules. |
| License/attribution | BLOCKED | Repository, dependency, artifact, contributor, fixture, and documentation notices. |
| Provenance | PARTIAL | Source, packages, site, fixtures, tuples, reports, attestations, reviews, and retention. |
| Rollback | PARTIAL | Runtime, contract, integration, consumer, and Pages rollback drills with post-validation. |
| Pages publication | BLOCKED | Approved source/workflow, exact-head build, public validation, approval, and rollback. |
| Package publication/deployment | BLOCKED | Every runtime, interface, security, documentation, policy, recovery, and approval gate passes. |
| Final approval | PENDING | Explicit human approval after every blocking gate passes. |

## Required compatibility witnesses

- Repository `0` → Repository `1` → runtime proposal, capability, admission, and receipt.
- QSO-GENOMES → runtime → QSO-FABRIC identity, policy, lifecycle, lineage, and rollback.
- QSO-SEEKER → temporal/Digitalis → runtime source, freshness, replay, correction, privacy, and subject.
- Runtime event ledger → runtime report → Fabric receipt.
- Runtime → QSO-FABRIC → Repository `1` execution/collaboration/canonical-state separation.
- Runtime → Bridge → QSO-STUDIO/AionUi integrity, redaction, correction, cache invalidation, and denied approval inference.
- Capability revocation → runtime freeze → final ledger/report evidence → Repository `1` recovery.
- Correction → downstream invalidation → corrected report and reconciliation.
- Schema migration → mixed-version consumers → rollback and rebinding.

## Artifact requirements

- Immutable source archive, sdist, and wheel from accepted exact and merged heads.
- Versioned schemas, configurations, genomes, observations, proposals, capabilities, tasks, admissions, messages, ledgers, reports, checkpoints, corrections, revocations, receipts, results, dispositions, source tuples, registry generations, and manifests.
- Producer and independent-consumer fixtures with malformed, unsupported, stale, replay, conflict, wrong-identity, broadened-scope, partial-failure, correction, revocation, freeze, rollback, privacy, and recovery cases.
- Exact-head and merged-head build, test, admission, deterministic, interruption, recovery, freeze, rollback, documentation, and interface-conformance reports.
- Source, package, site, tuple, fixture, profile, and report SHA-256 values.
- SBOM where applicable, provenance/attestation, review disposition, privacy/license/accessibility approval, emergency-stop evidence, and tested rollback instructions.

## Pages publication requirements

1. Build from an approved immutable source SHA in a clean environment.
2. Pin and record documentation, Python, and workflow versions.
3. Assert the exact submitted source before building.
4. Run strict MkDocs, generated-site, machine-profile, and independent link checks.
5. Review diagrams and prose alternatives, navigation, headings, tables, code, search, keyboard access, contrast, mobile layout, and reduced motion.
6. Verify status claims against current repository and portfolio evidence.
7. Confirm no sensitive or unintended personal data appears in source or built artifacts.
8. Hash and retain the built site, dependencies, source tuples, fixture/profile manifests, and logs.
9. Publish only after explicit approval.
10. Validate public URL, content identity, navigation, and rollback.

## Deployment readiness

No runtime or persistent deployment is authorized. The first permitted environment remains a disposable local or CI verification context with no credentials, external writes, network-dependent inputs, generated-code execution, production data, or device-administration authority; bounded resources and explicit human controls remain mandatory.

A successful runtime test, copied fixture, synthetic conformance result, documentation profile validation, or site build does not authorize package publication, Pages publication, external integration, autonomous-development integration, a four-QSO experiment, or production use.

## Health, observability, rollback, and post-validation

Health requires exact source/configuration/policy/capability/admission/interface identities, bounded startup/shutdown, fail-closed inputs, valid ledgers/reports/checkpoints, deterministic replay, resource compliance, and absence of denied external capabilities. Observability records non-secret identities, source-tuple currency, lifecycle transitions, admission decisions, rejections, limits, receipts, corrections, revocations, reconciliation, rollback, artifact hashes, cleanup, and post-validation.

Roll back on any identity, schema, namespace, hash, type, source expiry, reason-order, admission, atomicity, ledger, report, checkpoint, determinism, replay, resource, security, privacy, contract, documentation, provenance, authority, or approval failure. Preserve failed evidence, revoke applicable capabilities, rebind consumers to the last accepted registry generation, restore the last accepted checkpoint or clean disposable state, verify no external mutation, and do not resume without a new accepted head and explicit approval.

## Release log

- 2026-07-16 — Set runnable local-package acceptance ahead of cross-repository and four-QSO claims.
- 2026-07-17 — Selected PR #7 as the sole package/configuration/runtime candidate.
- 2026-07-18 — Merged the repaired repository-wide policy validator to `main`; PR #7 requires reconciliation and fresh evidence.
- 2026-07-19 — Added Pages-ready architecture, design, onboarding, security, operations, and release documentation.
- 2026-07-20 — Defined QuantumStateObjects as A.L.I.S.T.A.I.R.E.'s bounded local runtime/evidence subsystem and added portfolio gluing gates.
- 2026-07-21 — Added the runtime admission and reconciliation contract candidate.
- 2026-07-23 — Bound the QSO-FABRIC interface producer tuple and fixture; reconciled interface documentation; kept independent consumer, payload, architecture, release, publication, and deployment gates blocked.
