# Deployment Plan

## Current Decision

Status: `BLOCKED — NO DEPLOYMENT TARGET AUTHORIZED`

This repository has no approved runtime, package publication, four-QSO execution, payment, or production deployment. PR #7 has successful exact-head Python 3.11/3.13 CI, 15 passing tests, and retained artifacts, but the candidate remains blocked by three unresolved parser/schema-enforcement findings, repaired final-head and merged-head verification, complete runtime integrity, resource limits, freeze/rollback, upstream contracts, privacy/licensing, provenance, and release approval.

## Permitted First Target

After every release gate passes, the first permitted target is a disposable local or CI verification environment with:

- no production or personal credentials;
- no network-dependent inputs;
- no external repository writes;
- no generated-code execution;
- no payment, custody, signing, or settlement capability;
- synthetic, non-sensitive local fixtures only;
- bounded CPU, memory, wall time, message, event, proposal, and artifact limits;
- explicit human start, stop, freeze, rollback, and cleanup controls.

## Source and Version Gate

Deployment preparation must bind to one immutable accepted source head and record:

- repository, accepted PR, commit SHA, review disposition, and merged-head SHA;
- package, Python, schema, instance, configuration, ledger, freeze, rollback, and upstream-contract versions;
- source archive, sdist, wheel, configuration, fixture, and report SHA-256 values;
- exact workflow run IDs, jobs, retained artifact names/digests, and expiry;
- SBOM and provenance/attestation references where applicable.

PR #7 head `80e0546a53c139b26e956bce8f20c41e907739a6` is exact-head verified by run `29614395650`, but it is not accepted or deployable. Three unresolved P2 findings show that non-UTF-8 JSON can be accepted, schema-required instance blocks can be bypassed, and booleans can pass as numeric schema versions. PR #6 and earlier candidate branches are closed as superseded. No merged head has passed the complete gate set.

## Permission Gate

Before any verification deployment:

- GitHub Actions permissions remain `contents: read` or narrower and checkout credentials are not persisted.
- No secret, token, SSH key, cloud credential, package-publishing credential, payment credential, or personal identifier is available to the runtime.
- Filesystem writes are limited to a disposable run directory and declared evidence outputs.
- External commands, subprocesses, plugins, dynamic imports, and generated snippets are denied unless separately reviewed and explicitly allowlisted.
- Network access is disabled or independently enforced as unavailable.

## Artifact Gate

Required retained non-secret artifacts:

- exact-head and merged-head checkout/identity reports;
- clean build/install, unit, smoke, strict-UTF-8, missing-required-block, boolean-version, invalid-configuration, wrong-repository/path, non-canonical-name, deterministic, resource-limit, interruption, freeze, rollback, and security reports;
- source archive, sdist, wheel, checksums, and SBOM where applicable;
- sanitized configuration and fixture manifests;
- sample append-only event and attribution ledgers;
- freeze point, rollback checkpoint, recovery, and cleanup evidence;
- review-thread disposition and explicit release/deployment approval.

Run `29614395650` retained Python 3.11 and 3.13 candidate artifacts with digests `cdfd6817c3d0e0c07b41613072443c4fdd5aa0952ea68e4969ccee362ed7470a` and `221cfa42111ed0a6ac42c0311934d812f437f9eeeaa80d3f5cb574d155cde7ed`. These are review evidence only and do not satisfy the full artifact gate. No artifact may contain credentials, private identifiers, unapproved confidential data, or executable generated content.

## Configuration Gate

Configuration and genome files must be local, bounded, strict UTF-8, versioned, schema-validated, and fail closed for:

- missing required identity, development, review, status, or genome fields;
- unknown fields where forbidden;
- duplicate identifiers;
- non-canonical QSO names or casing;
- booleans, strings, floats, or unsupported values used as schema versions;
- repositories or paths outside the accepted upstream contract;
- missing required hash pins or mismatched hashes;
- missing Atlas or upstream artifacts;
- unsupported capabilities or resource limits outside approved bounds;
- network, credential, repository-write, generated-code, or payment capability requests.

The schema, loader, resolver, and later instantiation path must express the same contract. No CLI success may defer a required-field or type failure until object instantiation.

## Pre-Deployment Validation

Run from a clean disposable environment:

