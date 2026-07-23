# Ecosystem interface compatibility review checklist

Use this checklist before accepting, implementing, consuming, migrating, publishing, or releasing either `qso-event-ledger` or `qso-runtime-report`.

Current bounded disposition: `PRODUCER_CORPUS_BOUND_CONSUMER_AND_PAYLOAD_PENDING`.

## Source identity

- [x] QSO-FABRIC PR #21 source tuple identifies exact head `25036a5cfcea79e204a4660ddd1af09c054935b1`.
- [x] Producer fixture path and Git blob are fixed as `fixtures/qso-interface-compatibility-v1.json` and `143b80448cb4623682669ab8e6a9599239dd5847`.
- [x] Producer workflow run, retained artifact, digest, and expiration are recorded.
- [x] QuantumStateObjects carries a byte-identical producer fixture and machine-readable source tuple.
- [ ] An independent consumer implementation validates the fixture without importing producer validation code.
- [ ] Any superseding tuple identifies the prior tuple, reason, affected consumers, and correction path.

## Producer corpus

- [x] Contract is `QSO-INTERFACE-COMPATIBILITY-001@1.0.0`.
- [x] Corpus contains 17 cases, 14 facts, and 14 ordered obstruction reasons.
- [x] Positive cases derive `COMPATIBLE_PENDING_ARCHITECTURE_APPROVAL`.
- [x] Adverse cases derive `BLOCKED` with reasons in canonical order.
- [ ] Independent runtime consumer reproduces every expected disposition and ordered reason set.
- [ ] Producer and consumer exact-head evidence remain independently retained and available.

## Namespace and ownership

- [ ] One accepted registry generation owns interface names.
- [ ] Runtime-local and Fabric collaboration ledgers cannot share an ambiguous sequence space.
- [ ] Runtime execution reports and Fabric aggregate reports have distinct semantic classes.
- [ ] Producer, consumer, subject, run, schema, canonicalization, and payload identities are mandatory.
- [ ] Repository `1` disposition remains a separate record and authority boundary.
- [ ] Bridge, QSO-STUDIO, and AionUi cannot promote transport or display into approval.

## Protocol and payload schemas

- [ ] `append-only-json` defines record boundaries, ordering, canonicalization, hash chaining, correction, supersession, withdrawal, and truncation behavior.
- [ ] `json-file` defines complete report shape, canonicalization, content identity, ledger references, partial failure, cleanup, uncertainty, and rollback fields.
- [ ] `idempotent: true` identifies the idempotency key and duplicate outcome.
- [ ] `retry_limit: 0` prohibits automatic replay but permits explicit correction and recovery records.
- [ ] Boolean values do not satisfy integer fields.
- [ ] Duplicate keys, non-finite numbers, lone surrogates, unknown fields, unsupported versions, malformed hashes, and ambiguous identities fail closed.
- [ ] Privacy classification, redaction, retention, deletion, and withdrawal behavior are accepted.

## Compatibility fixtures

- [ ] Runtime-local event-ledger payload fixture passes.
- [ ] Fabric collaboration-ledger payload fixture passes.
- [ ] Runtime execution-report payload fixture passes.
- [ ] Fabric aggregate-report payload fixture passes.
- [ ] Producer/semantic-class mismatch fails before mutation.
- [ ] Sequence gap, reorder, truncation, replay, duplicate delivery, conflict, and wrong previous hash behave as specified.
- [ ] Unsupported schema and canonicalization versions fail closed.
- [ ] Correction, revocation, supersession, withdrawal, and cache invalidation fixtures pass.
- [ ] Runtime success and Fabric acceptance cannot satisfy Repository `1` reconciliation.

## Triple-overlap witnesses

- [ ] Genome identity → runtime admission → event-ledger record.
- [ ] Event-ledger record → runtime report → Fabric receipt.
- [ ] Correction → downstream invalidation → corrected report.
- [ ] Capability revocation → runtime freeze → final ledger/report evidence.
- [ ] Rollback checkpoint → restored runtime → Repository `1` reconciliation.
- [ ] Runtime evidence → Bridge transport → QSO-STUDIO/AionUi projection.

## Migration and rollback

- [ ] Old and new producers are tested independently.
- [ ] Old and new consumers are tested independently.
- [ ] Supported and unsupported mixed-version combinations are explicit.
- [ ] Failed or withdrawn generations remain preserved.
- [ ] Consumer rebinding is recorded before currentness is restored.
- [ ] Rollback returns every controlled consumer to the last accepted registry generation.
- [ ] Post-rollback integrity, cache, projection, and authority-separation checks pass.

## Documentation and accessibility

- [x] Human-readable compatibility page and machine-readable documentation profile are present.
- [x] Mermaid diagram has an equivalent prose explanation.
- [x] Status is not communicated only through color, position, icons, or animation.
- [x] Interface declarations, source evidence, unresolved payload fields, gluing witnesses, and authority limits are documented.
- [ ] README, Pages navigation, design contracts, task chain, punch list, release plan, and changelog remain aligned after every source movement.
- [ ] Rendered Pages output passes heading, keyboard, contrast, table, code, mobile, and reduced-motion review.

## Governance and release

- [ ] Namespace and payload-schema owners are appointed.
- [ ] Canonicalization, signing, key custody, trusted time, migration, correction, revocation, retention, incident, recovery, and rollback owners are appointed.
- [ ] Independent producer and consumer conformance evidence exists.
- [ ] Security, privacy, licensing, legal, and accessibility review is complete.
- [ ] Resulting default branches and generated documentation artifacts are independently verified.
- [ ] Architecture, merge, release, publication, and deployment approvals are separately recorded.

## Fail-closed conclusion

Producer-corpus availability and documentation validation do not complete the independent consumer or payload contracts. Until every applicable item is satisfied, the interface remains blocked from runtime admission, Fabric integration, ecosystem acceptance, merge, release, publication, deployment, and operational use.
