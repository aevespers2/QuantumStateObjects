# ADR-0001: Preserve ecosystem interface semantic separation

- **Status:** Proposed
- **Date:** 2026-07-23
- **Decision type:** Documentation and architecture boundary
- **Authority effect:** None

## Context

QSO-FABRIC PR #21 at exact head `25036a5cfcea79e204a4660ddd1af09c054935b1` provides the synthetic `QSO-INTERFACE-COMPATIBILITY-001@1.0.0` corpus for `qso-event-ledger` and `qso-runtime-report`. The producer fixture is identified by Git blob `143b80448cb4623682669ab8e6a9599239dd5847`; its exact-head workflow and retained evidence are recorded in the source tuple.

QuantumStateObjects now carries that exact fixture and tuple, but an independent consumer implementation is not yet present. More importantly, the corpus evaluates declaration-level compatibility facts rather than final payload schemas. QuantumStateObjects independently owns candidate runtime-local event evidence and execution-report semantics, while QSO-FABRIC owns candidate collaboration and aggregate-run semantics.

The same coarse interface names therefore still cover multiple producer and record-class candidates without accepted payload schemas, namespace ownership, canonicalization, idempotency identities, correction behavior, or migration policy.

## Decision

Until a portfolio architecture decision and independent conformance evidence resolve the boundary:

1. classify the current state as `PRODUCER_CORPUS_BOUND_CONSUMER_AND_PAYLOAD_PENDING`;
2. preserve runtime-local events, Fabric collaboration events, runtime execution reports, Fabric aggregate reports, Bridge artifacts, interface projections, and Repository `1` dispositions as separate record classes;
3. recognize the copied fixture and source tuple as evidence inputs, not accepted interfaces;
4. require a separately implemented QuantumStateObjects consumer to reproduce all 17 case outcomes and 14 ordered reasons;
5. require payload-level pairwise and triple-overlap fixtures before runtime admission or Fabric integration;
6. prohibit runtime or Fabric success, transport, display, byte identity, or schema-version equality from implying canonical acceptance or authority;
7. preserve old evidence and require explicit migration, consumer rebinding, correction, revocation, supersession, withdrawal, and rollback records.

This ADR does not select separate names, qualified names, or a shared partitioned envelope. It also does not accept either payload schema. Those choices remain pending.

## Consequences

### Positive

- reconciles the producer-corpus and local-documentation lineages without discarding either;
- prevents ledger and report semantic collapse;
- distinguishes source binding from independent consumer completion;
- exposes payload-schema and namespace ownership before implementation;
- gives maintainers a bounded fixture, migration, and rollback plan;
- keeps transport, display, reconciliation, and authority states separate.

### Costs

- ecosystem integration remains blocked;
- current interface names and synthetic cases are insufficient as payload contracts;
- a second implementation and payload fixtures are required;
- mixed-version behavior cannot be inferred from version equality;
- source-tuple movement must trigger documentation and consumer revalidation.

## Alternatives considered

### Treat producer-corpus success as interface acceptance

Rejected because the corpus intentionally ends at `COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL` and does not define complete payload bytes.

### Accept current names as globally canonical

Rejected for now because the current profile does not distinguish runtime-local and Fabric-level record semantics.

### Let each repository interpret the names independently

Rejected because local validity would not guarantee cross-repository gluing, correction propagation, or rollback.

### Import the QSO-FABRIC validator into every consumer

Rejected because shared code would not prove independent interpretation and could create a validator monoculture.

## Required follow-up decisions

Architecture review must approve:

- separate interface names, qualified names, or a shared envelope with mandatory producer and semantic-class partitioning;
- ledger and report payload-schema ownership;
- producer, consumer, subject, run, semantic-class, idempotency, canonicalization, and hash identities;
- correction, revocation, supersession, withdrawal, replay, retention, migration, and rollback semantics;
- registry, signing, key, trusted-time, consumer-registration, incident, recovery, and publication custody.

## Skill-tree mapping

This ADR maps planning work to `CAT-012/012-B`, `CAT-017/017-C`, `CAT-031/031-A`, `CAT-040/040-D`, `CAT-054/054-A`, and `CAT-059/059-B`. Selection does not establish competence, interface acceptance, or authority.
