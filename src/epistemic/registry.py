"""
Registry Loader for TRIZEL Epistemic Engine

Loads and validates state registries.
No analysis logic - only registry management.
"""

from pathlib import Path
from typing import Dict, List, Any, Union

from .io import load_json


def load_registry(registry_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a state registry file.
    
    Args:
        registry_path: Path to the state_registry.json file
        
    Returns:
        Dictionary containing the registry data
        
    Raises:
        FileNotFoundError: If registry file not found
        json.JSONDecodeError: If registry file is not valid JSON
        ValueError: If registry structure is invalid
    """
    registry = load_json(registry_path)
    
    # Basic validation
    if "states" not in registry:
        raise ValueError(f"Registry missing 'states' field: {registry_path}")
    
    if not isinstance(registry["states"], list):
        raise ValueError(f"Registry 'states' must be a list: {registry_path}")
    
    return registry


def validate_registry(registry_path: Union[str, Path]) -> List[str]:
    """
    Validate a state registry and return list of issues.
    
    Args:
        registry_path: Path to the state_registry.json file
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    registry_path = Path(registry_path)
    
    try:
        registry = load_json(registry_path)
    except FileNotFoundError:
        return [f"Registry file not found: {registry_path}"]
    except Exception as e:
        return [f"Failed to load registry: {e}"]
    
    # Check required fields
    required_fields = ["registry_version", "last_updated", "states"]
    for field in required_fields:
        if field not in registry:
            errors.append(f"Missing required field: {field}")
    
    # Validate states array
    if "states" in registry:
        if not isinstance(registry["states"], list):
            errors.append("Field 'states' must be an array")
        else:
            # Check for duplicate state_ids
            state_ids = []
            for i, state_entry in enumerate(registry["states"]):
                if not isinstance(state_entry, dict):
                    errors.append(f"State entry {i} is not an object")
                    continue
                
                # Check required fields in state entry
                if "state_id" not in state_entry:
                    errors.append(f"State entry {i} missing 'state_id'")
                else:
                    state_id = state_entry["state_id"]
                    if state_id in state_ids:
                        errors.append(f"Duplicate state_id: {state_id}")
                    state_ids.append(state_id)
                
                if "file_path" not in state_entry:
                    errors.append(f"State entry {i} missing 'file_path'")
                
                if "active" not in state_entry:
                    errors.append(f"State entry {i} missing 'active' field")
                elif not isinstance(state_entry["active"], bool):
                    errors.append(f"State entry {i} 'active' must be boolean")
                
                # Check if file exists
                if "file_path" in state_entry:
                    file_path = registry_path.parent / state_entry["file_path"]
                    if not file_path.exists():
                        errors.append(f"State file not found: {state_entry['file_path']}")
    
    return errors


def get_active_states(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get all active states from a registry.
    
    Args:
        registry: Registry dictionary
        
    Returns:
        List of active state entries
    """
    if "states" not in registry:
        return []
    
    return [
        state for state in registry["states"]
        if isinstance(state, dict) and state.get("active", False)
    ]


def get_state_by_id(registry: Dict[str, Any], state_id: str) -> Union[Dict[str, Any], None]:
    """
    Get a specific state entry by its state_id.
    
    Args:
        registry: Registry dictionary
        state_id: The state_id to search for
        
    Returns:
        State entry dictionary if found, None otherwise
    """
    if "states" not in registry:
        return None
    
    for state in registry["states"]:
        if isinstance(state, dict) and state.get("state_id") == state_id:
            return state
    
    return None
