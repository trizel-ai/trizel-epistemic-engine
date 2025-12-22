"""
Test suite for TRIZEL epistemic state validation and determinism.

This module tests:
1. Schema validation of epistemic states
2. Registry validation
3. Determinism of loading and validation
4. File I/O operations

No analysis logic is tested - only structural validation.
"""

import json
import unittest
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.epistemic.io import load_json, save_json, validate_json_syntax, read_schema
from src.epistemic.registry import (
    load_registry,
    validate_registry,
    get_active_states,
    get_state_by_id
)
from src.epistemic.validate_states import (
    validate_state,
    validate_state_file,
    validate_all_states
)


class TestSchemaValidation(unittest.TestCase):
    """Test JSON schema validation of epistemic states."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.schema_path = cls.repo_root / "schema" / "epistemic_state.schema.json"
        cls.registry_path = cls.repo_root / "states" / "3I_ATLAS" / "state_registry.json"
        cls.states_dir = cls.repo_root / "states" / "3I_ATLAS" / "states"
    
    def test_schema_exists(self):
        """Test that schema file exists and is valid JSON."""
        self.assertTrue(self.schema_path.exists(), "Schema file not found")
        self.assertTrue(validate_json_syntax(self.schema_path), "Schema is not valid JSON")
    
    def test_schema_has_required_fields(self):
        """Test that schema has required JSON Schema fields."""
        schema = read_schema(self.schema_path)
        self.assertIn("$schema", schema, "Schema missing $schema field")
        self.assertIn("type", schema, "Schema missing type field")
        self.assertIn("required", schema, "Schema missing required field")
        self.assertIn("properties", schema, "Schema missing properties field")
    
    def test_schema_required_fields(self):
        """Test that schema defines all required state fields."""
        schema = read_schema(self.schema_path)
        required_fields = schema.get("required", [])
        
        expected_fields = [
            "state_id",
            "timestamp",
            "zenodo_doi",
            "description",
            "metadata",
            "interpretation",
            "data_references"
        ]
        
        for field in expected_fields:
            self.assertIn(field, required_fields, f"Required field {field} not in schema")


class TestRegistryValidation(unittest.TestCase):
    """Test registry validation and loading."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.registry_path = cls.repo_root / "states" / "3I_ATLAS" / "state_registry.json"
    
    def test_registry_exists(self):
        """Test that registry file exists."""
        self.assertTrue(self.registry_path.exists(), "Registry file not found")
    
    def test_registry_loads(self):
        """Test that registry can be loaded."""
        registry = load_registry(self.registry_path)
        self.assertIsInstance(registry, dict, "Registry is not a dictionary")
        self.assertIn("states", registry, "Registry missing 'states' field")
    
    def test_registry_validation(self):
        """Test registry validation."""
        errors = validate_registry(self.registry_path)
        self.assertEqual(len(errors), 0, f"Registry validation errors: {errors}")
    
    def test_registry_has_required_fields(self):
        """Test that registry has all required fields."""
        registry = load_registry(self.registry_path)
        required_fields = ["registry_version", "last_updated", "states"]
        
        for field in required_fields:
            self.assertIn(field, registry, f"Registry missing required field: {field}")
    
    def test_registry_states_is_list(self):
        """Test that states field is a list."""
        registry = load_registry(self.registry_path)
        self.assertIsInstance(registry["states"], list, "States field is not a list")
    
    def test_no_duplicate_state_ids(self):
        """Test that there are no duplicate state IDs in registry."""
        registry = load_registry(self.registry_path)
        state_ids = [state.get("state_id") for state in registry["states"] if isinstance(state, dict)]
        
        self.assertEqual(len(state_ids), len(set(state_ids)), "Duplicate state IDs found")
    
    def test_get_active_states(self):
        """Test getting active states from registry."""
        registry = load_registry(self.registry_path)
        active_states = get_active_states(registry)
        
        self.assertIsInstance(active_states, list, "Active states is not a list")
        for state in active_states:
            self.assertTrue(state.get("active", False), "Non-active state in active states list")
    
    def test_get_state_by_id(self):
        """Test retrieving a state by ID."""
        registry = load_registry(self.registry_path)
        
        # Get first state ID
        if registry["states"]:
            first_state_id = registry["states"][0].get("state_id")
            state = get_state_by_id(registry, first_state_id)
            self.assertIsNotNone(state, "State not found by ID")
            self.assertEqual(state["state_id"], first_state_id, "Wrong state returned")


