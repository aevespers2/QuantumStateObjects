# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Set the immediate product objective to a runnable, locally verifiable QuantumStateObjects package before any cross-repository or four-QSO experiment claim.
- 2026-07-16 — Prioritized repair of the missing CLI, real tests/CI, deterministic local fixtures, and freeze/rollback evidence; upstream integration remains blocked by QSO-GENOMES and QSO-SEEKER contracts.
- 2026-07-17 — Split P0 into canonical CLI-candidate acceptance followed by local configuration/runtime evidence so duplicate branches cannot silently redefine the release path.
- 2026-07-17 — Advanced the immediate objective to repairing PR #6's schema/source/name contract findings before broader runtime or integration work.

### Architecture
- The portfolio sequence now begins with one accepted exact-head CLI/configuration baseline, then local runtime/message/ledger/freeze evidence, schema/hash contract validation, and finally the bounded four-QSO runner.
- Draft Experimenter object-model work remains outside the first release and cannot displace P0.
- Configuration acceptance now explicitly requires agreement among the published schema, loader, canonical QSO names, accepted upstream repository/path boundary, and SHA-256 pins.

### Added
- PR #6 adds the canonical bounded `qso-run` implementation, standard-library local configuration validation, four deterministic CLI tests, seven configuration tests, constrained setuptools package discovery, and Python 3.11/3.13 exact-head CI with read-only permissions, disabled checkout credential persistence, and retained artifacts.
- `deploy.md` defines fail-closed environment, permission, artifact, configuration, health, observability, rollback, and post-deployment gates.

### Changed
- PR #2, PR #4, and PR #5 are closed as superseded without merge; PR #6 is the sole selected candidate.
- Planning records now distinguish an exact-head passing candidate from an accepted or merged release head.
- Atlas's absent accepted genome hash is represented as an explicit fail-closed upstream-contract gate rather than an implicit missing-file condition.

### Verification
- Workflow run `29610600428` checked out and asserted PR #6 head `6e382853e6746f8eb18e97c64481dccfe6684652`.
- Python 3.11 and 3.13 jobs passed installation, compilation, all 11 unit/smoke tests, installed CLI smoke, boundary validation, version output, wheel construction, checksum generation, and retained-artifact upload.
- Artifact digests are `505be6dae69827c150c72161ed348a752cf623a9589b29045c70000ff7aa2422` and `f44653928b2974f10f76822aebdac89fd31cdedf485f3ee9b5758be2766ae5f1`.
- Wheel SHA-256 values are `9c1a1fe0209864d1e614d491da881f004792fac288b14a98596e021de2abf7f2` and `be85a103430e911974c28073a2e3bb283c7fdc9d30812b5b8ef9f0fd49e5a225`.
- Three unresolved P2 findings block acceptance: the instance schema omits the required genome hash pin, the resolver can accept references outside the declared QSO-GENOMES repository/path contract, and non-canonical QSO name casing can pass.

### Security
- The candidate explicitly declares no credential access, generated-code execution, network access, or repository writes.
- Exact-head checkout/assertion and retained evidence now pass, but schema/loader contract agreement, canonical source/name enforcement, merged-head verification, complete parser/dependency/secret/adversarial review, and local runtime validation remain required.

### Release
- The `0.1.0-alpha.1` candidate remains blocked. The CLI/configuration sub-slice advanced to exact-head matrix CI with retained artifacts, but unresolved review findings, merged-head acceptance, runtime/freeze/rollback evidence, upstream contracts, privacy/licensing, provenance, and approval remain incomplete.

### Deployment
- No runtime, package publication, four-QSO experiment, payment path, or production deployment is authorized.
- The only future initial target is a disposable credential-free local/CI verification environment after every release gate passes.
- PR #6 artifacts are review evidence only and do not authorize deployment.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable