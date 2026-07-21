# Release Plan

## Current decision

Status: `BLOCKED — DOCUMENTATION AND GLUING MODEL READY FOR EXACT-HEAD REVIEW; RUNTIME AND CROSS-REPOSITORY CONTRACTS UNACCEPTED`

QuantumStateObjects contains an accepted bounded prototype and repository-wide consent-capacity policy controls on `main`, plus draft package/runtime candidate PR #7. No package release, GitHub Pages publication, experiment activation, Repository `0`/`1` integration, external adapter, canonical-state mutation, or deployment is authorized.

Draft PR #7 remains the sole package/configuration/runtime candidate at pre-reconciliation head `40a0c123c271c883356b9315dc213556d4abbb14`. It must be reconciled with current `main` and pass the repaired policy control plus the complete runtime matrix at one new exact head. Historical successful runs remain evidence only for their named immutable sources.

Within A.L.I.S.T.A.I.R.E., this repository is the bounded local runtime and evidence subsystem. Repository `0` is the portable bootstrap, planning, proposal, and maintenance-orchestration candidate; Repository `1` is the independent capability, canonical-state, revocation, and recovery authority candidate. QuantumStateObjects may consume their outputs only after versioned contracts, shared fixtures, authority ownership, and explicit approval exist.

## Versioning

- Scheme: Semantic Versioning.
- Existing package metadata is `0.1.0`; the first eligible candidate remains `0.1.0-alpha.1` until every blocking gate passes.
- Identity, configuration, genome, observation, capability, task, message, event, attribution, checkpoint, freeze, interruption, recovery, rollback, correction, revocation, evidence, and upstream-contract versions must be explicit.
- Incompatible schema, canonicalization, hash-input, lifecycle, clock, replay, checkpoint, ledger, rollback, authority, or cross-repository changes require migrations and coordinated consumer fixtures.
- Experimenter work, four-QSO execution, autonomous-development integration, device administration, and payment behavior remain separate later scopes.

## First candidate scope

- Installable local package and `qso-run` CLI on supported Python versions.
- Strict, bounded, local-only configuration and artifact validation.
- Canonical local fixture identities for Atlas, Nova, Orion, and Lyra.
- Isolated QSO partitions and inactive generated proposals.
- Atomic canonical-record and message handling.
- Versioned event and attribution evidence.
- Canonical checkpoints, freeze, interruption, recovery, and rollback.
- Deterministic local replay with fixed inputs and recorded hashes.
- Accepted hash-fixed genome, observation, capability, and task-envelope validation without importing or executing producer code.
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
7. resolve every material review thread;
8. pass fresh exact-head and approved merged-head acceptance with retained evidence.

## Documentation and gluing candidate

The `docs/pages-architecture-onboarding` branch adds:

- Pages-ready MkDocs configuration and pinned documentation tooling;
- project overview, architecture, design contracts, onboarding, security, operations, and release guidance;
- an updated A.L.I.S.T.A.I.R.E. integration model reflecting Repositories `0` and `1`;
- an obstruction ledger covering sixteen active compatibility and authority failures;
- pairwise gluing maps and six required triple-overlap witnesses;
- a release punch list spanning runtime acceptance, security, semantic ownership, Repository `0`/`1`, genomes, observations, Fabric/kernel, Bridge/interfaces, resources/replay, experiment readiness, publication, and recovery;
- a read-only exact-submitted-head Documentation workflow with strict build validation, generated-site checks, dependency capture, SHA-256 manifests, and retained artifacts.

