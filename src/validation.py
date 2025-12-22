"""
Validation utilities for TRIZEL epistemic engine.

This module provides schema validation and business logic checks for epistemic states.
No data ingestion, interpretation ranking, or numerical analysis is performed here.
"""

import json
import re
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def load_schema(schema_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load the epistemic state JSON schema.
    
    Args:
        schema_path: Path to schema file. If None, uses default location.
        
    Returns:
        Dictionary containing the JSON schema.
        
    Raises:
        FileNotFoundError: If schema file doesn't exist.
        json.JSONDecodeError: If schema is invalid JSON.
    """
    if schema_path is None:
        # Default to schemas/epistemic_state.schema.json relative to project root
        project_root = Path(__file__).parent.parent
        schema_path = project_root / "schemas" / "epistemic_state.schema.json"
    else:
        schema_path = Path(schema_path)
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
    registry_file = Path(registry_path)
    
    if not registry_file.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")
    
    with open(registry_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_state_id(state_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate state_id format.
    
    Expected format: {system}_{sequence} (e.g., 3i_atlas_001)
    
    Args:
        state_id: The state identifier to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = r'^[a-z0-9_]+_[0-9]{3,}$'
    if not re.match(pattern, state_id):
        return False, f"state_id '{state_id}' does not match pattern: {pattern}"
    return True, None


def validate_timestamp(timestamp: str) -> Tuple[bool, Optional[str]]:
    """
    Validate ISO 8601 timestamp format (UTC).
    
    Expected format: YYYY-MM-DDTHH:MM:SSZ
    
    Args:
        timestamp: The timestamp string to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
    if not re.match(pattern, timestamp):
        return False, f"timestamp '{timestamp}' does not match ISO 8601 UTC format"
    
    # Validate it's a real date/time
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        return False, f"Invalid datetime: {e}"
    
    return True, None


def validate_doi(doi: str) -> Tuple[bool, Optional[str]]:
    """
    Validate DOI format.
    
    Expected format: 10.xxxx/suffix
    
    Args:
        doi: The DOI string to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = r'^10\.[0-9]{4,}(\.[0-9]+)*/[^\s]+$'
    if not re.match(pattern, doi):
        return False, f"source_doi '{doi}' does not match DOI format pattern"
    return True, None


def validate_epistemic_status(status: str) -> Tuple[bool, Optional[str]]:
    """
    Validate epistemic_status value.
    
    Allowed values: competing, consensus, rejected, preliminary
    
    Args:
        status: The epistemic status to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    allowed = {"competing", "consensus", "rejected", "preliminary"}
    if status not in allowed:
        return False, f"epistemic_status '{status}' not in allowed values: {allowed}"
    return True, None


def validate_version(version: str) -> Tuple[bool, Optional[str]]:
    """
    Validate semantic version format.
    
    Expected format: X.Y.Z
    
    Args:
        version: The version string to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = r'^[0-9]+\.[0-9]+\.[0-9]+$'
    if not re.match(pattern, version):
        return False, f"version '{version}' does not match semantic version format (X.Y.Z)"
    return True, None


def validate_epistemic_state(state: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    """
    Validate an epistemic state against the schema and business rules.
    
    Args:
        state: Dictionary representing an epistemic state.
        schema: Optional JSON schema. If None, loads default schema.
        
    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    
    # Check required fields
    required_fields = ["state_id", "timestamp", "source_doi", "epistemic_status", "metadata"]
    for field in required_fields:
        if field not in state:
            errors.append(f"Missing required field: {field}")
    
    # If missing required fields, return early
    if errors:
        return False, errors
    
    # Validate state_id
    is_valid, error = validate_state_id(state["state_id"])
    if not is_valid:
        errors.append(error)
    
    # Validate timestamp
    is_valid, error = validate_timestamp(state["timestamp"])
    if not is_valid:
        errors.append(error)
    
    # Validate source_doi
    is_valid, error = validate_doi(state["source_doi"])
    if not is_valid:
        errors.append(error)
    
    # Validate epistemic_status
    is_valid, error = validate_epistemic_status(state["epistemic_status"])
    if not is_valid:
        errors.append(error)
    
    # Validate metadata is a dictionary
    if not isinstance(state["metadata"], dict):
        errors.append(f"metadata must be a dictionary, got {type(state['metadata']).__name__}")
    
    # Validate optional fields if present
    if "description" in state:
        if not isinstance(state["description"], str):
            errors.append(f"description must be a string, got {type(state['description']).__name__}")
        elif len(state["description"]) > 1000:
            errors.append(f"description exceeds maximum length of 1000 characters")
    
    if "tags" in state:
        if not isinstance(state["tags"], list):
            errors.append(f"tags must be an array, got {type(state['tags']).__name__}")
        elif not all(isinstance(tag, str) for tag in state["tags"]):
            errors.append("All tags must be strings")
    
    if "related_states" in state:
        if not isinstance(state["related_states"], list):
            errors.append(f"related_states must be an array, got {type(state['related_states']).__name__}")
        else:
            for related_id in state["related_states"]:
                if not isinstance(related_id, str):
                    errors.append(f"related_states must contain strings, got {type(related_id).__name__}")
                else:
                    is_valid, error = validate_state_id(related_id)
                    if not is_valid:
                        errors.append(f"Invalid related state ID: {error}")
    
    if "version" in state:
        is_valid, error = validate_version(state["version"])
        if not is_valid:
            errors.append(error)
    
    return len(errors) == 0, errors


def validate_registry(registry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate an epistemic state registry structure.
    
    Args:
        registry: Dictionary representing a state registry.
        
    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    
    # Check required registry fields
    required_fields = ["registry_version", "system", "created", "states"]
    for field in required_fields:
        if field not in registry:
            errors.append(f"Missing required registry field: {field}")
    
    if errors:
        return False, errors
    
    # Validate states is a list
    if not isinstance(registry["states"], list):
        errors.append(f"states must be an array, got {type(registry['states']).__name__}")
        return False, errors
    
    # Validate each state in the registry
    state_ids = set()
    for i, state in enumerate(registry["states"]):
        is_valid, state_errors = validate_epistemic_state(state)
        if not is_valid:
            for error in state_errors:
                errors.append(f"State {i}: {error}")
        
        # Check for duplicate state_ids
        if "state_id" in state:
            if state["state_id"] in state_ids:
                errors.append(f"Duplicate state_id: {state['state_id']}")
            state_ids.add(state["state_id"])
    
    return len(errors) == 0, errors


def get_state_by_id(registry: Dict[str, Any], state_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific epistemic state from a registry by ID.
    
    Args:
        registry: The state registry dictionary.
        state_id: The state identifier to search for.
        
    Returns:
        The epistemic state dictionary if found, None otherwise.
    """
    for state in registry.get("states", []):
        if state.get("state_id") == state_id:
            return state
    return None
