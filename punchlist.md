# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [x] **Select one canonical CLI/configuration candidate.** PR #7 is the sole selected path; superseded candidates are closed without merge and draft PR #3 remains outside P0.
- [x] **Reconcile PR #7 with current `main` without rewriting reviewed history.** Head `395915b60510e9a62c53ad128cf23d151e73eb1f` is a normal two-parent merge, mergeable, and zero commits behind `main`.
- [x] **Verify the reconciled exact head.** Run `29617877793` passed Python 3.11/3.13 installation, compilation, 22 tests, installed CLI/configuration smoke, wheel construction, checksum generation, and retained-artifact upload.
- [x] **Add one bounded runtime-primitives verification slice.** Synthetic local tests cover lifecycle, message validation, event/attribution ledgers, resource limits, freeze, interruption, recovery, rollback, checkpoints, and deterministic state/event hashes.
- [ ] **Enforce strict UTF-8 JSON.** Decode bounded configuration and genome bytes with strict UTF-8 before `json.loads`; add UTF-16/UTF-32 negative fixtures.
- [ ] **Enforce all schema-required instance fields.** Reject manifests missing required identity, development, review, or status blocks before constructing an accepted runtime manifest.
- [ ] **Reject Boolean schema versions.** Require `type(value) is int` and value `1` for instance and genome schema versions.
- [ ] **Enforce canonical instance IDs.** Require the published lower-case `^[a-z][a-z0-9-]{2,127}$` pattern before emitting configuration or runtime evidence.
- [ ] **Make ingest failures atomic.** Normalize required limits before delegation or restore the pre-operation checkpoint on every delegated ingest exception; prove no unledgered partial mutation remains.
- [ ] **Use one canonical freeze checkpoint.** Freeze certificates, controller checkpoints, resume, high-severity annotation rollback, and message state must hash and restore the same canonical snapshot.
- [ ] **Guarantee rollback at event capacity.** Reserve safety-event capacity or restore state through an invariant-safe path even when `max_events` is full.
- [ ] **Validate persisted event-entry shape strictly.** Reject missing required fields, Boolean/non-integer sequences, unexpected shape, invalid hashes, and non-canonical entries before reporting a ledger as verified.
- [ ] **Resolve every PR #7 review thread and rerun final-head CI.** Retain artifacts and inspect exact checkout, all tests, wheel/source hashes, negative fixtures, and review disposition at the repaired immutable head.
- [ ] **Run merged-head acceptance.** After explicit merge authorization, require clean installation, compilation, complete tests, installed CLI/version/configuration smoke, deterministic evidence, wheel and sdist, checksums, and retained logs at the merged head.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that consume only accepted, hash-fixed QSO-GENOMES and QSO-SEEKER fixtures.

## Current evidence

- [x] Workflow run `29617877793` completed successfully for exact head `395915b60510e9a62c53ad128cf23d151e73eb1f` on Python 3.11 and 3.13.
- [x] Both jobs used exact submitted-head checkout/assertion, read-only contents permission, and disabled checkout credential persistence.
- [x] Both jobs passed 22 tests with zero failures, errors, or skips and retained JUnit, CLI/configuration, version, checked-out-SHA, wheel, and checksum evidence.
- [x] Artifact digests: Python 3.11 `c53ecc7692716519be67c92e4e51cc04695187437790c784d8b42f78d70a76fd`; Python 3.13 `cf2290f7469b71ebb92cc7b1cb7eb86a64ee9ff56df8b89203fa157bd6b65816`.
- [x] Wheel SHA-256: Python 3.11 `97c6ec287e2eb1b23776dc232a16641f566202f1aacf792755a992930adf5dc3`; Python 3.13 `b074c2328f90585c2fe8fb7a83d023ef34ea7374b6ee9915c57209d589e678cc`.
- [ ] Eight P2 correctness threads remain unresolved: three configuration/parser findings plus atomic ingest recovery, canonical freeze/checkpoint parity, rollback capacity, instance-ID schema parity, and strict event-entry validation.
- [ ] QSO-GENOMES PR #2 remains unaccepted and cannot yet supply a trusted Atlas hash-pinned fixture.

## After upstream contracts are green

- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, events, and proposal counts.
- [ ] Emit reproducible append-only JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, interruptions, recoveries, rollbacks, and attribution.

## Held behind approval

- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, scheduled execution, and unrestricted repository writes are out of scope.

## Quality Gates

- [ ] Deterministic runtime tests and documented rollback path remain valid under malformed inputs and exhausted limits.
- [ ] Security, dependency, workflow, secret, parser/contract, persisted-evidence, and adversarial review pass at accepted exact and merged heads.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.
