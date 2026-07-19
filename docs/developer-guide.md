# Developer guide

## Development posture

Work in this repository should be small, deterministic, local-first, and evidence-backed. Do not broaden capabilities while repairing a parser, runtime invariant, evidence format, documentation gap, or release gate.

The safest default is read-only inspection followed by one bounded change on a dedicated branch.

## Prerequisites

- Git
- Python 3.11 or 3.13 for the current candidate matrix
- A fresh virtual environment
- No credentials in the repository or shell environment
- No network-dependent runtime inputs
- No production data

The package has no declared runtime dependencies. Test and documentation tools are development-only.

## Clone and inspect

```bash
git clone https://github.com/aevespers2/QuantumStateObjects.git
cd QuantumStateObjects
git status --short
git log -1 --oneline
```

Before running a candidate branch, record the exact head:

```bash
git rev-parse HEAD
```

Do not treat branch names, pull-request numbers, or a successful historical run as substitutes for the exact checked-out SHA.

## Create an isolated environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

For current accepted `main`, inspect the prototype and policy validator before assuming the candidate package surface exists.

For draft PR #7 or a reconciled successor:

```bash
git fetch origin pull/7/head:review/pr-7
git switch review/pr-7
python -m pip install -e . --no-build-isolation
python -m pip install pytest
```

## Baseline verification

Run compilation and tests from a clean working tree:

```bash
python -m compileall -q qso_runtime tests scripts
python -m pytest
```

Where the candidate CLI exists:

```bash
qso-run
qso-run --version
qso-run --config config/instances.json
```

The default self-check should remain machine-readable and should report denied external capabilities. A successful self-check is local health evidence only; it does not activate a four-QSO experiment or authorize publication.

## Build artifacts

For a candidate package review:

```bash
rm -rf build dist *.egg-info
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
python -m build --sdist --wheel
sha256sum dist/*
```

Install the wheel into a second clean virtual environment before claiming artifact usability. Record Python, pip, setuptools, wheel, and operating-system versions with the exact source SHA.

## Build the documentation

```bash
python -m pip install -r docs/requirements.txt
mkdocs build --strict
mkdocs serve
```

`mkdocs build --strict` must pass before Pages publication is proposed. A local build does not prove that GitHub Pages is configured or deployed.

## Repository map

| Path | Purpose |
|---|---|
| `README.md` | Repository entry point and status boundary |
| `taskchain.md` | Dependency order, active tasks, and acceptance criteria |
| `release.md` | Release decision, gates, artifacts, rollback, and approval |
| `changelog.md` | Evidence-backed history of notable changes |
| `deploy.md` | Deployment target constraints and post-validation requirements |
| `punchlist.md` | Bounded implementation and review tasks |
| `qso_runtime/` | Prototype and candidate runtime package |
| `schema/` | Versioned local schemas |
| `config/` | Local instance configuration candidate |
| `tests/` | Unit, negative, adversarial, replay, and acceptance tests |
| `scripts/` | Repository validation and evidence helpers |
| `.consent/` | Repository-wide policy source |
| `.github/workflows/` | Exact-head validation workflows |
| `docs/` | Pages-ready project and developer documentation |

Some paths exist only on the candidate branch until merged. Documentation must label them accordingly.

## Change workflow

### 1. Select one acceptance criterion

Choose one item from `taskchain.md`, `punchlist.md`, an unresolved review thread, or a named documentation gate. Do not combine unrelated runtime, policy, publication, and architecture work merely because the files are nearby.

### 2. Establish the pre-change invariant

Write down:

- current exact SHA;
- current test result;
- input fixture that exposes the gap;
- expected fail-closed behavior;
- files permitted to change;
- rollback plan.

### 3. Add the negative test first

For validation or runtime defects, add a fixture that demonstrates the rejected shape or failure mode. Confirm it fails for the intended reason before changing the implementation.

### 4. Make the narrowest repair

Preserve existing public names, schemas, hashes, lifecycle states, and evidence shapes unless the task explicitly approves a versioned contract change.

### 5. Re-run the complete relevant matrix

A focused test is useful during development, but acceptance requires the full relevant suite. For changes touching canonicalization, state, ledgers, messages, checkpoints, or rollback, include repeated deterministic runs and tamper fixtures.

### 6. Review the diff as evidence

```bash
git diff --check
git diff --stat
git diff
```

Confirm the diff does not add credentials, network calls, generated-code execution, external writes, unbounded reads, silent normalization, or unsupported capability claims.

### 7. Record exact-head evidence

Capture:

- commit SHA;
- commands and exit codes;
- supported Python versions;
- test counts and reports;
- artifact names and hashes;
- deterministic fixture hashes;
- review-thread disposition;
- residual risks;
- rollback instructions.

## Testing expectations

### Parser and configuration changes

Include tests for:

- malformed and non-UTF-8 bytes;
- duplicate keys;
- non-finite numbers;
- Boolean values in integer fields;
- missing and extra fields;
- wrong enum values;
- invalid IDs, names, paths, repositories, versions, and hashes;
- symlinks, non-files, path escapes, oversized files, and read errors;
- atomic behavior when validation or delegated loading fails.

### Message changes

Include tests for unknown identities, unauthorized peers, unknown kinds, malformed payloads, digest mismatch, duplicate/replay handling, size limits, queue capacity, and unchanged state after rejection.

### Ledger changes

Include tests for missing and extra keys, mixed key types, Boolean sequences, sequence gaps, identity changes, payload type errors, non-canonical values, broken previous links, invalid current hashes, truncated ledgers, reordered entries, and replay.

### Checkpoint, freeze, and rollback changes

Verify that every mutable field needed for future behavior is captured and restored. Test full-capacity rollback, message-inclusive checkpoints, interruption during operations, severe annotation behavior, repeated rollback, and recovery from tampered evidence.

### Cross-repository changes

Use only immutable accepted fixtures. Tests must fail when repository, path, schema version, canonicalization version, artifact digest, or content digest differs.

## Documentation rules

- State which branch or commit a behavior belongs to.
- Do not call a draft candidate accepted.
- Do not call a local documentation build published.
- Link design statements to schemas, tests, or planning gates where possible.
- Update `taskchain.md`, `release.md`, and `changelog.md` when a documentation milestone changes readiness or clarifies a blocker.
- Keep examples local, synthetic, and free of personal, confidential, or credential data.

## Pull-request checklist

- [ ] Scope maps to one or more named acceptance criteria.
- [ ] Base and exact head are recorded.
- [ ] Runtime scope is unchanged unless a versioned decision explicitly approves expansion.
- [ ] Negative tests demonstrate the repaired failure mode.
- [ ] Full relevant test matrix passes at the submitted head.
- [ ] Generated content remains inactive data.
- [ ] No network, credentials, external repository writes, or production targets are introduced.
- [ ] Documentation distinguishes implemented, tested, accepted, released, and deployed states.
- [ ] Artifact and evidence hashes are retained.
- [ ] Rollback is documented and tested where behavior changes.
- [ ] Open findings and residual risks are listed plainly.

## Stop conditions

Stop and request architectural review when a change would:

- redefine which repository owns a contract;
- change the canonical QSO names or identity authority;
- add a new external capability;
- alter canonicalization or hash input without a version;
- create a second competing runtime or configuration path;
- introduce persistent storage, networking, scheduling, concurrency, or deployment;
- change the meaning of freeze, checkpoint, interruption, recovery, or rollback;
- use an upstream artifact that has not been independently accepted;
- weaken the repository-wide policy validator or human approval boundary.
