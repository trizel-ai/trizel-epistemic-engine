# PHASE-4 BUILD PLAN (WITH MANDATORY TCRL)

Repository: trizel-ai/trizel-epistemic-engine  
Branch: phase4/initialize-tcrl-and-phase4  
Status: Phase-4 Planning + Initialization Only (no execution beyond scaffolding)

## 0) Non-Negotiable Context Locks

1) Phase-1 ingest is immutable ground truth and must not be modified or re-ingested:
- Ingest DOI (locked): 10.5281/zenodo.18012859

2) Phase-2 artifacts are epistemic-only and immutable.

3) Phase-3 artifacts are deterministic execution infrastructure and immutable after Phase-3 completion/freeze.

## 1) The Core Methodological Problem (Formal)

There exist theories that are:
- non-classical,
- structurally closed (axiomatic / constructive),
- not directly translatable into conventional observables without distortion.

Therefore, Phase-4 must NOT attempt to "understand theories".

## 2) Mandatory Prior Layer

Pre-Phase-4: Theory Comprehension & Reduction Layer (TCRL)

TCRL is a mandatory preparatory layer that:
- DOES: holistic theory reading + internal reduction into testable or constrainable claim units
- DOES NOT: test, classify validity, rank theories, or publish results

Phase-4 consumes only TCRL outputs, never raw theory text directly.

## 3) Phase-4 Role (Strict)

Phase-4 is allowed to:
- test what has already been reduced into explicit testable/constraint claims
- evaluate determinacy against observational records (ingest-linked)
- classify outcomes only under declared test conditions

Phase-4 is not allowed to:
- interpret theories holistically
- declare any theory "true" or "superior"
- introduce physics endorsement language

## 4) Canonical Artifact Types

### 4.1 TCRL Output Artifact (TCP: Testable Claim Pack)
A TCRL run must produce a TCP JSON document containing:
- theory_id (string)
- source_refs (citations or pointers; may include DOI/URL/commit)
- closed_unit_summary (neutral; no endorsement)
- ontology (entities / quantities / primitives)
- axioms (enumerated)
- measurement_interface (how the theory defines observation, if any)
- reduced_claims[] (each claim is independently testable or constrainable)
- non_reducible_components[] (declared as not testable at present)

TCRL output MUST NOT contain any computed results or data-derived conclusions.

### 4.2 Phase-4 Evaluation Output Artifact (EVAL)
Phase-4 produces EVAL JSON per claim pack:
- evaluation_id
- tcp_id + claim_id
- ingest_doi lock
- record_ids used
- test_conditions (explicit)
- outcome classification (see Section 5)
- constraint summary (if constrainable)
- reproducibility block (no network, deterministic ordering)

## 5) Phase-4 Outcome Classification Rule (Testability-Based)

For each reduced claim (claim_id) in a TCP:

1) If the claim yields a measurable prediction under defined conditions:
- classify: TESTABLE
- execute test against ingest-linked records

2) If the claim yields no measurable prediction but yields observational constraints:
- classify: CONSTRAINABLE
- execute constraint evaluation against ingest-linked records

3) If the claim yields neither measurable predictions nor constraints at present:
- classify: NON_TESTABLE_PRESENTLY
- do not test; record as boundary of current observability

4) If the claim is inconsistent with the selected records under declared conditions:
- classify: EXCLUDED_UNDER_CONDITIONS
- exclusion is always conditional on explicit test conditions

5) Alternative / non-traditional theories are handled identically:
- no privilege
- no a priori dismissal
- same reduction + claim evaluation protocol

## 6) Phase-4 Scope Boundaries (Hard)

Phase-4 includes:
- TCP schema + validators
- EVAL schema + validators
- deterministic pipeline scaffolding
- CI gates enforcing immutability + determinism
- initial “no-op” run proving wiring

Phase-4 excludes (not now):
- broad automated scientific interpretation
- open-ended theory comparison dashboards
- ranking theories globally
- any physics claims not reducible to TCP claims

## 7) Required Directory Targets (Phase-4 Additive Only)

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

## 8) Stop Rule

Stop after:
- contracts + schemas exist
- deterministic validators exist
- CI gates pass
- templates exist
- no scientific execution beyond no-op wiring

No additional features beyond scaffolding are permitted until the Phase-4 directive is merged.
