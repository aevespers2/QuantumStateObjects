from __future__ import annotations

import json

from qso_runtime.cli import main


def test_default_self_check_is_bounded_and_machine_readable(capsys) -> None:
    assert main([]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "boundaries": {
            "executes_generated_code": False,
            "external_content": "data_only",
            "network_access": False,
            "repository_write": False,
        },
        "command": "qso-run",
        "package": "quantum-state-objects",
        "status": "ok",
        "version": "0.1.0",
    }


def test_version_matches_project_metadata(capsys) -> None:
    assert main(["--version"]) == 0
    assert capsys.readouterr().out == "quantum-state-objects 0.1.0\n"


def test_pretty_output_remains_valid_json(capsys) -> None:
    assert main(["--pretty"]) == 0
    output = capsys.readouterr().out
    assert output.startswith("{\n")
    assert json.loads(output)["status"] == "ok"
