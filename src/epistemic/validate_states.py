"""
State validation for TRIZEL epistemic engine.

This module provides validation functions for epistemic states.
No data ingestion, interpretation ranking, or numerical analysis is performed here.
"""

import re
from typing import Tuple, Dict, List, Any, Optional
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


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


def validate_determinacy(determinacy: str) -> Tuple[bool, Optional[str]]:
    """
    Validate determinacy value.
    
    Allowed values: confirmed, plausible, underdetermined, unfalsified, falsified
    
    Args:
        determinacy: The determinacy status to validate.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    allowed = {"confirmed", "plausible", "underdetermined", "unfalsified", "falsified"}
    if determinacy not in allowed:
        return False, f"determinacy '{determinacy}' not in allowed values: {allowed}"
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


def validate_provenance(provenance: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate provenance structure.
    
    Args:
        provenance: The provenance dictionary to validate.
        
    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    
    # Check required fields
    if "ingest_doi" not in provenance:
        errors.append("Missing required provenance field: ingest_doi")
    elif provenance["ingest_doi"] != "10.5281/zenodo.18012859":
        errors.append(f"provenance.ingest_doi must be '10.5281/zenodo.18012859', got '{provenance['ingest_doi']}'")
    
    if "record_ids" not in provenance:
        errors.append("Missing required provenance field: record_ids")
    elif not isinstance(provenance["record_ids"], list):
        errors.append(f"provenance.record_ids must be a list, got {type(provenance['record_ids']).__name__}")
    
    return len(errors) == 0, errors


def validate_epistemic_state(state: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    """
    Validate an epistemic state against the schema and business rules.
    
    Args:
        state: Dictionary representing an epistemic state.
        schema: Optional JSON schema. If None, validation is performed without schema.
        
    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors = []
    
    # Check required fields
    required_fields = [
        "state_id", "timestamp", "source_doi", "determinacy",
        "assumptions", "required_observations", "provenance", "incompatibilities"
    ]
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
    
    # Validate determinacy
    is_valid, error = validate_determinacy(state["determinacy"])
    if not is_valid:
        errors.append(error)
    
    # Validate assumptions (non-empty list of strings)
    if not isinstance(state["assumptions"], list):
        errors.append(f"assumptions must be a list, got {type(state['assumptions']).__name__}")
    elif len(state["assumptions"]) == 0:
        errors.append("assumptions must be non-empty")
    elif not all(isinstance(a, str) for a in state["assumptions"]):
        errors.append("All assumptions must be strings")
    
    # Validate required_observations (non-empty list of strings)
    if not isinstance(state["required_observations"], list):
        errors.append(f"required_observations must be a list, got {type(state['required_observations']).__name__}")
    elif len(state["required_observations"]) == 0:
        errors.append("required_observations must be non-empty")
    elif not all(isinstance(o, str) for o in state["required_observations"]):
        errors.append("All required_observations must be strings")
    
    # Validate provenance
    if not isinstance(state["provenance"], dict):
        errors.append(f"provenance must be a dictionary, got {type(state['provenance']).__name__}")
    else:
        is_valid, prov_errors = validate_provenance(state["provenance"])
        if not is_valid:
            errors.extend(prov_errors)
    
    # Validate incompatibilities (list of state IDs)
    if not isinstance(state["incompatibilities"], list):
        errors.append(f"incompatibilities must be a list, got {type(state['incompatibilities']).__name__}")
    else:
        for incomp_id in state["incompatibilities"]:
            if not isinstance(incomp_id, str):
                errors.append(f"incompatibilities must contain strings, got {type(incomp_id).__name__}")
            else:
                is_valid, error = validate_state_id(incomp_id)
                if not is_valid:
                    errors.append(f"Invalid incompatibility state ID: {error}")
    
    # Validate optional fields if present
    if "description" in state:
        if not isinstance(state["description"], str):
            errors.append(f"description must be a string, got {type(state['description']).__name__}")
        elif len(state["description"]) > 1000:
            errors.append(f"description exceeds maximum length of 1000 characters")
    
    if "tags" in state:
        if not isinstance(state["tags"], list):
            errors.append(f"tags must be a list, got {type(state['tags']).__name__}")
        elif not all(isinstance(tag, str) for tag in state["tags"]):
            errors.append("All tags must be strings")
    
    if "related_states" in state:
        if not isinstance(state["related_states"], list):
            errors.append(f"related_states must be a list, got {type(state['related_states']).__name__}")
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
