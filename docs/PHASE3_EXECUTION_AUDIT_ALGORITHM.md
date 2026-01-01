# Phase-3 Execution Audit Algorithm (Deterministic)

## Target
Repository: trizel-ai/trizel-epistemic-engine
Branch: phase3/initialize-analytic-engine
PR: #5 (compare -> phase3/initialize-analytic-engine, base -> phase2/initialize-epistemic-engine)

---

## A. Hard Preconditions (MUST PASS)
A1. Confirm Phase-2 closure marker exists:
- docs/PHASE2_COMPLETION.md

A2. Confirm Phase-2 artifacts are unchanged in Phase-3 branch:
- docs/PHASE2_EXECUTION_DIRECTIVE.md
- schema/epistemic_state.schema.json
- states/ (registry + all states)
- src/epistemic/ (Phase-2 validation logic)
- .github/workflows/deterministic-validation.yml

A3. Confirm Phase-3 outputs are restricted to:
- analysis_artifacts/
- releases/

A4. Confirm Phase-3 CI prohibits network use for analysis steps.

---

## B. Execution State Reconstruction (ALWAYS DO THIS FIRST)
B1. Read Phase-2 completion marker:
- docs/PHASE2_COMPLETION.md

B2. Read Phase-3 declaration and directive:
- docs/PHASE3_DECLARATION.md
- docs/PHASE3_EXECUTION_DIRECTIVE.md

B3. Verify current Phase-3 tree exists:
- analysis/
- analysis_artifacts/
- releases/
- tests/test_phase3_smoke.py
- .github/workflows/phase3-analysis-validation.yml

B4. Verify CI is green on PR #5.

Output of B-step is the “Current Execution State”.

---

## C. Phase-3 Contract Adoption (REQUIRED BEFORE ANALYSIS LOGIC)
C1. Create analysis contract:
- docs/PHASE3_ANALYSIS_CONTRACT.md

C2. Create method registry:
- docs/PHASE3_METHOD_REGISTRY.md

C3. Create release contract:
- docs/PHASE3_RELEASE_CONTRACT.md

No analysis logic may be merged into the Phase-3 branch unless C1–C3 exist.

---

## D. Deterministic Analysis Implementation (CONTROLLED)
D1. Implement method interface:
- analysis/methods/base.py

D2. Implement deterministic runner:
- analysis/pipelines/run_analysis.py

D3. Ensure runner produces ONLY:
- analysis_artifacts/<RUN_ID>/manifest.json
- analysis_artifacts/<RUN_ID>/reports/*.md
- analysis_artifacts/<RUN_ID>/tables/*.csv

D4. Add fixtures + golden outputs:
- tests/fixtures/
- tests/golden/

D5. Add tests that verify:
- stable ordering
- stable hashing
- identical outputs across runs for same input

---

## E. CI Enforcement (MUST BLOCK NON-DETERMINISM)
E1. Update Phase-3 workflow to run:
- unit tests
- deterministic analysis run against fixtures
- diff vs golden outputs

E2. CI MUST fail if:
- any file changes outside allowed output paths
- golden outputs mismatch
- ordering changes without explicit version bump

---

## F. Release Procedure (AUDITABLE)
F1. Release build must be reproducible from repository state.
F2. Release output must be written only under:
- releases/<RELEASE_ID>/
F3. Release must contain:
- release manifest
- method versions
- input state registry hash
- output file hashes

---

## G. “Stop Point” Rule (FOR CONTINUITY)
At the end of any work session:
- Update docs/PHASE3_DAILY_LOG.md
- Record: commit hash, what changed, what remains

This prevents re-opening foundational questions later.
