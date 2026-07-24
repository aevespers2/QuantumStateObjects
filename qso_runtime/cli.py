from __future__ import annotations

import argparse
import json
import sys
import tomllib
from importlib import metadata
from pathlib import Path
from typing import Sequence

from qso_runtime.config import (
    REQUIRED_QSOS,
    ConfigurationError,
    load_runtime_config,
    resolve_local_genomes,
)

PACKAGE_NAME = "quantum-state-objects"
COMMAND_NAME = "qso-run"


def _package_version() -> str:
    """Return the installed version or the source-tree version during development."""
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        try:
            project = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]
            version = project["version"]
        except (OSError, KeyError, TypeError, tomllib.TOMLDecodeError):
            return "unknown"
        return str(version)


def _self_check() -> dict[str, object]:
    """Return deterministic, machine-readable evidence of the local safety boundary."""
    return {
        "boundaries": {
            "credentials_access": False,
            "executes_generated_code": False,
            "external_content": "data_only",
            "network_access": False,
            "repository_write": False,
        },
        "command": COMMAND_NAME,
        "package": PACKAGE_NAME,
        "status": "ok",
        "version": _package_version(),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=COMMAND_NAME,
        description="Run a bounded local Quantum State Objects health check.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="print the package version and exit",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="indent the self-check JSON output",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="validate a local QSO instance configuration without network access",
    )
    parser.add_argument(
        "--genome-root",
        type=Path,
        help="resolve hash-pinned genome files beneath this local directory",
    )
    return parser


def _config_check(config_path: Path, genome_root: Path | None) -> dict[str, object]:
    config = load_runtime_config(config_path, expected_primary_names=REQUIRED_QSOS)
    resolved = resolve_local_genomes(config, genome_root) if genome_root is not None else None
    return {
        **_self_check(),
        "configuration": {
            "config_sha256": config.sha256,
            "genomes_resolved": resolved is not None,
            "instance_ids": [instance.instance_id for instance in config.instances],
            "primary_names": [instance.primary_name for instance in config.instances],
            "resolved_genome_sha256": resolved,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.version:
        print(f"{PACKAGE_NAME} {_package_version()}")
        return 0
    if args.genome_root is not None and args.config is None:
        print(
            json.dumps(
                {
                    "error": "configuration_invalid",
                    "message": "--genome-root requires --config",
                    "status": "error",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2

    try:
        payload = _config_check(args.config, args.genome_root) if args.config else _self_check()
    except ConfigurationError as exc:
        print(
            json.dumps(
                {
                    "error": "configuration_invalid",
                    "message": str(exc),
                    "status": "error",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2

    indent = 2 if args.pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
