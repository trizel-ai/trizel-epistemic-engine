# Phase-3 Analysis Contract (Deterministic, Offline)

## Repository
trizel-ai/trizel-epistemic-engine

## Inputs (Authoritative)
Primary inputs (Phase-2 outputs):
- states/ (including canonical registry file for 3I_ATLAS)
- schema/epistemic_state.schema.json (validation reference only; MUST NOT be modified)

Provenance lock:
- All interpretation must reference the Phase-1 ingest DOI only:
  10.5281/zenodo.18012859

## Output Locations (Exclusive)
All generated outputs MUST be written only to:
- analysis_artifacts/
- releases/

## Determinism Requirements (Non-Negotiable)
1) No network calls during analysis execution (CI or local).
2) Stable ordering everywhere:
   - sort keys
   - sort lists
   - stable file traversal
3) Fixed formatting:
   - UTF-8
   - LF newlines
4) Hashing:
   - All produced files MUST be listed in a manifest with SHA256.
5) Reproducibility:
   - Same git commit + same inputs => byte-identical outputs.

## Analysis Levels (Defined)
Level 0 — Structural Audit
- Validate registry and state structural invariants (beyond schema).
- Detect missing fields, invalid cross-references, forbidden keys.

Level 1 — Descriptive Statistics (Data Analysis, Non-Interpretive)
- Counts, distributions, timelines, completeness metrics.
- No ranking of theories, no “best interpretation”.
- Only descriptive outputs derived from existing epistemic fields.

Level 2 — Consistency Checks (Formal, Rule-Based)
- Contradiction detection between states (rule-defined).
- Trace provenance consistency and evidence linkage integrity.

Level 3 — Release Packaging (Deterministic)
- Bundle results + manifest into releases/<RELEASE_ID>/.

## Forbidden (Explicit)
- Any modification to Phase-2 artifacts.
- Any subjective theory selection, scoring, or interpretive ranking unless explicitly declared later
  in a separate Phase-3 amendment file with version bump.
- Any reliance on live web data in the core pipeline.

## Canonical Run ID Format
RUN_ID MUST be:
YYYYMMDD_HHMMSSZ__<SHORT_GIT_SHA>

Example:
20260101_120000Z__a1b2c3d

## Minimum Required Outputs Per Run
analysis_artifacts/<RUN_ID>/manifest.json
analysis_artifacts/<RUN_ID>/reports/summary.md
analysis_artifacts/<RUN_ID>/tables/state_inventory.csv
analysis_artifacts/<RUN_ID>/tables/field_completeness.csv
