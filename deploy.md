# Deployment Plan

## Current Decision

Status: `BLOCKED — NO DEPLOYMENT TARGET AUTHORIZED`

PR #7 is open, unmerged, mergeable, and reconciled with current `main` at head `395915b60510e9a62c53ad128cf23d151e73eb1f`. Exact-head run `29617877793` passed Python 3.11/3.13 installation, compilation, 22 tests, installed CLI/configuration smoke, wheel construction, and retained-artifact upload. This is candidate review evidence only. Eight unresolved P2 findings, merged-head verification, accepted upstream contracts, full security/provenance/privacy/licensing evidence, rollback drill, and approval still block every deployment.

## Permitted First Target

Only after every release gate passes, the first target may be a disposable local or CI verification environment with synthetic non-sensitive fixtures, no production or personal credentials, no network-dependent inputs, no external repository writes, no generated-code execution, no payment/custody/signing/settlement capability, bounded CPU/memory/time/message/event/artifact limits, and explicit human start, stop, freeze, rollback, and cleanup controls.

## Source, Version, Permission, and Artifact Gates

Bind a verification run to one accepted immutable source and merged head. Record repository, PR, source/merged SHA, review disposition, package/Python/schema/configuration/instance/message/event/attribution/checkpoint/freeze/rollback/upstream-contract versions, source/sdist/wheel/configuration/fixture/report hashes, workflow run/job/artifact identities and expiry, SBOM where applicable, and provenance/attestation references.

PR #7 artifacts currently retained through August 16, 2026 have digests `c53ecc7692716519be67c92e4e51cc04695187437790c784d8b42f78d70a76fd` and `cf2290f7469b71ebb92cc7b1cb7eb86a64ee9ff56df8b89203fa157bd6b65816`; wheel SHA-256 values are `97c6ec287e2eb1b23776dc232a16641f566202f1aacf792755a992930adf5dc3` and `b074c2328f90585c2fe8fb7a83d023ef34ea7374b6ee9915c57209d589e678cc`. They do not satisfy the full artifact gate.

GitHub Actions permissions must remain `contents: read` or narrower, checkout credentials must not persist, no secret/token/key/cloud/package/payment credential may be present, writes must stay inside a disposable evidence directory, external commands/plugins/dynamic imports/generated snippets must be denied unless separately reviewed, and network access must be independently unavailable.

Required retained evidence includes exact-head and merged-head identity, clean build/install, complete positive/negative/adversarial tests, source/sdist/wheel/checksums, sanitized manifests/fixtures, sample event and attribution ledgers, checkpoints/freeze/rollback/recovery evidence, security and dependency reports, review-thread disposition, rollback drill, and explicit release/deployment approval.

## Configuration and Runtime Gate

Configuration and genomes must be bounded, local, strict UTF-8, versioned, schema-validated, and fail closed for missing required blocks, unknown/duplicate identities, invalid instance IDs, non-canonical names, Boolean/string/float schema versions, unapproved repository/path, missing or mismatched hashes, unsupported capabilities, and denied network/credential/write/generated-code/payment requests.

Runtime operations must be atomic. Delegated ingest exceptions may not leave unledgered state. Freeze certificates and controller checkpoints must use one canonical message-inclusive state. Rollback must restore state even when the event ceiling is full. Persisted event ledgers must reject malformed shapes, missing fields, Boolean/non-integer sequences, invalid hashes, and non-canonical entries.

## Pre-Deployment Validation

1. Assert the checked-out SHA equals the accepted source head.
2. Verify source, sdist, wheel, configuration, schema, fixture, and upstream hashes.
3. Install in a clean disposable environment and compile source/tests.
4. Run the complete unit, smoke, negative, adversarial, security, dependency, and secret suite.
5. Run `qso-run`, `qso-run --version`, configuration smoke, deterministic replay, and invalid-argument paths.
6. Exercise all eight current finding classes and prove fail-closed atomic behavior.
7. Exercise lifecycle, resource ceilings, interruption, freeze, checkpoint, rollback, recovery, event and attribution integrity.
8. Confirm no network, credentials, external writes, generated execution, payment activity, or sensitive-data access.
9. Produce a hash-bound deployment-readiness report for human review.

## Health Checks

A verification run is healthy only when startup and clean shutdown succeed; instances load exactly once with accepted source identity and complete schema fields; repeated fixtures reproduce canonical state/event hashes; message/event/attribution/checkpoint heads validate; failed operations leave no partial state; rollback succeeds at capacity; resource use stays within limits; invalid inputs fail closed; no denied capability appears; all output remains in the disposable directory; and status clearly distinguishes `PASS`, `FAIL`, and `UNKNOWN`.

## Observability

Retain structured non-secret evidence for source/configuration/upstream identity, schema/loader/runtime versions, lifecycle transitions, message counts/sizes/order/rejections/hashes, mutation attempts and atomic restoration, resource limits, validation failures, denied capabilities, event/attribution/checkpoint/freeze/rollback heads, test/health/cleanup/post-validation results, and exact artifact hashes. Do not capture credentials or unapproved personal/confidential content.

## Rollback Triggers and Procedure

Immediately stop and roll back if source or artifact identity differs; encoding/schema/type/ID/source/path/hash checks fail; malformed evidence is accepted; delegated mutation leaves partial state; checkpoint/freeze/rollback diverges or fails at capacity; deterministic outputs diverge; limits or stop controls fail; denied capability appears; sensitive data enters artifacts; upstream contracts disappear/change; or health becomes `FAIL` or materially `UNKNOWN`.

Preserve logs, failed inputs, exact identities, ledger/checkpoint heads, and resource evidence; restore the last accepted checkpoint or remove the disposable run state; verify no external repository, credential, registry, network service, or payment system was modified; record trigger/scope/recovery; and do not resume until a new immutable candidate passes the complete gates and receives approval.

## Post-Deployment Validation

Repeat CLI/configuration smoke and deterministic replay; validate final event/attribution/checkpoint hashes; prove cleanup removed transient state without deleting retained evidence; confirm no denied capability or sensitive-data leakage occurred; compare resource use with approved bounds; test disablement/revocation controls; archive checksums/reports/disposition; and return the environment to a known clean state.

## Promotion Rules

A disposable verification pass does not authorize package publication, persistent hosting, scheduled execution, multi-user service, four-QSO operation, external integration, credentials, or production deployment. Every promotion requires a separately scoped architecture, threat model, acceptance matrix, rollback drill, evidence bundle, and explicit approval.

## Deployment Log

- 2026-07-17 — Added a fail-closed deployment plan; no deployment was attempted or authorized.
- 2026-07-17 — Recorded PR #7 exact-head configuration evidence and three parser/schema blockers.
- 2026-07-17 — Recorded reconciled head `395915b60510e9a62c53ad128cf23d151e73eb1f`, run `29617877793`, 22-test runtime evidence, and five additional runtime/evidence findings. Deployment remains blocked.
