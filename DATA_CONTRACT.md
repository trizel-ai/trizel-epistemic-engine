# Data Contract

**Version**: 1.0.0  
**Last Updated**: 2025-12-22  
**Scope**: Epistemic Layer for 3I/ATLAS

## Purpose

This document defines the data contracts, interfaces, and constraints for the TRIZEL epistemic engine. It ensures strict separation between the epistemic layer and external systems (ingest and analytical layers).

## Core Principles

1. **Immutability**: Epistemic states, once registered, are immutable
2. **Traceability**: All states reference read-only DOI sources
3. **Determinism**: All operations produce consistent, reproducible results
4. **Audit-safety**: Complete provenance chain for all states

## Epistemic State Schema

### Required Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `state_id` | string | Unique identifier for this state | Format: `{system}_{sequence}` (e.g., `3i_atlas_001`) |
| `timestamp` | string | ISO 8601 timestamp of state creation | UTC timezone, format: `YYYY-MM-DDTHH:MM:SSZ` |
| `source_doi` | string | DOI reference to source data | Must be valid DOI format: `10.xxxx/...` |
| `epistemic_status` | string | Status of this interpretation | One of: `competing`, `consensus`, `rejected`, `preliminary` |
| `metadata` | object | Additional metadata | Free-form JSON object |

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
  "source_doi": "10.5281/zenodo.example",
  "epistemic_status": "competing",
  "metadata": {
    "interpretation": "variant_A",
    "confidence": "medium",
    "reviewer": "anonymous"
  },
  "description": "Alternative interpretation of 3I/ATLAS observational data",
  "tags": ["3I", "ATLAS", "competing_interpretation"],
  "version": "1.0.0"
}
```

## State Registry Contract

### Format
- **File Format**: JSON
- **Encoding**: UTF-8
- **Structure**: Array of epistemic state objects

### Constraints
- Registry files are append-only (logical)
- Each state must pass schema validation
- `state_id` must be unique within registry
- `source_doi` must reference published, immutable datasets

### Example Registry

```json
{
  "registry_version": "1.0.0",
  "system": "3i_atlas",
  "created": "2025-12-22T19:52:24Z",
  "states": []
}
```

## Interface Boundaries

### What This Layer Does
✅ Validate epistemic state schemas  
✅ Store validated states in registry  
✅ Provide read access to registry  
✅ Verify DOI format compliance  
✅ Ensure state uniqueness  

### What This Layer Does NOT Do
❌ Fetch data from DOIs (read-only references only)  
❌ Parse or interpret external data  
❌ Rank or score epistemic states  
❌ Perform numerical analysis  
❌ Execute simulations  
❌ Make epistemic judgments beyond schema validation  

## Upstream Dependencies (Ingest Layer)

**Relationship**: Read-only DOI references  
**Data Flow**: One-way (Ingest → Epistemic via DOI publication)  

### Expected from Ingest Layer
- Published datasets with permanent DOIs
- No direct data transfer
- No API calls or synchronization

### Provided to Ingest Layer
- Nothing (one-way dependency)

## Downstream Dependencies (Analytical Layer)

**Relationship**: Read-only state access  
**Data Flow**: One-way (Epistemic → Analytical)  

### Expected from Analytical Layer
- Read epistemic state registry
- No writes to registry
- No ranking feedback loops

### Provided to Analytical Layer
- Validated epistemic states
- Schema-compliant JSON
- Immutable state history

## Validation Rules

### Schema Validation
1. All required fields must be present
2. Field types must match schema definition
3. String formats (DOI, ISO 8601) must be valid
4. `epistemic_status` must be from allowed enumeration

### Business Logic Validation
1. `state_id` must be unique within registry
2. `source_doi` must follow DOI format pattern
3. `timestamp` must be valid ISO 8601 UTC timestamp
4. `related_states` must reference existing states (if provided)

### Immutability Enforcement
1. Once a state is in the registry, it cannot be modified
2. Corrections require new state entries with versioning
3. Deletions are not permitted (use `epistemic_status: "rejected"`)

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

## Change Log

### Version 1.0.0 (2025-12-22)
- Initial data contract definition
- Epistemic state schema v1.0.0
- Registry format specification
- Interface boundary documentation
