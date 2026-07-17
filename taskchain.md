# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Accept PR #7's current-main configuration repair, then inventory and verify local runtime primitives before adding cross-repository experiments.
- **User outcome:** A researcher can install the package, invoke `qso-run`, load and validate canonical local instance configuration, reject uncontracted genome references, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** preserve the verified CLI baseline; keep loader, schema, repository/path, canonical-name, and hash-pin rules aligned; verify instance, message, ledger, attribution, limit, freeze, and rollback primitives with local fixtures; document supported Python versions, privacy/licensing boundaries, commands, failures, and recovery.
- **Priority:** Exact-head acceptance of PR #7 now precedes broader runtime evidence, QSO-GENOMES/QSO-SEEKER integration, and the four-QSO experiment.
- **Success criteria:** exact-head and merged-head clean build/install succeed; `qso-run` default and configuration smoke pass; schema and loader agree; wrong repository/path, wrong case, invalid configuration, and mismatched hashes fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** The repaired configuration candidate is useful only after it is verified on a current-main immutable head and broader runtime behavior is reproducibly tested.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Accept the runnable CLI/configuration candidate | Architect / QSOBuilder | — | REVIEW | PR #7 is based on current `main`, passes exact-head Python 3.11/3.13 CI with retained checksummed artifacts, remains mergeable, and superseded PR #6 is dispositioned without losing evidence. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | IN PROGRESS | Schema permits the optional hash pin; repository/path and canonical case-sensitive names are enforced; invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## P0-B bounded slices

1. **Local configuration contract — REVIEW.** PR #7 restores the CLI/configuration candidate on current `main`, permits optional schema hash pins, requires exact canonical QSO names, and enforces the accepted repository plus per-QSO path contract. Reconstructed compilation and 15 tests pass; hosted exact-head evidence is pending.
2. **Atlas genome gate — IMPLEMENTED.** Require an accepted local hash-pinned genome file; reject the current unpinned Atlas reference before execution or network access.
3. **Runtime primitive inventory — READY AFTER PR #7 ACCEPTANCE.** Inspect instance, message, ledger, attribution, limits, and freeze/rollback modules and add focused positive/negative tests.
4. **Deterministic local smoke — BLOCKED ON SLICE 3.** Reproduce canonical state/event hashes under fixed seeds and limits.

## Candidate evidence

- PR #6 exact-head run `29610600428` established the initial Python 3.11/3.13 CLI/configuration baseline at `6e382853e6746f8eb18e97c64481dccfe6684652`, but its branch later diverged five planning commits behind `main`.
- PR #7 starts from current `main` commit `dd455b52beb0c257d2f11abc994da6b94085c2c3` and ports the accepted baseline plus all three configuration-contract repairs.
- Reconstructed PR #7 verification passed compilation, 15 unit/smoke tests, and local configuration CLI validation. It performed no network calls, imported no upstream code, executed no generated snippets, accessed no credentials, and wrote only to the authorized target repository branch.
- Atlas fails closed because its current reference has no accepted SHA-256. This remains correct behavior and a hard upstream blocker.

## Portfolio dependency order

PR #7 exact-head acceptance → local runtime/message/ledger/freeze evidence → QSO-GENOMES and QSO-SEEKER canonical artifact/hash acceptance → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

- 2026-07-17 — PR #6 established the initial exact-head CLI/configuration baseline in run `29610600428` with 11 tests and retained Python 3.11/3.13 artifacts.
- 2026-07-17 — PR #6 review identified schema/hash-pin disagreement, uncontracted repository/path acceptance, and noncanonical QSO casing.
- 2026-07-17 — Claimed the highest-priority unblocked P0 repair. Rebuilt the candidate from current `main` as PR #7, aligned schema and loader contracts, added four regression tests for 15 total, and locally verified compilation plus configuration CLI behavior without generated-code execution, credentials, network access, or external-repository writes.
