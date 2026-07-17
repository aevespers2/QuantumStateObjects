# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [ ] **Accept one canonical CLI candidate.** PR #6 is the clean candidate rebuilt from current `main`; accept it only after its latest submitted head passes exact-head Python 3.11/3.13 CI and retained artifacts are inspected.
- [ ] **Disposition older candidates.** Keep PR #4 and PR #5 open only until PR #6 is verified; then record them as superseded without discarding their evidence. PR #2 is already superseded and draft PR #3 remains outside P0.
- [ ] **Run and record the accepted repository baseline.** Require exact-head checkout assertion, clean installation, compilation, tests, installed `qso-run`, `qso-run --version`, deterministic output, invalid-argument failure, wheel/sdist creation, checksums, and retained logs at one immutable head.
- [ ] Inventory the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Add validated local configuration loading plus malformed, missing, duplicate, and mismatched-hash fixtures that fail closed.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #6 was created from current `main` as a conflict-free replacement candidate containing the missing `qso_runtime/cli.py`, four deterministic CLI tests, constrained `qso_runtime*` package discovery, and least-privilege CI.
- [x] PR #6 CI checks out `${{ github.event.pull_request.head.sha || github.sha }}`, asserts the checked-out SHA, disables persisted checkout credentials, and retains the SHA, Python version, deterministic CLI output, CLI version, wheel, and SHA-256 manifest for 30 days.
- [x] Independent reconstructed verification passed four tests, source/test compilation, workflow YAML parsing, wheel construction, and checksum generation; the reconstructed wheel SHA-256 was `df0bc69d33ac9165f4f75c074c6b7b21b304dbe83a1c2517442c8b21bf1650c3`.
- [ ] Latest-head GitHub-hosted CI and artifact inspection for PR #6 remain required before canonical acceptance.
- [ ] Earlier PR #4 matrix CI passed functional checks but used a synthetic merge ref and retained no artifact; PR #5 has local replay evidence but no attached workflow.

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
