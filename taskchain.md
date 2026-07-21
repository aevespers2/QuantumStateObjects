# Task Chain

## Repository role

QuantumStateObjects owns bounded local QSO identities, runtime partitions, message handling, deterministic experiments, event and attribution evidence, checkpoints, freeze/interruption/recovery/rollback, local admission decisions, execution receipts, and local validation of accepted genome, observation, capability, and task-envelope artifacts.

Within A.L.I.S.T.A.I.R.E., it is the bounded local execution and evidence subsystem. It is not constitutional governance, Repository `0` portable bootstrap or planning, Repository `1` capability or canonical-state authority, genome authorship, hostile-source retrieval, temporal or Digitalis interpretation, portfolio-wide collaboration, generic evidence transport, credentials, merge/release/deployment, or final approval authority.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Reconcile draft PR #7 with accepted `main`, repair the current configuration/runtime/security findings, and independently accept one immutable local package/runtime head before any upstream or Repository `0`/`1` integration.
- **User outcome:** A researcher can install the package, invoke `qso-run`, validate canonical local configuration, exercise one bounded deterministic runtime controller, and inspect integrity-checked admission, event, attribution, checkpoint, freeze, interruption, recovery, rollback, and execution-receipt evidence.
- **MVP scope:** one local Python package and CLI; strict local configuration and hash-fixed artifact validation; isolated partitions; bounded messages and records; atomic fail-closed admission and mutation; canonical local evidence; deterministic replay; explicit human review; no network, credentials, generated-code execution, external writes, payment behavior, device administration, scheduling, or persistent deployment.
- **Priority:** Final acceptance of the reconciled PR #7 lineage precedes genome, observation, capability, Fabric, Bridge, four-QSO, or autonomous-development integration.
- **Success criteria:** clean install/build on supported Python versions; complete positive, negative, adversarial, admission, interruption, recovery, freeze, rollback, replay, correction, and deterministic tests at exact and merged heads; accepted ownership and upstream contracts; reproducible artifacts and provenance; no unapproved external capability.
- **Non-goals:** autonomous internet learning, host-security collection, executing retrieved or generated code, production payments, unrestricted repository writes, persistent services, distributed execution, canonical-state authority, or claims that Atlas, Nova, Orion, or Lyra are active without authorized append-only runtime evidence.

## Current status

Accepted `main` includes the repaired repository-wide consent-capacity policy validator and exact-head workflow controls. Draft PR #7 remains open, unmerged, mergeable, and the sole package/configuration/runtime candidate at pre-reconciliation head `40a0c123c271c883356b9315dc213556d4abbb14`. Its successful runs are historical exact-head evidence only; it must be reconciled with current `main` and reverified with the policy control and complete runtime matrix at one new head.

