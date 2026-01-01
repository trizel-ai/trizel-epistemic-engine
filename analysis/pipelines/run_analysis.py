from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List


REPO_SLUG = "trizel-ai/trizel-epistemic-engine"
PHASE = "Phase-3"
INPUT_SCOPE_DEFAULT = "states/3I_ATLAS"


def _sorted_json_dump(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _list_state_files(input_scope: str) -> List[str]:
    root = Path(input_scope)
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Input scope does not exist or is not a directory: {input_scope}")

    files = sorted([str(p.as_posix()) for p in root.rglob("*.json") if p.is_file()])
    return files


def _load_method_registry() -> Dict[str, Any]:
    reg_path = Path("analysis/methods/method_registry.json")
    if not reg_path.exists():
        raise SystemExit("Missing method registry: analysis/methods/method_registry.json")
    with reg_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _assert_method_allowed(method_id: str, registry: Dict[str, Any]) -> None:
    methods = registry.get("methods", [])
    for m in methods:
        if m.get("method_id") == method_id and m.get("status") == "active":
            return
    raise SystemExit(f"METHOD_ID not found or not active: {method_id}")


def _git_commit() -> str:
    # Deterministic in CI via GITHUB_SHA; deterministic locally if user exports it.
    sha = os.environ.get("GITHUB_SHA", "").strip()
    return sha if sha else "UNKNOWN_COMMIT"


def main() -> int:
    parser = argparse.ArgumentParser(description="TRIZEL Phase-3 deterministic analysis runner")
    parser.add_argument("--run-id", required=True, help="Stable run identifier (no timestamps)")
    parser.add_argument("--method-id", required=True, help="Must exist in analysis/methods/method_registry.json")
    parser.add_argument("--input-scope", default=INPUT_SCOPE_DEFAULT, help="Default: states/3I_ATLAS")
    args = parser.parse_args()

    run_id = args.run_id.strip()
    method_id = args.method_id.strip()
    input_scope = args.input_scope.strip()

    if not run_id:
        raise SystemExit("RUN_ID must be non-empty")
    if any(c.isspace() for c in run_id):
        raise SystemExit("RUN_ID must not contain whitespace")

    registry = _load_method_registry()
    _assert_method_allowed(method_id, registry)

    input_files = _list_state_files(input_scope)

    # Contract-mandated outputs
    manifest_path = Path(f"analysis_artifacts/{run_id}/manifest.json")
    summary_path = Path(f"analysis_artifacts/{run_id}/summary.json")

    manifest: Dict[str, Any] = {
        "repository": REPO_SLUG,
        "git_commit": _git_commit(),
        "phase": PHASE,
        "run_id": run_id,
        "method_id": method_id,
        "input_scope": input_scope,
        "input_files_count": len(input_files),
        "determinism": {
            "network": "disabled",
            "ordering": "lexicographic",
            "json_keys": "sorted",
        },
        "outputs": [
            str(manifest_path.as_posix()),
            str(summary_path.as_posix()),
        ],
    }

    summary: Dict[str, Any] = {
        "run_id": run_id,
        "method_id": method_id,
        "analyzed_states_count": len(input_files),
        "notes": "Contract-only run. No interpretation performed.",
    }

    _sorted_json_dump(manifest_path, manifest)
    _sorted_json_dump(summary_path, summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
