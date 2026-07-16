# Release Plan

## Current Decision
Status: `BLOCKED`

No runtime work is currently eligible for release. P0 is only `READY`, all punch-list and quality-gate items are unchecked, P1 depends on unpublished QSO-GENOMES and QSO-SEEKER contracts, and reviewed commit `6e44f89b682958dd3ef0bc382c706c6395194c6a` has no reported commit-status checks.

## Versioning
- Scheme: Semantic Versioning.
- First eligible runtime candidate: `0.1.0-alpha.1`.
- Schema, message, ledger, genome-contract, freeze/rollback, and evidence-format versions must be explicit; incompatible changes require a major version after `1.0.0` and a documented migration before then.

## Candidate Scope
- P0 runtime, instance, ledger, security, resource-cap, test, and CI baseline.
- Versioned validation of fixed genome and canonical-record fixtures once upstream manifests exist.
- Deterministic four-instance configuration inventory without claiming a verified multi-object run.
- Tested freeze and rollback behavior; generated proposals remain inert and human-authorized.
- Approved privacy, confidentiality, licensing, and public-evidence boundaries.

## Selected Completed Work
None. Coordination files and `changelog.md` are present, but no runtime capability has completed acceptance evidence.

## Planned Changelog Entries
- `Added`: reproducible runtime baseline, versioned contract validators, and deterministic evidence formats.
- `Security`: resource caps, fail-closed hash/schema checks, inert proposal handling, and least-privilege boundaries.
- `Fixed`: defects in message integrity, freeze/rollback, event ordering, attribution, or deterministic execution found during validation.
- `Documentation`: instance manifests, trust boundaries, exact commands, limitations, and recovery procedures.

## Acceptance Gates
| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is `DONE`; included P1 work is complete and linked to commits. |
| Upstream contracts | BLOCKED | Versioned, hashed QSO-GENOMES and QSO-SEEKER manifests/fixtures are unavailable. |
| Tests/determinism | NO EVIDENCE | Full tests pass; repeated seeded runs and fixtures reproduce identical hashes. |
| Freeze/rollback | NO EVIDENCE | Limits, freeze triggers, recovery, and rollback are tested without state corruption. |
| Security | NO EVIDENCE | No generated code executes; external data fails closed; credentials/network/repository writes remain bounded. |
| Documentation | NO EVIDENCE | Runtime partitions, messages, ledgers, limitations, and operational recovery are current. |
| Privacy/licensing | BLOCKED | Public notice model requires approval before artifacts may be published. |
| Provenance | NO EVIDENCE | Commit, seeds, inputs, tool versions, command logs, artifact hashes, and attestations recorded. |
| Approval | PENDING | Release approval after all included-scope gates pass. |

## Artifact Requirements
- Source archive or package for the reviewed commit.
- Versioned schemas, instance manifests, and fixed contract fixtures.
- Test, deterministic-run, security, resource-limit, freeze, and rollback reports.
- Append-only sample event and attribution artifacts containing no unapproved sensitive data.
- SBOM where packaged, checksums, and provenance manifest.

## Rollback Criteria
Rollback if schema/hash validation can be bypassed, generated material is executed without authorization, resource limits fail, freeze or rollback loses/corrupts evidence, deterministic runs diverge, attribution is inconsistent, or privacy/licensing approval is absent. Restore the last verified tag and preserve the failed candidate's evidence for diagnosis.

## Unresolved Blockers
- P0 baseline and every immediate punch-list item remain incomplete.
- Required QSO-GENOMES and QSO-SEEKER contracts are not published.
- No test, deterministic, freeze/rollback, security, documentation, or provenance evidence is recorded.
- Privacy, confidentiality, and licensing notice model requires approval.
- Payment-intent/distribution records remain outside release scope pending an approved policy boundary.
- No CI status is attached to the reviewed commit.

## Release Log
- 2026-07-16: Runtime candidate evaluated and held `BLOCKED`; no completed work selected.