from __future__ import annotations

import argparse
import json
import sys
import tomllib
from importlib import metadata
from pathlib import Path
from typing import Sequence

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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.version:
        print(f"{PACKAGE_NAME} {_package_version()}")
        return 0

    indent = 2 if args.pretty else None
    print(json.dumps(_self_check(), indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
