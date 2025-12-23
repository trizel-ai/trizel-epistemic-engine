## Phase-2 scope (epistemic only)

This repository implements TRIZEL Phase-2: an audit-safe epistemic state engine for 3I/ATLAS. It manages **epistemic states** (assumptions, required observations, determinacy, and provenance) and is **strictly separated** from Phase-1 ingest and any analytical/modeling layers.

### Non-negotiable constraints

- Phase-1 ingest is immutable and is the sole ground-truth reference.
  - Ingest DOI (locked): `10.5281/zenodo.18012859`
- Phase-2 is epistemic only:
  - No physics explanations, no theory endorsement, no “ToE/STOE superiority” framing.
  - No equations, fitting, simulation, inference, ranking, or model selection.
- Any content implying “validated”, “superior”, “winner”, or similar comparative claims is out of scope and must not exist in code, docs, tests, or state files.

### Authoritative execution policy

All implementation and review must comply with:

- `docs/PHASE2_EXECUTION_DIRECTIVE.md` (authoritative)

### Verification (must pass)

- `python -m src.epistemic.validate_states`
- `python -m unittest -q`