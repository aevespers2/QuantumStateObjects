# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Set the immediate objective to a runnable, locally verifiable QuantumStateObjects package before cross-repository or four-QSO claims.
- 2026-07-17 — Selected PR #7 as the sole canonical CLI/configuration path and kept Experimenter work outside P0.
- 2026-07-17 — Advanced P0 from configuration-only evidence to one bounded runtime-primitives slice while retaining fail-closed review gates.

### Architecture
- The accepted sequence is: final PR #7 configuration/runtime acceptance → accepted QSO-GENOMES and QSO-SEEKER contracts → bounded four-QSO experiment with append-only evidence.
- Configuration, runtime instantiation, persisted evidence, checkpoints, freeze, and rollback must share one canonical schema/type/hash contract.
- Atlas, Nova, Orion, and Lyra may not be described as running without authorized append-only runtime and ledger proof.

### Added
- PR #7 adds a deterministic `RuntimeController` and focused synthetic tests for active/frozen/interrupted lifecycle states, message validation, hash-linked event and attribution ledgers, resource limits, freeze/resume, interruption/recovery, rollback/checkpoint restoration, and canonical state/event hashes.
- Exact-head CI retains JUnit, CLI/configuration, checked-out-SHA, wheel, and checksum evidence on Python 3.11 and 3.13.

### Changed
- PR #7 was reconciled with current `main` through normal two-parent head `395915b60510e9a62c53ad128cf23d151e73eb1f` without force-rewriting reviewed history; it is open, unmerged, mergeable, and zero commits behind `main`.
- Planning now treats the runtime slice as `REVIEW`, not accepted capability, because new correctness findings remain.

### Verification
- Workflow run `29617877793` passed on Python 3.11 and 3.13 at exact head `395915b60510e9a62c53ad128cf23d151e73eb1f`.
- Both jobs passed installation, compilation, 22 tests with zero failures/errors/skips, installed default/configuration CLI smoke, wheel construction, checksum generation, and retained-artifact upload.
- Artifact digests are `c53ecc7692716519be67c92e4e51cc04695187437790c784d8b42f78d70a76fd` and `cf2290f7469b71ebb92cc7b1cb7eb86a64ee9ff56df8b89203fa157bd6b65816`.
- Wheel SHA-256 values are `97c6ec287e2eb1b23776dc232a16641f566202f1aacf792755a992930adf5dc3` and `b074c2328f90585c2fe8fb7a83d023ef34ea7374b6ee9915c57209d589e678cc`.

### Review findings
- Three existing P2 findings remain: strict UTF-8 decoding, enforcement of all required instance blocks, and rejection of Boolean schema versions.
- Five additional P2 findings were recorded: enforce the instance-ID schema pattern; restore state when delegated ingest raises; use one canonical message-inclusive checkpoint when freezing; preserve rollback at a full event ceiling; and reject malformed persisted event-entry shapes/types.

### Security
- Candidate CI uses read-only contents permission, exact submitted-head checkout/assertion, and disabled checkout credential persistence.
- The runtime slice uses synthetic local fixtures and does not execute generated snippets, access credentials, consume networked runtime inputs, write external repositories, or run the four named QSOs.
- Complete parser, state-atomicity, checkpoint, rollback-capacity, persisted-evidence, dependency, secret, workflow, and adversarial review remains required.

### Release
- The first eligible version remains `0.1.0-alpha.1`.
- Release remains blocked by eight unresolved P2 findings, repaired final-head and merged-head verification, accepted upstream contracts, source/sdist/SBOM/provenance, privacy/licensing, rollback drill, and approval.

### Deployment
- No runtime, package publication, scheduled execution, four-QSO experiment, external integration, payment path, or production deployment is authorized.
- The only future initial target is a disposable credential-free, network-disabled local/CI verification environment after every release gate passes.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
