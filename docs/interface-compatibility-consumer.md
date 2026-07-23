# Independent interface-compatibility consumer

## Current source correction

The earlier documentation observation was pinned to QSO-FABRIC head `738cf25aec9b2bae0b71c50374585bab36934ef3`, which predates the producer's machine-readable interface-compatibility corpus. That observation remains useful historical evidence for the manifest generation, but it is not the current compatibility source.

This consumer is bound to the immutable producer tuple below:

| Field | Value |
|---|---|
| Producer repository | `aevespers2/QSO-FABRIC` |
| Producer pull request | `#21` |
| Producer head | `25036a5cfcea79e204a4660ddd1af09c054935b1` |
| Corpus path | `fixtures/qso-interface-compatibility-v1.json` |
| Git blob | `143b80448cb4623682669ab8e6a9599239dd5847` |
| SHA-256 | `baac67caaa6b213e5a50019c8cad011be1e1906699c7903391313b11677ac5d4` |
| Contract | `QSO-INTERFACE-COMPATIBILITY-001@1.0.0` |
| Cases | 17 |

The workflow downloads those exact public bytes from the immutable commit, verifies the raw SHA-256 before parsing, and then evaluates the corpus with a separately authored QuantumStateObjects validator. It does not import QSO-FABRIC or QSO-STUDIO validation code.

## What is independently checked

The consumer rejects invalid UTF-8, duplicate JSON keys, non-finite values, unknown or missing fields, Boolean/type ambiguity, fact-order drift, reason-order drift, duplicate case identities, inconsistent known-interface declarations, incomplete positive or reason coverage, and disposition/reason divergence.

It independently evaluates both `qso-event-ledger` and `qso-runtime-report` across source freshness, interface identity, producer and consumer roles, protocol, schema generation, idempotency, retry behavior, default-deny preservation, correction, rollback, evidence binding, and authority-promotion absence.

```text
raw producer-byte identity
!= semantic compatibility
!= namespace ownership
!= final payload-schema acceptance
!= ecosystem admission
!= execution or canonical-state authority
```

## Architecture and evidence flow

```mermaid
flowchart LR
    Fabric[QSO-FABRIC PR 21\nimmutable producer head] --> Raw[Raw compatibility corpus]
    Raw --> Hash[SHA-256 gate\nbefore parsing]
    Hash --> Consumer[QuantumStateObjects\nindependent validator]
    Consumer --> Results[Ordered reasons and dispositions]
    Results --> Evidence[Exact-head retained evidence]
    Evidence --> Review[Human architecture review]
    Review -. no automatic authority .-> Blocked[No admission, execution, merge, release, publication, or deployment]
```

In prose: the workflow retrieves one immutable producer artifact, verifies its byte identity before any semantic processing, evaluates it with an independent implementation, and retains exact-head evidence. A successful result means only that the consumer converges on the proposed synthetic compatibility surface.

## Skill-tree mapping

- `CAT-012` — API and lifecycle documentation, navigation, and ambiguity control;
- `CAT-017` — immutable source tuples, raw-byte identity, derivation, and supersession;
- `CAT-031` — independent invariant implementation and hostile regression testing;
- `CAT-032` — distributed interface composition and producer/consumer boundaries;
- `CAT-040` — correction, migration, consumer rebinding, and rollback readiness;
- `CAT-052` — cryptographic provenance;
- `CAT-054` — cross-repository supply-chain integrity;
- `CAT-059` — exact-head attestation and evidence transport.

Proposed subdivision: **cross-repository interface differential conformance**, covering raw source binding, independently implemented semantics, replay/conflict behavior, correction propagation, rollback witnesses, and ordered reason/disposition convergence.

## Remaining blockers

This evidence does not resolve the documented role and namespace collision. Architecture review still must approve final interface names or qualification, payload schemas, canonical bytes, producer and semantic-class identities, ordering, duplicate/conflict and retry semantics, correction and revocation behavior, retention, signatures, trusted time, consumer registration, migration, rollback, recovery, privacy, licensing, security, accessibility, and resulting-default-branch validation.
