# PHASE-5 TRANSITION CHECKLIST

**Repository**: trizel-ai/trizel-epistemic-engine  
**Phase**: Phase-5 Planning and Governance Documentation  
**Purpose**: Define requirements for phase transitions, freezes, and unfreezes  
**Status**: Planning Documentation (Authoritative)

---

## Overview

This document defines the **mandatory checklist** for transitioning between phases of the TRIZEL Epistemic Engine.

Phase transitions include:
1. **Opening a new phase** (initialization)
2. **Freezing a completed phase** (immutability declaration)
3. **Unfreezing a frozen phase** (rare; requires governance approval)

---

## 1. Opening a New Phase

Before opening a new phase, the following requirements **must** be satisfied:

### 1.1 Prerequisites

- [ ] **All prior phases are completed and frozen** (or explicitly documented as incomplete)
- [ ] **Phase number and name are assigned** (e.g., Phase-6: [Name])
- [ ] **Epistemic question is defined** (What question does this phase answer?)
- [ ] **Scope boundaries are explicit** (What is included? What is excluded?)

### 1.2 Governance Documentation

- [ ] **Phase directive created** (`docs/PHASE[N]_EXECUTION_DIRECTIVE.md`)
  - Defines phase scope, objectives, and constraints
  - Lists prohibited actions and behaviors
  - Establishes contract requirements
  - Declares governance rules

- [ ] **Build plan or initialization status created** (`docs/PHASE[N]_BUILD_PLAN.md` or `docs/PHASE[N]_INITIALIZATION_STATUS.md`)
  - Lists deliverables and milestones
  - Defines completion criteria
  - Documents dependencies on prior phases

- [ ] **Project tree documented** (`docs/PHASE[N]_PROJECT_TREE.md`)
  - Declares directory structure
  - Lists expected artifacts
  - Documents file organization

### 1.3 Phase Structure

- [ ] **Phase directory created** (if applicable, e.g., `phase[N]/`)
- [ ] **Schema directory created** (if applicable, e.g., `schema/phase[N]/`)
- [ ] **Placeholder files added** (e.g., `.gitkeep`, `README.md`)

### 1.4 Contract and Testing

- [ ] **Contract test created** (`tests/test_phase[N]_contract.py`)
  - Enforces governance rules
  - Validates schema compliance (if applicable)
  - Checks for prohibited tokens or behaviors

- [ ] **Smoke test created** (`tests/test_phase[N]_smoke.py`)
  - Validates directory structure
  - Checks for required files
  - Ensures basic functionality

- [ ] **CI gate added** (`.github/workflows/phase[N]-contract.yml`)
  - Runs contract tests on every PR
  - Prevents merging of non-compliant code
  - Enforces governance automatically

### 1.5 Compliance

- [ ] **Governance invariants acknowledged** (see `docs/phase5/GOVERNANCE_INVARIANTS.md`)
- [ ] **No violations of prior phase freezes**
- [ ] **No retroactive modifications to frozen phases**

### 1.6 Review and Approval

- [ ] **Phase initialization PR reviewed**
- [ ] **All contract tests pass**
- [ ] **Documentation is complete and accurate**
- [ ] **Phase initialization is merged to base branch**

---

## 2. Freezing a Completed Phase

Before freezing a phase, the following requirements **must** be satisfied:

### 2.1 Completion Criteria

- [ ] **All phase objectives completed** (as defined in phase directive or build plan)
- [ ] **All deliverables produced and committed**
- [ ] **All contract tests pass**
- [ ] **No unresolved execution defects**

### 2.2 Freeze Documentation

- [ ] **Freeze notice created** (`docs/PHASE[N]_FREEZE_NOTICE.md`)
  - Declares phase completion and freeze
  - Lists frozen artifacts (code, schemas, contracts)
  - Defines prohibited actions after freeze
  - Establishes unfreeze protocol

- [ ] **Completion document created** (`docs/PHASE[N]_COMPLETION.md`)
  - Summarizes phase achievements
  - Documents execution history (if applicable)
  - Lists publication records (if applicable)
  - Declares forward path

### 2.3 Archival and Publication

- [ ] **Phase artifacts committed and pushed**
- [ ] **Git tag created** (e.g., `phase-[N]-freeze`)
- [ ] **Publication record established** (optional but recommended)
  - Zenodo DOI or equivalent
  - Phase description and scope
  - License declaration (e.g., CC BY 4.0)

### 2.4 Forward Compatibility

