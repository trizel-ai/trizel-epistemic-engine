# Phase-3 Execution Directive (authoritative)

Repository: trizel-ai/trizel-epistemic-engine

Phase: Phase-3 — Analytical Engine (Deterministic, Audit-Safe)

## 1. Authority and Execution Channel
Phase-3 is executed ONLY through a single canonical Pull Request on a single Phase-3 branch.
No parallel PRs or side branches are permitted for Phase-3 execution.

## 2. Hard Boundary: Phase-2 Immutability
Phase-2 is CLOSED and IMMUTABLE.
The following Phase-2 artifacts MUST NOT be modified, amended, reformatted, or reinterpreted by Phase-3:

- docs/PHASE2_EXECUTION_DIRECTIVE.md
- docs/PHASE2_COMPLETION.md
- schema/epistemic_state.schema.json
- src/epistemic/
- states/3I_ATLAS/
- .github/workflows/deterministic-validation.yml
- tests/test_state_validation.py

Any Phase-3 commit that changes Phase-2 artifacts is NON-COMPLIANT.

## 3. Phase-3 Scope (allowed)
Phase-3 MAY:
- Implement deterministic, offline analysis code.
- Produce derived analysis artifacts that are traceable to locked ingest provenance.
- Define a deterministic release packaging structure for “deeply analyzed releases”.
- Add Phase-3 CI workflows that validate determinism and reproducibility.

## 4. Phase-3 Scope (forbidden)
Phase-3 MUST NOT:
- Alter Phase-2 epistemic schema, semantics, or registry rules.
- Add subjective theory ranking inside Phase-2 state files.
- Fetch data from the network during CI runs.
- Introduce non-determinism (timestamps, random seeds without fixed control, unordered iteration).

## 5. Determinism Rules (mandatory)
All Phase-3 outputs MUST be reproducible:
- Same inputs => byte-identical outputs.
- All iteration must be explicitly ordered.
- All generated files must be written into Phase-3-only directories.

## 6. Phase-3 Output Locations (exclusive)
All Phase-3 generated artifacts MUST be placed only under:
- analysis_artifacts/
- releases/

No generated files may be written into Phase-2 directories.

## 7. Provenance Lock
All Phase-3 analysis MUST trace to the immutable Phase-1 ingest DOI:
10.5281/zenodo.18012859
