# Task Chain

## Repository role

Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, attribution journey records, and the local integration boundary for accepted QSO-GENOMES and QSO-SEEKER artifacts.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Reconcile draft PR #7 with accepted `main` commit `40efcbf8ce2bda7d6b05b3fb1f3ccf0384facc51`, repair the current configuration/runtime/security findings, and independently accept one immutable local package/runtime head before any upstream integration or four-QSO experiment.
- **User outcome:** A researcher can install the package, invoke `qso-run`, validate canonical local instance configuration, exercise one bounded deterministic runtime controller, and inspect integrity-checked event, attribution, checkpoint, freeze, interruption, recovery, and rollback evidence.
- **MVP scope:** one local Python package and CLI; strict local configuration and hash-fixed artifact validation; isolated QSO partitions; bounded messages and records; atomic fail-closed mutation; canonical evidence; deterministic replay; explicit human review; no network, credentials, generated-code execution, external writes, payment behavior, scheduling, or persistent deployment.
- **Priority:** Final acceptance of the reconciled PR #7 lineage precedes QSO-GENOMES/QSO-SEEKER integration, any population experiment, and all later Experimenter work.
- **Success criteria:** clean install/build on supported Python versions; complete positive, negative, adversarial, interruption, recovery, freeze, rollback, and deterministic tests at exact and merged heads; resolved review threads; accepted upstream contracts; reproducible artifacts and provenance; no unapproved external capability.
- **Non-goals:** autonomous internet learning, executing retrieved or generated code, production payments, unrestricted repository writes, persistent services, distributed execution, or claims that Atlas, Nova, Orion, or Lyra are running without authorized append-only runtime evidence.

## Current status

The accepted `main` branch includes the repaired repository-wide policy validator and exact-head workflow controls. Draft PR #7 remains open, unmerged, mergeable, and the sole canonical runtime/configuration candidate. Its current pre-reconciliation head observed during the documentation review is `40a0c123c271c883356b9315dc213556d4abbb14`; it must be reconciled with current `main` and reverified.

Historical PR #7 runs provide evidence for their exact heads only. The latest candidate description records successful historical Python 3.11/3.13 testing with 150 tests, but the current/reconciled and eventual merged heads are not accepted by that evidence.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Maintain one canonical candidate and reconcile current `main` | Architect | — | REVIEW | PR #7 remains the sole path; current `main` is merged normally without rewriting reviewed history; exact head is recorded. |
| P0-B | Remove retired review identity and bind accepted human-review authority | Architect / Builder | P0-A | BLOCKED | Configuration, runtime, evidence, and release paths reject retired aliases and preserve explicit human final approval. |
| P0-C | Complete configuration and file-boundary hardening | QSOBuilder | P0-A | REVIEW | Canonical repository shape, singleton allowlists, exact limit/default handling, enum guards, strict bounded file errors, and complete negative fixtures pass atomically. |
| P0-D | Complete message and identity hardening | QSOBuilder | P0-C | REVIEW | Unknown kinds, malformed shapes, unauthorized senders/recipients, aliases, digest mismatches, replay, and capacity failures reject before mutation. |
| P0-E | Complete runtime atomicity and recovery invariants | QSOBuilder | P0-C, P0-D | REVIEW | Delegated failures restore complete state; checkpoints include message state; freeze paths share one canonical checkpoint; rollback works at full event capacity. |
| P0-F | Complete ledger and persisted-evidence validation | QSOBuilder | P0-E | REVIEW | Exact entry shape/type, sequence, identity, canonical payload, chain, digest, truncation, reorder, and replay fixtures fail closed. |
| P0-G | Close hostile-input security envelope | Security reviewer | P0-C through P0-F, issue #8 | BLOCKED | Direct, indirect, encoded, nested, metadata, filename, document, JSON, Markdown, comment, and cross-repository injection fixtures pass with provenance, quarantine, and denied authority. |
| P0-H | Final exact-head and merged-head acceptance | Architect / independent reviewer | P0-B through P0-G | BLOCKED | Clean builds, complete tests, deterministic reports, artifacts, checksums, review disposition, policy controls, provenance, and rollback pass at one immutable head and approved merged head. |
| P1 | Accept cross-repository contracts | Architect / QSOBuilder | P0-H, accepted QSO-GENOMES, accepted QSO-SEEKER | BLOCKED | Runtime validates immutable manifests and fixtures by repository, path, schema/canonicalization version, and digest without importing or executing external code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic local seeds within configured limits; proposals remain inactive; freeze/rollback and append-only evidence verify. |
| P3 | Resolve public privacy, confidentiality, licensing, and attribution notices | Architect | User approval | BLOCKED | Public source, docs, samples, reports, and artifacts use an approved notice/license model and contain no unintended sensitive data. |
| P4 | Validate and publish documentation | Documentation reviewer | P0 contract accuracy, P3 | REVIEW | `mkdocs build --strict`, link/accessibility review, exact-status review, artifact provenance, publication approval, deployment validation, and rollback evidence pass. |
| P5 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records are simulation-only and distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Documentation milestone

The `docs/pages-architecture-onboarding` branch adds a Pages-ready documentation foundation:

- expanded repository overview and status vocabulary;
- project and portfolio boundary guide;
- component, sequence, state, dependency, and trust-zone diagrams;
- configuration, identity, genome, record, message, proposal, ledger, attribution, resource, checkpoint, freeze, interruption, recovery, rollback, determinism, and compatibility contracts;
- developer onboarding and contribution workflow;
- hostile-input threat model and security evidence guide;
- local operations, incident, recovery, cleanup, and rollback runbook;
- evidence-qualified release and Pages readiness guide.

This milestone is documentation-only. It does not change runtime behavior, resolve PR #7 findings, accept upstream artifacts, publish Pages, or mark release/deployment gates passed.

## Portfolio dependency order

Reconcile PR #7 with accepted `main` → repair identity/configuration/message/runtime/evidence/security findings → final exact-head and merged-head acceptance → accepted QSO-GENOMES compatibility set → accepted QSO-SEEKER canonical-record contract → local cross-repository validation → bounded four-QSO experiment → reviewed evidence → optional later scopes.

## Builder log requirements

Record commits, base and head SHAs, install/build/test commands, workflow runs, supported Python versions, deterministic seeds, schema/canonicalization and artifact hashes, retained reports, review-thread dispositions, hostile-input fixtures, atomic-failure evidence, checkpoint/freeze/rollback evidence, privacy/license review, documentation build, publication result, residual risks, and follow-ups.
