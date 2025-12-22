"""
TRIZEL Epistemic Engine - Phase-2

An audit-safe epistemic state engine for managing competing interpretations
of 3I/ATLAS data.

This module provides validation utilities for epistemic states and registries.
"""

__version__ = "1.0.0"

from .validation import (
    validate_epistemic_state,
    validate_registry,
    load_schema,
    load_state_registry,
    get_state_by_id,
    ValidationError,
)

__all__ = [
    "validate_epistemic_state",
    "validate_registry",
    "load_schema",
    "load_state_registry",
    "get_state_by_id",
    "ValidationError",
]
