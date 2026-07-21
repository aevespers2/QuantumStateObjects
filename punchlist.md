# QuantumStateObjects Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked runtime, security, cross-repository, or authority gates. Completion requires immutable evidence; checking an item does not itself authorize merge, release, publication, deployment, or integration.

## Current evidence state

- [x] PR #7 remains the sole selected package/configuration/runtime candidate.
- [x] Historical heads passed substantial Python 3.11/3.13 package, CLI, runtime, and artifact checks.
- [x] Accepted `main` contains the repaired repository-wide consent-capacity policy control.
- [ ] PR #7 head `40a0c123c271c883356b9315dc213556d4abbb14` remains pre-reconciliation against current `main`; its successful runtime run is historical exact-head evidence only.
- [ ] The prior reconciled-head evidence recorded in earlier punch-list text is superseded by the later accepted `main` policy repair and must not be treated as current acceptance.
- [ ] No accepted QSO-GENOMES, QSO-SEEKER, Repository `0`/`1`, QSO-FABRIC, Bridge, or `qsio-kernel` compatibility set is active in this runtime.

## P0 — Canonical runtime lineage

- [ ] Reconcile draft PR #7 with accepted `main` without rewriting reviewed history.
- [ ] Record the exact integrated base and head commits.
- [ ] Remove retired review-identity dependencies while preserving explicit human final approval.
- [ ] Resolve all material review threads and document their disposition.
- [ ] Pass clean install, wheel/sdist build, CLI smoke, compile, unit, negative, adversarial, deterministic, interruption, recovery, freeze, and rollback tests on supported Python versions.
- [ ] Re-run the repository-wide consent-capacity policy control at the same exact head.
- [ ] Produce approved merged-head verification in addition to exact-PR-head verification.

## P0 — Parser, identity, and configuration invariants

- [ ] Reject invalid UTF-8, UTF-16/32 input, duplicate JSON keys, non-finite values, lone surrogates, Boolean-as-integer values, unknown fields, and unsupported versions.
- [ ] Pin canonical repository, path, package, object, role, schema, policy, and content identity rules.
- [ ] Enforce all schema-required identity, development, review, status, and repository fields before constructing accepted runtime state.
- [ ] Prove default and maximum limits cannot be bypassed by missing, zero, negative, overflowed, aliased, or wrong-type values.
- [ ] Prove file reads are bounded and fail atomically on truncation, oversize, mutation, missing paths, permission failures, and digest mismatch.
- [ ] Publish canonical serialization and golden fixtures for every persisted structure.

## P0 — Message, runtime atomicity, and evidence

- [ ] Reject unknown kinds, malformed shapes, unauthorized senders or recipients, aliases, digest mismatches, replay, and capacity failures before any mutation.
- [ ] Normalize limits before delegation or restore complete prior state on every delegated ingest exception.
- [ ] Use one message-inclusive canonical checkpoint for freeze, interruption, recovery, and rollback.
- [ ] Prove rollback succeeds at full event and attribution capacity.
- [ ] Validate persisted events and attribution for exact shape, types, sequence, object identity, canonical payload, chain, digest, truncation, reorder, replay, and tampering.
- [ ] Define correction, supersession, contradiction, revocation, and downstream invalidation records without deleting history.
- [ ] Confirm every generated snippet remains inert and requires accepted policy plus explicit human review.

## P0 — Hostile-input and authority security

- [ ] Complete issue #8 adversarial fixtures for direct, indirect, encoded, nested, Unicode, metadata, filename, Markdown, JSON, comment, document, and cross-repository injection.
- [ ] Preserve immutable raw and canonical hashes for hostile or transformed inputs.
- [ ] Separate data from instructions at parser, model, review, and interface boundaries.
- [ ] Prove prompts, records, comments, artifacts, and model output cannot grant capabilities or approval.
- [ ] Scan dependencies, workflows, artifacts, and repository history for secrets and unsafe authority paths.

## P1 — Ownership and gluing decisions

- [ ] Approve the responsibility split among `qsio-kernel`, QuantumStateObjects, QSO-FABRIC, QSO-GENOMES, QSO-SEEKER, Bridge, Repository `0`, and Repository `1`.
- [ ] Designate the canonical owner of QSO format, canonicalization, lifecycle vocabulary, message types, event/ledger semantics, checkpoint/freeze/rollback semantics, and migrations.
- [ ] Distinguish local runtime state, Fabric collaboration state, transported evidence, and Repository `1` canonical state.
- [ ] Approve one cross-repository stop-state lattice covering freeze, Quietus, revocation, emergency stop, recovery, and bounded restart.
- [ ] Assign human owners for policy, security, credentials, incident response, emergency stop, recovery, release, and rollback.

## P1 — Repository `0` / Repository `1` task route

- [ ] Accept the canonical route: `0:working → 0:proposal` as local non-authoritative staging, followed by a versioned envelope into `1:quarantine`.
- [ ] Define runtime task-envelope, capability-reference, expected-head, device/environment, policy, expiry, replay, and receipt schemas.
- [ ] Prove Repository `0` proposals cannot self-authorize execution.
- [ ] Prove Repository `1` capabilities are narrow, expiring, revocable, identity-bound, and unusable against a different runtime/configuration head.
- [ ] Prove execution success does not imply Repository `1` canonical acceptance.
- [ ] Add partial-execution, revocation-during-execution, receipt-rejection, rollback, and recovery fixtures.