1. Assert the checked-out SHA equals the accepted source head.
2. Verify source, sdist, wheel, configuration, schema, fixture, and upstream hashes.
3. Install without undeclared dependencies; compile source and tests.
4. Run the complete unit, smoke, negative, adversarial, and security suite.
5. Run `qso-run`, `qso-run --version`, deterministic repeatability, and invalid-argument checks.
6. Reject UTF-16/32 payloads, missing schema-required blocks, boolean schema versions, wrong repository/path, absent pins, hash mismatch, duplicate identity, and non-canonical casing.
7. Exercise resource ceilings, interruption, freeze, checkpoint, rollback, and recovery.
8. Verify ledgers are append-only, hash-linked, ordered, attributable, and preserved across rollback.
9. Confirm no network, credentials, repository writes, generated-code execution, or sensitive data access.
10. Produce a hash-bound deployment-readiness report for human review.

## Health Checks

A verification deployment is healthy only when:

- startup and clean shutdown succeed;
- configured instances load exactly once with complete required blocks, canonical names/IDs/source paths, integer versions, and accepted hashes;
- deterministic seed and input replay produces the expected canonical output hash;
- message, event, attribution, freeze, and rollback ledgers validate;
- resource consumption remains inside declared limits;
- invalid inputs fail closed without partial state mutation;
- no network attempt, credential lookup, external repository write, generated-code execution, or payment action occurs;
- all output remains inside the disposable run directory;
- health status clearly distinguishes `PASS`, `FAIL`, and `UNKNOWN`.

## Observability

Retain structured local evidence for source/configuration identity, schema/loader contract versions, accepted upstream identities, start/stop/freeze/rollback/recovery events, instance transitions, message counts/sizes/order/rejections/hashes, resource limits, validation failures, denied capabilities, ledger heads, checkpoints, test/health/cleanup/post-validation results, and exact artifact hashes. Observability must not capture secrets or unapproved personal/confidential content.

## Rollback Triggers

Immediately stop and roll back if:

- the running source differs from the approved SHA;
- artifacts or configuration fail hash, strict-UTF-8, schema, required-field, or type validation;
- a boolean schema version, non-canonical name, unapproved repository/path, missing pin, or mismatched hash is accepted;
- deterministic outputs diverge or invalid input produces partial accepted state;
- resource limits, stop controls, freeze, checkpoint, rollback, or ledger integrity fail;
- network, credential, repository-write, generated-code, payment, or undeclared subprocess capability appears;
- sensitive data enters artifacts, required upstream contracts disappear/change, or health becomes `FAIL` or materially `UNKNOWN`.

## Rollback Procedure

1. Stop the process and deny further input.
2. Preserve logs, failed inputs, exact source/configuration/schema/upstream hashes, ledger heads, and resource evidence.
3. Restore the last accepted checkpoint or remove the disposable run directory when no accepted checkpoint exists.
4. Verify no external state, repository, credential, package registry, or payment system was modified.
5. Re-run integrity checks on preserved evidence and record the trigger, affected scope, recovery result, and required remediation.
6. Do not resume until a new immutable candidate passes the complete gate set and receives approval.

## Post-Deployment Validation

After a permitted verification run:

- repeat CLI/configuration smoke and deterministic replay;
- validate final event/attribution ledger heads and checkpoint hashes;
- prove cleanup removed transient state without deleting retained evidence;
- confirm no network, credentials, external writes, generated execution, payment actions, or sensitive-data leakage occurred;
- compare resource use with approved bounds and test disablement/revocation controls;
- archive checksums, reports, and human disposition; return the environment to a known clean state.

## Promotion Rules

A disposable verification pass does not authorize package publication, persistent hosting, scheduled execution, multi-user service, four-QSO operation, external integration, credentials, or production deployment. Each promotion requires a separately scoped architecture, threat model, acceptance matrix, rollback drill, evidence bundle, and explicit approval.

## Deployment Log

- 2026-07-17 — Added the fail-closed deployment plan. No deployment was attempted or authorized.
- 2026-07-17 — Recorded PR #6 exact-head evidence and its unresolved configuration-contract blockers.
- 2026-07-17 — Advanced the evidence record to PR #7 run `29614395650`; deployment remains blocked by three new parser/schema findings plus merged-head/runtime/upstream/security/publication gates and approval.