A successful documentation workflow proves only that its named immutable head built under the recorded environment. It does not select canonical owners, accept contracts, complete accessibility/privacy/license review, publish Pages, activate adapters, approve PR #7, or authorize release or deployment.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical implementation candidate | REVIEW | PR #7 remains the sole path and is reconciled normally with current `main`. |
| Repository-wide policy control | PASS ON MAIN | Accepted consent-capacity tests, validator report, workflow controls, and retained evidence remain intact. |
| Runnable package and CLI | PARTIAL | Fresh clean install, smoke, build, and error-path evidence at repaired exact and merged heads. |
| Parser/configuration/identity contract | REVIEW | Strict UTF-8, duplicate-key, exact-type, canonical identity, schema, limits, paths, hashes, and complete negative fixtures. |
| Message and runtime atomicity | REVIEW | Kind, identity, allowlist, shape, digest, replay, capacity, delegated failure, and unchanged-state evidence. |
| Event, attribution, checkpoint, and rollback evidence | REVIEW | Exact shape, types, ordering, chain, hashes, corrections, revocations, full-capacity rollback, and post-validation. |
| Hostile-input security | BLOCKED | Issue #8 adversarial matrix, dependency/workflow review, secret scan, exact-head evidence, and independent disposition. |
| Semantic ownership | BLOCKED | `qsio-kernel`, runtime, Fabric, genomes, Seeker, Bridge, Repository `0`, and Repository `1` responsibilities and migrations are approved. |
| Repository `0`/`1` route | BLOCKED | Proposal, quarantine, capability, task, expected-head, expiry, replay, receipt, revocation, and reconciliation contracts and fixtures are accepted. |
| Genome compatibility | BLOCKED | Accepted QSO-GENOMES identity, lineage, schema, canonicalization, policy, lifecycle, digest, migration, and fixtures. |
| Observation/temporal compatibility | BLOCKED | Accepted subject, source, provenance, clocks, freshness, replay, correction, revocation, classification, uncertainty, and fixtures. |
| Fabric/kernel gluing | BLOCKED | Format, lifecycle, message, resource, ledger, checkpoint, freeze, rollback, and collaboration ownership and triple-overlap fixtures. |
| Bridge/interface gluing | BLOCKED | Evidence transport, integrity, redaction, correction, privacy, retention, read-only presentation, and approval-separation fixtures. |
| Local versus canonical state | BLOCKED | Runtime and Fabric success remain distinct from Repository `1` canonical reconciliation and later correction. |
| Emergency stop and recovery | BLOCKED | Runtime freeze, Fabric stop, capability revocation, evidence preservation, interface invalidation, human recovery, and bounded restart agree. |
| Determinism and replay | PARTIAL | Repeated fixed-input reports plus clocks, causal order, nonce, expiry, restart, and replay-window evidence. |
| Documentation source/build | REVIEW | Exact-head content alignment, strict build, generated-site checks, local links, and retained evidence. |
| Accessibility | PENDING | Keyboard, headings, landmarks, contrast, reduced motion, tables, code, diagrams, and mobile review. |
| Privacy/confidentiality | BLOCKED | Approved classification, minimization, redaction, retention, deletion, and public-artifact rules. |
| License/attribution | BLOCKED | Approved repository, dependency, artifact, contributor, and documentation notices. |
| Provenance | PARTIAL | Source/sdist/wheel/site hashes, SBOM where applicable, attestations, reviews, approvals, and retention. |
| Rollback | PARTIAL | Runtime, integration, and Pages rollback drills with post-validation evidence. |
| Pages publication | BLOCKED | Approved source/workflow, exact-head build, deployment artifact, public validation, explicit approval, and rollback. |
| Package publication | BLOCKED | Every runtime, contract, artifact, security, documentation, policy, recovery, and approval gate passes. |
| Deployment | BLOCKED | Approved target, capability, health checks, observability, emergency stop, rollback, and post-deployment validation. |
| Final approval | PENDING | Explicit human approval after every blocking gate passes. |

## Required compatibility witnesses

