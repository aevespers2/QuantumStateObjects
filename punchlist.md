# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates. Checked implementation work is candidate evidence only; it does not authorize merge, release, deployment, or runtime activation.

## Immediate

- [x] **Select one canonical CLI/configuration candidate.** PR #7 is the sole selected path; superseded candidates remain outside P0.
- [x] **Verify the current submitted exact head.** Run `29657511858` passed the Python 3.11 and 3.13 matrix at head `291d7419bf29a3d979762c4655c05a2a672c6f82` with 150 tests and retained artifacts.
- [x] **Enforce strict UTF-8 JSON and reject Boolean schema versions.** Configuration and genome bytes use strict UTF-8 decoding, and schema versions must be integer `1` rather than Boolean truthy values.
- [x] **Enforce the published required instance fields and canonical instance IDs.** Identity, development, review, status, and lower-case instance-ID contracts are checked before runtime acceptance.
- [ ] **Remove the retired Aequitas runtime dependency.** Replace `sprite_review.sprite == "aequitas"` and its activation rule with the accepted Jacob Thomas Redmond human-review authority contract, preserve human final approval, and add negative tests proving retired identity aliases cannot resolve through configuration, runtime, evidence, or release paths.
- [ ] **Require canonical repository-field shape.** Validate repository references against the accepted object/string contract consistently across configuration, evidence, and downstream fixtures.
- [ ] **Require singleton message allowlists where the schema requires one value.** Reject extra allowed senders, recipients, or message kinds rather than silently widening authority.
- [ ] **Correct `max_records` default handling.** Preserve an explicit zero where allowed, reject Boolean/non-integer values, and do not replace caller intent through truthiness defaults.
- [ ] **Add complete configuration enum guards.** Reject unsupported lifecycle, status, edit-mode, review-state, and other enum-like values before constructing runtime state.
- [ ] **Add message-kind guards.** Reject unknown incoming and outgoing kinds before queueing, ledger mutation, or evidence emission.
- [ ] **Validate outgoing recipients against the canonical instance set.** No message may target an unknown, alias-only, or retired identity.
- [ ] **Reject malformed incoming-message shape atomically.** Validate required fields, exact key set, sizes, identities, kind, and provenance before changing queues, counters, or ledgers.
- [ ] **Wrap bounded file-read failures consistently.** Convert operating-system, decoding, size, type, and path failures into the published fail-closed configuration/runtime error taxonomy without leaking partial state.
- [ ] **Make ingest failures atomic.** Normalize required limits before delegation or restore the pre-operation checkpoint on every delegated ingest exception; prove no unledgered partial mutation remains.
- [ ] **Use one canonical freeze checkpoint.** Freeze certificates, controller checkpoints, resume, high-severity annotation rollback, and message state must hash and restore the same canonical snapshot.
- [ ] **Guarantee rollback at event capacity.** Reserve safety-event capacity or restore state through an invariant-safe path even when `max_events` is full.
- [ ] **Validate persisted event-entry shape strictly.** Reject missing required fields, Boolean/non-integer sequences, unexpected shape, invalid hashes, and non-canonical entries before reporting a ledger as verified.
- [ ] **Resolve every PR #7 review thread and rerun final-head CI.** Retain artifacts and inspect exact checkout, all tests, wheel/source hashes, negative fixtures, and review disposition at one repaired immutable head.
- [ ] **Run merged-head acceptance.** After explicit merge authorization, require clean installation, compilation, complete tests, installed CLI/version/configuration smoke, deterministic evidence, wheel and sdist, checksums, and retained logs at the merged head.
- [ ] Prepare contract-validation tests that consume only accepted, hash-fixed QSO-GENOMES and QSO-SEEKER fixtures.

## Current evidence

- [x] Workflow run `29657511858` completed successfully for exact head `291d7419bf29a3d979762c4655c05a2a672c6f82` on Python 3.11 and 3.13.
- [x] Both jobs used exact submitted-head checkout/assertion, read-only contents permission, and disabled checkout credential persistence.
- [x] Both jobs passed 150 tests with retained runtime evidence.
- [x] Artifact digests: Python 3.11 `b0b302798c234922e9f75323d60da85dd810c957bd4af4922512f1a5aa714388`; Python 3.13 `930f14ed7a411b5d6c36f901c0d80280db093cef2b367e406641e81289da6d49`.
- [ ] Eight current correctness findings remain unresolved: repository-field shape, singleton message allowlists, `max_records` default handling, config enum guards, message-kind guards, outgoing-recipient canonical validation, malformed incoming-message shape, and file-read error wrapping.
- [ ] Additional runtime invariants remain open for atomic ingest, canonical freeze/checkpoint parity, rollback capacity, and strict persisted-event validation.
- [ ] QSO-GENOMES PRs #2, #12, and #13 are not yet reconciled into one accepted compatibility head and cannot supply final trusted hashes.
- [ ] QSO-SEEKER candidates remain unreconciled with current `main` and cannot supply final accepted canonical-record fixtures.
- [ ] Issue #8 hostile-input and prompt-injection hardening remains open.

## After upstream contracts are green

- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, events, and proposal counts.
- [ ] Emit reproducible append-only JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, interruptions, recoveries, rollbacks, and attribution.

## Held behind approval

- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, scheduled execution, and unrestricted repository writes remain out of scope.

## Quality Gates

- [ ] Deterministic runtime tests and documented rollback paths remain valid under malformed inputs and exhausted limits.
- [ ] Security, dependency, workflow, secret, parser/contract, persisted-evidence, and adversarial review pass at accepted exact and merged heads.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.
