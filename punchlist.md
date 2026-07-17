# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [x] **Select one canonical CLI/configuration candidate.** PR #6 is the sole selected path; PR #4 and PR #5 are closed as superseded, PR #2 remains superseded, and draft PR #3 remains outside P0.
- [x] **Make the candidate exact-head verifiable.** Run `29610600428` checked out and asserted head `6e382853e6746f8eb18e97c64481dccfe6684652`, passed Python 3.11/3.13 CI, and retained non-secret artifacts.
- [ ] **Repair PR #6 schema/hash-pin agreement.** Add the accepted `genome.sha256` field and constraints to `schema/qso-instance.schema.json` so schema-valid manifests can satisfy the resolver without weakening fail-closed behavior.
- [ ] **Enforce the declared genome source contract.** Reject repositories and paths outside the accepted `aevespers2/QSO-GENOMES` boundary and exact versioned artifact layout; add positive and negative tests.
- [ ] **Require canonical QSO names.** Reject non-canonical case variants and require exactly `Atlas`, `Nova`, `Orion`, and `Lyra` with unique identities.
- [ ] **Resolve all PR #6 review threads and rerun final-head CI.** Retain artifacts and inspect checked-out SHA, test results, configuration evidence, wheel hashes, and review disposition at the repaired immutable head.
- [ ] **Run merged-head acceptance.** After review and merge authorization, require clean installation, compilation, complete tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument/configuration failures, wheel and sdist creation, checksums, and retained logs at the merged head.
- [ ] Inventory and test the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #6 workflow run `29610600428` passed Python 3.11 and 3.13 matrix jobs.
- [x] Both jobs checked out and asserted exact submitted head `6e382853e6746f8eb18e97c64481dccfe6684652` with checkout credential persistence disabled and read-only contents permission.
- [x] The run passed installation, compilation, all 11 unit/smoke tests, installed CLI smoke, boundary validation, version output, wheel construction, checksum generation, and retained-artifact upload.
- [x] Artifact digests: Python 3.11 `505be6dae69827c150c72161ed348a752cf623a9589b29045c70000ff7aa2422`; Python 3.13 `f44653928b2974f10f76822aebdac89fd31cdedf485f3ee9b5758be2766ae5f1`.
- [x] Wheel SHA-256: Python 3.11 `9c1a1fe0209864d1e614d491da881f004792fac288b14a98596e021de2abf7f2`; Python 3.13 `be85a103430e911974c28073a2e3bb283c7fdc9d30812b5b8ef9f0fd49e5a225`.
- [x] Local configuration validation covers bounded UTF-8 JSON, exact instance count/set, uniqueness, schema versions, relative JSON paths, regular non-symlink files, file-size limits, and optional SHA-256 resolution beneath an explicit local root.
- [x] Atlas currently fails closed before file access or network activity because no accepted upstream SHA-256 is present.
- [ ] Three P2 correctness threads remain unresolved: schema omission of the hash pin, repository/path contract bypass, and case-insensitive acceptance of QSO names.
- [ ] QSO-GENOMES PR #2 remains unaccepted and cannot yet supply a trusted Atlas hash-pinned fixture.

## After upstream contracts are green

- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, and proposal counts.
- [ ] Emit reproducible JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, rollbacks, and attribution.

## Held behind approval

- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, and unrestricted repository writes are out of scope.

## Quality Gates

- [ ] Deterministic runtime tests and documented rollback path.
- [ ] Security, dependency, workflow, secret, parser/contract, and adversarial review at the accepted exact and merged heads.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.