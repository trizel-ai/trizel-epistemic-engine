"""
TRIZEL Epistemic Engine - Phase-2

An audit-safe epistemic state engine for managing competing interpretations
of 3I/ATLAS data.

This package provides validation utilities for epistemic states and registries.
"""

__version__ = "1.0.0"

from .io import load_schema, load_state, load_json, save_json
from .registry import (
    load_state_registry,
    validate_registry_structure,
    validate_registry_sorting,
    get_state_by_id,
    list_all_states,
)
from .validate_states import (
    validate_epistemic_state,
    validate_state_id,
    validate_timestamp,
    validate_doi,
    validate_determinacy,
    validate_version,
    validate_provenance,
    ValidationError,
)

__all__ = [
    # I/O functions
    "load_schema",
    "load_state",
    "load_json",
    "save_json",
    # Registry functions
    "load_state_registry",
    "validate_registry_structure",
    "validate_registry_sorting",
    "get_state_by_id",
    "list_all_states",
    # Validation functions
    "validate_epistemic_state",
    "validate_state_id",
    "validate_timestamp",
    "validate_doi",
    "validate_determinacy",
    "validate_version",
    "validate_provenance",
    "ValidationError",
]
