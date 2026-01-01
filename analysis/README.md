# Phase-3 Analysis Layer (deterministic, offline)

This directory is the exclusive execution surface for Phase-3 analytical code.

## Scope
- Deterministic, offline, reproducible analysis over Phase-2 epistemic states.
- No network access during CI.
- Outputs must be written ONLY to:
  - analysis_artifacts/
  - releases/

## Hard boundaries
Phase-3 MUST NOT modify any Phase-2 artifacts, including those listed in:
- docs/PHASE2_COMPLETION.md

## Entry point
- analysis/pipelines/run_analysis.py

## CI gates
- tests/test_phase3_smoke.py
- .github/workflows/phase3-analysis-validation.yml
