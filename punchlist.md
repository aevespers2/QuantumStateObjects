# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate
- [ ] Run and record the repository test/CI baseline. **IN PROGRESS:** PR #4 restores `qso-run`, adds four deterministic CLI tests, and adds Python 3.11/3.13 CI; exact-head workflow results are required before completion.
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
- 2026-07-17 — PR #4 created from current `main` at base `6eb647919a40618066c272569c0d3e320394e89a`. Candidate head initially `d684938ced6333df22c1fc2bc7ebc61dfc89973b`; it restores `qso_runtime.cli:main`, adds four focused deterministic tests, and adds least-privilege CI for Python 3.11 and 3.13. The workflow compiles source/tests, runs pytest, installs and invokes `qso-run`, verifies explicit no-credential/no-network/no-repository-write/no-generated-code-execution boundaries, and builds a wheel. Exact-head CI must pass before this item is checked.
