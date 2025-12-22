# trizel-epistemic-engine

TRIZEL Phase-2 implements an **epistemic state engine** for a single target object: **3I/ATLAS**.

This repository is **structural and audit-safe**: it defines schemas, registries, validators, and tests for representing multiple mutually-incompatible hypotheses **without** selecting, ranking, or endorsing any physical theory.

## Non-negotiable scope lock

Phase-1 (TRIZEL Scientific Ingest Layer) is complete, immutable, and the sole ground-truth reference.

- Ingest DOI (immutable): **10.5281/zenodo.18012859**
- Phase-2 reads ingest outputs **read-only by DOI reference**.
- Phase-2 MUST NOT modify ingest repositories, re-ingest data, recompute results, or perform analysis.

## Canonical execution policy (authoritative)

All Copilot execution and all Phase-2 constraints are defined in:

- **docs/PHASE2_EXECUTION_DIRECTIVE.md**

This file is the merge gate for Phase-2: it enumerates allowed outputs, prohibited content (including any theory-superiority framing), required paths, required schema keys, determinism rules, and stop conditions.

## Repository structure (canonical)

Phase-2 work must remain within these canonical paths:

- `schema/epistemic_state.schema.json`
- `states/3I_ATLAS/state_registry.json`
- `states/3I_ATLAS/states/*.json`
- `src/epistemic/`
- `tests/`

## Validation

Run locally:

- `python -m src.epistemic.validate_states`
- `python -m unittest -q`

Both commands must pass deterministically before approval/merge.