# PHASE-4 FORMAL START — EXECUTION DIRECTIVE (COPY/PASTE AUTHORITY)

Repository: trizel-ai/trizel-epistemic-engine  
Branch: phase4/initialize-tcrl-and-phase4  
Canonical PR: SINGLE PR ONLY (no parallel PRs / no alternate branches)

## 0) Authority and Context Locks (Non-Negotiable)

- Phase-1 ingest is immutable ground truth:
  - ingest_doi MUST equal: "10.5281/zenodo.18012859"
- Phase-2 and Phase-3 artifacts are immutable and must not be modified.
- Phase-4 is additive-only and audit-safe.

## 1) Mandatory Architecture Rule

Phase-4 MUST NOT "understand theories".

All theory comprehension and reduction MUST occur in:
TCRL — Theory Comprehension & Reduction Layer.

Phase-4 consumes only TCRL outputs (TCP artifacts) plus ingest-linked observational records.

## 2) Prohibited Content (Absolute)

The following are forbidden anywhere in Phase-4 (code, docs, tests, artifacts):
- physics endorsements, interpretive superiority claims, ToE/STOE superiority language
- theory ranking or model selection as an outcome
- hidden assumptions without explicit declaration
- timestamps used as epistemic or evaluative evidence
- network access during deterministic execution

If found: REMOVE immediately.

## 3) Canonical Phase-4 Paths (Must Exist)

- docs/PHASE4_BUILD_PLAN.md
- docs/PHASE4_EXECUTION_DIRECTIVE.md
- docs/TCRL_CONTRACT.md
- docs/PHASE4_PROJECT_TREE.md

- schema/tcrl_tcp.schema.json
- schema/phase4_eval.schema.json

- tcrl/tcp/TEMPLATE_TCP.json
- phase4/pipelines/run_phase4.py
- phase4/methods/method_registry.json

- tests/test_phase4_smoke.py
- tests/test_phase4_contract.py

- .github/workflows/phase4-validation.yml

No deviations without explicit written justification inside docs/PHASE4_PROJECT_TREE.md.

## 4) Phase-4 Contracts (Required Semantics)

### 4.1 TCP (TCRL output)
- TCP is descriptive and reductive only.
- TCP MUST NOT include results, fits, rankings, or conclusions.

### 4.2 EVAL (Phase-4 output)
- EVAL must be deterministic and conditional on declared test conditions.
- EVAL must reference:
  - ingest_doi (locked)
  - record_ids (list)
  - tcp_id + claim_id
  - outcome classification

## 5) Outcome Classification (Exact Allowed Values)

For each claim_id, outcome MUST be one of:
- TESTABLE
- CONSTRAINABLE
- NON_TESTABLE_PRESENTLY
- EXCLUDED_UNDER_CONDITIONS

No other outcome values are allowed.

## 6) Determinism Rules

- No network access in CI.
- Sorted ordering for any iteration over files or lists.
- JSON serialization must be stable (sort keys, stable indentation).
- CI must fail if:
  - non-canonical paths are introduced
  - ingest_doi is not exactly locked
  - forbidden content appears
  - outputs violate schemas

## 7) Execution Stages for Phase-4 (Strict Order)

Stage A — Policy + Contracts (DOCS)
- Add contract docs and project tree.
STOP.

Stage B — Schemas (SCHEMA)
- Add TCP + EVAL JSON Schemas.
STOP.

Stage C — Pipeline Scaffolding (CORE)
- Add minimal pipeline file + method registry (no scientific logic).
STOP.

Stage D — Deterministic Gates (CI + TEST)
- Add tests + CI workflow that runs:
  - python -m unittest -q
STOP.

No Phase-4 scientific execution is allowed until all stages A–D are merged.

## 8) Stop Rule (Critical)

STOP after Stage D passes green.
Do not add analysis methods, evaluators, or automated run generation in this PR.
