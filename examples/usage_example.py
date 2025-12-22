"""
Example usage of the TRIZEL epistemic engine validation utilities.

This script demonstrates how to:
1. Load and validate the JSON schema
2. Load and validate the state registry
3. Create and validate epistemic states
4. Add states to a registry (in-memory only)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation import (
    validate_epistemic_state,
    validate_registry,
    load_schema,
    load_state_registry,
    get_state_by_id,
)


def main():
    print("=" * 70)
    print("TRIZEL Epistemic Engine - Usage Examples")
    print("=" * 70)
    
    # Example 1: Load and display schema
    print("\n1. Loading JSON Schema")
    print("-" * 70)
    schema = load_schema()
    print(f"   Schema Title: {schema['title']}")
    print(f"   Required Fields: {schema['required']}")
    
    # Example 2: Load registry
    print("\n2. Loading 3I/ATLAS State Registry")
    print("-" * 70)
    registry = load_state_registry("registry/3i_atlas_states.json")
    print(f"   System: {registry['system']}")
    print(f"   Registry Version: {registry['registry_version']}")
    print(f"   Current State Count: {len(registry['states'])}")
    
    # Example 3: Create and validate a minimal epistemic state
    print("\n3. Validating a Minimal Epistemic State")
    print("-" * 70)
    minimal_state = {
        "state_id": "3i_atlas_001",
        "timestamp": "2025-12-22T19:52:24Z",
        "source_doi": "10.5281/zenodo.1234567",
        "epistemic_status": "competing",
        "metadata": {}
    }
    is_valid, errors = validate_epistemic_state(minimal_state)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Example 4: Create and validate a full epistemic state
    print("\n4. Validating a Full Epistemic State")
    print("-" * 70)
    full_state = {
        "state_id": "3i_atlas_002",
        "timestamp": "2025-12-22T20:00:00Z",
        "source_doi": "10.5281/zenodo.1234568",
        "epistemic_status": "preliminary",
        "metadata": {
            "interpretation": "variant_B",
            "confidence": "high",
            "reviewer": "research_team_alpha"
        },
        "description": "Preliminary interpretation of 3I/ATLAS spectroscopic data",
        "tags": ["3I", "ATLAS", "spectroscopy", "preliminary"],
        "related_states": ["3i_atlas_001"],
        "version": "1.0.0"
    }
    is_valid, errors = validate_epistemic_state(full_state)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Example 5: Demonstrate validation failure
    print("\n5. Example of Invalid State (Missing Required Field)")
    print("-" * 70)
    invalid_state = {
        "state_id": "3i_atlas_003",
        "timestamp": "2025-12-22T20:00:00Z",
        # Missing source_doi (required)
        "epistemic_status": "competing",
        "metadata": {}
    }
    is_valid, errors = validate_epistemic_state(invalid_state)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Example 6: Validate registry with states
    print("\n6. Validating Registry with Multiple States")
    print("-" * 70)
    test_registry = {
        "registry_version": "1.0.0",
        "system": "3i_atlas",
        "created": "2025-12-22T19:52:24Z",
        "states": [minimal_state, full_state]
    }
    is_valid, errors = validate_registry(test_registry)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Example 7: Search for a state by ID
    print("\n7. Searching for State by ID")
    print("-" * 70)
    state = get_state_by_id(test_registry, "3i_atlas_002")
    if state:
        print(f"   Found: {state['state_id']}")
        print(f"   Status: {state['epistemic_status']}")
        print(f"   Description: {state.get('description', 'N/A')}")
    else:
        print("   State not found")
    
    print("\n" + "=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    
    # Important notes
    print("\n📝 IMPORTANT NOTES:")
    print("-" * 70)
    print("• This engine does NOT fetch data from DOIs (read-only references)")
    print("• This engine does NOT rank or prefer interpretations")
    print("• This engine does NOT perform simulations or numerical analysis")
    print("• All operations are deterministic and audit-safe")
    print("• Registry modifications should be done carefully with version control")
    print("=" * 70)


if __name__ == "__main__":
    main()
