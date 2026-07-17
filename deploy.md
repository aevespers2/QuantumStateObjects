# Deployment Plan

## Current Decision

Status: `BLOCKED — NO DEPLOYMENT TARGET AUTHORIZED`

This repository has no approved runtime, package publication, four-QSO execution, payment, or production deployment. PR #4 has successful Python 3.11/3.13 CI on a synthetic merge ref, not accepted exact-head evidence. Local configuration, runtime integrity, resource limits, freeze/rollback, upstream contracts, privacy/licensing, provenance, and release approval remain incomplete.

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

- repository and commit SHA;
- accepted PR and review disposition;
- merged-head SHA, if applicable;
- package version and Python versions;
- source archive, sdist, and wheel SHA-256 values;
- schema, instance, configuration, ledger, freeze, rollback, and upstream-contract versions;
- exact workflow run IDs and retained artifact digests;
- SBOM and provenance/attestation references where applicable.

PR #4 head `cdc808db74d165dfb7cb4d5604aab96e10f1af4b` is not accepted because run `29599534913` checked out synthetic merge commit `2ab66a8e5f6e463bbe6b5200b92c3d5005934701`. PR #5 is a duplicate candidate without attached CI. Neither may be deployed.

## Permission Gate

Before any verification deployment:

- GitHub Actions permissions remain `contents: read` or narrower.
- Checkout credentials are not persisted.
- No secret, token, SSH key, cloud credential, package-publishing credential, payment credential, or personal identifier is available to the runtime.
- Filesystem writes are limited to a disposable run directory and declared evidence outputs.
- External commands, subprocesses, plugins, dynamic imports, and generated snippets are denied unless separately reviewed and explicitly allowlisted.
- Network access is disabled or independently enforced as unavailable.

## Artifact Gate

Required retained non-secret artifacts:

- exact-head checkout and identity report;
- clean build/install report;
- unit, smoke, invalid-configuration, deterministic, resource-limit, interruption, freeze, rollback, and security reports;
- source archive, sdist, wheel, checksums, and SBOM where applicable;
- sanitized configuration and fixture manifests;
- sample append-only event and attribution ledgers;
- freeze point, rollback checkpoint, recovery, and cleanup evidence;
- review-thread disposition and explicit release/deployment approval.

No artifact may contain credentials, private identifiers, unapproved confidential data, or executable generated content.

## Configuration Gate

Configuration must be local, versioned, schema-validated, and fail closed for:

- missing required fields;
- unknown fields where forbidden;
- duplicate identifiers;
- invalid versions;
- mismatched hashes;
- missing Atlas or upstream artifacts;
- unsupported capabilities;
- resource limits outside approved bounds;
- network, credential, repository-write, generated-code, or payment capability requests.

## Pre-Deployment Validation

Run from a clean disposable environment:

1. Assert the checked-out SHA equals the accepted source head.
2. Verify source, sdist, wheel, configuration, schema, and fixture hashes.
3. Install without undeclared dependencies.
4. Run compilation and the complete test suite.
5. Run `qso-run`, `qso-run --version`, deterministic repeatability, and invalid-argument checks.
6. Validate local configuration and all negative fixtures.
7. Exercise resource ceilings, interruption, freeze, checkpoint, rollback, and recovery.
8. Verify ledgers are append-only, hash-linked, ordered, attributable, and preserved across rollback.
9. Confirm no network, credentials, repository writes, generated-code execution, or sensitive data access.
10. Produce a signed or hash-bound deployment-readiness report for human review.

## Health Checks

A verification deployment is healthy only when:

- process startup and clean shutdown succeed;
- configured instances load exactly once with expected IDs and hashes;
- deterministic seed and input replay produces the expected canonical output hash;
- message, event, attribution, freeze, and rollback ledgers validate;
- resource consumption remains inside declared limits;
- invalid inputs fail closed without partial state mutation;
- no network attempt, credential lookup, external repository write, generated-code execution, or payment action occurs;
- all output remains inside the disposable run directory;
- health status clearly distinguishes `PASS`, `FAIL`, and `UNKNOWN`.

## Observability

Retain structured local evidence for:

- source and configuration identity;
- start, stop, freeze, rollback, and recovery events;
- instance state transitions;
- message counts, sizes, ordering, rejection reasons, and hashes;
- CPU, memory, wall time, output size, event, proposal, and retry limits;
- validation failures and denied capability requests;
- ledger heads and checkpoint hashes;
- test, health, cleanup, and post-validation results.

Observability must not capture secrets or unapproved personal/confidential content.

## Rollback Triggers

Immediately stop and roll back if:

- the running source differs from the approved SHA;
- artifacts or configuration fail hash or schema validation;
- deterministic outputs diverge;
- invalid input produces partial accepted state;
- resource limits, stop controls, freeze, checkpoint, or rollback fail;
- ledger ordering, hashes, attribution, or append-only behavior breaks;
- network, credential, repository-write, generated-code, payment, or undeclared subprocess capability appears;
- sensitive data enters artifacts;
- required upstream contracts disappear or change;
- health becomes `FAIL` or materially `UNKNOWN`.

## Rollback Procedure

1. Stop the process and deny further input.
2. Preserve logs, failed inputs, exact source/configuration hashes, ledger heads, and resource evidence.
3. Restore the last accepted checkpoint or remove the disposable run directory when no accepted checkpoint exists.
4. Verify no external state, repository, credential, package registry, or payment system was modified.
5. Re-run integrity checks on preserved evidence.
6. Record the trigger, affected scope, recovery result, and required remediation.
7. Do not resume until a new immutable candidate passes the complete gate set and receives approval.

## Post-Deployment Validation

After a permitted verification run:

- repeat CLI smoke and deterministic replay;
- validate final event/attribution ledger heads and checkpoint hashes;
- prove cleanup removed transient state without deleting retained evidence;
- confirm no network, credentials, external writes, generated execution, payment actions, or sensitive-data leakage occurred;
- compare resource use with approved bounds;
- test disablement and revocation controls;
- archive checksums, reports, and human disposition;
- return the environment to a known clean state.

## Promotion Rules

A disposable verification pass does not authorize package publication, persistent hosting, scheduled execution, multi-user service, four-QSO operation, external integration, or production deployment. Each promotion requires a separately scoped architecture, threat model, acceptance matrix, rollback drill, evidence bundle, and explicit approval.

## Deployment Log

- 2026-07-17 — Added the fail-closed deployment plan. No deployment was attempted or authorized.