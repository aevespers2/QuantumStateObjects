# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate
- [x] Run and record the repository test/CI baseline. PR #4 restores `qso-run`, adds four deterministic CLI tests, constrains package discovery to `qso_runtime*`, and adds Python 3.11/3.13 CI. Workflow run `29599420796` passed compilation, pytest, installed CLI smoke, boundary validation, version output, and wheel construction in both matrix jobs.
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
- 2026-07-17 — PR #4 created from current `main` at base `6eb647919a40618066c272569c0d3e320394e89a`. Candidate head `62bc5784619c1d689694f0d0182692302acf6316` restored `qso_runtime.cli:main`, added four focused deterministic tests, constrained setuptools discovery to the runtime package, and added least-privilege CI for Python 3.11 and 3.13 with checkout credential persistence disabled.
- 2026-07-17 — GitHub Actions run `29599420796` completed successfully for Python 3.11 and 3.13. Both jobs passed package installation, bytecode compilation, four pytest cases, installed `qso-run` JSON smoke, explicit no-credential/no-network/no-repository-write/no-generated-code-execution boundary checks, `qso-run --version`, and wheel construction. The next P0 slice is local configuration loading and fail-closed validation; broader runtime, freeze/rollback, Atlas genome, and upstream contract gates remain open.
