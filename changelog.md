# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Set the immediate product objective to a runnable, locally verifiable QuantumStateObjects package before any cross-repository or four-QSO experiment claim.
- 2026-07-16 — Prioritized repair of the missing CLI, real tests/CI, deterministic local fixtures, and freeze/rollback evidence; upstream integration remains blocked by QSO-GENOMES and QSO-SEEKER contracts.
- 2026-07-17 — Split P0 into canonical CLI-candidate acceptance followed by local configuration/runtime evidence so duplicate branches cannot silently redefine the release path.

### Architecture
- The portfolio sequence now begins with one accepted exact-head CLI/package baseline, then local runtime/configuration evidence, schema/hash contract validation, and finally the bounded four-QSO runner.
- Draft Experimenter object-model work remains outside the first release and cannot displace P0.

### Added
- PR #4 adds the preferred bounded `qso-run` implementation, four deterministic CLI tests, constrained setuptools package discovery, and Python 3.11/3.13 CI with read-only permissions and disabled checkout credential persistence.
- `deploy.md` defines fail-closed environment, permission, artifact, health, observability, rollback, and post-deployment gates.

### Changed
- PR #2 is closed as superseded.
- PR #5 is classified as a duplicate local-replay candidate and is not selected while PR #4 remains the stronger evidence path.
- Planning records now distinguish successful merge-ref CI from accepted exact-head CI.

### Verification
- Workflow run `29599534913` passed installation, compilation, four tests, installed CLI smoke, boundary JSON validation, version output, and wheel construction for Python 3.11 and 3.13.
- The run checked out synthetic merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701`, not submitted head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`; exact-head acceptance remains open.
- The run retained no workflow artifacts, and PR #4 review threads remain unresolved.
- PR #5 reports five reconstructed exact-file tests and wheel SHA-256 `8562d17728721c7f2ba4f4ad0fc0ec262ed0e1bc0bc853f4a2643518ba55f14f`, but has no attached CI or independent complete-tree clone evidence.

### Security
- The preferred candidate explicitly declares no credential access, generated-code execution, network access, or repository writes.
- Exact-head checkout/assertion, retained evidence, complete parser/dependency/secret/adversarial review, and local runtime validation remain required.

### Release
- The `0.1.0-alpha.1` candidate remains blocked. The CLI/test sub-slice advanced from missing implementation to successful merge-ref matrix CI, but canonical candidate disposition, exact-head verification, retained artifacts, local configuration/runtime evidence, upstream contracts, privacy/licensing, provenance, rollback, and approval are incomplete.

### Deployment
- No runtime, package publication, four-QSO experiment, payment path, or production deployment is authorized.
- The only future initial target is a disposable credential-free local/CI verification environment after every release gate passes.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable