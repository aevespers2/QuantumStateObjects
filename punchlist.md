# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [ ] **Select one canonical CLI candidate.** Prefer PR #4 because it includes package-discovery repair, Python 3.11/3.13 CI, and explicit credential boundaries; keep PR #5 as a duplicate candidate until disposition is recorded.
- [ ] **Make PR #4 exact-head verifiable.** The workflow now checks out `${{ github.event.pull_request.head.sha || github.sha }}`, asserts the checked-out SHA, disables persisted credentials, builds checksummed wheels, and retains evidence artifacts for 30 days. Final latest-head GitHub Actions evidence is still required.
- [ ] **Resolve PR #4 review threads.** Confirm package discovery, build requirements, and `persist-credentials: false` remain repaired; resolve only after the final head passes.
- [ ] **Disposition duplicates.** Record PR #2 as superseded, keep draft PR #3 outside P0, and explicitly supersede or close PR #5 only after PR #4's canonical status is accepted.
- [ ] **Run and record the accepted repository baseline.** Require clean installation, compilation, tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument failure, wheel/sdist creation, checksums, and retained logs at one immutable head.
- [ ] Inventory the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Add validated local configuration loading plus malformed, missing, duplicate, and mismatched-hash fixtures that fail closed.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #4 workflow run `29599534913` passed two matrix jobs on Python 3.11 and 3.13.
- [x] The prior run passed installation, compilation, four focused tests, CLI smoke, boundary JSON validation, version output, and wheel construction.
- [x] Checkout credential persistence is disabled, package discovery is constrained to `qso_runtime*`, and build dependencies are installed.
- [x] Commit `e9ba8736a00b7f356c352a81a1e7bf409c38c18e` repaired exact-head checkout/assertion and added retained evidence containing checked-out SHA, Python version, deterministic CLI JSON, CLI version, wheel, and SHA-256 manifest.
- [x] Independent reconstructed verification of that bounded slice passed four tests, source/test compilation, wheel construction, workflow YAML parsing, and wheel SHA-256 `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`.
- [ ] Final GitHub-hosted exact-head evidence is not yet recorded for the latest PR head.
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
