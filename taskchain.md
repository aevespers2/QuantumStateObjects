# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Finish fail-closed local configuration contract hardening, then inventory and verify the local runtime primitives before consuming upstream contracts.
- **User outcome:** A researcher can install the package, invoke `qso-run`, validate the four canonical local instance declarations, reject missing, altered, mis-cased, or uncontracted genome inputs, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** maintain the accepted CLI and CI baseline; validate local instance configuration; test malformed, missing, duplicate, traversal, schema, repository, path, name-casing, and hash failures; inventory and verify runtime, ledger, limits, freeze, and rollback primitives; later validate upstream fixtures by data and hash only.
- **Priority:** Local configuration and runtime evidence precede QSO-GENOMES/QSO-SEEKER integration and the four-QSO experiment.
- **Success criteria:** clean exact-head build/install succeeds; `qso-run` and `qso-run --config` pass; noncanonical or mismatched genome references fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** The core runtime cannot safely anchor the portfolio until local configuration, deterministic behavior, resource limits, and rollback evidence are reproducible at one immutable head.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Reconcile the runnable CLI candidates | Architect / QSOBuilder | — | DONE | PR #6 passed exact-head Python 3.11/3.13 CI with retained checksummed artifacts; PR #4 and PR #5 were superseded without losing evidence. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | IN PROGRESS | Instance loading, canonical repository/name/path validation, invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## P0-B bounded slices

1. **Local instance configuration — IMPLEMENTED, HARDENING EVIDENCE PENDING.** Exact-head run `29610600428` passed the initial loader and Atlas gate. The current follow-up enforces canonical QSO casing, the accepted QSO-GENOMES repository, per-QSO canonical paths, and schema support for optional SHA-256 pins; 15 reconstructed tests pass.
2. **Atlas genome gate — IMPLEMENTED.** Require an accepted local hash-pinned genome file; reject the current unpinned Atlas reference before execution or network access.
3. **Runtime primitive inventory — READY AFTER CURRENT CI.** Inspect instance, message, ledger, attribution, limits, and freeze/rollback modules and add focused positive/negative tests.
4. **Deterministic local smoke — BLOCKED ON SLICE 3.** Reproduce canonical state/event hashes under fixed seeds and limits.

## Candidate evidence

- PR #6 established the accepted canonical CLI baseline at exact head `9389d5322f535f59bd5db386dffe7ca2c9b052cf`; workflow run `29607170551` passed Python 3.11 and 3.13 with exact-head assertion and retained checksummed evidence.
- Exact-head configuration run `29610600428` passed Python 3.11 and 3.13 at `6e382853e6746f8eb18e97c64481dccfe6684652`, including installation, compilation, 11 tests, installed CLI validation, wheel construction, checksums, and retained artifacts.
- The loader performs no network calls, imports no upstream code, rejects symbolic links and path traversal, limits configuration/genome file sizes, requires unique canonical identities, and requires lowercase SHA-256 pins before local genome resolution.
- The contract-hardening follow-up rejects noncanonical QSO casing, unaccepted genome repositories, and per-QSO path mismatches, while the schema now permits the optional pin required by resolution. Reconstructed verification passed 15 tests and compilation; final hosted exact-head evidence remains pending.
- The current `config/instances.json` structurally validates as Atlas, Nova, Orion, and Lyra, but genome resolution fails closed at Atlas because the reference lacks an accepted SHA-256.

## Portfolio dependency order

Canonical exact-head CLI baseline → local runtime/configuration evidence → QSO-GENOMES and QSO-SEEKER contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

- 2026-07-17 — Created clean branch `builder/runnable-baseline-v3` from current `main`, restored `qso_runtime.cli:main`, added deterministic tests and least-privilege exact-head CI, and accepted the result after run `29607170551` passed with retained artifacts.
- 2026-07-17 — Claimed P0-B local configuration slice. Added bounded JSON loading, identity/schema/path validation, hash-pinned local genome resolution, Atlas fail-closed handling, CLI exposure, and seven focused tests. Exact-head run `29610600428` passed 11 total tests on Python 3.11 and 3.13.
- 2026-07-17 — Claimed the highest-priority unblocked review-hardening item. Added canonical name, repository, and per-QSO genome-path enforcement; aligned the instance schema with optional SHA-256 pins; and added four regression tests. Reconstructed verification passed 15 tests and compilation without generated-code execution, credentials, network access, or external repository writes.
