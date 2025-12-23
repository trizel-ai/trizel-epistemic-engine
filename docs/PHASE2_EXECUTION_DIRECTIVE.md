# COPILOT ALGORITHMIC DIRECTIVE — TRIZEL PHASE-2 (EPISTEMIC ONLY)

## 0) Hard context lock (non-negotiable)
- Phase-1 ingest is immutable and is the sole ground-truth reference for Phase-2.
- Ingest DOI (locked): **10.5281/zenodo.18012859**
- Do not modify ingest repositories and do not re-ingest data.

## 1) Scope definition (Phase-2 only)
Phase-2 implements **epistemic state tracking** only:
- verification / decidability states
- schema + registry + validation gates
- deterministic checks suitable for audit

Phase-2 explicitly excludes analysis and interpretation.

## 2) Absolute exclusions (prohibited content)
Do not introduce any of the following in code, docs, tests, or state files:
- physics explanations or interpretive commentary
- theory endorsement, theory comparison, ranking, “superiority” language
- equations, fitting, simulations, inference, model selection
- any phrasing that implies a “best” framework or “winner”

If any text suggests “X explains,” “superior,” “validated theory,” or similar, it must be removed.

## 3) Canonical work location (prevent drift)
- All Phase-2 work must occur on the canonical Phase-2 pull request branch only.
- No parallel PRs or alternative branches may be used for Phase-2 execution.
- `main` remains untouched until Phase-2 is complete and compliant.

## 4) Canonical repository structure (required, exact)
Phase-2 must implement and reference only the following canonical paths:

- `schema/epistemic_state.schema.json`
- `states/3I_ATLAS/state_registry.json`
- `states/3I_ATLAS/states/*.json`
- `src/epistemic/__init__.py`
- `src/epistemic/io.py`
- `src/epistemic/registry.py`
- `src/epistemic/validate_states.py`
- `docs/PHASE2_EXECUTION_DIRECTIVE.md`
- `docs/epistemic_overview.md`
- `docs/3i_atlas_scope.md`
- `tests/test_state_validation.py`

Non-canonical legacy paths must not be used or referenced. If present, they must be removed or migrated:
- `schemas/`
- `registry/`
- `src/validation.py`
- `tests/test_validation.py`

## 5) Phase-2 epistemic contract (schema semantics)
Epistemic states are hypothesis containers with no interpretive preference.

### Mandatory state fields (schema must require all)
- `state_id` (string; unique)
- `label` (string)
- `assumptions` (array of strings; non-empty)
- `required_observations` (array of strings; non-empty)
- `incompatibilities` (array of `state_id` strings; may be empty)
- `determinacy` (enum, exact):
  - `confirmed`
  - `plausible`
  - `underdetermined`
  - `unfalsified`
  - `falsified`
- `provenance` (object; required):
  - `ingest_doi` (string; must equal **"10.5281/zenodo.18012859"**)
  - `record_ids` (array of strings; may be empty)

Optional (must remain neutral if present):
- `falsification_criteria` (array of strings)
- `notes` (string)

### Explicitly forbidden
- `timestamp` as a required epistemic property
- generic `source_doi` not locked to the ingest DOI
- `epistemic_status` with values like competing/consensus/rejected/preliminary
- any field or semantics implying “best theory” / “winner” / “validated framework”

## 6) Determinism requirements
- `states/3I_ATLAS/state_registry.json` must list state filenames in lexicographic order.
- Validation must fail if the registry is unsorted, duplicated, or references missing files.
- Validation must fail if ingest DOI is not exactly **"10.5281/zenodo.18012859"**.

## 7) Test gate (merge precondition)
Before merge, the following commands must pass deterministically:
- `python -m src.epistemic.validate_states`
- `python -m unittest -q`

## 8) Stop rule (critical)
Stop after completing:
- canonical structure
- strict schema
- neutral registry + placeholder states
- validator + deterministic tests passing

Do not add analysis features, physical modeling, or theory comparison.
