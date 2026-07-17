# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Set the immediate product objective to a runnable, locally verifiable QuantumStateObjects package before any cross-repository or four-QSO experiment claim.
- 2026-07-16 — Prioritized repair of the missing CLI, real tests/CI, deterministic local fixtures, and freeze/rollback evidence; upstream integration remains blocked by QSO-GENOMES and QSO-SEEKER contracts.
- 2026-07-17 — Split P0 into canonical CLI-candidate acceptance followed by local configuration/runtime evidence so duplicate branches cannot silently redefine the release path.
- 2026-07-17 — Advanced the immediate objective from PR #6's earlier source/name/hash findings to PR #7's strict-UTF-8, schema-parity, and integer-version findings before broader runtime or integration work.

### Architecture
- The portfolio sequence begins with one accepted exact-head CLI/configuration baseline, then local runtime/message/ledger/freeze evidence, schema/hash contract validation, and finally the bounded four-QSO runner.
- Draft Experimenter object-model work remains outside the first release and cannot displace P0.
- Configuration acceptance requires agreement among the published schema, loader, resolver, later instantiation path, canonical QSO names, accepted upstream repository/path boundary, SHA-256 pins, strict UTF-8 decoding, complete required blocks, and integer-only schema versions.

### Added
- PR #7 rebuilds the bounded `qso-run` and local configuration candidate from current `main`, adds 15 deterministic unit/smoke tests, constrained setuptools package discovery, and Python 3.11/3.13 exact-head CI with read-only permissions, disabled checkout credential persistence, and retained artifacts.
- `deploy.md` defines fail-closed environment, permission, artifact, configuration, health, observability, rollback, and post-deployment gates.

### Changed
- PR #6 is closed without merge as superseded after its three review findings were repaired in PR #7; PR #2, PR #4, and PR #5 remain closed as superseded. PR #7 is the sole selected candidate.
- Planning records distinguish an exact-head passing candidate from an accepted or merged release head.
- Atlas's absent accepted genome hash remains an explicit fail-closed upstream-contract gate rather than an implicit missing-file condition.

### Verification
- Workflow run `29614395650` checked out and asserted PR #7 head `80e0546a53c139b26e956bce8f20c41e907739a6`.
- Python 3.11 and 3.13 jobs passed installation, compilation, all 15 unit/smoke tests, installed default/configuration CLI smoke, wheel construction, checksum generation, and retained-artifact upload.
- Artifact digests are `cdfd6817c3d0e0c07b41613072443c4fdd5aa0952ea68e4969ccee362ed7470a` and `221cfa42111ed0a6ac42c0311934d812f437f9eeeaa80d3f5cb574d155cde7ed`.
- Wheel SHA-256 values are `99fa4f424f4c1ca12ece6d0971e887708e7083275934904d264ace80ecac1790` and `7afba2f01fc3d9481989ea68302b79a8e671c7121572899c374e6c8f6a606dfd`.
- PR #7 resolved the earlier schema hash-pin, declared repository/path, and canonical-name findings.
- Three new unresolved P2 findings block acceptance: raw-byte JSON parsing can accept UTF-16/32 payloads, the CLI can accept manifests missing schema-required runtime blocks, and booleans can pass as numeric schema versions.

### Security
- The candidate explicitly declares no credential access, generated-code execution, network access, or repository writes.
- Exact-head checkout/assertion and retained evidence pass, but strict-UTF-8 parsing, complete schema parity, integer-only versions, merged-head verification, complete parser/dependency/secret/adversarial review, and local runtime validation remain required.

### Release
- The `0.1.0-alpha.1` candidate remains blocked. The CLI/configuration sub-slice advanced to PR #7 exact-head matrix CI with retained artifacts, but unresolved review findings, repaired final-head and merged-head acceptance, runtime/freeze/rollback evidence, upstream contracts, privacy/licensing, provenance, and approval remain incomplete.

### Deployment
- No runtime, package publication, four-QSO experiment, payment path, or production deployment is authorized.
- The only future initial target is a disposable credential-free local/CI verification environment after every release gate passes.
- PR #7 artifacts are review evidence only and do not authorize deployment.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
