# Release Plan

## Current decision

Status: `BLOCKED — DOCUMENTATION FOUNDATION READY FOR REVIEW; RUNTIME CANDIDATE UNRECONCILED AND UNACCEPTED`

QuantumStateObjects contains an accepted bounded prototype and repository-wide policy controls on `main`, plus a draft candidate package/runtime lineage in PR #7. No package release, GitHub Pages publication, experiment activation, external integration, or deployment is authorized.

The documentation branch starts from accepted `main` commit `40efcbf8ce2bda7d6b05b3fb1f3ccf0384facc51`. Draft PR #7 remains the sole canonical package/configuration/runtime candidate. Its current pre-reconciliation head observed during this review is `40a0c123c271c883356b9315dc213556d4abbb14`; it must be reconciled with current `main` and pass fresh exact-head review.

Historical successful PR #7 runs, including a Python 3.11/3.13 matrix reported with 150 tests at an earlier immutable head, remain historical evidence only. They do not accept the current candidate, a reconciled future head, or an eventual merged head.

## Versioning

- Scheme: Semantic Versioning.
- Existing package metadata is `0.1.0`; the first eligible candidate remains `0.1.0-alpha.1` until runtime, contract, test, security, provenance, documentation, privacy, licensing, rollback, and approval gates pass.
- Identity, configuration, genome reference, canonical record, message, event, attribution, checkpoint, freeze, interruption, recovery, rollback, evidence, and upstream-contract versions must be explicit.
- Incompatible schema, canonicalization, hash-input, lifecycle, checkpoint, ledger, or rollback changes require migrations and coordinated consumer fixtures.
- Experimenter object-model work and four-QSO execution remain separate later scopes.

## First candidate scope

- Installable local package and `qso-run` CLI on supported Python versions.
- Strict, bounded, local-only configuration and genome-file validation.
- Canonical identities for Atlas, Nova, Orion, and Lyra.
- Isolated QSO partitions and inactive generated proposals.
- Atomic canonical-record and message handling.
- Versioned event and attribution evidence.
- Canonical checkpoints, freeze, interruption, recovery, and rollback.
- Deterministic local replay with fixed inputs and recorded hashes.
- Accepted hash-fixed QSO-GENOMES and QSO-SEEKER fixture validation without importing or executing external code.
- Reproducible source, sdist, wheel, checksums, test reports, provenance, rollback bundle, and approved documentation.

### Explicitly excluded

- Autonomous internet learning or background retrieval.
- Executing generated or retrieved code.
- Credential, cookie, session, or production-secret access.
- External repository or system writes.
- Scheduled, persistent, remote, concurrent, or distributed execution.
- Production payment, custody, settlement, or investment behavior.
- Unapproved Experimenter objects or competing runtime paths.
- Claims that Atlas, Nova, Orion, or Lyra are independently active without authorized append-only runtime evidence.

## Selected candidate work

PR #7 remains the sole canonical P0 implementation path. Before acceptance it must:

1. reconcile current accepted `main` without rewriting reviewed history;
2. remove retired runtime review identity dependencies and preserve accepted human final approval;
3. resolve repository-field shape, singleton allowlists, limit/default handling, enum guards, message-kind and recipient validation, malformed message atomicity, and bounded file-read errors;
4. complete atomic ingest, canonical message-inclusive checkpoints, freeze parity, rollback at full event capacity, and strict persisted-event validation;
5. close issue #8 hostile-input and prompt-injection hardening requirements;
6. consume only accepted, immutable QSO-GENOMES and QSO-SEEKER contracts;
7. resolve every material review thread;
8. pass fresh exact-head and approved merged-head acceptance with retained evidence.

## Documentation candidate

The `docs/pages-architecture-onboarding` branch adds:

- Pages-ready MkDocs configuration and pinned documentation toolchain;
- expanded README and project overview;
- component, sequence, state, dependency, and trust-zone diagrams;
- design contracts for identity, configuration, genomes, records, messages, proposals, ledgers, attribution, resources, checkpoints, freeze, interruption, recovery, rollback, determinism, and compatibility;
- developer onboarding and contribution guidance;
- security threat model and hostile-input controls;
- operations, incident, recovery, cleanup, and rollback runbook;
- evidence-qualified release and Pages readiness documentation.

