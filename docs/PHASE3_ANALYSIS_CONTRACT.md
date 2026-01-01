# Phase-3 Analysis Contract — TRIZEL (Authoritative)

## Repository
trizel-ai/trizel-epistemic-engine

## Phase
Phase-3 — Analytical Engine (Deterministic, Offline, Audit-Safe)

## Authority and Execution Channel
All Phase-3 execution MUST occur only on the Phase-3 canonical branch and PR.
Phase-2 artifacts are immutable as defined in:
docs/PHASE2_COMPLETION.md

## Inputs (Exclusive)
Phase-3 analysis is allowed to read ONLY:
1) Phase-2 epistemic state files under:
states/3I_ATLAS/
2) Phase-2 schema and validation surfaces (read-only):
schema/
src/epistemic/
3) Phase-3 analysis code surface:
analysis/

No other input sources are permitted during CI runs.

## Determinism Rules (Non-Negotiable)
1) No network access (CI and default execution).
2) Stable ordering:
   - Files MUST be processed in lexicographic order.
   - Output JSON MUST use sorted keys.
3) No timestamps, randomness, or system-dependent values in outputs.
4) Any run MUST be reproducible from the same git commit + same inputs.

## Outputs (Exclusive, Write-Only)
Phase-3 MUST write outputs ONLY to:
1) analysis_artifacts/
2) releases/

Outputs MUST NOT modify:
- states/
- schema/
- src/epistemic/
- docs/PHASE2_*

## Run Identity (Deterministic Run ID)
Each run MUST declare:
- RUN_ID: user-supplied stable identifier (string)
- METHOD_ID: one value from analysis/methods/method_registry.json
- INPUT_SCOPE: fixed logical target (e.g., "states/3I_ATLAS")

RUN_ID MUST NOT be auto-generated.

## Minimal Required Outputs for Any Run
For any successful run, the following MUST exist:

1) analysis_artifacts/<RUN_ID>/manifest.json
2) analysis_artifacts/<RUN_ID>/summary.json

No other outputs are required until a specific method defines them.

## Manifest Contract (Exact Fields)
manifest.json MUST contain exactly these top-level fields:

- repository
- git_commit
- phase
- run_id
- method_id
- input_scope
- input_files_count
- determinism
- outputs

Where:
- determinism MUST be an object that asserts:
  - network: "disabled"
  - ordering: "lexicographic"
  - json_keys: "sorted"
- outputs MUST list produced file paths relative to repository root.

## Summary Contract (Exact Fields)
summary.json MUST contain exactly these top-level fields:

- run_id
- method_id
- analyzed_states_count
- notes

No scores, rankings, or interpretive conclusions are allowed in summary.json unless explicitly authorized by a Phase-3 method specification.

## Effective Lock
This contract is authoritative for Phase-3.
Any analytical method MUST conform to this contract before producing additional artifacts.
