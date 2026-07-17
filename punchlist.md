# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [ ] **Select one canonical CLI candidate.** Prefer PR #4 because it includes package-discovery repair, Python 3.11/3.13 CI, and explicit credential boundaries; keep PR #5 as a duplicate candidate until disposition is recorded.
- [ ] **Make PR #4 exact-head verifiable.** Configure checkout with `ref: ${{ github.event.pull_request.head.sha }}`, assert `git rev-parse HEAD` equals `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`, rerun CI, and retain non-secret test/build evidence.
- [ ] **Resolve PR #4 review threads.** Confirm package discovery, build requirements, and `persist-credentials: false` remain repaired; resolve only after the final head passes.
- [ ] **Disposition duplicates.** Record PR #2 as superseded, keep draft PR #3 outside P0, and explicitly supersede or close PR #5 only after PR #4's canonical status is accepted.
- [ ] **Run and record the accepted repository baseline.** Require clean installation, compilation, tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument failure, wheel/sdist creation, checksums, and retained logs at one immutable head.
- [ ] Inventory the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Add validated local configuration loading plus malformed, missing, duplicate, and mismatched-hash fixtures that fail closed.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #4 workflow run `29599534913` passed two matrix jobs on Python 3.11 and 3.13.
- [x] The run passed installation, compilation, four focused tests, CLI smoke, boundary JSON validation, version output, and wheel construction.
- [x] Checkout credential persistence was disabled, package discovery was constrained to `qso_runtime*`, and build dependencies were installed.
- [ ] Exact-head evidence is **not** satisfied: the workflow checked out synthetic merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701`, not PR head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b`.
- [ ] No workflow artifact was retained for run `29599534913`.
- [ ] PR #5 has five local replay tests and a wheel checksum, but no attached workflow and no complete-tree independent clone evidence.

## After upstream contracts are green

- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, and proposal counts.
- [ ] Emit reproducible JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, rollbacks, and attribution.

## Held behind approval

- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, and unrestricted repository writes are out of scope.

## Quality Gates

- [ ] Deterministic tests and documented rollback path.
- [ ] Security, dependency, workflow, secret, and adversarial review at the accepted exact head.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.