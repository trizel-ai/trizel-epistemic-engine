# Data Contract

## Overview

This document defines the data contract for the TRIZEL Epistemic Engine. All data structures must conform to these specifications to ensure reproducibility, immutability, and audit compliance.

## Epistemic State Format

### Structure

Each epistemic state is a JSON file conforming to `schema/epistemic_state.schema.json`.

### Required Fields

```json
{
  "state_id": "string",           // Unique identifier (format: YYYY-MM-DD_descriptor)
  "timestamp": "string",          // ISO 8601 timestamp
  "zenodo_doi": "string",         // Immutable DOI reference
  "description": "string",        // Human-readable description
  "metadata": {                   // Metadata object
    "author": "string",           // State author
    "version": "string",          // Version number (semver)
    "tags": ["string"]            // Categorization tags
  },
  "interpretation": {             // Interpretation details
    "framework": "string",        // Epistemic framework used
    "assumptions": ["string"],    // Key assumptions
    "scope": "string"             // Scope of interpretation
  },
  "data_references": [            // Dataset references
    {
      "dataset_id": "string",     // Dataset identifier
      "zenodo_doi": "string",     // Immutable DOI
      "description": "string"     // Dataset description
    }
  ]
}
```

### Validation Rules

1. **state_id**: Must be unique across all states in the registry
2. **timestamp**: Must be valid ISO 8601 format
3. **zenodo_doi**: Must reference a valid, immutable Zenodo DOI
4. **version**: Must follow semantic versioning (semver)
5. **data_references**: At least one reference required

## State Registry Format

The state registry (`state_registry.json`) maintains an ordered list of all epistemic states.

### Structure

```json
{
  "registry_version": "string",   // Registry version (semver)
  "last_updated": "string",       // ISO 8601 timestamp
  "states": [                     // Array of state entries
    {
      "state_id": "string",       // Matches state file
      "file_path": "string",      // Relative path to state file
      "active": boolean           // Whether state is active
    }
  ]
}
```

### Constraints

1. **Ordering**: States listed in chronological order by creation
2. **Uniqueness**: No duplicate state_id values
3. **File Paths**: All paths must be relative to repository root
4. **Active Status**: Only active states are used in analyses

## Immutability Requirements

### Zenodo DOI References

All external data must be referenced via permanent Zenodo DOIs:
- ✅ **Correct**: `10.5281/zenodo.1234567`
- ❌ **Incorrect**: `https://example.com/data.zip` (mutable URL)
- ❌ **Incorrect**: `doi:10.1234/arxiv.5678` (preprint, may change)

### State Versioning

Once a state is committed:
- **Never modify** the state file content
- **Create new version** if changes are needed
- **Increment version number** following semver

## Schema Validation

All state files must pass validation against `epistemic_state.schema.json`:

```bash
python -m src.epistemic.validate_states
```

Validation checks:
- JSON syntax correctness
- Schema compliance
- DOI format validity
- Timestamp format
- Version number format

## Data Flow

```
Zenodo Dataset (immutable)
    ↓
Epistemic State (JSON)
    ↓
Schema Validation
    ↓
Registry Entry
    ↓
Available for Analysis (external)
```

## Compliance

This data contract ensures:
1. **Reproducibility**: Same inputs always produce same outputs
2. **Immutability**: Referenced data never changes
3. **Auditability**: Complete provenance tracking
4. **Interoperability**: Standard JSON format
5. **Version Control**: Git-based change tracking

## Updates

This contract is versioned with the repository. Any changes require:
1. Version bump in registry
2. Migration plan for existing states
3. Updated schema validation
4. Documentation update

**Current Contract Version**: 1.0.0  
**Last Updated**: 2025-12-22