## P2 — Genome compatibility

- [ ] Accept one immutable QSO-GENOMES compatibility set by repository, commit, path, schema, canonicalization version, and SHA-256.
- [ ] Define genome identity, lineage, immutable fields, mutation classes, policy digest, lifecycle version, and migration ownership.
- [ ] Add producer/consumer fixtures for valid, unsupported-version, digest-mismatch, lineage-mismatch, immutable-field mutation, and rollback cases.
- [ ] Bind Atlas, Nova, Orion, and Lyra runtime fixtures to accepted genome identities before describing them as instantiated.

## P2 — Observation and temporal compatibility

- [ ] Accept one QSO-SEEKER observation/evidence envelope with subject identity, source identity, provenance, classification, content hash, clocks, freshness, replay, correction, and revocation fields.
- [ ] Assign temporal interpretation to `datarepo-temporal-invariants` or another approved owner without duplicating runtime responsibility.
- [ ] Add stale, reordered, ambiguous-clock, replayed, corrected, revoked, wrong-subject, privacy, and retention fixtures.
- [ ] Prove rejected records cause no state mutation.

## P2 — Fabric and kernel compatibility

- [ ] Approve whether `qsio-kernel` is the canonical low-level semantic kernel, a conformance implementation, a migration source, or an independent prototype.
- [ ] Approve QSO-FABRIC ownership of collaboration and experiment semantics without duplicating local runtime semantics.
- [ ] Pin format-registry, envelope, stream/package serialization, lifecycle, resource, and evidence contracts.
- [ ] Add genome → runtime → Fabric and format → runtime → Fabric triple-overlap fixtures.
- [ ] Prove Fabric acceptance remains distinct from runtime success and Repository `1` canonical acceptance.

## P3 — Bridge and interface evidence path

- [ ] Define a transport-neutral evidence envelope for runtime events, attribution, checkpoints, proposals, results, corrections, and revocations.
- [ ] Assign classification, redaction, privacy, retention, correction, publication, and destination-policy ownership.
- [ ] Prove Bridge transport cannot create authority or canonical status.
- [ ] Prove QSO-STUDIO and AionUi remain read-only unless a separately approved action contract is used.
- [ ] Add runtime → Bridge → interface fixtures for integrity, redaction, stale/corrected evidence, offline display, and denied approval inference.

## P3 — Resource and replay governance

- [ ] Define common units for CPU, memory, storage, message count, event count, duration, retries, and experiment budget.
- [ ] Bind every run to local hard limits and any stricter Repository `1` capability limits.
- [ ] Define wall-clock, monotonic-clock, causal-order, sequence, nonce, expiry, and restart-safe replay semantics.
- [ ] Add exhaustion, boundary, clock-skew, restart, replay-window, and resource-accounting fixtures.

## P4 — Four-QSO experiment readiness

- [ ] Complete P0–P3 blockers.
- [ ] Approve deterministic seeds, accepted genome and record fixtures, resource ceilings, stop conditions, and human review gates.
- [ ] Keep all generated proposals inactive and non-executable.
- [ ] Produce append-only run, event, attribution, checkpoint, freeze, rollback, and cleanup evidence.
- [ ] Repeat the experiment and prove deterministic or explicitly bounded nondeterministic behavior.
- [ ] Conduct independent review before any capability claim or reuse.

## P4 — Documentation and publication

- [ ] Keep README, Pages, architecture, design contracts, obstruction ledger, task chain, release plan, deployment plan, and changelog aligned.
- [ ] Pass exact-head strict MkDocs build and local-link validation.
- [ ] Review Mermaid rendering, headings, navigation, keyboard access, contrast, tables, code blocks, mobile layout, and reduced motion.
- [ ] Approve privacy, confidentiality, licensing, attribution, and public-artifact rules.
- [ ] Retain source, dependency, built-site, manifest, and SHA-256 evidence.
- [ ] Publish Pages only after explicit approval and test public rollback.

## P5 — Release, emergency stop, and recovery

- [ ] Produce one release manifest containing source identities, contract versions, fixtures, tests, artifacts, SBOM where applicable, reviews, approvals, denied capabilities, incident contacts, and rollback.
- [ ] Run a portfolio tabletop covering runtime freeze, Fabric stop, Repository `1` revocation, Bridge/interface invalidation, evidence preservation, and bounded restart.
- [ ] Prove emergency stop and recovery do not depend on the component being stopped.
- [ ] Require a new immutable head and explicit human approval before resumption.
- [ ] Preserve failed-candidate evidence and never rewrite the incident record.

## Scope boundary

This punch list is documentation and planning. It does not alter runtime code, schemas, tests, credentials, adapters, network access, device control, repository permissions, canonical state, package publication, Pages publication, experiment activation, release, or deployment authority.
