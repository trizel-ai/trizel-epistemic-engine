# Data Contract

**Version**: 2.0.0  
**Last Updated**: 2025-12-22  
**Scope**: Epistemic Layer for 3I/ATLAS

## Purpose

This document defines the data contracts, interfaces, and constraints for the TRIZEL epistemic engine. It ensures strict separation between the epistemic layer and external systems (ingest and analytical layers).

## Core Principles

1. **Immutability**: Epistemic states, once registered, are immutable
2. **Traceability**: All states reference read-only DOI sources via provenance
3. **Determinism**: All operations produce consistent, reproducible results
4. **Audit-safety**: Complete provenance chain for all states
5. **Lexicographic ordering**: Registry state files must be sorted

## Epistemic State Schema

### Required Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `state_id` | string | Unique identifier for this state | Format: `{system}_{sequence}` (e.g., `3i_atlas_001`) |
| `timestamp` | string | ISO 8601 timestamp of state creation | UTC timezone, format: `YYYY-MM-DDTHH:MM:SSZ` |
| `source_doi` | string | DOI reference to source data | Must be valid DOI format: `10.xxxx/...` |
| `determinacy` | string | Epistemic determinacy status | One of: `confirmed`, `plausible`, `underdetermined`, `unfalsified`, `falsified` |
| `assumptions` | array | Assumptions underlying this state | Non-empty array of strings |
| `required_observations` | array | Observations required to validate | Non-empty array of strings |
| `provenance` | object | Provenance linking to ingest layer | See Provenance Structure below |
| `incompatibilities` | array | Incompatible state IDs | Array of `state_id` strings |

### Provenance Structure

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `ingest_doi` | string | Fixed DOI to ingest layer | Must be `10.5281/zenodo.18012859` |
| `record_ids` | array | Record identifiers from ingest | Array of strings (may be empty) |

### Optional Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `description` | string | Human-readable description | Max 1000 characters |
| `tags` | array | Categorical tags | Array of strings |
| `related_states` | array | References to related states | Array of `state_id` strings |
| `version` | string | Semantic version | Format: `X.Y.Z` |

### Example

```json
{
  "state_id": "3i_atlas_001",
  "timestamp": "2025-12-22T19:52:24Z",
  "source_doi": "10.5281/zenodo.18012859",
  "determinacy": "plausible",
  "assumptions": [
    "Standard cosmology",
    "No active outgassing"
  ],
  "required_observations": [
    "Multi-wavelength photometry",
    "High-resolution spectroscopy"
  ],
  "provenance": {
    "ingest_doi": "10.5281/zenodo.18012859",
    "record_ids": ["rec_001", "rec_042"]
  },
  "incompatibilities": ["3i_atlas_002"],
  "description": "Alternative interpretation of 3I/ATLAS observational data",
  "tags": ["3I", "ATLAS", "plausible_interpretation"],
  "version": "1.0.0"
}
```

## State Registry Contract

### Format
- **File Format**: JSON
- **Encoding**: UTF-8
- **Structure**: Registry with state file references

### Constraints
- Registry contains file paths, not inline states
- Each state stored in separate JSON file
- `state_files` list must be sorted lexicographically
- `state_id` must be unique across all referenced states
- All referenced states must pass schema validation

### Example Registry

```json
{
  "registry_version": "1.0.0",
  "system": "3I_ATLAS",
  "created": "2025-12-22T19:52:24Z",
  "state_files": [
    "states/3i_atlas_000.json",
    "states/3i_atlas_001.json"
  ]
}
```

## Interface Boundaries

### What This Layer Does
✅ Validate epistemic state schemas  
✅ Store validated states in separate files  
✅ Maintain sorted registry of state files  
✅ Verify DOI format compliance  
✅ Ensure state uniqueness  
✅ Validate provenance.ingest_doi is fixed to `10.5281/zenodo.18012859`  
✅ Enforce non-empty assumptions and required_observations  

### What This Layer Does NOT Do
❌ Fetch data from DOIs (read-only references only)  
❌ Parse or interpret external data  
❌ Rank or score epistemic states  
❌ Perform numerical analysis  
❌ Execute simulations  
❌ Make epistemic judgments beyond schema validation  
❌ Perform theory ranking or selection  

## Upstream Dependencies (Ingest Layer)

**Relationship**: Read-only DOI references via fixed provenance  
**Data Flow**: One-way (Ingest → Epistemic via DOI publication)  
**Fixed Ingest DOI**: `10.5281/zenodo.18012859`

### Expected from Ingest Layer
- Published datasets with permanent DOI `10.5281/zenodo.18012859`
- Record IDs for traceability
- No direct data transfer
- No API calls or synchronization

### Provided to Ingest Layer
- Nothing (one-way dependency)

## Downstream Dependencies (Analytical Layer)

**Relationship**: Read-only state access  
**Data Flow**: One-way (Epistemic → Analytical)  

### Expected from Analytical Layer
- Read epistemic state registry and individual state files
- No writes to registry or states
- No ranking feedback loops

### Provided to Analytical Layer
- Validated epistemic states in separate JSON files
- Schema-compliant states with determinacy classification
- Immutable state history
- Lexicographically sorted registry

## Validation Rules

### Schema Validation
1. All required fields must be present (state_id, timestamp, source_doi, determinacy, assumptions, required_observations, provenance, incompatibilities)
2. Field types must match schema definition
3. String formats (DOI, ISO 8601) must be valid
4. `determinacy` must be from allowed enumeration: {confirmed, plausible, underdetermined, unfalsified, falsified}
5. `assumptions` and `required_observations` must be non-empty arrays of strings
6. `provenance.ingest_doi` must be exactly `10.5281/zenodo.18012859`
7. `provenance.record_ids` must be an array (may be empty)

### Business Logic Validation
1. `state_id` must be unique across all states in registry
2. `source_doi` must follow DOI format pattern
3. `timestamp` must be valid ISO 8601 UTC timestamp
4. `related_states` and `incompatibilities` must reference valid state IDs (if provided)
5. Registry `state_files` list must be sorted lexicographically

### Immutability Enforcement
1. Once a state file is created, it cannot be modified
2. Corrections require new state entries with versioning
3. Deletions are not permitted (use `determinacy: "falsified"` instead)
4. Registry is append-only (new state files added in sorted order)

## Error Handling

### Validation Failures
- Return structured error messages
- Do not modify registry on validation failure
- Log all validation attempts

### Schema Evolution
- Major version bump for breaking changes
- Minor version bump for backward-compatible additions
- Patch version for documentation/clarification

## Compliance Checklist

- [x] No data ingestion from DOIs
- [x] No interpretation ranking
- [x] No physics models
- [x] No simulations
- [x] Read-only external references
- [x] Deterministic operations
- [x] Audit-safe design
- [x] Fixed ingest DOI enforced
- [x] Lexicographic sorting enforced
- [x] Structural initialization only

## Change Log

### Version 2.0.0 (2025-12-22)
- Replace `epistemic_status` with `determinacy` enum
- Add required fields: assumptions, required_observations, provenance, incompatibilities
- Change registry structure to reference separate state files
- Enforce lexicographic sorting of state_files
- Fix provenance.ingest_doi to 10.5281/zenodo.18012859
- Move to modular code structure (src/epistemic/)

### Version 1.0.0 (2025-12-22)
- Initial data contract definition
- Epistemic state schema v1.0.0
- Registry format specification
- Interface boundary documentation
