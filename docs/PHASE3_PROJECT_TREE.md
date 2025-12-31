# Phase-3 Project Tree (authoritative)

Repository: trizel-ai/trizel-epistemic-engine
Phase: Phase-3 — Analytical Engine

## 1) Phase-3 Directories (exclusive)
analysis/
  Purpose: Deterministic analytical engine (offline, reproducible).

analysis_artifacts/
  Purpose: Generated deterministic outputs (byte-stable).

releases/
  Purpose: Immutable “deeply analyzed release” packages derived from analysis_artifacts/.

tests/
  Purpose: Unit tests enforcing Phase-3 determinism and boundaries.

.github/workflows/
  Purpose: Phase-3 CI gates for deterministic analysis validation.

## 2) Phase-2 Directories (immutable; read-only for Phase-3)
docs/ (Phase-2 files listed in PHASE2_COMPLETION.md are frozen)
schema/
src/epistemic/
states/3I_ATLAS/
.github/workflows/deterministic-validation.yml
tests/test_state_validation.py

## 3) Phase-3 Minimum Deliverables
1) Phase-3 execution directive: docs/PHASE3_EXECUTION_DIRECTIVE.md
2) Phase-3 project tree: docs/PHASE3_PROJECT_TREE.md
3) Phase-3 CI validation gate (analysis determinism)
4) Analysis scaffold (no execution yet)
