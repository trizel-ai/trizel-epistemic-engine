"""
State Validation for TRIZEL Epistemic Engine

Validates epistemic state files against JSON Schema.
No analysis logic - only structural validation.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Union, Tuple

try:
    import jsonschema
    from jsonschema import Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .io import load_json, read_schema


def validate_state(
    state_data: Dict[str, Any],
    schema: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Validate a state dictionary against a JSON schema.
    
    Args:
        state_data: State data to validate
        schema: JSON Schema to validate against
        
    Returns:
        Tuple of (is_valid: bool, errors: List[str])
    """
    if not JSONSCHEMA_AVAILABLE:
        return False, ["jsonschema package not installed. Install with: pip install jsonschema"]
    
    validator = Draft7Validator(schema)
    errors = []
    
    for error in validator.iter_errors(state_data):
        error_path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"{error_path}: {error.message}")
    
    return len(errors) == 0, errors


def validate_state_file(
    state_file: Union[str, Path],
    schema_file: Union[str, Path]
) -> Tuple[bool, List[str]]:
    """
    Validate a state file against a schema file.
    
    Args:
        state_file: Path to the state JSON file
        schema_file: Path to the schema JSON file
        
    Returns:
        Tuple of (is_valid: bool, errors: List[str])
    """
    errors = []
    
    # Load state file
    try:
        state_data = load_json(state_file)
    except FileNotFoundError:
        return False, [f"State file not found: {state_file}"]
    except Exception as e:
        return False, [f"Failed to load state file: {e}"]
    
    # Load schema file
    try:
        schema = read_schema(schema_file)
    except FileNotFoundError:
        return False, [f"Schema file not found: {schema_file}"]
    except Exception as e:
        return False, [f"Failed to load schema file: {e}"]
    
    # Validate
    return validate_state(state_data, schema)


def validate_all_states(
    registry_path: Union[str, Path],
    schema_path: Union[str, Path],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Validate all states in a registry against the schema.
    
    Args:
        registry_path: Path to state_registry.json
        schema_path: Path to epistemic_state.schema.json
        verbose: Whether to print progress messages
        
    Returns:
        Dictionary with validation results:
        {
            "total": int,
            "valid": int,
            "invalid": int,
            "errors": Dict[str, List[str]]  # state_id -> error messages
        }
    """
    from .registry import load_registry
    
    results = {
        "total": 0,
        "valid": 0,
        "invalid": 0,
        "errors": {}
    }
    
    registry_path = Path(registry_path)
    schema_path = Path(schema_path)
    
    # Load registry
    try:
        registry = load_registry(registry_path)
    except Exception as e:
        if verbose:
            print(f"Error loading registry: {e}", file=sys.stderr)
        return results
    
    # Load schema
    try:
        schema = read_schema(schema_path)
    except Exception as e:
        if verbose:
            print(f"Error loading schema: {e}", file=sys.stderr)
        return results
    
    # Validate each state
    if "states" not in registry:
        if verbose:
            print("No states found in registry", file=sys.stderr)
        return results
    
    for state_entry in registry["states"]:
        if not isinstance(state_entry, dict):
            continue
        
        state_id = state_entry.get("state_id", "unknown")
        file_path = state_entry.get("file_path")
        
        if not file_path:
            results["total"] += 1
            results["invalid"] += 1
            results["errors"][state_id] = ["Missing file_path in registry"]
            continue
        
        # Construct full path relative to registry
        full_path = registry_path.parent / file_path
        
        if verbose:
            print(f"Validating {state_id}...")
        
        results["total"] += 1
        
        is_valid, errors = validate_state_file(full_path, schema_path)
        
        if is_valid:
            results["valid"] += 1
            if verbose:
                print(f"  ✓ Valid")
        else:
            results["invalid"] += 1
            results["errors"][state_id] = errors
            if verbose:
                print(f"  ✗ Invalid:")
                for error in errors:
                    print(f"    - {error}")
    
    return results


def main():
    """
    Command-line interface for state validation.
    
    Usage:
        python -m src.epistemic.validate_states
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate TRIZEL epistemic state files"
    )
    parser.add_argument(
        "--registry",
        default="states/3I_ATLAS/state_registry.json",
        help="Path to state registry file"
    )
    parser.add_argument(
        "--schema",
        default="schema/epistemic_state.schema.json",
        help="Path to JSON schema file"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )
    
    args = parser.parse_args()
    
    if not JSONSCHEMA_AVAILABLE:
        print("Error: jsonschema package not installed", file=sys.stderr)
        print("Install with: pip install jsonschema", file=sys.stderr)
        sys.exit(1)
    
    results = validate_all_states(
        args.registry,
        args.schema,
        verbose=not args.quiet
    )
    
    # Print summary
    print("\n" + "="*50)
    print("Validation Summary")
    print("="*50)
    print(f"Total states: {results['total']}")
    print(f"Valid: {results['valid']}")
    print(f"Invalid: {results['invalid']}")
    
    if results['invalid'] > 0:
        print("\nStates with errors:")
        for state_id, errors in results['errors'].items():
            print(f"\n  {state_id}:")
            for error in errors:
                print(f"    - {error}")
        sys.exit(1)
    else:
        print("\n✓ All states valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
