# Obstruction and gluing analysis

## Purpose and method

QuantumStateObjects sits at the center of several A.L.I.S.T.A.I.R.E. contract paths: declarative genomes become local runtime state, sanitized observations become bounded records, local state produces evidence, and evidence is reviewed or proposed for broader use. Those paths compose safely only when adjacent repositories agree on identity, versioning, canonicalization, authority, failure behavior, correction, and recovery.

This ledger treats each repository as a local capability section and each versioned contract as a gluing map. A compatibility fixture, immutable receipt, or deterministic replay is a witness that two or more local sections agree on their overlap. The terminology is inspired by sheaf and homological reasoning, but this page is an engineering compatibility analysis—not a claim that a complete mathematical cohomology or homology computation has been performed.

## Current role boundary

QuantumStateObjects owns bounded **local runtime semantics and evidence production**. It does not own:

- A.L.I.S.T.A.I.R.E. constitutional governance;
- Repository `0` portable bootstrap, planning, or maintenance orchestration;
- Repository `1` canonical-state, capability, approval, revocation, or recovery authority;
- genome authorship and immutable declarative policy;
- hostile-source retrieval and sanitization;
- portfolio-wide collaboration, publication, payment, credential, merge, release, or deployment authority.

A local runtime transition is therefore not automatically a portfolio decision. Execution success is evidence; it is not canonical acceptance.

## Active obstruction ledger

