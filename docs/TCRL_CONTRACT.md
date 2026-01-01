# TCRL_CONTRACT — Theory Comprehension & Reduction Layer (Pre-Phase-4)

## Purpose (Strict)
TCRL converts a theory (treated as a closed unit) into a test-ready representation WITHOUT testing it.

TCRL outputs:
- TCP (Testable Claim Pack)

TCRL does NOT output:
- test results
- validity claims
- rankings
- scientific conclusions

## TCRL Process (Deterministic Passes)

### Pass 1 — Hermeneutic Closed Reading
Extract, neutrally:
- entities / primitives
- axioms / postulates
- causal structure
- defined notion of "phenomenon"
- measurement interface (if any)

### Pass 2 — Reduction into Claims
Produce reduced_claims[] such that each claim is:
- either TESTABLE (measurable prediction under conditions)
- or CONSTRAINABLE (observationally restrictable)
- or NON_TESTABLE_PRESENTLY (cannot be tested or constrained currently)

### Pass 3 — Observable Mapping (If Possible)
For each reduced claim:
- define required_observations (names, types, constraints)
- specify test_conditions (explicit)
- specify falsification / exclusion conditions (explicit)

### Pass 4 — Non-Reducible Declaration
Anything not reducible must be stated as:
- non_reducible_components[] with reason

## TCRL Output Artifact: TCP (Required Fields)

TCP MUST contain:
- tcp_id (string)
- theory_id (string)
- source_refs (array of strings)
- closed_unit_summary (string; neutral)
- ontology (array of strings)
- axioms (array of strings)
- measurement_interface (array of strings; may be empty)
- reduced_claims (array of objects; non-empty)
- non_reducible_components (array; may be empty)

Each reduced_claims[] entry MUST include:
- claim_id (string)
- claim_text (string; neutral)
- classification (one of: TESTABLE, CONSTRAINABLE, NON_TESTABLE_PRESENTLY)
- assumptions (non-empty array)
- required_observations (non-empty array) for TESTABLE/CONSTRAINABLE; may be empty only for NON_TESTABLE_PRESENTLY
- test_conditions (array; may be empty only for NON_TESTABLE_PRESENTLY)
- exclusion_conditions (array; may be empty)

## Prohibitions
- No theory preference language.
- No claims of empirical success.
- No inferred results from data.
- No timestamps as epistemic evidence.

## Hand-off to Phase-4
Phase-4 may only evaluate:
- TCP.claim_id entries
against ingest-linked record_ids under declared conditions.