- QSO-GENOMES → QuantumStateObjects producer/consumer fixtures.
- QSO-SEEKER → temporal owner → QuantumStateObjects freshness, replay, correction, and subject fixtures.
- Repository `0` → Repository `1` → QuantumStateObjects capability and task fixtures.
- Genome → runtime → QSO-FABRIC identity, policy, lifecycle, and rollback fixtures.
- QuantumStateObjects → QSO-FABRIC → Repository `1` execution/collaboration/canonical-state separation fixtures.
- QuantumStateObjects → Bridge → QSO-STUDIO/AionUi integrity, redaction, correction, and denied-approval-inference fixtures.
- Runtime freeze → Fabric stop → Repository `1` revocation and human-approved recovery fixtures.

## Artifact requirements

- Immutable source archive, sdist, and wheel from accepted exact and merged heads.
- Versioned schemas, configurations, genomes, observations, capabilities, tasks, messages, ledgers, checkpoints, corrections, revocations, receipts, and upstream manifests.
- Positive, malformed, unsupported-version, stale, replay, wrong-identity, expected-head, expiry, partial-failure, correction, revocation, freeze, rollback, privacy, and recovery fixtures.
- Exact-head and merged-head clean install, compile, unit, adversarial, deterministic, interruption, recovery, freeze, rollback, and CLI reports.
- Source, sdist, wheel, documentation-site, fixture, and report SHA-256 values.
- SBOM where applicable, provenance/attestation, review disposition, privacy/license approval, emergency-stop evidence, and tested rollback instructions.

## Pages publication requirements

1. Build from an approved immutable source SHA in a clean environment.
2. Pin and record documentation, Python, and workflow versions.
3. Assert the exact submitted source before building.
4. Run `mkdocs build --strict`, generated-site checks, and independent link review.
5. Review rendered diagrams, navigation, headings, tables, code, search, keyboard access, contrast, mobile layout, and reduced motion.
6. Verify all status claims against accepted repository and portfolio evidence.
7. Confirm no sensitive or unintended personal data appears in source or built artifacts.
8. Hash and retain the built site, dependency inventory, manifest, and logs.
9. Publish only after explicit approval.
10. Validate the public URL, content identity, navigation, and rollback procedure.

## Deployment readiness

No runtime or persistent deployment is authorized. The first permitted environment remains a disposable local or CI verification context with no credentials, external writes, network-dependent inputs, generated-code execution, production data, or device-administration authority; bounded resources and explicit human controls remain mandatory.

A successful runtime test or documentation build does not authorize package publication, Pages publication, hosting, scheduling, external integration, autonomous-development integration, a four-QSO experiment, or production use.

## Health, observability, rollback, and post-validation

Health requires exact source/configuration/policy/capability identity, bounded startup/shutdown, fail-closed inputs, valid ledgers and checkpoints, deterministic replay, resource compliance, and absence of denied external capabilities. Observability records non-secret identities, lifecycle transitions, rejections, limits, evidence heads, corrections, revocations, rollback decisions, artifact hashes, cleanup, and post-validation.

Roll back on any identity, schema, hash, type, atomicity, ledger, checkpoint, determinism, replay, resource, security, privacy, contract, documentation, provenance, authority, or approval failure. Preserve failed evidence, revoke applicable capabilities, restore the last accepted checkpoint or clean disposable state, verify no external mutation, and do not resume without a new accepted head and explicit approval.

## Release log

- 2026-07-16 — Set runnable local-package acceptance ahead of cross-repository and four-QSO claims.
- 2026-07-17 — Selected PR #7 as the sole package/configuration/runtime candidate.
- 2026-07-18 — Merged the repaired repository-wide policy validator to `main`; PR #7 requires reconciliation and fresh evidence.
- 2026-07-19 — Added the Pages-ready architecture, design, onboarding, security, operations, and release documentation candidate.
- 2026-07-20 — Defined QuantumStateObjects as A.L.I.S.T.A.I.R.E.'s bounded local runtime/evidence subsystem.
- 2026-07-20 — Added portfolio obstruction/gluing analysis, aligned Repositories `0` and `1`, expanded the release punch list, and introduced pairwise and triple-overlap compatibility gates without changing implementation scope.
