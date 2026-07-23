# ADR-0001: Preserve ecosystem interface semantic separation

- **Status:** Proposed
- **Date:** 2026-07-23
- **Decision type:** Documentation and architecture boundary
- **Authority effect:** None

## Context

QSO-FABRIC candidate manifest `qso.manifest.json` at commit `738cf25aec9b2bae0b71c50374585bab36934ef3` declares itself producer of `qso-event-ledger` and `qso-runtime-report`. QuantumStateObjects independently owns candidate runtime-local event evidence and execution-report semantics.

The same interface names therefore cover multiple producer and record-class candidates without an accepted namespace, envelope, schema owner, idempotency identity, correction model, or migration policy.

## Decision

Until a portfolio architecture decision resolves the collision:

1. treat the interface profile as `BLOCKED_ROLE_COLLISION`;
2. preserve runtime-local events, Fabric collaboration events, runtime execution reports, Fabric aggregate reports, Bridge artifacts, interface projections, and Repository `1` dispositions as separate record classes;
3. require explicit producer and semantic-class identity before any consumer claims compatibility;
4. require pairwise and triple-overlap fixtures before implementation or admission;
5. prohibit runtime or Fabric success, transport, display, or schema-version equality from implying canonical acceptance or authority;
6. preserve old evidence and require explicit migration, consumer rebinding, correction, revocation, and rollback records.

This ADR does not select separate names, qualified names, or a shared partitioned envelope. That choice remains pending.

## Consequences

### Positive

- prevents ledger and report semantic collapse;
- exposes the producer-role conflict before implementation;
- gives maintainers a bounded review and fixture plan;
- keeps transport, display, reconciliation, and authority states separate;
- makes migration and rollback responsibilities visible.

### Costs

- ecosystem integration remains blocked;
- current interface names cannot be treated as sufficient contracts;
- producers and consumers need additional fixtures and governance decisions;
- mixed-version behavior cannot be inferred from schema-version equality.

## Alternatives considered

### Accept current names as globally canonical

Rejected for now because the manifest does not distinguish runtime-local and Fabric-level records.

### Let each repository interpret the names independently

Rejected because local validity would not guarantee cross-repository gluing or rollback.

### Import the QSO-FABRIC validator into every consumer

Rejected because shared code would not prove independent interpretation and could create a validator monoculture.

## Required follow-up decision

Architecture review must approve one of:

- separate interface names;
- qualified interface names;
- a shared envelope with mandatory producer and semantic-class partitioning.

It must also assign registry, schema, canonicalization, signing, trusted-time, correction, migration, consumer-registration, incident, recovery, and rollback custody.

## Skill-tree mapping

This ADR maps planning work to `CAT-012/012-B`, `CAT-017/017-C`, `CAT-031/031-A`, `CAT-040/040-D`, `CAT-054/054-A`, and `CAT-059/059-B`. Selection does not establish competence or authority.
