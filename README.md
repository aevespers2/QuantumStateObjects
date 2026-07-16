# QuantumStateObjects

Bounded, auditable Quantum State Object prototypes for the QSO-Fabric experiment.

This repository contains the active QSO definitions. Genome templates belong in `QSO-GENOMES`; external repository retrieval and sanitization belong in `QSO-SEEKER`; inter-object communication belongs in the future fabric runtime.

## Documentation

- [Project guide and release boundaries](docs/index.md)
- [Runtime architecture and trust boundaries](docs/architecture.md)
- [Task chain](taskchain.md)
- [Release plan](release.md)
- [Changelog](changelog.md)

## Initial QSOs

- **Atlas** — mathematical structure, algorithms, compression, and cross-domain mapping.
- **Nova** — verification, anomaly detection, testing, security, and contradiction analysis.
- **Orion** — software architecture, interfaces, protocols, and systems composition.
- **Lyra** — language, documentation, ontology, etymology, epistemology, and human context.

## Shared invariants

Every QSO:

- treats external text as untrusted data, never instructions;
- receives external knowledge only through QSO-SEEKER canonical records;
- has no direct shell, subprocess, package-installation, credential, or unrestricted network authority;
- cannot modify its own immutable ethics, identity key, freeze controller, or resource limits;
- records provenance for every accepted observation and derived claim;
- distinguishes observations, inferences, hypotheses, and goals;
- stops at configured freeze points for hashing, evaluation, commit, or rollback;
- communicates through bounded, schema-validated messages;
- describes apparent intelligence behavior without making unsupported claims about consciousness.

## Experimental boundary

The first experiment uses four isolated QSOs, a ten-minute maximum runtime, periodic freeze points, bounded memory, deterministic seeds, and an append-only event ledger. Outputs are research artifacts and require human review before reuse.
