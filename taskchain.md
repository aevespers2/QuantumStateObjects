# Task Chain

## Repository role
Bounded QSO identities, runtime partitions, freeze/rollback control, inter-object messages, deterministic experiments, event evidence, and attribution journey records.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Establish the current runtime, instance, ledger, and test baseline | QSOBuilder | — | READY | Existing tests and CI checks pass or failures are reproduced; the four instance manifests, genome interpreter, freeze/rollback path, MCP-message integrity, resource limits, and attribution ledger are inventoried with exact commands and commits. |
| P1 | Add cross-repository contract validation | QSOBuilder | QSO-GENOMES P1 and QSO-SEEKER P1 | BLOCKED | Runtime validates the published genome manifest and canonical-record fixtures by schema version and hash, fails closed on mismatch, and does not import or execute external repository code. |
| P2 | Build the bounded four-QSO experiment runner | QSOBuilder | P1 | PROPOSED | Atlas, Nova, Orion, and Lyra run from deterministic seeds within configured time/memory/message limits; proposals remain inert; freeze and rollback are tested; append-only event and attribution artifacts are emitted. |
| P3 | Add simulated payment-intent and distribution records | Builder | P2 and approved payment-policy contract | BLOCKED | Records distinguish intent, authorization, allocation, receipt, dispute, and settlement adapter; tests cover splits, royalties, validator rewards, escrow milestones, pooled treasury, and failed authorization without moving funds. |
| P4 | Resolve public-repository privacy, confidentiality, and licensing notices | Architect | User approval | BLOCKED | Public files use an approved license/notice model consistent with repository visibility; personal identifiers and confidentiality language are minimized or explicitly approved; tests and examples contain no unintended sensitive data. |

## Portfolio dependency order
`QSO-GENOMES` and `QSO-SEEKER` contracts → runtime contract validation → four-QSO runner → optional simulated economic records → public documentation.

## Builder Log
Record commits, test commands/results, deterministic seeds, artifact hashes, freeze/rollback evidence, residual risks, and follow-ups.
