from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_phase3_contract_outputs(tmp_path, monkeypatch):
    # Run inside repo root; enforce stable RUN_ID in a temp-safe way
    run_id = "CI_CONTRACT_TEST"
    method_id = "P3.M0.CONTRACT_ONLY"

    # Ensure output location is clean for the test
    out_dir = Path(f"analysis_artifacts/{run_id}")
    if out_dir.exists():
        # do not delete recursively; just fail to keep deterministic audit behavior
        raise AssertionError(f"Output directory already exists: {out_dir}")

    cmd = [
        "python",
        "-m",
        "analysis.pipelines.run_analysis",
        "--run-id",
        run_id,
        "--method-id",
        method_id,
        "--input-scope",
        "states/3I_ATLAS",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

    manifest_path = Path(f"analysis_artifacts/{run_id}/manifest.json")
    summary_path = Path(f"analysis_artifacts/{run_id}/summary.json")

    assert manifest_path.exists(), "manifest.json missing"
    assert summary_path.exists(), "summary.json missing"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    # Exact top-level fields per contract
    assert set(manifest.keys()) == {
        "repository",
        "git_commit",
        "phase",
        "run_id",
        "method_id",
        "input_scope",
        "input_files_count",
        "determinism",
        "outputs",
    }

    assert set(summary.keys()) == {
        "run_id",
        "method_id",
        "analyzed_states_count",
        "notes",
    }

    assert manifest["run_id"] == run_id
    assert manifest["method_id"] == method_id
    assert manifest["input_scope"] == "states/3I_ATLAS"

    det = manifest["determinism"]
    assert det == {
        "network": "disabled",
        "ordering": "lexicographic",
        "json_keys": "sorted",
    }
