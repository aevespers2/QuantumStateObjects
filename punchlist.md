# QSOBuilder Punch List

The Architect sets dependency order in `taskchain.md`. Execute one bounded, testable item at a time and do not bypass blocked cross-repository gates.

## Immediate

- [x] **Accept one canonical CLI candidate.** PR #6 exact-head Python 3.11/3.13 CI and retained artifacts passed at `9389d5322f535f59bd5db386dffe7ca2c9b052cf`.
- [x] **Disposition older candidates.** PR #4 and PR #5 were closed as superseded without discarding their evidence; PR #2 remains superseded and draft PR #3 remains outside P0.
- [x] **Run and record the canonical repository baseline.** Exact-head checkout assertion, installation, compilation, four tests, installed `qso-run`, version output, deterministic JSON, wheel construction, checksums, and retained artifacts passed in run `29607170551`.
- [ ] Inventory the four instance manifests, runtime partitions, message integrity, freeze/rollback controller, resource caps, event ledger, and attribution ledger.
- [ ] **Complete validated local configuration loading.** `qso_runtime/config.py` now validates bounded local JSON, unique instance identities, the Atlas/Nova/Orion/Lyra set, normalized genome paths, schema versions, optional SHA-256 pins, file size limits, and non-symlink files. `qso-run --config` exposes the data-only validation path. Final exact-head CI remains required.
- [x] **Make Atlas fail closed while its upstream genome is absent.** Local genome resolution now requires a hash-pinned file beneath an explicit local root. The current Atlas reference has no accepted SHA-256, so resolution rejects it before any execution or network access.
- [ ] Confirm every generated snippet remains inert and requires Sprite plus human review.
- [ ] Prepare contract-validation tests that can consume fixed QSO-GENOMES and QSO-SEEKER fixtures once their manifests are published.

## Current evidence

- [x] PR #6 is the canonical conflict-free runnable baseline and retained exact-head evidence for Python 3.11 and 3.13.
- [x] Retained artifacts identify exact head `9389d5322f535f59bd5db386dffe7ca2c9b052cf`; wheel SHA-256 values are `824f4cb6566ee57c928e7c454e85820361bb16aa1c215ce894650817a92e582a` and `d042860df91eb43522bbbe3ce6a89fd1c4bceb274a1737bc3a53edb2785a7651`.
- [x] The local configuration slice added `qso_runtime/config.py`, CLI configuration validation, and seven configuration tests covering the repository manifest, malformed JSON, duplicate identities, Atlas's missing hash, mismatched hashes, and deterministic resolution of bounded local fixtures.
- [x] Reconstructed verification passed 11 tests, source/test compilation, and `python -m qso_runtime.cli --config config/instances.json`; no generated snippets, credentials, network access, or external repository writes were used.
- [ ] GitHub-hosted exact-head CI and retained-artifact inspection remain required for the new configuration slice.
- [ ] The repository manifest references `genomes/atlas.json` but has no accepted genome SHA-256; this is now an explicit fail-closed upstream-contract blocker rather than an implicit missing-file failure.

## After upstream contracts are green

- [ ] Validate genome and canonical-record schema versions and hashes without importing external code.
- [ ] Run the four-QSO deterministic experiment with bounded time, memory, records, messages, and proposal counts.
- [ ] Emit reproducible JSON evidence for seeds, inputs, events, proposals, critiques, freeze decisions, rollbacks, and attribution.

## Held behind approval

- [ ] Simulated payment-intent/distribution records remain blocked until the declarative policy contract is approved.
- [ ] Production settlement, credentials, custody, automatic transfers, and unrestricted repository writes are out of scope.

## Quality Gates

- [ ] Deterministic runtime tests and documented rollback path.
- [ ] Security, dependency, workflow, secret, and adversarial review at the accepted exact head.
- [ ] No generated code is executed without validation and explicit human authorization.
- [ ] Observations, inferences, hypotheses, proposals, and goals remain distinguishable.
- [ ] Public artifacts contain only approved privacy, confidentiality, and licensing notices.
