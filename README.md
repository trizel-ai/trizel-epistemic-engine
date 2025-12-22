# TRIZEL Epistemic Engine

**Phase-2 of the TRIZEL project**: An audit-safe epistemic state engine for managing competing interpretations of 3I/ATLAS, strictly separated from ingest and analytical layers.

## Overview

The TRIZEL Epistemic Engine is designed to:
- **Store** versioned epistemic states representing competing interpretations of 3I/ATLAS data
- **Validate** all state files against a strict JSON schema
- **Ensure** immutability and reproducibility via DOI-referenced datasets
- **Separate** state representation from analytical logic

## Repository Structure

```
trizel-epistemic-engine/
├── schema/                          # JSON Schema definitions
│   └── epistemic_state.schema.json  # Schema for epistemic state files
├── states/                          # Epistemic state storage
│   └── 3I_ATLAS/
│       ├── state_registry.json      # Registry of all states
│       └── states/                  # Individual state files
├── src/epistemic/                   # Core validation and loading
│   ├── __init__.py
│   ├── io.py                        # I/O utilities
│   ├── registry.py                  # Registry loader
│   └── validate_states.py           # Schema validation
├── docs/                            # Documentation
│   ├── epistemic_overview.md        # Epistemic framework
│   └── 3i_atlas_scope.md           # 3I/ATLAS scope
├── tests/                           # Test suite
└── ZENODO_LINKS.md                  # Immutable DOI references
```

## Key Principles

1. **Immutability**: All data references use permanent DOIs (Zenodo)
2. **Separation of Concerns**: No analytical code in this repository
3. **Schema Validation**: All states must pass JSON schema validation
4. **Determinism**: Reproducible outputs from identical inputs
5. **Audit Trail**: Complete versioning and documentation

## Usage

### Validate States
```bash
python -m src.epistemic.validate_states
```

### Load Registry
```python
from src.epistemic.registry import load_registry
registry = load_registry('states/3I_ATLAS/state_registry.json')
```

## Development

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current phase status and roadmap.

See [DATA_CONTRACT.md](DATA_CONTRACT.md) for data format specifications.

## License

See [LICENSE](LICENSE) file for details.
