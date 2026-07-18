# Preflight Error Immunity

## Purpose

Preflight Error Immunity is a preventive assurance layer for QuantumStateObjects. It treats every observed failure as evidence of a missing invariant and moves that invariant to the earliest safe boundary.

The feature's governing rule is:

> A failure that can be predicted from repository state, packaging metadata, input bytes, schemas, dependency contracts, resource limits, or evidence requirements must be rejected before installation, object construction, state mutation, ledger append, or runtime execution.

This does not claim that software can become literally error-free. It establishes a systematic process by which known failure classes become permanent, testable preconditions instead of recurring runtime incidents.

## Error-to-insight model

Every error is converted into an `InsightRule` with:

- a stable identifier;
- the failure class and observed symptom;
- the earliest boundary at which it can be detected;
- a deterministic validator;
- a fail-closed remediation message;
- positive, negative, atomicity, and regression tests;
- evidence proving the validator ran against the exact submitted head.

Once an insight rule is accepted, future paths must not reach the original failure point without first passing that rule.

## Prevention layers

### Layer 0 — Repository and environment

Prevents failures before `pip` or build execution:

- required files and package directories exist;
- `pyproject.toml` is parseable and internally consistent;
- build backend supports the requested installation mode;
- declared console-script targets resolve to importable modules and callables;
- supported Python versions are checked before installation;
- local paths remain within the repository boundary;
- required tools and dependencies are declared rather than discovered mid-run;
- source tree and generated artifacts are free of unresolved conflict markers.

This layer covers the earlier editable-install and missing-entry-point class of failures.

### Layer 1 — Canonical bytes and parsing

Prevents ambiguous or nonportable data from entering the system:

- strict UTF-8 only;
- duplicate JSON keys rejected;
- `NaN`, `Infinity`, overflow-to-infinity numbers, lone surrogates, non-string object keys, and other noncanonical JSON values rejected;
- canonical serialization is deterministic;
- hashes are computed from the canonical byte representation only.

### Layer 2 — Schema and identity contracts

Prevents structurally valid but contract-invalid objects:

- all required identity, development, review, status, communication, and resource blocks are present;
- schema versions are integers, never Booleans;
- primary, secondary, declared, and instance names obey one canonical naming contract;
- collection fields are the correct collection type even when empty or falsy;
- optional fields distinguish omission from explicit `null`;
- resource objects and nested field shapes are validated before access.

### Layer 3 — Dependency and provenance contracts

Prevents unaccepted upstream material from becoming runtime input:

- accepted schema version and artifact hash are required;
- genome and canonical-record references are repository/path constrained;
- declared `content_sha256` must match the exact UTF-8 content bytes;
- lowercase hexadecimal SHA-256 values are required everywhere;
- compatibility sets must be immutable and accepted, not merely candidate or proposed;
- exact source commit and artifact digests are recorded.

### Layer 4 — Construction and mutation boundaries

Prevents partial objects and partial state:

- all inputs are validated before `RuntimeController` or QSO construction;
- validation failure creates no controller, state, event, attribution entry, checkpoint, or evidence artifact;
- public event and message APIs validate canonical payloads before hashing or append;
- sent and received messages are defensively copied so caller mutation cannot corrupt evidence;
- delegated-ingest exceptions restore the complete prior state.

### Layer 5 — Ledger and identity integrity

Prevents internally consistent but semantically invalid evidence:

- event and attribution ledgers validate exact entry shapes;
- malformed or mixed-type keys fail closed with deterministic errors;
- every event in a per-object ledger carries the same canonical QSO identity;
- state and event hashes are recomputed from canonical values;
- stitched, identity-switching, reordered, truncated, or mutated ledgers are rejected.

### Layer 6 — Resource, freeze, recovery, and rollback safety

Prevents safety actions from failing after destructive mutation:

- resource ceilings are validated before runtime;
- safety-event capacity is reserved;
- rollback and high-severity freeze capacity is checked before checkpoint restoration;
- failed freeze, recovery, or rollback attempts leave state unchanged;
- checkpoints include the full canonical state needed for exact restoration;
- annotations are canonical and serializable before safety mutation.

### Layer 7 — Build, test, and evidence readiness

Prevents an apparently successful change from becoming accepted without proof:

- exact-head checkout and SHA assertion;
- build and editable-install preflight without networked runtime input;
- supported Python matrix;
- positive, negative, deterministic, aliasing, atomicity, capacity, and rollback tests;
- wheel and checksum generation;
- retained JUnit, head-SHA, artifact digest, and provenance evidence;
- unresolved review findings block acceptance;
- merge, release, deployment, and experiment gates remain distinct.

## Known failure classes absorbed by this feature

The initial rule catalog includes:

1. missing CLI target or importable entry point;
2. editable-install/build-backend incompatibility;
3. invalid or incomplete manifest blocks;
4. Boolean schema versions;
5. noncanonical QSO and instance identities;
6. invalid UTF-8 and lone-surrogate strings;
7. duplicate JSON keys;
8. `NaN`, `Infinity`, and overflowed numeric values;
9. noncanonical message, event, genome, and identity payloads;
10. malformed peer, artifact, forbidden-capability, and resource collections;
11. omitted-versus-null hash ambiguity;
12. mismatched content hashes and uppercase/noncanonical digests;
13. mutable inbox/outbox aliasing;
14. partial state after delegated-ingest exceptions;
15. malformed, mixed-key, stitched, or identity-switching ledgers;
16. incomplete freeze checkpoints;
17. rollback or recovery failure at event capacity;
18. mutation before safety annotation or capacity validation;
19. unaccepted upstream schemas, versions, or artifacts;
20. evidence not bound to the exact submitted commit.

## Runtime contract

`run_preflight()` returns a `PreflightReport` containing every evaluated rule. It never mutates runtime state. A report is ready only when every required rule passes.

The caller must invoke `report.require_ready()` before installation, controller construction, or execution. A failed report raises `PreflightRejected` with stable rule identifiers and remediation details.

## Acceptance criteria

The feature is acceptable when:

- every known failure class has a registered rule and regression test;
- identical inputs produce identical reports and report hashes;
- malformed inputs fail before side effects;
- the preflight report is canonically serializable and hashable;
- exact-head CI retains the report and test evidence;
- adding a newly observed error requires adding a rule before repairing the downstream symptom;
- no rule silently normalizes malformed input into an accepted default.

## Non-goals

- predicting every possible future defect;
- automatically executing generated repair code;
- bypassing human review, security adjudication, or acceptance gates;
- treating synthetic tests as proof that Atlas, Nova, Orion, or Lyra are running;
- consuming candidate or proposed upstream artifacts.

## Development policy

For every future failure:

1. preserve the original evidence;
2. identify the earliest detectable boundary;
3. add a failing regression test;
4. add or strengthen an `InsightRule` at that boundary;
5. verify no state mutation occurred on rejection;
6. rerun exact-head evidence;
7. resolve the downstream error only after the preventive rule passes.
