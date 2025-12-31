from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from analysis.methods.base import MethodSpec

REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_ARTIFACTS = REPO_ROOT / "analysis_artifacts"

# Hard lock: outputs can ONLY go here.
ALLOWED_OUTPUT_PREFIX = str(ANALYSIS_ARTIFACTS.resolve())


def _sha256(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _stable_json(obj: object) -> bytes:
    # Deterministic JSON encoding.
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _run_id(short_sha: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    return f"{ts}__{short_sha}"


def _git_short_sha() -> str:
    # Deterministic fallback: allow env override for CI.
    env = os.environ.get("GIT_SHORT_SHA")
    if env:
        return env.strip()
    head = (REPO_ROOT / ".git" / "HEAD")
    if not head.exists():
        return "nogit"
    ref = head.read_text(encoding="utf-8").strip()
    if ref.startswith("ref: "):
        ref_path = REPO_ROOT / ".git" / ref.replace("ref: ", "").strip()
        if ref_path.exists():
            return ref_path.read_text(encoding="utf-8").strip()[:7]
    return ref[:7]


def _write_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _assert_allowed(path: Path) -> None:
    rp = str(path.resolve())
    if not rp.startswith(ALLOWED_OUTPUT_PREFIX):
        raise RuntimeError(f"Forbidden output path: {rp}")


def main() -> int:
    short_sha = _git_short_sha()
    run_id = _run_id(short_sha)
    run_dir = ANALYSIS_ARTIFACTS / run_id
    _assert_allowed(run_dir)

    # Minimal deterministic “inputs” snapshot.
    # NOTE: We do not parse or interpret states here yet; that comes as methods.
    inputs: Dict[str, object] = {
        "repository": "trizel-ai/trizel-epistemic-engine",
        "phase": "Phase-3",
        "git_short_sha": short_sha,
        "run_id": run_id,
    }

    # Minimal required outputs (contract):
    summary_md = (
        "# Phase-3 Analysis Run Summary\n\n"
        f"- run_id: {run_id}\n"
        f"- git_short_sha: {short_sha}\n"
        "- scope: deterministic pipeline bootstrap (no interpretation)\n"
    ).encode("utf-8")

    state_inventory_csv = (
        "object_id,states_path\n"
        "3I_ATLAS,states/3I_ATLAS/\n"
    ).encode("utf-8")

    field_completeness_csv = (
        "field,completeness\n"
        "N/A,0\n"
    ).encode("utf-8")

    outputs: List[Tuple[str, bytes]] = [
        ("reports/summary.md", summary_md),
        ("tables/state_inventory.csv", state_inventory_csv),
        ("tables/field_completeness.csv", field_completeness_csv),
    ]

    file_hashes: Dict[str, str] = {}
    for rel, data in outputs:
        out_path = run_dir / rel
        _assert_allowed(out_path)
        _write_file(out_path, data)
        file_hashes[rel] = _sha256(data)

    manifest = {
        "run_id": run_id,
        "git_short_sha": short_sha,
        "created_utc": run_id.split("__")[0],
        "outputs": dict(sorted(file_hashes.items(), key=lambda x: x[0])),
        "determinism": {
            "json_sorted_keys": True,
            "utf8": True,
            "lf_newlines_expected": True,
            "network_forbidden": True,
        },
    }

    _write_file(run_dir / "manifest.json", _stable_json(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
