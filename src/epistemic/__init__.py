"""
TRIZEL Epistemic Engine - Core Package

This package provides validation and loading utilities for epistemic states.
It does NOT perform any analysis - only validation and I/O operations.
"""

__version__ = "0.1.0"
__author__ = "TRIZEL Project Team"

from .io import load_json, save_json
from .registry import load_registry, validate_registry
from .validate_states import validate_state, validate_all_states

__all__ = [
    "load_json",
    "save_json",
    "load_registry",
    "validate_registry",
    "validate_state",
    "validate_all_states",
]