- [ ] **Next phase identified** (if applicable)
- [ ] **Dependency documentation updated** (how future phases may use this phase)
- [ ] **Citation format established** (how to reference this frozen phase)

### 2.5 Enforcement

- [ ] **Freeze is effective immediately upon merge**
- [ ] **All team members notified of freeze**
- [ ] **CI contracts updated to enforce freeze** (if applicable)

### 2.6 Review and Approval

- [ ] **Freeze PR reviewed**
- [ ] **All stakeholders acknowledge freeze**
- [ ] **Freeze is merged to base branch**

---

## 3. Unfreezing a Frozen Phase (Exceptional)

Unfreezing a phase is **rare and discouraged**. It should only occur when:

- A critical bug or security vulnerability is discovered
- A governance error requires correction
- An explicit, documented need arises

### 3.1 Prerequisites

- [ ] **Explicit justification documented** (Why is the unfreeze necessary?)
- [ ] **Impact assessment completed** (What is affected by the unfreeze?)
- [ ] **Alternative approaches considered** (Can this be addressed in a new phase instead?)

### 3.2 Unfreeze Documentation

- [ ] **Unfreeze proposal created** (`docs/PHASE[N]_UNFREEZE_PROPOSAL.md`)
  - Explains the reason for unfreezing
  - Documents what will be modified
  - Establishes scope limits for modifications
  - Defines re-freeze criteria

- [ ] **Unfreeze approved by governance** (author review or equivalent)

### 3.3 Modification and Re-Freeze

- [ ] **Minimum necessary changes made** (surgical fixes only)
- [ ] **All contract tests pass after modifications**
- [ ] **Documentation updated to reflect changes**
- [ ] **Re-freeze notice created** (`docs/PHASE[N]_REFREEZE_NOTICE.md`)
  - Documents what was changed
  - Declares phase re-frozen
  - Updates publication record (if applicable)

### 3.4 Archival Update

- [ ] **New git tag created** (e.g., `phase-[N]-freeze-v2`)
- [ ] **Publication record updated** (if applicable)
- [ ] **Changelog or modification log created**

### 3.5 Review and Approval

- [ ] **Unfreeze PR reviewed**
- [ ] **Re-freeze is approved**
- [ ] **Re-freeze is merged to base branch**

---

## 4. Cross-Phase Dependencies

When a new phase depends on a frozen phase, the following requirements **must** be satisfied:

- [ ] **Dependency is documented explicitly** (in phase directive or build plan)
- [ ] **Frozen phase is referenced by tag or commit SHA** (immutable reference)
- [ ] **Frozen phase artifacts are consumed as read-only inputs**
- [ ] **No modifications to frozen phase are made**
- [ ] **Citation format is followed** (if frozen phase has a publication record)

---

## 5. Common Anti-Patterns (Prohibited)

### Prohibited Actions During Phase Transitions

- ❌ **Opening a new phase before the prior phase is frozen** (unless explicitly documented as parallel work)
- ❌ **Modifying a frozen phase without an unfreeze proposal**
- ❌ **Merging incomplete phases without documenting incompleteness**
- ❌ **Skipping contract tests or CI gates**
- ❌ **Silent modifications to governance documents**
- ❌ **Retroactive changes to frozen artifacts**

---

## 6. Phase Lifecycle Summary

### Standard Phase Lifecycle

1. **Initialization**: Open new phase (Section 1)
2. **Development**: Implement phase objectives (governed by phase directive)
3. **Completion**: Freeze phase (Section 2)
4. **Archival**: Tag and publish (Section 2.3)
5. **Reference**: Cite frozen phase in future work (Section 4)

### Exceptional Lifecycle (Rare)

1. **Initialization**: Open new phase
2. **Development**: Implement phase objectives
3. **Completion**: Freeze phase
4. **Critical Issue Discovered**: Unfreeze phase (Section 3)
5. **Modification**: Fix issue (surgical changes only)
6. **Re-Freeze**: Re-freeze phase (Section 3.3)
7. **Archival Update**: Update tags and publications

---

## Enforcement

This checklist is **mandatory** for all phase transitions.

Violations of this checklist result in:

- Immediate rejection of PRs
- Requirement to revert non-compliant changes
- Documentation of the violation and corrective action

---

## Declaration

This checklist is effective immediately and applies to all current and future phases.

All phase transitions must comply with this checklist or explicitly document deviations (with governance approval).

---

END OF PHASE-5 TRANSITION CHECKLIST
