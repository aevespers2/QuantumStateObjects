# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [x] **Rebase the canonical configuration repair on current `main`.** PR #7 was created from current `main` after PR #6 diverged by five planning commits and could no longer produce an exact-head pull-request workflow run.
- [x] **Repair schema/hash-pin agreement.** `schema/qso-instance.schema.json` now permits an optional lowercase 64-character `genome.sha256` while the resolver continues to require it before reading local genome data.
- [x] **Enforce the declared genome source contract.** The loader rejects repositories other than `aevespers2/QSO-GENOMES` and rejects any per-QSO path other than its canonical `genomes/<name>.json` location.
- [x] **Require canonical QSO names.** The loader now accepts only exact case-sensitive `Atlas`, `Nova`, `Orion`, and `Lyra` names with unique identities.
- [ ] **Accept PR #7 at an immutable head.** Require Python 3.11/3.13 exact-head CI, all 15 tests, installed default/configuration CLI smoke, wheel hashes, retained artifacts, review disposition, and a mergeable current-main diff.
- [ ] **Disposition PR #6.** Close it as superseded only after PR #7 passes exact-head verification so its earlier evidence and review history remain available.
- [ ] **Run merged-head acceptance.** After review and merge authorization, require clean installation, compilation, complete tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument/configuration failures, wheel and sdist creation, checksums, and retained logs at the merged head.
- [ ] Inventory and test the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] Earlier PR #6 workflow run `29610600428` passed Python 3.11 and 3.13 at exact head `6e382853e6746f8eb18e97c64481dccfe6684652`, establishing the initial CLI/configuration baseline and retained artifacts.
- [x] PR #7 starts from current `main` commit `dd455b52beb0c257d2f11abc994da6b94085c2c3`, eliminating PR #6's five-commit planning divergence.
- [x] Reconstructed verification for PR #7 passed source/test compilation, all 15 unit/smoke tests, and `python -m qso_runtime.cli --config config/instances.json`.
- [x] Four focused regression tests cover exact canonical name casing, accepted genome repository, canonical per-QSO paths, and schema support for the optional hash pin.
- [x] Atlas continues to fail closed before file access or network activity because no accepted upstream SHA-256 is present.
- [ ] PR #7 exact-head hosted CI, retained-artifact inspection, review, and mergeability confirmation remain required.
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
