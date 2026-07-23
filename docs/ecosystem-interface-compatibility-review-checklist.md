# Ecosystem interface compatibility review checklist

Use this checklist before accepting, implementing, consuming, migrating, publishing, or releasing either `qso-event-ledger` or `qso-runtime-report`.

## Recorded synthetic evidence

- [x] QSO-FABRIC producer head is `25036a5cfcea79e204a4660ddd1af09c054935b1`.
- [x] Producer compatibility corpus Git blob is `143b80448cb4623682669ab8e6a9599239dd5847`.
- [x] Producer Interface Compatibility Conformance run `29986841042` passed.
- [x] Producer artifact `8555344357` is retained with digest `sha256:09be1df24f4ab8b08708dd521c6720f4c95195d3e4379cecaad6d1a4b026a238` through October 21, 2026.
- [x] QuantumStateObjects carries the byte-identical corpus and a separately implemented evaluator.
- [ ] QuantumStateObjects exact-head consumer workflow and resulting artifact are recorded for the final candidate head.

These checks close only the declaration-level synthetic reproduction sub-gate. They do not resolve namespace ownership or payload compatibility.

## Source identity

- [ ] QSO-FABRIC producer repository, commit, path, Git blob, SHA-256, and byte size match the recorded manifest source tuple.
- [ ] The producer corpus repository, pull request, commit, path, Git blob, workflow, artifact, digest, and expiry match the consumer source tuple.
- [ ] The observed manifest, source tuple, and corpus are parsed as strict UTF-8 JSON with duplicate-key and non-finite-number rejection.
- [ ] Any superseding source tuple identifies the prior tuple and correction reason.
- [ ] Producer and consumer evidence are retained independently.

## Namespace and ownership

- [ ] One accepted registry generation owns interface names.
- [ ] Runtime-local and Fabric collaboration ledgers cannot share an ambiguous sequence space.
- [ ] Runtime execution reports and Fabric aggregate reports have distinct semantic classes.
- [ ] Producer, consumer, subject, run, schema, canonicalization, and payload identities are mandatory.
- [ ] Repository `1` disposition remains a separate record and authority boundary.
- [ ] Bridge, QSO-STUDIO, and AionUi cannot promote transport or display into approval.

## Protocol and schema

- [ ] `append-only-json` defines record boundaries, ordering, canonicalization, hash chaining, correction, and truncation behavior.
- [ ] `json-file` defines complete report shape, canonicalization, content identity, partial failure, cleanup, uncertainty, and rollback fields.
- [ ] `idempotent: true` identifies the idempotency key and duplicate outcome.
- [ ] `retry_limit: 0` prohibits automatic replay but permits explicit correction and recovery records.
- [ ] Boolean values do not satisfy integer fields.
- [ ] Duplicate keys, non-finite numbers, lone surrogates, unknown fields, unsupported versions, malformed hashes, and ambiguous identities fail closed.

## Declaration-level corpus

- [x] Both declared interfaces have positive synthetic cases.
- [x] All 14 ordered obstruction reasons are covered.
- [x] Source-tuple, interface, role, protocol, schema, idempotency, retry, default-deny, correction, rollback, evidence, and authority facts fail closed.
- [x] The local consumer rejects fixture-byte, order, field, type, case-identity, disposition, and reason drift.
- [ ] A second independent consumer outside QSO-FABRIC and QuantumStateObjects reproduces the same generation.

## Payload compatibility fixtures

- [ ] Runtime-local event-ledger positive fixture passes.
- [ ] Fabric collaboration-ledger positive fixture passes.
- [ ] Runtime execution-report positive fixture passes.
- [ ] Fabric aggregate-report positive fixture passes.
- [ ] Producer/semantic-class mismatch fails before mutation.
- [ ] Sequence gap, reorder, truncation, replay, duplicate delivery, and wrong previous hash behave as specified.
- [ ] Unsupported schema and canonicalization versions fail closed.
- [ ] Correction, revocation, supersession, and cache invalidation fixtures pass.
- [ ] Runtime success and Fabric acceptance cannot satisfy Repository `1` reconciliation.

## Triple-overlap witnesses

- [ ] Runtime event ledger → Fabric collaboration ledger → Repository `1` reconciliation.
- [ ] Runtime execution report → Fabric aggregate report → Repository `1` disposition.
- [ ] Runtime evidence → Bridge transport → QSO-STUDIO/AionUi display.
- [ ] Correction/revocation → downstream invalidation → bounded recovery.
- [ ] Schema migration → mixed-version consumers → rollback.

## Migration and rollback

- [ ] Old and new producers are tested independently.
- [ ] Old and new consumers are tested independently.
- [ ] Supported and unsupported mixed-version combinations are explicit.
- [ ] Failed or withdrawn generations remain preserved.
- [ ] Consumer rebinding is recorded before currentness is restored.
- [ ] Rollback returns every controlled consumer to the last accepted registry generation.
- [ ] Post-rollback integrity, cache, projection, and authority-separation checks pass.

## Documentation and accessibility

- [ ] Human-readable architecture and machine-readable profile agree.
- [ ] Mermaid diagrams have equivalent prose explanations.
- [ ] Status is not communicated only through color, position, icons, or animation.
- [ ] Interface names, roles, protocol, schema, idempotency, retry, migration, correction, and rollback semantics are documented.
- [ ] README, Pages navigation, design contracts, task chain, punch list, release plan, and changelog are aligned.

## Governance and release

- [ ] Namespace and schema owners are appointed.
- [ ] Canonicalization, signing, key custody, trusted time, migration, correction, revocation, retention, incident, recovery, and rollback owners are appointed.
- [ ] Independent producer and consumer conformance evidence exists for the accepted payload generation.
- [ ] Security, privacy, licensing, legal, and accessibility review is complete.
- [ ] Resulting default branches and generated documentation artifacts are independently verified.
- [ ] Architecture, merge, release, publication, and deployment approvals are separately recorded.

## Fail-closed conclusion

Until every applicable acceptance item is satisfied, the disposition remains `BLOCKED_ROLE_COLLISION`. Documentation or synthetic validation alone grants no interface acceptance, producer registration, ecosystem admission, capability, execution authority, merge, release, publication, or deployment approval.
