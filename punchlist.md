# QSOBuilder Punch List

Policy binding: `QSO-CONSENT-CAPACITY-LOCK-v1`; explicit consent and capacity review remain required for every covered human/AI interaction and fail closed on ambiguity or withdrawal.

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates. Checked implementation work is candidate evidence only; it does not authorize merge, release, deployment, or runtime activation.

## Immediate

- [x] **Select one canonical CLI/configuration candidate.** PR #7 is the sole selected path; superseded candidates remain outside P0.
- [x] **Reconcile the current consent-lock base without rewriting reviewed history.** PR #17 merged `main@40efcbf8ce2bda7d6b05b3fb1f3ccf0384facc51` into the focused repair branch as the true dual-parent merge `e4df1a886eb8529da6b28525e64e06ec0aaab1ea`.
- [x] **Enforce strict UTF-8 JSON and reject Boolean schema versions.** Configuration and genome bytes use strict UTF-8 decoding, and schema versions must be integer `1` rather than Boolean truthy values.
- [x] **Enforce the published required instance fields and canonical instance IDs.** Identity, development, review, status, and lower-case instance-ID contracts are checked before runtime acceptance.
- [ ] **Remove the retired Aequitas runtime dependency.** Replace `sprite_review.sprite == "aequitas"` and its activation rule with the accepted human-review authority contract, preserve human final approval, and add negative tests proving retired identity aliases cannot resolve through configuration, runtime, evidence, or release paths.
- [ ] **Require canonical repository-field shape.** Validate repository references against the accepted object/string contract consistently across configuration, evidence, and downstream fixtures.
- [ ] **Require singleton message allowlists where the schema requires one value.** Reject strings and malformed collections rather than splitting them into character-level permissions.
- [ ] **Correct `max_records` default handling.** Materialize or require the default before delegated ingest, reject Boolean/non-integer values, and do not replace caller intent through truthiness defaults.
- [x] **Add complete configuration enum guards.** Structured or unsupported identity, development, review, activation, and lifecycle values now fail through deterministic `ConfigurationError` boundaries; PR #16 added five hostile enum regressions.
- [ ] **Add message-kind guards.** Reject non-string and unknown incoming or outgoing kinds before hashing, queueing, ledger mutation, or evidence emission.
- [ ] **Validate outgoing recipients before message hashing.** Reject non-canonical, unknown, alias-only, or retired recipients through `RuntimeInvariantError` before constructing an `MCPMessage`.
- [ ] **Reject malformed incoming-message shape atomically.** Require `MCPMessage` shape and validate fields, identities, kind, payload, and provenance before copying or mutating inbox state.
- [x] **Wrap bounded file-read failures consistently.** Configuration, genome-root inspection, path resolution, stat, and read `OSError` failures now normalize to `ConfigurationError`; PR #16 added focused configuration and genome read-failure regressions.
- [ ] **Make ingest failures atomic.** Normalize required limits before delegation or restore the pre-operation checkpoint on every delegated ingest exception; prove no unledgered partial mutation remains.
- [ ] **Use one canonical freeze checkpoint.** Freeze certificates, controller checkpoints, resume, high-severity annotation rollback, and message state must hash and restore the same canonical snapshot.
- [ ] **Guarantee rollback at event capacity.** Reserve safety-event capacity or restore state through an invariant-safe path even when `max_events` is full.
- [ ] **Validate persisted event-entry shape strictly.** Reject missing required fields, Boolean/non-integer sequences, unexpected shape, invalid hashes, and non-canonical entries before reporting a ledger as verified.
- [ ] **Resolve every remaining PR #7 review thread and rerun final-head CI.** Retain artifacts and inspect exact checkout, all tests, wheel/source hashes, negative fixtures, and review disposition at one repaired immutable head.
- [ ] **Run merged-head acceptance.** After explicit default-branch merge authorization, require clean installation, compilation, complete tests, installed CLI/version/configuration smoke, deterministic evidence, wheel and sdist, checksums, and retained logs at the merged head.
- [ ] Prepare contract-validation tests that consume only accepted, hash-fixed QSO-GENOMES and QSO-SEEKER fixtures.

## Current evidence

- [x] Focused repair head `e4df1a886eb8529da6b28525e64e06ec0aaab1ea` passed CI run `30065932577` on Python 3.11/3.13 and Consent Capacity Lock run `30065932623`.
- [x] Focused artifacts were retained as `8586230775`, `8586230674`, and `8586229184` with digests `sha256:0b2955378621ecf26f3d11a3f4f00321c52c389e594aff3a7f456f9043fc52d7`, `sha256:9eb8946c17562a3076067edb774b0b221bf36645989495d8196f23d1563c6ee5`, and `sha256:ca9648a8eb69c3af083c87071e72aa065ce3723e73644e9feeea0f77d039fc66`.
- [x] PR #16 merged only into this non-default candidate as `c9c20e36e67b8bbe2f8f1edd916fb108925939b9`.
- [x] Integrated candidate `c9c20e36e67b8bbe2f8f1edd916fb108925939b9` independently passed CI run `30066019620` and Consent Capacity Lock run `30066019642`.
- [x] Integrated artifacts were retained as `8586264300`, `8586265980`, and `8586261679` with digests `sha256:e0bd62d6ce0b5c11e6cbc81e1446a04c79ae41be88a375f1d60a3a2daeaea082`, `sha256:990441e884d768095b0c0120c24147e1ddf93a7ecc7507e34b6684e99dbd0c0b`, and `sha256:3a467642b75ee8b9c0ebb1c193ef0e9c0355c602c3349b31b824b6e4f56365f1`.
- [ ] Six current input-boundary findings remain unresolved: repository-field shape, singleton message allowlists, `max_records` default handling, message-kind guards, outgoing-recipient validation, and malformed incoming-message shape.
- [ ] Additional runtime invariants remain open for atomic ingest, canonical freeze/checkpoint parity, rollback capacity, and strict persisted-event validation.
- [ ] QSO-GENOMES PRs #2, #12, and #13 are not yet reconciled into one accepted compatibility head and cannot supply final trusted hashes.
- [ ] QSO-SEEKER candidates remain unreconciled with current `main` and cannot supply final accepted canonical-record fixtures.
- [ ] Issue #8 hostile-input and prompt-injection hardening remains open.
- [ ] Any descendant of the validated integration generation must independently rerun CI and Consent Capacity Lock before its exact-head evidence is current.

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
