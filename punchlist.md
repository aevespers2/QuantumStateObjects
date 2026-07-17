# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate
- [ ] Run and record the repository test/CI baseline. **IN PROGRESS:** PR #5 adds the missing `qso-run` entry point and five focused unit/smoke/fail-closed tests on a fresh branch from current `main`; reconstructed exact-file replay passed, while attached exact-head CI and a complete-tree clean checkout remain pending.
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
- 2026-07-17 — PR #5 added `qso_runtime/cli.py` and five tests covering deterministic machine-readable output, version metadata, pretty JSON, module-entry smoke, and invalid-argument fail-closed behavior. Reconstructed exact-file replay passed `python -m pytest` (5 passed), bytecode compilation, no-isolation wheel construction, isolated wheel installation, `qso-run`, and `qso-run --version`; wheel SHA-256 was `8562d17728721c7f2ba4f4ad0fc0ec262ed0e1bc0bc853f4a2643518ba55f14f`. The execution environment could not resolve `github.com`, so a cloned complete-tree replay and attached CI are still required.
