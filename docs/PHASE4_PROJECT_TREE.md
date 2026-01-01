# PHASE-4 PROJECT TREE (CANONICAL)

Repository: trizel-ai/trizel-epistemic-engine

## Phase-4 Additive Tree (Must Exist)

docs/
  PHASE4_BUILD_PLAN.md
  PHASE4_EXECUTION_DIRECTIVE.md
  TCRL_CONTRACT.md
  PHASE4_PROJECT_TREE.md

schema/
  tcrl_tcp.schema.json
  phase4_eval.schema.json

tcrl/
  README.md
  tcp/
    TEMPLATE_TCP.json

phase4/
  README.md
  pipelines/
    run_phase4.py
  methods/
    method_registry.json

phase4_artifacts/
  .gitkeep

tests/
  test_phase4_smoke.py
  test_phase4_contract.py

.github/workflows/
  phase4-validation.yml

## Immutability Note
Phase-2 and Phase-3 directories are not modified in Phase-4 initialization PRs.