| ID | Overlap | Obstruction | Consequence | Lowest-scope repair candidate |
|---|---|---|---|---|
| O-01 | QSO-GENOMES ↔ QuantumStateObjects | Genome identity, immutable fields, mutation classes, canonicalization, hash inputs, and lifecycle-version ownership are not yet accepted in one shared contract. | The runtime could instantiate a locally valid object that does not represent the producer's intended genome. | Accept one hash-fixed genome compatibility set with producer and consumer fixtures and explicit migration rules. |
| O-02 | QSO-SEEKER ↔ QuantumStateObjects | A canonical record hash does not by itself establish subject identity, observation freshness, replay domain, correction state, or revocation state. | Stale, replayed, corrected, or wrong-subject evidence could enter runtime state as current fact. | Wrap records in a versioned observation/evidence envelope carrying subject, source, clocks, freshness, replay, correction, revocation, and provenance fields. |
| O-03 | Repository `0` ↔ Repository `1` ↔ QuantumStateObjects | The portable-security route is documented, but the runtime task envelope, capability reference, expected state, expiry, and receipt contract are not machine-accepted here. | Repository `0` proposals could be confused with authority, or a valid capability could be applied to the wrong runtime/configuration head. | Consume only Repository `1`-issued, device/environment/task-scoped capability envelopes bound to immutable runtime and policy identities. |
| O-04 | QuantumStateObjects ↔ QSO-FABRIC ↔ `qsio-kernel` | Runtime lifecycle, message bus, event ledger, checkpoint, freeze, rollback, format registry, and low-level semantic ownership overlap. | Competing implementations may assign different meanings to the same QSO state or transition. | Approve a responsibility split: kernel-level primitives, local runtime semantics, and collaboration semantics each have one owner and conformance suite. |
| O-05 | QuantumStateObjects ↔ Repository `1` | Local append-only events and checkpoints are not the same as canonical portfolio state, but the promotion/reconciliation contract is not accepted. | A local ledger head could be mistaken for an authoritative state transition. | Define immutable evidence receipts and an independent Repository `1` reconciliation decision; never infer acceptance from runtime success. |
| O-06 | QuantumStateObjects ↔ Bridge ↔ QSO-STUDIO/AionUi | Evidence transport, public/read-only presentation, review requests, correction, and redaction lack one accepted envelope. | Interfaces could display incomplete or sensitive evidence as authoritative or current. | Use a transport-neutral evidence envelope with classification, redaction, correction, retention, and authority metadata; interfaces remain non-authoritative. |
| O-07 | Atlas/Nova/Orion/Lyra ↔ QSO-GENOMES | Role names exist in runtime documentation, while authoritative identity and policy artifacts remain upstream and unaccepted. | Documentation labels could drift from genome identity or imply active autonomous agents. | Treat local names as fixtures until accepted genome references and runtime receipts bind them. |
| O-08 | Runtime ↔ persisted evidence | Event, attribution, checkpoint, message, and rollback records require one canonical serialization and exact type system. | Equivalent logical state may hash differently, or malformed persisted data may pass one component and fail another. | Pin canonical JSON or another approved encoding, reject duplicate keys and non-finite values, and publish cross-language golden fixtures. |
| O-09 | Runtime ↔ security policy | Prompt injection, hostile metadata, Unicode ambiguity, filenames, comments, and cross-repository documents can enter parser and review paths. | Untrusted content could be treated as instruction or alter authority interpretation. | Preserve raw/canonical hashes, quarantine hostile fields, separate data from instructions, and require issue #8 adversarial fixtures. |
| O-10 | Runtime ↔ clocks/replay | Sequence numbers, wall clocks, monotonic clocks, expiry, causal ordering, and restart behavior are not unified across messages, records, capabilities, and receipts. | Replays, stale tasks, and reordered evidence may be accepted inconsistently. | Define clock domains, nonce/replay keys, causal links, expiry rules, and restart-safe replay storage. |
| O-11 | Freeze/Quietus/revocation/recovery | Repository-local freeze and rollback terms do not yet glue to Fabric freeze, Repository `1` revocation, portfolio emergency stop, or bounded restart. | One subsystem may resume while another remains revoked or uncertain. | Define one cross-repository stop-state lattice and a fail-closed restart witness covering capability revocation, evidence preservation, and human recovery approval. |
| O-12 | Resource governance | Runtime limits, Fabric experiment budgets, Repository `1` capabilities, and host/device limits may describe different units and ceilings. | A locally bounded operation can exceed a portfolio or device-level budget. | Bind every run to versioned resource units, hard ceilings, accounting receipts, and independent enforcement boundaries. |
| O-13 | Correction and contradiction | Runtime evidence is append-only, but correction, supersession, contradiction, and downstream cache invalidation are not portfolio-wide contracts. | Consumers may continue using invalidated evidence or silently overwrite history. | Use compensating records with explicit `supersedes`, `contradicts`, `revokes`, and affected-consumer references. |
| O-14 | Privacy and retention | Runtime events, prompts, observations, identities, and checkpoints may include sensitive data, but classification and retention ownership remain unresolved. | Pages artifacts, CI logs, fixtures, or review interfaces could expose data beyond its purpose. | Approve a data-classification, minimization, redaction, retention, deletion, and public-artifact policy before external fixtures. |
| O-15 | Draft implementation lineages | PR #7, security/preflight candidates, format candidates in Fabric, and accepted `main` are separate evidence states. | Historical passing runs can be misapplied to a new or combined head. | Reconcile normally, preserve lineage, test one exact integrated head, and require approved merged-head evidence. |
| O-16 | Release and authority | Runtime verification, documentation success, interface review, and external execution are separate gates, but no single accepted release bundle joins them. | A partial success could be represented as package, experiment, or system readiness. | Require a release manifest containing source identities, contract versions, tests, artifacts, reviews, approvals, rollback, and denied capabilities. |

## Pairwise gluing maps

