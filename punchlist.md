# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate
- [ ] Run and record the repository test/CI baseline. **IN PROGRESS:** the missing `qso-run` entry point and three focused CLI tests are present on `builder/runnable-cli-baseline-v1`; full repository tests and attached CI remain pending.
- [ ] Inventory the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## After upstream contracts are green
- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, and proposal counts.
- [ ] Emit reproducible JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, rollbacks, and attribution.

## Held behind approval
- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, and unrestricted repository writes are out of scope.

## Quality Gates
- [ ] Deterministic tests and documented rollback path.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.

## Evidence Log
- 2026-07-17 — Bounded CLI candidate added with machine-readable self-check, version output, and explicit no-network/no-repository-write/no-generated-code-execution boundaries. Exact candidate-file replay under CPython 3.13.5 passed three focused tests, bytecode compilation, no-isolation wheel construction, isolated installation, `qso-run`, and `qso-run --version`. A clean checkout and GitHub Actions result are still required before the baseline item can be checked.
