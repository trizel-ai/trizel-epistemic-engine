# TRIZEL Epistemic Engine (Phase-2)

An audit-safe epistemic state engine for managing competing interpretations of 3I/ATLAS data, strictly separated from ingest and analytical layers.

## Overview

This repository implements the epistemic layer for the TRIZEL project, focusing exclusively on managing epistemic states for the 3I/ATLAS system. It does **not** include:
- Physics models
- Numerical simulations
- Data ingestion pipelines
- Interpretation ranking algorithms

## Scope

The epistemic engine provides:
- **Deterministic state management**: JSON-based epistemic state representation
- **Validation utilities**: Schema validation and consistency checks
- **State registry**: Immutable registry for 3I/ATLAS epistemic states
- **Read-only DOI references**: Links to published datasets (no data ingestion)

## Project Structure

```
trizel-epistemic-engine/
├── README.md                 # This file
├── PROJECT_STATUS.md         # Current status and roadmap
├── DATA_CONTRACT.md          # Interface definitions and constraints
├── ZENODO_LINKS.md          # Read-only DOI references
├── schema/                   # JSON schema
│   └── epistemic_state.schema.json
├── states/                   # State registries and files
│   └── 3I_ATLAS/
│       ├── state_registry.json
│       └── states/
│           └── *.json        # Individual state files
├── src/                      # Source code
│   └── epistemic/
│       ├── __init__.py
│       ├── io.py             # I/O utilities
│       ├── registry.py       # Registry management
│       └── validate_states.py # State validation
├── tests/                    # Test suite
│   └── test_epistemic.py
└── examples/                 # Usage examples
    └── usage_example.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Validate an Epistemic State

```python
from src.epistemic import validate_epistemic_state

state = {
    "state_id": "3i_atlas_001",
    "timestamp": "2025-12-22T19:52:24Z",
    "source_doi": "10.5281/zenodo.18012859",
    "determinacy": "plausible",
    "assumptions": ["Standard cosmology"],
    "required_observations": ["Multi-wavelength photometry"],
    "provenance": {
        "ingest_doi": "10.5281/zenodo.18012859",
        "record_ids": []
    },
    "incompatibilities": []
}

is_valid, errors = validate_epistemic_state(state)
```

### Load State Registry

```python
from src.epistemic import load_state_registry

registry = load_state_registry("states/3I_ATLAS/state_registry.json")
```

## Testing

```bash
pytest tests/
```

## Examples

See the `examples/` directory for usage demonstrations:

```bash
python3 examples/usage_example.py
```

## Hard Rules

1. **Read-only DOI references**: All external data references must be through immutable DOIs
2. **No data ingestion**: This layer does not fetch, parse, or interpret external data
3. **No interpretation ranking**: Epistemic states are stored without preference ordering
4. **Audit-safe**: All operations are deterministic and traceable
5. **Fixed ingest DOI**: All states must reference provenance.ingest_doi = "10.5281/zenodo.18012859"
6. **Lexicographic sorting**: Registry state_files list must be sorted lexicographically

## Determinacy Status

Epistemic states use determinacy classification:
- **confirmed**: Empirically verified with high confidence
- **plausible**: Consistent with observations, not yet confirmed
- **underdetermined**: Multiple competing interpretations possible
- **unfalsified**: Not yet contradicted by evidence
- **falsified**: Contradicted by empirical evidence

## License

See LICENSE file for details.
