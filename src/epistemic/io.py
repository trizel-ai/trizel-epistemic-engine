"""
I/O Utilities for TRIZEL Epistemic Engine

Provides JSON loading and saving with validation.
No analysis logic - pure I/O operations.
"""

import json
from pathlib import Path
from typing import Any, Dict, Union


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the JSON data
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {file_path}: {e.msg}",
                e.doc,
                e.pos
            )
    
    return data


def save_json(
    data: Dict[str, Any],
    file_path: Union[str, Path],
    indent: int = 2,
    sort_keys: bool = True
) -> None:
    """
    Save a dictionary as a JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to save the JSON file
        indent: Number of spaces for indentation (default: 2)
        sort_keys: Whether to sort keys alphabetically (default: True)
        
    Raises:
        TypeError: If data is not serializable to JSON
        OSError: If unable to write to file
    """
    file_path = Path(file_path)
    
    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
        # Add newline at end of file
        f.write('\n')


def validate_json_syntax(file_path: Union[str, Path]) -> bool:
    """
    Validate that a file contains valid JSON syntax.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        True if valid JSON, False otherwise
    """
    try:
        load_json(file_path)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def read_schema(schema_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a JSON Schema file.
    
    Args:
        schema_path: Path to the JSON Schema file
        
    Returns:
        Dictionary containing the schema
        
    Raises:
        FileNotFoundError: If schema file not found
        json.JSONDecodeError: If schema file is not valid JSON
    """
    return load_json(schema_path)