This documentation is a candidate only. It has not yet been strictly built, accessibility-reviewed, link-checked, published, or independently approved.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical implementation candidate | REVIEW | PR #7 remains the sole path and is reconciled normally with current `main`. |
| Repository-wide policy control | PASS ON MAIN | Accepted exact-head tests, validator report, retained evidence, and merged commit remain intact. |
| Runnable package and CLI | PARTIAL | Fresh clean install, smoke, and error-path evidence at repaired exact and merged heads. |
| Configuration contract | REVIEW | Exact schema/type/path/hash behavior and complete positive, negative, and adversarial fixtures. |
| Identity and review authority | BLOCKED | Retired aliases removed; accepted human-review authority and migration behavior approved. |
| Message contract | REVIEW | Kind, identity, allowlist, shape, digest, replay, capacity, and atomic-failure evidence. |
| Runtime atomicity and lifecycle | REVIEW | Complete active/frozen/interrupted/recovery/rollback behavior with unchanged state on rejection. |
| Event and attribution evidence | REVIEW | Exact shape, types, ordering, chain, hashes, provenance, truncation, reorder, replay, and tamper tests. |
| Checkpoint/freeze/rollback | REVIEW | One complete canonical checkpoint, message parity, full-capacity rollback, and post-validation. |
| Determinism | PARTIAL | Repeated fixed-input reports at accepted exact and merged heads. |
| Upstream contracts | BLOCKED | Accepted QSO-GENOMES and QSO-SEEKER versions, schemas, canonicalization rules, artifact identities, hashes, and fixtures. |
| Security | PARTIAL | Issue #8 adversarial matrix, dependency/workflow review, secret scan, exact-head evidence, and independent disposition. |
| Documentation source | REVIEW | Content accuracy and alignment with `taskchain.md`, `release.md`, `changelog.md`, code, schemas, and tests. |
| Documentation build | PENDING | Clean `mkdocs build --strict`, Mermaid rendering, link check, and retained build artifact. |
| Accessibility | PENDING | Keyboard, headings, landmarks, contrast, reduced motion, tables, code, and mobile review. |
| Privacy/confidentiality | BLOCKED | Approved public-data and artifact-handling rules; no unintended sensitive data. |
| License/attribution | BLOCKED | Approved repository, dependency, artifact, contributor, and documentation notices. |
| Provenance | PARTIAL | Source/sdist/wheel/site hashes, SBOM where applicable, attestations, review disposition, and retention. |
| Rollback | PARTIAL | Runtime and Pages rollback drills with post-validation evidence. |
| Pages publication | BLOCKED | Approved source/workflow, exact-head build, deployment artifact, public validation, and approval. |
| Package publication | BLOCKED | Every runtime, artifact, security, documentation, policy, and approval gate passes. |
| Deployment | BLOCKED | Approved target, health checks, observability, rollback, and post-deployment validation. |
| Final approval | PENDING | Explicit recorded approval after every blocking gate passes. |

## Artifact requirements

- Immutable source archive, sdist, and wheel from accepted exact and merged heads.
- Versioned schemas, configurations, manifests, messages, ledgers, checkpoints, freeze/rollback records, and upstream fixtures.
- Strict-UTF-8, duplicate-key, non-finite-number, missing/extra-field, Boolean-type, invalid-ID/name/path/repository/hash, malformed-message, unknown-recipient, atomic-ingest, full-capacity rollback, message-inclusive checkpoint, malformed-ledger, prompt-injection, replay, reorder, and tamper fixtures.
- Exact-head and merged-head clean install, compile, unit, adversarial, deterministic, interruption, recovery, freeze, rollback, and CLI reports.
- Source, sdist, wheel, documentation-site, fixture, and report SHA-256 values.
- SBOM where applicable, provenance/attestation, review disposition, privacy/license approval, and tested rollback instructions.

## Pages publication requirements

1. Build from an approved immutable source SHA in a clean environment.
2. Pin and record MkDocs, theme, extension, Python, and workflow versions.
3. Run `mkdocs build --strict` and a link checker.
4. Review rendered diagrams, navigation, headings, tables, code blocks, search, keyboard access, contrast, mobile layout, and reduced-motion behavior.
5. Verify all status claims against accepted repository and PR evidence.
6. Confirm no sensitive or unintended personal data appears in source or built artifacts.
7. Hash and retain the built site artifact and build logs.
8. Publish only after explicit approval.
9. Validate the public URL, content identity, navigation, and rollback procedure.

## Deployment readiness

No runtime or persistent deployment is authorized. The first permitted environment remains a disposable local or CI verification context with no credentials, no external writes, no network-dependent inputs, no generated-code execution, no production data, bounded resources, explicit human controls, and hash-bound evidence.

A successful test or documentation build does not authorize package publication, Pages publication, hosting, scheduling, external integration, a four-QSO experiment, or production use.

## Health, observability, rollback, and post-validation

Health requires exact source/configuration identity, successful bounded startup/shutdown, strict fail-closed inputs, valid canonical ledgers and checkpoints, deterministic replay, resource compliance, and absence of denied external capabilities. Observability records non-secret source/configuration identities, lifecycle transitions, rejections, limits, evidence heads, rollback decisions, artifact hashes, cleanup, and post-validation.

Roll back on any identity, schema, hash, type, atomicity, ledger, checkpoint, determinism, resource, security, privacy, documentation, provenance, or approval failure. Preserve failed evidence, restore the last accepted checkpoint or clean disposable state, verify no external mutation, and do not resume without a new accepted head and allowed transition.

## Release log

- 2026-07-16 — Set runnable local-package acceptance ahead of cross-repository and four-QSO claims.
- 2026-07-17 — Selected PR #7 as the sole canonical configuration/runtime candidate and recorded historical exact-head evidence and findings.
- 2026-07-18 — Merged the repaired repository-wide policy validator to `main`; PR #7 became stale against the accepted base and requires reconciliation and fresh evidence.
- 2026-07-19 — Added the Pages-ready architecture, design, onboarding, security, operations, and release documentation candidate; publication and runtime release remain blocked.
