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
| P0-A | Reconcile the runnable CLI candidates | Architect / QSOBuilder | — | IN PROGRESS | PR #4 dynamically checks out and asserts the submitted head, retains checksummed evidence, passes final latest-head CI, resolves review threads, and explicitly dispositions duplicate PR #5. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | BLOCKED | Instance loading, invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #4 remains the preferred canonical path because it contains the bounded CLI, focused tests, constrained packaging, and least-privilege two-version CI.
- Earlier workflow run `29599534913` passed Python 3.11 and 3.13 installation, compilation, tests, CLI smoke, boundary validation, version output, and wheel construction, but checked out a synthetic merge ref and retained no artifact.
- Commit `e9ba8736a00b7f356c352a81a1e7bf409c38c18e` repaired the workflow to check out `${{ github.event.pull_request.head.sha || github.sha }}`, assert that exact SHA, disable persisted checkout credentials, build a checksum manifest, and retain per-Python evidence for 30 days.
- Independent reconstructed verification passed four tests, source/test compilation, workflow YAML parsing, wheel construction, and produced wheel SHA-256 `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`.
- Final GitHub-hosted CI evidence for the latest PR head remains required before P0-A can move to review or done.
- PR #5 remains a duplicate candidate without attached workflow evidence; PR #2 is superseded; draft PR #3 remains outside P0.

## Portfolio dependency order

Canonical exact-head CLI baseline → local runtime/configuration evidence → QSO-GENOMES and QSO-SEEKER contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

- 2026-07-17 — Repaired PR #4 exact-head verification and evidence retention. The workflow now dynamically binds checkout and assertion to the submitted pull-request head, records the checked-out SHA and Python version, preserves deterministic CLI output and version, builds a wheel and SHA-256 manifest, and uploads retained artifacts without credentials, network-dependent inputs, external repository writes, or generated-code execution.
- 2026-07-17 — Reconstructed local verification of the bounded workflow slice passed four CLI tests, compilation, wheel construction, YAML parsing, and checksum generation. GitHub-hosted latest-head CI remains the sole open verification step for this slice.
