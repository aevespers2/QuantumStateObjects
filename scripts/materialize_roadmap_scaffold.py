"""Materialize the QuantumStateObjects roadmap scaffold.

Phase: bounded object-model development. Stages: contracts, lifecycle implementation, verification, fabric integration, release. Tasks: validate the manifest, create missing paths, preserve existing work, generate unique headers, require review. Steps: dry-run, inspect, write, diff, test, approve.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "roadmap" / "scaffold-plan.json"

def roadmap(path: Path) -> dict[str, object]:
    area = path.parent.as_posix() or "repository root"
    return {"file": path.as_posix(), "purpose": f"Define the bounded QSO responsibility for {path.stem} within {area}.", "phase": "planned", "stages": ["contract", "implementation", "verification", "integration", "release"], "tasks": ["Define typed state, ownership, inputs, outputs, invariants, and failure behavior.", "Implement deterministic behavior under immutable ethics and resource limits.", "Add positive, negative, boundary, mutation, restoration, and tamper tests.", "Connect provenance, communication permissions, freeze points, and human review.", "Document compatibility, migration, rollback, and release evidence."], "steps": ["Review genome and fabric contracts.", "Implement or document the responsibility.", "Add fail-closed fixtures and tests.", "Run deterministic serialization, restoration, and exact-head checks.", "Record human acceptance evidence."], "status": "scaffold"}

def render(path: Path) -> str:
    item = roadmap(path); suffix = path.suffix.lower(); body = "\n".join([f"Roadmap: {item['file']}", f"Purpose: {item['purpose']}", f"Phase: {item['phase']}", "Stages: contract -> implementation -> verification -> integration -> release", "Tasks:", *[f"- {x}" for x in item["tasks"]], "Steps:", *[f"{i}. {x}" for i, x in enumerate(item["steps"], 1)]])
    if suffix == ".json": return json.dumps({"roadmap": item}, indent=2) + "\n"
    if suffix == ".py": return f'"""\n{body}\n"""\n\nfrom __future__ import annotations\n\n# TODO: implement and test.\n'
    if suffix in {".yml", ".yaml", ".toml"} or path.name in {"requirements.txt", "CODEOWNERS"}: return "# " + body.replace("\n", "\n# ") + "\n"
    return f"# {path.stem.replace('-', ' ').title()}\n\n{body}\n"

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); parser.add_argument("--force", action="store_true"); args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    for folder, names in plan["groups"].items():
        for name in names:
            relative = Path(folder) / name; target = ROOT / relative
            print(("replace" if target.exists() else "create") + ": " + relative.as_posix())
            if not args.write or (target.exists() and not args.force): continue
            target.parent.mkdir(parents=True, exist_ok=True); target.write_text(render(relative), encoding="utf-8")
if __name__ == "__main__": main()