class TestStateValidation(unittest.TestCase):
    """Test individual state file validation."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.schema_path = cls.repo_root / "schema" / "epistemic_state.schema.json"
        cls.registry_path = cls.repo_root / "states" / "3I_ATLAS" / "state_registry.json"
    
    def test_all_states_validate(self):
        """Test that all states in registry validate against schema."""
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        
        results = validate_all_states(
            self.registry_path,
            self.schema_path,
            verbose=False
        )
        
        self.assertGreater(results["total"], 0, "No states found to validate")
        self.assertEqual(
            results["invalid"],
            0,
            f"Invalid states found: {results['errors']}"
        )
    
    def test_placeholder_states_exist(self):
        """Test that all placeholder state files exist."""
        registry = load_registry(self.registry_path)
        
        for state_entry in registry["states"]:
            file_path = self.registry_path.parent / state_entry["file_path"]
            self.assertTrue(
                file_path.exists(),
                f"State file not found: {state_entry['file_path']}"
            )
    
    def test_placeholder_states_are_valid_json(self):
        """Test that all placeholder states are valid JSON."""
        registry = load_registry(self.registry_path)
        
        for state_entry in registry["states"]:
            file_path = self.registry_path.parent / state_entry["file_path"]
            self.assertTrue(
                validate_json_syntax(file_path),
                f"Invalid JSON in {state_entry['file_path']}"
            )


class TestDeterminism(unittest.TestCase):
    """Test determinism of loading and validation operations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.schema_path = cls.repo_root / "schema" / "epistemic_state.schema.json"
        cls.registry_path = cls.repo_root / "states" / "3I_ATLAS" / "state_registry.json"
    
    def test_registry_loading_is_deterministic(self):
        """Test that loading registry multiple times gives identical results."""
        registry1 = load_registry(self.registry_path)
        registry2 = load_registry(self.registry_path)
        
        self.assertEqual(
            json.dumps(registry1, sort_keys=True),
            json.dumps(registry2, sort_keys=True),
            "Registry loading is not deterministic"
        )
    
    def test_schema_loading_is_deterministic(self):
        """Test that loading schema multiple times gives identical results."""
        schema1 = read_schema(self.schema_path)
        schema2 = read_schema(self.schema_path)
        
        self.assertEqual(
            json.dumps(schema1, sort_keys=True),
            json.dumps(schema2, sort_keys=True),
            "Schema loading is not deterministic"
        )
    
    def test_validation_is_deterministic(self):
        """Test that validation produces consistent results."""
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        
        results1 = validate_all_states(
            self.registry_path,
            self.schema_path,
            verbose=False
        )
        results2 = validate_all_states(
            self.registry_path,
            self.schema_path,
            verbose=False
        )
        
        # Compare results (excluding timing-dependent fields)
        self.assertEqual(results1["total"], results2["total"], "Total count differs")
        self.assertEqual(results1["valid"], results2["valid"], "Valid count differs")
        self.assertEqual(results1["invalid"], results2["invalid"], "Invalid count differs")
        
        # Compare error messages
        self.assertEqual(
            set(results1["errors"].keys()),
            set(results2["errors"].keys()),
            "Error state IDs differ"
        )


class TestIOOperations(unittest.TestCase):
    """Test I/O utility functions."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.test_dir = cls.repo_root / "tests" / "test_data"
    
    def setUp(self):
        """Create test directory before each test."""
        self.test_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test files after each test."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_save_and_load_json(self):
        """Test saving and loading JSON files."""
        test_data = {
            "key1": "value1",
            "key2": 42,
            "key3": [1, 2, 3]
        }
        test_file = self.test_dir / "test.json"
        
        save_json(test_data, test_file)
        loaded_data = load_json(test_file)
        
        self.assertEqual(test_data, loaded_data, "Saved and loaded data differ")
    
    def test_save_json_creates_directory(self):
        """Test that save_json creates parent directories."""
        test_data = {"test": "data"}
        test_file = self.test_dir / "subdir" / "test.json"
        
        save_json(test_data, test_file)
        
        self.assertTrue(test_file.exists(), "File not created")
        self.assertTrue(test_file.parent.exists(), "Parent directory not created")
    
    def test_load_json_nonexistent_file(self):
        """Test that loading nonexistent file raises FileNotFoundError."""
        nonexistent_file = self.test_dir / "nonexistent.json"
        
        with self.assertRaises(FileNotFoundError):
            load_json(nonexistent_file)
    
    def test_validate_json_syntax(self):
        """Test JSON syntax validation."""
        valid_file = self.test_dir / "valid.json"
        save_json({"test": "data"}, valid_file)
        
        self.assertTrue(validate_json_syntax(valid_file), "Valid JSON marked as invalid")
        
        # Test invalid JSON
        invalid_file = self.test_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{invalid json")
        
        self.assertFalse(validate_json_syntax(invalid_file), "Invalid JSON marked as valid")


class TestPlaceholderStates(unittest.TestCase):
    """Test specific properties of placeholder states."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent.parent
        cls.registry_path = cls.repo_root / "states" / "3I_ATLAS" / "state_registry.json"
    
    def test_placeholder_states_have_correct_ids(self):
        """Test that placeholder states have expected IDs."""
        registry = load_registry(self.registry_path)
        state_ids = [s.get("state_id") for s in registry["states"]]
        
        expected_ids = [
            "2025-12-22_neutral_baseline",
            "2025-12-22_placeholder_bayesian",
            "2025-12-22_placeholder_frequentist"
        ]
        
        for expected_id in expected_ids:
            self.assertIn(expected_id, state_ids, f"Expected state ID not found: {expected_id}")
    
    def test_placeholder_states_are_active(self):
        """Test that all placeholder states are marked as active."""
        registry = load_registry(self.registry_path)
        
        for state in registry["states"]:
            self.assertTrue(
                state.get("active", False),
                f"State {state.get('state_id')} is not active"
            )
    
    def test_placeholder_states_have_valid_zenodo_dois(self):
        """Test that placeholder states have valid DOI format."""
        registry = load_registry(self.registry_path)
        doi_pattern = r"^10\.5281/zenodo\.\d+$"
        
        import re
        
        for state_entry in registry["states"]:
            file_path = self.registry_path.parent / state_entry["file_path"]
            state_data = load_json(file_path)
            
            doi = state_data.get("zenodo_doi", "")
            self.assertIsNotNone(
                re.match(doi_pattern, doi),
                f"Invalid DOI format in {state_entry['state_id']}: {doi}"
            )


def run_tests():
    """Run all tests and return exit code."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
