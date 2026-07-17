# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [x] **Select one canonical CLI/configuration candidate.** PR #7 is the sole selected path; PR #6, PR #5, PR #4, and PR #2 are closed as superseded without merge, and draft PR #3 remains outside P0.
- [x] **Make PR #7 exact-head verifiable.** Run `29614395650` checked out and asserted head `80e0546a53c139b26e956bce8f20c41e907739a6`, passed Python 3.11/3.13 CI, and retained non-secret artifacts.
- [x] **Repair the prior schema/hash-pin, source-contract, and canonical-name findings.** PR #7 permits the optional lowercase SHA-256 field, restricts genomes to `aevespers2/QSO-GENOMES` canonical paths, and requires exact Atlas/Nova/Orion/Lyra names.
- [ ] **Enforce strict UTF-8 JSON.** Decode bounded configuration and genome bytes with strict UTF-8 before `json.loads`; add UTF-16/UTF-32 negative fixtures.
- [ ] **Enforce all schema-required instance fields.** Reject manifests missing required identity, development, review, or status blocks before constructing an accepted runtime manifest; add positive and negative schema-parity tests.
- [ ] **Reject boolean schema versions.** Require integer type and value `1` for both instance and genome schema versions; add `true`/`false` negative fixtures.
- [ ] **Resolve every PR #7 review thread and rerun final-head CI.** Retain artifacts and inspect checked-out SHA, all tests, configuration evidence, wheel hashes, and review disposition at the repaired immutable head.
- [ ] **Run merged-head acceptance.** After review and merge authorization, require clean installation, compilation, complete tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument/configuration failures, wheel and sdist creation, checksums, and retained logs at the merged head.
- [ ] Inventory and test the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #7 workflow run `29614395650` passed Python 3.11 and 3.13 matrix jobs.
- [x] Both jobs checked out and asserted exact submitted head `80e0546a53c139b26e956bce8f20c41e907739a6` with checkout credential persistence disabled and read-only contents permission.
- [x] The run passed installation, compilation, all 15 unit/smoke tests, installed default/configuration CLI smoke, boundary validation, wheel construction, checksum generation, and retained-artifact upload.
- [x] Artifact digests: Python 3.11 `cdfd6817c3d0e0c07b41613072443c4fdd5aa0952ea68e4969ccee362ed7470a`; Python 3.13 `221cfa42111ed0a6ac42c0311934d812f437f9eeeaa80d3f5cb574d155cde7ed`.
- [x] Wheel SHA-256: Python 3.11 `99fa4f424f4c1ca12ece6d0971e887708e7083275934904d264ace80ecac1790`; Python 3.13 `7afba2f01fc3d9481989ea68302b79a8e671c7121572899c374e6c8f6a606dfd`.
- [x] PR #6's three review findings were answered and resolved before it was closed as superseded.
- [x] Atlas fails closed before file access or network activity because no accepted upstream SHA-256 is present.
- [ ] Three new P2 correctness threads remain unresolved: non-UTF-8 payload acceptance, acceptance of manifests missing schema-required runtime fields, and boolean schema-version acceptance.
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
