# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Repair and independently accept the current PR #7 configuration and runtime-primitives head before adding upstream integration or a four-QSO experiment.
- **User outcome:** A researcher can install the package, invoke `qso-run`, validate canonical local instance configuration, exercise one bounded deterministic runtime controller, and inspect integrity-checked event/attribution, freeze, interruption, recovery, and rollback evidence.
- **MVP scope:** preserve the exact-head CLI/configuration and runtime-primitives evidence; enforce strict UTF-8, complete instance-schema parity, integer-only versions, canonical IDs/names/repository/path/hash rules, atomic ingest failure, canonical freeze checkpoints, rollback at event capacity, and strict event-ledger shape; then reverify one immutable head and merged head.
- **Priority:** Final-head acceptance of PR #7 precedes QSO-GENOMES/QSO-SEEKER integration, any population experiment, and all later Experimenter work.
- **Success criteria:** exact-head and merged-head clean build/install pass; all review threads are resolved; invalid encoding, missing blocks, invalid IDs/types, malformed ledgers, failed delegated mutations, full event capacity, checkpointed messages, wrong repository/path/case, and mismatched hashes fail closed without unledgered state; repeated fixtures reproduce canonical state/event hashes; no unapproved external code, credentials, network, or repository writes occur.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming Atlas, Nova, Orion, or Lyra are running without append-only runtime evidence from an authorized experiment.
- **Release rationale:** PR #7 is reconciled with current `main` and has exact-head matrix evidence for 22 tests, but eight unresolved P2 findings still prevent acceptance.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Reconcile and accept the canonical CLI/configuration candidate | Architect | — | REVIEW | PR #7 remains the sole path; it is mergeable and zero behind `main`; all eight current review threads are repaired/resolved; final immutable-head and merged-head checks pass. |
| P0-B | Verify the bounded local runtime-primitives slice | QSOBuilder | P0-A final-head repairs | REVIEW | Lifecycle, message validation, event/attribution ledgers, resource limits, freeze, interruption, recovery, rollback, checkpoints, and deterministic hashes pass with atomic failure behavior and strict persisted-evidence validation. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, accepted QSO-GENOMES, accepted QSO-SEEKER | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are verified. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #7 is open, unmerged, mergeable, and reconciled with current `main` at normal two-parent head `395915b60510e9a62c53ad128cf23d151e73eb1f`; no reviewed history was force-rewritten.
- Workflow run `29617877793` completed successfully on Python 3.11 and 3.13. Both jobs checked out and asserted the exact submitted head, installed and compiled the package/tests, passed 22 tests with JUnit evidence, ran installed CLI/configuration smoke, built wheels, generated SHA-256 values, and uploaded retained artifacts.
- Retained artifact digests are `c53ecc7692716519be67c92e4e51cc04695187437790c784d8b42f78d70a76fd` and `cf2290f7469b71ebb92cc7b1cb7eb86a64ee9ff56df8b89203fa157bd6b65816`; wheel SHA-256 values are `97c6ec287e2eb1b23776dc232a16641f566202f1aacf792755a992930adf5dc3` and `b074c2328f90585c2fe8fb7a83d023ef34ea7374b6ee9915c57209d589e678cc`.
- The bounded runtime slice covers lifecycle states, message participants/kinds/payload hashes, hash-linked event and attribution ledgers, resource prechecks, freeze/resume, interruption/recovery, rollback/checkpoint restoration, and repeatable state/event hashes using synthetic local fixtures only.
- Eight unresolved P2 findings block acceptance: strict UTF-8 decoding; complete required instance blocks; boolean schema-version rejection; instance-ID schema enforcement; atomic recovery when delegated ingest raises; canonical freeze checkpoints including messages; rollback capacity when the event ceiling is full; and strict event-entry shape/type validation.
- Atlas continues to fail closed because its current reference has no accepted upstream SHA-256. QSO-GENOMES PR #2 remains unaccepted and non-mergeable; QSO-SEEKER's canonical-record contract remains unaccepted.
- Draft PR #3 remains outside P0 and outside the first release.

## Portfolio dependency order

PR #7 eight-finding repair and final-head acceptance → local runtime/message/ledger/freeze acceptance → QSO-GENOMES canonical artifact/hash acceptance → QSO-SEEKER canonical-record acceptance → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

Record commits, install/test commands, workflow runs, checked-out SHAs, deterministic seeds, schema and artifact hashes, retained artifacts, review-thread dispositions, atomic-failure and freeze/rollback evidence, privacy review, residual risks, and follow-ups.
