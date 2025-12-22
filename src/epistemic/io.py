"""
I/O utilities for TRIZEL epistemic engine.

This module provides file loading and saving operations for epistemic states and registries.
No data ingestion, interpretation ranking, or numerical analysis is performed here.
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file from disk.
    
    Args:
        file_path: Path to JSON file.
        
    Returns:
        Dictionary containing the JSON data.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If file is invalid JSON.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_schema(schema_path: str = None) -> Dict[str, Any]:
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
        # Default to schema/epistemic_state.schema.json relative to project root
        project_root = Path(__file__).parent.parent.parent
        schema_path = project_root / "schema" / "epistemic_state.schema.json"
    else:
        schema_path = Path(schema_path)
    
    return load_json(str(schema_path))


def load_state(state_path: str) -> Dict[str, Any]:
    """
    Load an individual epistemic state from disk.
    
    Args:
        state_path: Path to state JSON file.
        
    Returns:
        Dictionary containing the epistemic state.
        
    Raises:
        FileNotFoundError: If state file doesn't exist.
        json.JSONDecodeError: If state is invalid JSON.
    """
    return load_json(state_path)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save a dictionary as JSON to disk.
    
    Args:
        data: Dictionary to save.
        file_path: Path to output file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
