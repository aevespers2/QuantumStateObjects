# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Repair and independently accept PR #7's local-configuration contract before adding broader runtime behavior or cross-repository experiments.
- **User outcome:** A researcher can install the package, invoke `qso-run`, load and validate canonical local instance configuration, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** preserve the verified CLI/configuration baseline; require strict UTF-8 JSON, full instance-schema identity blocks, exact integer schema versions, canonical repository/path/name/hash rules, and fail-closed genome resolution; then verify instance, message, ledger, attribution, limit, freeze, interruption, recovery, and rollback primitives with local fixtures.
- **Priority:** Final-head acceptance of PR #7 now precedes QSO-GENOMES/QSO-SEEKER integration, deterministic runtime evidence, and the four-QSO experiment.
- **Success criteria:** exact-head and merged-head clean build/install succeed; `qso-run` smoke passes; schema and loader agree; UTF-16/32 payloads, missing required identity/review/status blocks, booleans used as schema versions, wrong repository/path/case, invalid configuration, and mismatched hashes fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** PR #7 resolves PR #6's earlier schema/source/name findings and has exact-head matrix evidence, but three new parser/schema-enforcement findings must be repaired and reverified before it can anchor the portfolio.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Reconcile the runnable CLI/configuration candidates | Architect | — | REVIEW | PR #7 remains the sole canonical path; PR #6 is closed as superseded with review history preserved; all PR #7 review threads are resolved; final immutable-head and merged-head checks pass. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | IN PROGRESS | Strict UTF-8 decoding, complete schema-required identity blocks, integer-only schema versions, canonical source/name/hash enforcement, invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #7 is open and mergeable at head `80e0546a53c139b26e956bce8f20c41e907739a6`; PR #6 is closed without merge as superseded.
- Workflow run `29614395650` checked out and asserted that exact head with read-only contents permission and checkout credential persistence disabled.
- Python 3.11 and 3.13 jobs passed installation, compilation, all 15 unit/smoke tests, installed default/configuration CLI smoke, wheel construction, checksum generation, and retained artifact upload.
- Retained artifact digests are `cdfd6817c3d0e0c07b41613072443c4fdd5aa0952ea68e4969ccee362ed7470a` and `221cfa42111ed0a6ac42c0311934d812f437f9eeeaa80d3f5cb574d155cde7ed`; wheel SHA-256 values are `99fa4f424f4c1ca12ece6d0971e887708e7083275934904d264ace80ecac1790` and `7afba2f01fc3d9481989ea68302b79a8e671c7121572899c374e6c8f6a606dfd`.
- PR #7 resolves the earlier schema hash-pin, repository/path, and canonical-name findings, but three new unresolved P2 threads require strict UTF-8 decoding for configuration/genome payloads, enforcement of all schema-required runtime identity/development/review/status blocks, and explicit rejection of boolean schema versions.
- Atlas continues to fail closed because its current reference has no accepted SHA-256. QSO-GENOMES PR #2 remains unaccepted and non-mergeable; QSO-SEEKER's canonical-record contract remains unpublished or unaccepted.
- Draft PR #3 remains outside P0 and outside the first release.

## Portfolio dependency order

PR #7 parser/schema repair and final-head acceptance ↔ QSO-GENOMES canonical artifact/hash acceptance → local runtime/message/ledger/freeze evidence → QSO-SEEKER canonical-record acceptance → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

Record commits, install/test commands, workflow runs, checked-out SHAs, deterministic seeds, schema and artifact hashes, retained artifacts, review-thread dispositions, freeze/rollback evidence, privacy review, residual risks, and follow-ups.
