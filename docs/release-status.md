# Release status

## Decision

**Status: BLOCKED — documentation foundation prepared; runtime candidate remains draft and unreconciled with current `main`.**

This documentation branch does not authorize package publication, GitHub Pages publication, runtime activation, external integration, or deployment.

## Current lineage

- Accepted documentation base: `main` commit `40efcbf8ce2bda7d6b05b3fb1f3ccf0384facc51`.
- Accepted control milestone: repaired repository-wide policy validator merged to `main` with exact-head evidence.
- Sole runtime/configuration candidate: draft PR #7, branch `builder/config-contract-v4`.
- Current PR #7 head observed during this documentation review: `40a0c123c271c883356b9315dc213556d4abbb14`.
- PR #7 must be reconciled with the current accepted `main` before its next acceptance run.

Historical exact-head runs are useful evidence about the tested heads. They are not acceptance evidence for a different current or merged head.

## Candidate capability inventory

| Area | Current classification |
|---|---|
| Package metadata and Python 3.11+ declaration | Present in repository/candidate metadata |
| `qso-run` local health and configuration CLI | Draft PR #7 candidate |
| Strict local UTF-8/JSON configuration validation | Draft PR #7 candidate |
| Local hash-fixed genome resolution | Draft PR #7 candidate; blocked on accepted upstream artifacts |
| QSO prototype and inactive proposals | Present on accepted `main` |
| Runtime lifecycle controller | Draft PR #7 candidate |
| Message validation | Prototype plus stricter draft candidate |
| Event and attribution evidence | Draft PR #7 candidate |
| Checkpoint, freeze, interruption, recovery, and rollback | Draft PR #7 candidate |
| Four-QSO runner | Not implemented or authorized for the first acceptance stage |
| Persistent deployment | Not defined or authorized |

## Open candidate findings

The latest PR #7 description identifies unresolved work including:

- removal of a retired runtime review identity and binding to the accepted human-review authority;
- canonical repository-field shape;
- singleton message allowlists where required;
- correct `max_records` default and type handling;
- complete configuration enum guards;
- message-kind guards;
- canonical outgoing-recipient validation;
- atomic rejection of malformed incoming-message shapes;
- consistent bounded file-read error handling;
- atomic delegated ingest failure;
- one canonical message-inclusive freeze/checkpoint model;
- rollback under a full event ceiling;
- strict persisted-event validation;
- issue #8 hostile-input hardening;
- accepted, hash-fixed QSO-GENOMES and QSO-SEEKER contracts;
- complete review-thread disposition;
- exact-head and merged-head acceptance.

This list may change as review progresses. `taskchain.md`, `punchlist.md`, PR review threads, and the exact candidate head remain the operational sources for current acceptance work.

## Acceptance gates

| Gate | Status | Required evidence |
|---|---|---|
| Canonical candidate | Review | PR #7 remains sole path and is reconciled with current `main` without rewriting reviewed history |
| Repository-wide policy control | Pass on accepted `main` | Exact-head tests, validator report, retained artifact, and merged commit |
| Runnable package and CLI | Partial historical evidence | Fresh clean installation, smoke, and error-path evidence at repaired exact and merged heads |
| Configuration contract | Review | Complete positive/negative/adversarial fixtures and resolved findings |
| Runtime invariants | Review | Atomic state, lifecycle, resource, message, ledger, checkpoint, freeze, interruption, recovery, and rollback evidence |
| Determinism | Partial | Repeated fixed-input reports at accepted exact and merged heads |
| Upstream contracts | Blocked | Accepted QSO-GENOMES and QSO-SEEKER versions, hashes, schemas, and fixtures |
| Security | Partial | Hostile-input matrix, dependency/workflow review, secret scan, exact-head evidence, and disposition |
| Documentation | Review | Strict local build, link/navigation review, architecture verification, and approval |
| Privacy and confidentiality | Blocked | Approved data-handling and public-artifact rules |
| License and attribution | Blocked | Approved repository, dependency, artifact, and contributor notices |
| Provenance | Partial | Source/sdist/wheel hashes, SBOM where applicable, attestations, review disposition, and retention |
| Rollback | Partial | Full-capacity and tamper-path rollback drill with post-validation |
| Pages publication | Blocked | Approved Pages source, strict build, accessibility/link review, workflow evidence, and explicit publication approval |
| Package publication | Blocked | All release gates plus repository/package registry approval |
| Deployment | Blocked | Approved target, operations plan, observability, rollback, and post-deployment evidence |
| Final approval | Pending | Explicit recorded approval after every blocking gate passes |

## Required release artifacts

A first eligible candidate should include:

- immutable source archive;
- sdist and wheel built from the accepted merged head;
- SHA-256 checksums;
- versioned schemas and sample configurations;
- accepted upstream fixture manifest;
- unit, negative, adversarial, deterministic, interruption, recovery, freeze, and rollback reports;
- exact-head and merged-head identity reports;
- source and dependency inventory;
- SBOM where applicable;
- provenance or attestation manifest;
- documentation build report;
- security and privacy review disposition;
- rollback bundle and drill report;
- release approval record.

## Pages readiness

The `docs/` source and `mkdocs.yml` in this branch are **Pages-ready candidates**, not a published site. Before publication:

1. run `mkdocs build --strict` in a clean environment;
2. inspect navigation, Mermaid rendering, code blocks, tables, keyboard behavior, contrast, and mobile layout;
3. run a link checker against the built site;
4. verify repository and release status wording against the exact accepted heads;
5. approve the publication source and workflow;
6. retain the exact source SHA, tool versions, build logs, site artifact hash, and deployment result;
7. verify the public site after deployment and document rollback.

## Rollback decision

Any failed gate returns the candidate to review. Publication or deployment must be rolled back when the public artifact does not match the approved source, documentation claims exceed evidence, links or navigation materially fail, sensitive data appears, security controls regress, or provenance cannot be verified.

## Explicit exclusions

The first release does not include autonomous internet learning, generated-code execution, credentials, external repository writes, scheduled execution, persistent hosting, distributed agents, production payment behavior, or claims that Atlas, Nova, Orion, and Lyra are independently active.
