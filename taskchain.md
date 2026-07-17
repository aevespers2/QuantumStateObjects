# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Select and verify one canonical runnable-package candidate before adding local configuration or cross-repository experiments.
- **User outcome:** A researcher can install the package, invoke `qso-run`, load and validate local instance configuration, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** repair the missing CLI entry point; add real unit/smoke tests and CI; verify instance, message, ledger, attribution, limit, freeze, and rollback primitives with local fixtures; document supported Python versions, privacy/licensing boundaries, commands, failures, and recovery.
- **Priority:** Exact-head acceptance of one CLI/package path precedes local configuration evidence, QSO-GENOMES/QSO-SEEKER integration, and the four-QSO experiment.
- **Success criteria:** clean exact-head build/install succeeds; `qso-run` smoke passes; invalid configuration and mismatched hashes fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** The core runtime cannot safely anchor the portfolio until one immutable candidate is accepted and its local behavior is covered by reproducible tests and retained evidence.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Reconcile the runnable CLI candidates | Architect | — | REVIEW | PR #4 is the preferred canonical path; repair its workflow to check out and assert head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`, rerun CI, resolve review threads, retain artifacts, and explicitly disposition duplicate PR #5. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | BLOCKED | Instance loading, invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #4 is open and mergeable. Workflow run `29599534913` passed Python 3.11 and 3.13 installation, compilation, four tests, CLI smoke, boundary validation, version output, and wheel construction.
- The run checked out synthetic merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701`, not submitted head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`; therefore exact-head acceptance remains open.
- PR #4 has unresolved review threads. Package discovery, build-dependency installation, and credential persistence appear repaired in the current diff, but exact-head checkout is not.
- PR #5 is open and mergeable but duplicates the CLI slice, has only reconstructed exact-file replay, and has no attached workflow run. It is not selected while PR #4 remains the stronger evidence path.
- PR #2 is closed as superseded. Draft PR #3 remains outside P0 and outside the first release.

## Portfolio dependency order

Canonical exact-head CLI baseline → local runtime/configuration evidence → QSO-GENOMES and QSO-SEEKER contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

Record commits, install/test commands, workflow runs, checked-out SHAs, deterministic seeds, schema and artifact hashes, retained artifacts, review-thread dispositions, freeze/rollback evidence, privacy review, residual risks, and follow-ups.