The portfolio direction identifies Repository `0` as the portable bootstrap, planning, proposal, and maintenance-orchestration candidate and Repository `1` as the independent quarantine, capability, canonical-state, revocation, and recovery authority candidate. The documentation branch now adds a runtime admission and reconciliation profile that preserves separate proposal, quarantine, capability, admission, execution, receipt, transport, review, and canonical-disposition identities. QuantumStateObjects may consume only a narrow Repository `1` capability and accepted task envelope after the route, schemas, fixtures, and authority owners are approved.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0-A | Maintain one canonical candidate and reconcile current `main` | Architect | — | REVIEW | PR #7 remains the sole path; current `main` is merged normally without rewriting history; exact head is recorded. |
| P0-B | Remove retired review identity and preserve human authority | Architect / Builder | P0-A | BLOCKED | Configuration, runtime, evidence, and release paths reject retired aliases and retain explicit human final approval. |
| P0-C | Complete parser, configuration, and file-boundary hardening | QSOBuilder | P0-A | REVIEW | Strict UTF-8, duplicate-key, exact-type, canonical-ID, schema, default/limit, bounded-file, hash, and atomic rejection fixtures pass. |
| P0-D | Complete message and identity hardening | QSOBuilder | P0-C | REVIEW | Unknown kinds, malformed shapes, unauthorized identities, aliases, digest mismatch, replay, and capacity failures reject before mutation. |
| P0-E | Complete runtime atomicity and recovery invariants | QSOBuilder | P0-C, P0-D | REVIEW | Delegated failures restore complete state; one message-inclusive checkpoint governs freeze/recovery; rollback works at full capacity. |
| P0-F | Complete ledger and persisted-evidence validation | QSOBuilder | P0-E | REVIEW | Shape, types, sequence, identity, canonical payload, chain, digest, truncation, reorder, replay, tamper, correction, and revocation fixtures fail closed. |
| P0-G | Close hostile-input security envelope | Security reviewer | P0-C through P0-F, issue #8 | BLOCKED | Direct, indirect, encoded, nested, Unicode, metadata, filename, document, JSON, Markdown, comment, and cross-repository injection fixtures pass with quarantine and denied authority. |
| P0-H | Final exact-head and merged-head acceptance | Architect / independent reviewer | P0-B through P0-G | BLOCKED | Clean builds, complete tests, deterministic reports, artifacts, checksums, review disposition, policy controls, provenance, and rollback pass at one immutable head and approved merged head. |
| P1-A | Approve semantic ownership and obstruction repairs | Portfolio architect | P0-H | BLOCKED | `qsio-kernel`, runtime, Fabric, genomes, Seeker, Digitalis/temporal, Bridge, Repository `0`, and Repository `1` have non-overlapping accepted responsibilities and migrations. |
| P1-B | Accept Repository `0` → Repository `1` → runtime route | Portfolio architect / security owner | P1-A | BLOCKED | Proposal, quarantine, capability, task, expected-head, expiry, replay, receipt, revocation, and reconciliation contracts and shared fixtures are approved. |
| P1-C | Accept runtime admission and reconciliation contract | Portfolio architect / runtime owner | P1-B | BLOCKED | Proposal, quarantine, capability, admission decision, execution attempt, receipt, resulting-state evidence, correction, revocation, and canonical disposition retain separate identities and fail closed. |
| P2-A | Accept genome compatibility set | Architect / QSOBuilder | P0-H, accepted QSO-GENOMES | BLOCKED | Immutable genome identity, lineage, schema, canonicalization, policy, lifecycle, digest, migration, and producer/consumer fixtures pass. |
| P2-B | Accept observation, temporal, and interpretation compatibility set | Architect / QSOBuilder | P0-H, accepted QSO-SEEKER and temporal/Digitalis owners | BLOCKED | Source, subject, provenance, classification, clocks, freshness, replay, correction, revocation, privacy, uncertainty, and atomic rejection fixtures pass. |
| P2-C | Accept Fabric, Bridge, interface, and canonical-state gluing | Portfolio architect | P1-A through P2-B | BLOCKED | Pairwise and triple-overlap fixtures prove separation of local admission/execution, collaboration, transport, display, and canonical acceptance. |
| P3 | Build bounded four-QSO experiment runner | QSOBuilder | P2-C | PROPOSED | Atlas, Nova, Orion, and Lyra run from accepted identities and deterministic seeds within limits; proposals remain inactive; complete evidence verifies. |
| P4 | Resolve public privacy, confidentiality, licensing, and attribution | Architect | User approval | BLOCKED | Public source, docs, samples, reports, and artifacts use approved notices and contain no unintended sensitive data. |
| P5 | Validate and publish documentation | Documentation reviewer | Contract accuracy, P4 | REVIEW | Exact-head strict build, links, accessibility, privacy/license, artifact retention, publication approval, public validation, and rollback pass. |
| P6 | Integrate governed autonomous-development tasks | Portfolio architect | P1-C, P2-C, accepted Repository `0`/`1` implementation | BLOCKED | Task authority, capabilities, credentials, admission, evidence, incident, emergency-stop, recovery, and human approval are explicit and versioned. |
| P7 | Add simulated payment-intent records | Builder | P3 and approved payment policy | BLOCKED | Simulation distinguishes intent, authorization, allocation, receipt, dispute, and settlement adapter without moving funds. |

## Runtime admission milestone

The documentation branch now defines:

- a candidate admission envelope independently binding runtime head, configuration, policy, device/environment, workspace, task, capability, genome, observations, temporal assessments, limits, stop/recovery, and evidence requirements;
- a deterministic side-effect-free admission sequence that rejects before state mutation;
- execution and receipt boundaries that cannot broaden authority;
- independent Repository `1` reconciliation after execution;
- eight triple-overlap witness groups covering task authority, genomes, source interpretation, Fabric, Bridge/interfaces, revocation/recovery, device replacement, and correction propagation.

This milestone is documentation-only. It does not change runtime behavior, accept PR #7, select schema owners, activate capabilities or adapters, publish Pages, run the four-QSO experiment, or authorize merge, release, deployment, credentials, device control, payment, or canonical-state mutation.

## Portfolio dependency order

Reconcile and accept PR #7 → approve semantic ownership and stop/recovery vocabulary → accept Repository `0`/`1` route → accept runtime admission/reconciliation profile → accept genome compatibility → accept observation/temporal/Digitalis compatibility → validate Fabric, Bridge, interface, and Repository `1` gluing → run bounded four-QSO experiment → review evidence → consider governed autonomous-development integration → optional later scopes.

## Builder log requirements

Record commits, base and head SHAs, install/build/test commands, workflow runs, supported Python versions, deterministic seeds, schema/canonicalization and artifact hashes, proposal/quarantine/capability/admission/task/receipt/disposition identities, retained reports, review dispositions, hostile-input fixtures, atomic-failure evidence, pairwise/triple-overlap witnesses, checkpoint/freeze/revocation/recovery evidence, privacy/license review, documentation/site hashes, publication result, residual risks, and follow-ups.
