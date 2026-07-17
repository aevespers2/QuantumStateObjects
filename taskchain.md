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
| P0-A | Reconcile the runnable CLI candidates | Architect / QSOBuilder | — | IN PROGRESS | PR #6 passes latest-head Python 3.11/3.13 CI with exact-head assertion and retained checksummed artifacts; then PR #4 and PR #5 are explicitly superseded without losing evidence. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | BLOCKED | Instance loading, invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #6 was created from current `main` as a clean replacement candidate and contains only the bounded CLI, tests, package-discovery repair, and exact-head CI slice.
- Its workflow checks out `${{ github.event.pull_request.head.sha || github.sha }}`, asserts the checked-out SHA, uses read-only permissions, disables persisted checkout credentials, and retains the SHA, Python version, deterministic CLI output, CLI version, wheel, and SHA-256 manifest for 30 days.
- Independent reconstructed verification passed four tests, source/test compilation, workflow YAML parsing, wheel construction, and checksum generation; reconstructed wheel SHA-256: `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`.
- Latest-head GitHub-hosted CI and artifact inspection for PR #6 remain required before P0-A can move to `DONE`.
- Earlier PR #4 matrix CI passed functional checks but used a synthetic merge ref and retained no artifact. PR #5 has reconstructed local evidence but no attached workflow. PR #2 is superseded; draft PR #3 remains outside P0.

## Portfolio dependency order

Canonical exact-head CLI baseline → local runtime/configuration evidence → QSO-GENOMES and QSO-SEEKER contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

- 2026-07-17 — Created clean branch `builder/runnable-baseline-v3` from current `main` and opened PR #6 to remove PR #4's conflict/stale-evidence ambiguity. Restored `qso_runtime.cli:main`, added four deterministic tests, constrained package discovery, and added exact-head Python 3.11/3.13 CI with retained checksummed evidence.
- 2026-07-17 — Reconstructed verification passed four tests, compilation, workflow YAML parsing, wheel construction, and checksum generation. No generated snippets were executed; no credentials, network-dependent inputs, or external repository writes were used.
