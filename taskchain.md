# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Make the existing package runnable and independently verifiable before adding cross-repository experiments.
- **User outcome:** A researcher can install the package, invoke `qso-run`, load and validate local instance configuration, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** repair the missing CLI entry point; add real unit/smoke tests and CI; verify instance, message, ledger, attribution, limit, freeze, and rollback primitives with local fixtures; document supported Python versions, privacy/licensing boundaries, commands, failures, and recovery.
- **Priority:** Runnable package and local evidence baseline precede QSO-GENOMES/QSO-SEEKER integration and the four-QSO experiment.
- **Success criteria:** clean build/install succeeds; `qso-run` smoke passes; invalid configuration and mismatched hashes fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** The core runtime cannot safely anchor the portfolio until its published entry point works and its local behavior is covered by reproducible tests.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Repair and verify the runnable local package baseline | QSOBuilder | — | IN PROGRESS | `qso_runtime.cli:main` exists; clean install, CLI smoke, local fixtures, tests, and CI pass; runtime/ledger/freeze/rollback inventory and exact evidence are recorded. |
| P1 | Add cross-repository contract validation | QSOBuilder | QSO-GENOMES P1 and QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Portfolio dependency order

Runnable local baseline → QSO-GENOMES and QSO-SEEKER contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

- 2026-07-17 — Claimed the first P0 slice on `builder/runnable-cli-baseline-v2`. PR #5 adds the missing bounded `qso_runtime.cli:main` and five real tests covering unit output, module smoke, and invalid-argument fail-closed behavior. Reconstructed exact-file replay passed five tests, compilation, wheel build, isolated installation, `qso-run`, and `qso-run --version`; wheel SHA-256 `8562d17728721c7f2ba4f4ad0fc0ec262ed0e1bc0bc853f4a2643518ba55f14f`. A full-tree clone was unavailable because the runtime could not resolve `github.com`; exact-head CI remains the next P0 evidence gate.
