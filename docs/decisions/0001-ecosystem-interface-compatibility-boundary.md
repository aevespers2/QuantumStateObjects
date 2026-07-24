# ADR-0001: Preserve ecosystem interface semantic separation

- **Status:** Proposed
- **Date:** 2026-07-23
- **Decision type:** Documentation and architecture boundary
- **Authority effect:** None

## Context

QSO-FABRIC candidate manifest `qso.manifest.json` at commit `25036a5cfcea79e204a4660ddd1af09c054935b1` declares itself producer of `qso-event-ledger` and `qso-runtime-report`. QuantumStateObjects independently owns candidate runtime-local event evidence and execution-report semantics.

QSO-FABRIC also publishes the declaration-level `QSO-INTERFACE-COMPATIBILITY-001@1.0.0` synthetic corpus at Git blob `143b80448cb4623682669ab8e6a9599239dd5847`. QuantumStateObjects now carries the exact bytes and a separately implemented evaluator. This establishes independent agreement with the proposed 17-case fact/reason surface at one recorded generation.

The same interface names still cover multiple producer and record-class candidates without an accepted namespace, payload envelope, schema owner, idempotency identity, correction model, or migration policy. Synthetic agreement does not resolve that semantic collision.

## Decision

Until a portfolio architecture decision resolves the collision:

1. treat the real interface profile as `BLOCKED_ROLE_COLLISION`;
2. record the bounded declaration-level reproduction separately as `EVIDENCE_SATISFIED_AT_RECORDED_SYNTHETIC_TUPLE` only after exact-head consumer evidence passes;
3. preserve runtime-local events, Fabric collaboration events, runtime execution reports, Fabric aggregate reports, Bridge artifacts, interface projections, and Repository `1` dispositions as separate record classes;
4. require explicit producer and semantic-class identity before any consumer claims payload compatibility;
5. require pairwise payload fixtures and triple-overlap witnesses before implementation or admission;
6. prohibit runtime or Fabric success, transport, display, matching names, matching schema versions, or synthetic conformance from implying canonical acceptance or authority;
7. preserve old evidence and require explicit migration, consumer rebinding, correction, revocation, and rollback records.

This ADR does not select separate names, qualified names, or a shared partitioned envelope. That choice remains pending.

## Consequences

### Positive

- prevents ledger and report semantic collapse;
- exposes the producer-role conflict before payload implementation;
- preserves the useful independent synthetic consumer without promoting it into architecture acceptance;
- gives maintainers a bounded payload-fixture and gluing-witness plan;
- keeps transport, display, reconciliation, and authority states separate;
- makes migration and rollback responsibilities visible.

### Costs

- ecosystem integration remains blocked;
- current interface names cannot be treated as sufficient contracts;
- producers and consumers need payload schemas and additional fixtures;
- mixed-version behavior cannot be inferred from schema-version equality;
- any change to the producer tuple or consumer evidence reopens the synthetic sub-gate.

## Alternatives considered

### Accept current names as globally canonical

Rejected for now because the manifest does not distinguish runtime-local and Fabric-level records.

### Let each repository interpret the names independently

Rejected because local validity would not guarantee cross-repository gluing or rollback.

### Import the QSO-FABRIC validator into every consumer

Rejected because shared code would not prove independent interpretation and could create a validator monoculture.

### Treat independent synthetic agreement as payload compatibility

Rejected because the corpus evaluates declaration-level facts rather than canonical event and report bytes, identities, ordering, correction, or recovery behavior.

## Required follow-up decision

Architecture review must approve one of:

- separate interface names;
- qualified interface names;
- a shared envelope with mandatory producer and semantic-class partitioning.

It must also assign registry, payload-schema, canonicalization, signing, trusted-time, correction, migration, consumer-registration, incident, recovery, and rollback custody.

## Skill-tree mapping

This ADR maps planning and validation work to `CAT-012/012-B`, `CAT-017/017-C`, `CAT-031/031-A`, `CAT-032`, `CAT-040/040-D`, `CAT-044`, `CAT-054/054-A`, and `CAT-059/059-B`. Proposed subdivision `031-H` covers independent interface differential conformance; proposed `032-F` covers semantic partitioning and distributed interface gluing. Selection does not establish competence or authority.
