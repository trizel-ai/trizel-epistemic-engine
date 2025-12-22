"""
Registry management for TRIZEL epistemic engine.

This module provides utilities for loading and validating state registries.
No data ingestion, interpretation ranking, or numerical analysis is performed here.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from .io import load_json, load_state


def load_state_registry(registry_path: str) -> Dict[str, Any]:
    """
    Load an epistemic state registry from disk.
    
    Args:
        registry_path: Path to registry JSON file.
        
    Returns:
        Dictionary containing the registry.
        
    Raises:
        FileNotFoundError: If registry file doesn't exist.
        json.JSONDecodeError: If registry is invalid JSON.
    """
    return load_json(registry_path)


def validate_registry_sorting(registry: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate that state_files list is sorted lexicographically.
    
    Args:
        registry: Dictionary representing a state registry.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    state_files = registry.get("state_files", [])
    
    if not isinstance(state_files, list):
        return False, "state_files must be a list"
    
    # Check if list is sorted
    sorted_files = sorted(state_files)
    if state_files != sorted_files:
        return False, f"state_files must be sorted lexicographically. Expected: {sorted_files}, Got: {state_files}"
    
    return True, None


def validate_registry_structure(registry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the structure of an epistemic state registry.
    
    Args:
        registry: Dictionary representing a state registry.
        
    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    
    # Check required registry fields
    required_fields = ["registry_version", "system", "created", "state_files"]
    for field in required_fields:
        if field not in registry:
            errors.append(f"Missing required registry field: {field}")
    
    if errors:
        return False, errors
    
    # Validate state_files is a list
    if not isinstance(registry["state_files"], list):
        errors.append(f"state_files must be a list, got {type(registry['state_files']).__name__}")
        return False, errors
    
    # Validate lexicographic sorting
    is_sorted, sort_error = validate_registry_sorting(registry)
    if not is_sorted:
        errors.append(sort_error)
    
    return len(errors) == 0, errors


def get_state_by_id(registry_base_path: str, registry: Dict[str, Any], state_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific epistemic state from a registry by ID.
    
    Args:
        registry_base_path: Base path where registry file is located.
        registry: The state registry dictionary.
        state_id: The state identifier to search for.
        
    Returns:
        The epistemic state dictionary if found, None otherwise.
    """
    registry_path = Path(registry_base_path)
    
    for state_file in registry.get("state_files", []):
        state_path = registry_path / state_file
        try:
            state = load_state(str(state_path))
            if state.get("state_id") == state_id:
                return state
        except (FileNotFoundError, KeyError):
            continue
    
    return None


def list_all_states(registry_base_path: str, registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Load all states referenced in a registry.
    
    Args:
        registry_base_path: Base path where registry file is located.
        registry: The state registry dictionary.
        
    Returns:
        List of all epistemic states in the registry.
    """
    states = []
    registry_path = Path(registry_base_path)
    
    for state_file in registry.get("state_files", []):
        state_path = registry_path / state_file
        try:
            state = load_state(str(state_path))
            states.append(state)
        except (FileNotFoundError, KeyError):
            continue
    
    return states
