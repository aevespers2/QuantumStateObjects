# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Repair and independently accept PR #6's local-configuration contract before adding broader runtime behavior or cross-repository experiments.
- **User outcome:** A researcher can install the package, invoke `qso-run`, load and validate canonical local instance configuration, execute a bounded deterministic smoke run, and inspect event/attribution evidence plus freeze/rollback behavior.
- **MVP scope:** preserve the verified CLI baseline; make loader, schema, repository/path, canonical-name, and hash-pin rules agree; verify instance, message, ledger, attribution, limit, freeze, and rollback primitives with local fixtures; document supported Python versions, privacy/licensing boundaries, commands, failures, and recovery.
- **Priority:** Final-head acceptance of PR #6's configuration slice now precedes QSO-GENOMES/QSO-SEEKER integration, deterministic runtime evidence, and the four-QSO experiment.
- **Success criteria:** exact-head and merged-head clean build/install succeed; `qso-run` smoke passes; schema and loader agree; wrong repository/path, wrong case, invalid configuration, and mismatched hashes fail closed; deterministic runs reproduce canonical hashes; freeze and rollback preserve evidence; no unapproved external code, credentials, network, or sensitive data enter artifacts.
- **Non-goals:** autonomous internet learning, executing retrieved/generated code, production payments, unrestricted repository writes, or claiming a verified four-QSO run while upstream Atlas and canonical-record contracts are incomplete.
- **Release rationale:** The exact-head CLI/configuration candidate is useful evidence, but it cannot safely anchor the portfolio until the three current contract findings are repaired and broader runtime behavior is reproducibly verified.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Reconcile the runnable CLI candidates | Architect | — | REVIEW | PR #6 remains the sole canonical path; exact-head run `29610600428` and artifacts are verified, superseded PR #4/#5 remain closed, all PR #6 review threads are resolved, and final-head plus merged-head checks pass. |
| P0-B | Verify local configuration and runtime primitives | QSOBuilder | P0-A | IN PROGRESS | Schema permits the required hash pin; repository/path and canonical case-sensitive names are enforced; invalid fixtures, message/ledger/attribution integrity, resource limits, freeze, interruption, recovery, rollback, and deterministic hashes pass on the accepted immutable head. |
| P1 | Add cross-repository contract validation | QSOBuilder | P0-B, QSO-GENOMES P1, QSO-SEEKER P1 | BLOCKED | Runtime validates published manifests/fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured limits; proposals remain inert; freeze/rollback and append-only evidence are tested. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public files and sample artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Candidate evidence

- PR #6 is open, mergeable, and the sole canonical runnable/configuration candidate at head `6e382853e6746f8eb18e97c64481dccfe6684652`.
- Workflow run `29610600428` checked out and asserted that exact head. Python 3.11 and 3.13 jobs passed installation, compilation, 11 tests, installed CLI smoke, boundary validation, version output, wheel construction, checksum generation, and retained artifact upload.
- Retained artifact digests are `505be6dae69827c150c72161ed348a752cf623a9589b29045c70000ff7aa2422` and `f44653928b2974f10f76822aebdac89fd31cdedf485f3ee9b5758be2766ae5f1`; wheel SHA-256 values are `9c1a1fe0209864d1e614d491da881f004792fac288b14a98596e021de2abf7f2` and `be85a103430e911974c28073a2e3bb283c7fdc9d30812b5b8ef9f0fd49e5a225`.
- Three unresolved P2 threads block acceptance: add `genome.sha256` to the published schema, reject genome references outside the declared QSO-GENOMES repository/path contract, and require canonical case-sensitive Atlas/Nova/Orion/Lyra names.
- Atlas fails closed because its current reference has no accepted SHA-256. This is correct behavior but also a hard upstream blocker.
- PR #4 and PR #5 are closed without merge as superseded. PR #2 remains superseded. Draft PR #3 remains outside P0 and outside the first release.

## Portfolio dependency order

PR #6 contract repair and final-head acceptance ↔ QSO-GENOMES canonical artifact/hash acceptance → local runtime/message/ledger/freeze evidence → QSO-SEEKER canonical-record acceptance → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log

Record commits, install/test commands, workflow runs, checked-out SHAs, deterministic seeds, schema and artifact hashes, retained artifacts, review-thread dispositions, freeze/rollback evidence, privacy review, residual risks, and follow-ups.