| Edge | Required producer output | Required consumer proof | Fail-closed behavior |
|---|---|---|---|
| QSO-GENOMES → QuantumStateObjects | Immutable genome artifact, schema/canonicalization version, lineage, policy and content digest | Local validation against accepted golden fixtures without importing producer code | Reject before object creation |
| QSO-SEEKER → QuantumStateObjects | Sanitized canonical record inside an observation envelope | Subject, provenance, freshness, replay, correction, classification, and content-hash validation | Reject before state mutation |
| Repository `0` → Repository `1` | Non-authoritative proposal and evidence envelope | Quarantine admission, identity, policy, freshness, expected-head, and approval checks | Retain proposal as unapproved evidence |
| Repository `1` → QuantumStateObjects | Narrow expiring capability and accepted task envelope | Exact runtime/configuration/policy/device/environment binding | Do not start or mutate runtime |
| QuantumStateObjects → QSO-FABRIC | Versioned inactive proposals, events, attribution, checkpoints, and result hashes | Fabric schema, identity, resource, lifecycle, and authority validation | Preserve local state and record rejection |
| QuantumStateObjects → Bridge | Classified evidence envelope and transport intent | Integrity, redaction, version, destination, and authority validation | Keep evidence local |
| Bridge → QSO-STUDIO/AionUi | Read-only review projection with provenance and current correction status | Interface validates integrity and never infers approval from display or interaction | Display uncertainty or reject |
| QuantumStateObjects → Repository `1` | Execution receipt and resulting-state evidence | Independent reconciliation, policy, capability, correction, and expected-state checks | Execution remains non-canonical |

## Required triple-overlap witnesses

Pairwise agreement is insufficient where three components can each make locally valid but globally incompatible decisions. The following witness groups are mandatory before operational integration.

### Genome → runtime → Fabric

The same immutable genome identity, policy digest, lifecycle version, and role must produce compatible runtime state and Fabric collaboration records. Fixtures must cover accepted, unsupported-version, mutated-immutable-field, lineage-mismatch, and rollback cases.

### Seeker → temporal interpretation → runtime

A sanitized record must retain one subject identity, source identity, temporal interval, freshness result, replay key, correction state, and uncertainty meaning through `datarepo-temporal-invariants` and runtime ingestion. Fixtures must cover stale, reordered, ambiguous-clock, corrected, revoked, and wrong-subject records.

### Repository `0` → Repository `1` → runtime

A Repository `0` proposal remains non-authoritative until Repository `1` issues a capability and accepted task envelope. Fixtures must cover missing authority, wrong device/environment, wrong runtime head, expiry, replay, partial execution, revocation during execution, rollback, and receipt rejection.

### Runtime → Fabric → Repository `1`

A successful local run and accepted Fabric collaboration result must not become canonical state without independent Repository `1` reconciliation. Fixtures must prove separation among execution success, collaboration acceptance, canonical acceptance, and later correction.

### Runtime → Bridge → interface

Evidence must preserve identity, integrity, classification, redaction, correction, and authority status across transport and presentation. Fixtures must prove that display, annotation, or user interaction does not mutate canonical state or manufacture approval.

### Freeze → revocation → recovery

A runtime freeze, Fabric stop, Repository `1` capability revocation, and portfolio emergency stop must converge on a fail-closed state. Restart requires preserved evidence, resolved cause, fresh capabilities, exact-state verification, and explicit human approval.

## Repair sequence

1. Reconcile and accept one QuantumStateObjects runtime lineage.
2. Approve ownership for kernel, runtime, Fabric, genome, evidence, and canonical-state semantics.
3. Freeze one canonical serialization and identity vocabulary.
4. Accept the Repository `0` → Repository `1` task/capability route and runtime envelope.
5. Accept genome and observation-envelope compatibility sets.
6. Implement identical cross-repository positive, negative, stale, replay, correction, revocation, freeze, and rollback fixtures.
7. Validate pairwise and triple-overlap witnesses at immutable commits.
8. Perform an emergency-stop and bounded-recovery tabletop exercise.
9. Produce one release evidence bundle and explicit approval record.

## Documentation-only boundary

This analysis identifies compatibility work and recommends the lowest-coupling repairs. It does not select canonical schema owners, activate adapters, issue capabilities, modify runtime code, approve PR #7, publish Pages, run the four-QSO experiment, or authorize merge, release, deployment, credentials, payments, device control, or canonical-state mutation.
