# QSO-FABRIC interface compatibility review

Status: **producer corpus available; independent runtime consumer not yet implemented**

QuantumStateObjects is the candidate local runtime and evidence producer/consumer boundary. QSO-FABRIC draft PR #21 now publishes a synthetic compatibility profile for the two interfaces declared in its ecosystem manifest:

- `qso-event-ledger` using `append-only-json`, schema generation `1.0.0`, idempotent operation, and retry limit `0`;
- `qso-runtime-report` using `json-file`, schema generation `1.0.0`, idempotent operation, and retry limit `0`.

## Immutable producer observation

| Field | Value |
|---|---|
| Repository | `aevespers2/QSO-FABRIC` |
| Pull request | `#21` |
| Producer head | `25036a5cfcea79e204a4660ddd1af09c054935b1` |
| Fixture path | `fixtures/qso-interface-compatibility-v1.json` |
| Fixture Git blob | `143b80448cb4623682669ab8e6a9599239dd5847` |
| Contract | `QSO-INTERFACE-COMPATIBILITY-001@1.0.0` |
| Producer workflow | Interface Compatibility Conformance `29986841042` |
| Retained artifact | `8555344357` |
| Artifact digest | `sha256:09be1df24f4ab8b08708dd521c6720f4c95195d3e4379cecaad6d1a4b026a238` |
| Evidence expiry | October 21, 2026 |

This tuple is an observation of one draft producer generation. It is not an accepted source registry, payload-schema approval, or ecosystem-admission decision.

## Compatibility graph

```mermaid
flowchart LR
    M[QSO-FABRIC manifest declaration]
    C[Producer synthetic compatibility corpus]
    I[Independent QuantumStateObjects evaluator]
    R[Runtime admission profile]
    E[Exact-head retained evidence]
    A[Separate architecture decision]

    M --> C
    C --> I
    I --> R
    I --> E
    R --> A
    E --> A
```

Equivalent prose: the Fabric manifest declares the interface names and coarse protocol properties. The producer corpus expresses a closed synthetic compatibility fact surface. QuantumStateObjects must implement its own evaluator without importing the producer validator, bind the exact producer bytes, and connect the result to the local runtime-admission profile and exact-head evidence. Only a separately governed architecture decision may accept a real interface generation.

## Required independent-consumer behavior

The runtime consumer must:

1. verify the producer repository, pull request, exact head, fixture path, Git blob, and contract generation before semantic parsing;
2. use strict UTF-8 and JSON parsing with duplicate-key and non-finite-number rejection;
3. independently derive all 17 expected case outcomes and the 14 ordered obstruction reasons;
4. reject unknown fields, missing facts, non-Boolean facts, duplicate case identifiers, fact/reason-order drift, and disposition drift;
5. preserve the separation between a compatible synthetic case and runtime admission, Fabric acceptance, Repository `1` reconciliation, merge, release, publication, deployment, or operational authority;
6. retain exact-head evidence and fail closed if the producer tuple moves or expires.

## Unresolved payload-contract obstruction

The producer profile proves compatibility only over declaration-level facts. The portfolio still lacks accepted payload schemas and canonical bytes for:

- event identities, sequence and causal order;
- producer, object, run, policy, genome, capability, and source identities;
- append-only correction and supersession records;
- duplicate, replay, conflict, truncation, and tamper handling;
- report-to-ledger references and completeness claims;
- privacy, classification, retention, redaction, and withdrawal;
- checkpoint, freeze, rollback, recovery, and restored-state verification.

Until those fields are accepted, the runtime must not represent either interface as integration-ready.

## Gluing witnesses required

A later implementation must provide at least these witnesses:

- genome identity → runtime admission → event-ledger record;
- event-ledger record → runtime report → Fabric receipt;
- correction → downstream invalidation → corrected report;
- capability revocation → runtime freeze → final ledger/report evidence;
- rollback checkpoint → restored runtime → independent Repository `1` reconciliation.

## Skill-tree mapping

Applied FYSA-120 capabilities:

- `CAT-012` — technical documentation and developer guidance;
- `CAT-017` — immutable producer-source provenance;
- `CAT-031` — independent conformance implementation and regression testing;
- `CAT-032` — distributed interface composition;
- `CAT-040` — correction, migration, rollback, and recovery planning;
- `CAT-052` — Git-blob and digest provenance;
- `CAT-054` — cross-repository supply-chain verification;
- `CAT-059` — exact-head attestation and retained evidence.

Proposed subdivision: **cross-repository interface differential conformance**, covering independent evaluators, replay/conflict semantics, correction propagation, rollback witnesses, and reason/disposition convergence.

## Authority boundary

```text
producer corpus available
!= independent consumer complete
!= payload schema accepted
!= runtime admission approved
!= Fabric integration approved
!= Repository 1 canonical acceptance
```

This page changes no runtime code, accepted schemas, credentials, network access, repository permissions, canonical state, release status, or deployment authority.
