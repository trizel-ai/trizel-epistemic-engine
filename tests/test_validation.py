"""
Test suite for TRIZEL epistemic engine validation utilities.
"""

import pytest
import json
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validation import (
    validate_state_id,
    validate_timestamp,
    validate_doi,
    validate_epistemic_status,
    validate_version,
    validate_epistemic_state,
    validate_registry,
    load_schema,
    load_state_registry,
    get_state_by_id,
)


class TestStateIdValidation:
    """Tests for state_id validation."""
    
    def test_valid_state_id(self):
        """Test valid state_id formats."""
        valid_ids = [
            "3i_atlas_001",
            "3i_atlas_042",
            "test_system_123",
            "a_000",
        ]
        for state_id in valid_ids:
            is_valid, error = validate_state_id(state_id)
            assert is_valid, f"Expected {state_id} to be valid, got error: {error}"
    
    def test_invalid_state_id(self):
        """Test invalid state_id formats."""
        invalid_ids = [
            "3i_atlas_01",  # Too few digits
            "3i_atlas",  # Missing sequence
            "3I_ATLAS_001",  # Uppercase not allowed
            "3i atlas_001",  # Space not allowed
            "3i-atlas-001",  # Hyphen in system name
        ]
        for state_id in invalid_ids:
            is_valid, error = validate_state_id(state_id)
            assert not is_valid, f"Expected {state_id} to be invalid"


class TestTimestampValidation:
    """Tests for timestamp validation."""
    
    def test_valid_timestamp(self):
        """Test valid ISO 8601 UTC timestamps."""
        valid_timestamps = [
            "2025-12-22T19:52:24Z",
            "2024-01-01T00:00:00Z",
            "2023-06-15T12:30:45Z",
        ]
        for timestamp in valid_timestamps:
            is_valid, error = validate_timestamp(timestamp)
            assert is_valid, f"Expected {timestamp} to be valid, got error: {error}"
    
    def test_invalid_timestamp(self):
        """Test invalid timestamp formats."""
        invalid_timestamps = [
            "2025-12-22T19:52:24",  # Missing Z
            "2025-12-22 19:52:24Z",  # Space instead of T
            "2025-13-22T19:52:24Z",  # Invalid month
            "2025-12-32T19:52:24Z",  # Invalid day
            "2025-12-22T25:52:24Z",  # Invalid hour
        ]
        for timestamp in invalid_timestamps:
            is_valid, error = validate_timestamp(timestamp)
            assert not is_valid, f"Expected {timestamp} to be invalid"


class TestDOIValidation:
    """Tests for DOI validation."""
    
    def test_valid_doi(self):
        """Test valid DOI formats."""
        valid_dois = [
            "10.5281/zenodo.1234567",
            "10.1000/xyz123",
            "10.1234/example.doi",
        ]
        for doi in valid_dois:
            is_valid, error = validate_doi(doi)
            assert is_valid, f"Expected {doi} to be valid, got error: {error}"
    
    def test_invalid_doi(self):
        """Test invalid DOI formats."""
        invalid_dois = [
            "doi:10.5281/zenodo.1234567",  # Prefix not allowed
            "10.5281",  # Missing suffix
            "not_a_doi",  # Wrong format
            "10.123/suffix",  # Prefix too short
        ]
        for doi in invalid_dois:
            is_valid, error = validate_doi(doi)
            assert not is_valid, f"Expected {doi} to be invalid"


class TestEpistemicStatusValidation:
    """Tests for epistemic_status validation."""
    
    def test_valid_status(self):
        """Test valid epistemic_status values."""
        valid_statuses = ["competing", "consensus", "rejected", "preliminary"]
        for status in valid_statuses:
            is_valid, error = validate_epistemic_status(status)
            assert is_valid, f"Expected {status} to be valid, got error: {error}"
    
    def test_invalid_status(self):
        """Test invalid epistemic_status values."""
        invalid_statuses = ["unknown", "active", "deprecated", ""]
        for status in invalid_statuses:
            is_valid, error = validate_epistemic_status(status)
            assert not is_valid, f"Expected {status} to be invalid"


class TestVersionValidation:
    """Tests for version validation."""
    
    def test_valid_version(self):
        """Test valid semantic version formats."""
        valid_versions = ["1.0.0", "2.1.3", "0.0.1", "10.20.30"]
        for version in valid_versions:
            is_valid, error = validate_version(version)
            assert is_valid, f"Expected {version} to be valid, got error: {error}"
    
    def test_invalid_version(self):
        """Test invalid version formats."""
        invalid_versions = ["1.0", "v1.0.0", "1.0.0-alpha", "1.0.0.0"]
        for version in invalid_versions:
            is_valid, error = validate_version(version)
            assert not is_valid, f"Expected {version} to be invalid"


class TestEpistemicStateValidation:
    """Tests for complete epistemic state validation."""
    
    def test_valid_minimal_state(self):
        """Test minimal valid epistemic state."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.1234567",
            "epistemic_status": "competing",
            "metadata": {}
        }
        is_valid, errors = validate_epistemic_state(state)
        assert is_valid, f"Expected valid state, got errors: {errors}"
    
    def test_valid_full_state(self):
        """Test fully populated valid epistemic state."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.1234567",
            "epistemic_status": "competing",
            "metadata": {
                "interpretation": "variant_A",
                "confidence": "medium"
            },
            "description": "Alternative interpretation",
            "tags": ["3I", "ATLAS"],
            "related_states": ["3i_atlas_002"],
            "version": "1.0.0"
        }
        is_valid, errors = validate_epistemic_state(state)
        assert is_valid, f"Expected valid state, got errors: {errors}"
    
    def test_missing_required_field(self):
        """Test state with missing required field."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            # Missing source_doi
            "epistemic_status": "competing",
            "metadata": {}
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("source_doi" in error for error in errors)
    
    def test_invalid_state_id_in_state(self):
        """Test state with invalid state_id."""
        state = {
            "state_id": "INVALID_ID",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.1234567",
            "epistemic_status": "competing",
            "metadata": {}
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("state_id" in error for error in errors)
    
    def test_description_too_long(self):
        """Test state with description exceeding max length."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.1234567",
            "epistemic_status": "competing",
            "metadata": {},
            "description": "x" * 1001  # Exceeds 1000 char limit
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("description" in error for error in errors)


class TestRegistryValidation:
    """Tests for registry validation."""
    
    def test_valid_empty_registry(self):
        """Test valid empty registry."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3i_atlas",
            "created": "2025-12-22T19:52:24Z",
            "states": []
        }
        is_valid, errors = validate_registry(registry)
        assert is_valid, f"Expected valid registry, got errors: {errors}"
    
    def test_valid_registry_with_states(self):
        """Test valid registry with states."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3i_atlas",
            "created": "2025-12-22T19:52:24Z",
            "states": [
                {
                    "state_id": "3i_atlas_001",
                    "timestamp": "2025-12-22T19:52:24Z",
                    "source_doi": "10.5281/zenodo.1234567",
                    "epistemic_status": "competing",
                    "metadata": {}
                }
            ]
        }
        is_valid, errors = validate_registry(registry)
        assert is_valid, f"Expected valid registry, got errors: {errors}"
    
    def test_missing_registry_field(self):
        """Test registry with missing required field."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3i_atlas",
            # Missing created
            "states": []
        }
        is_valid, errors = validate_registry(registry)
        assert not is_valid
        assert any("created" in error for error in errors)
    
    def test_duplicate_state_ids(self):
        """Test registry with duplicate state_ids."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3i_atlas",
            "created": "2025-12-22T19:52:24Z",
            "states": [
                {
                    "state_id": "3i_atlas_001",
                    "timestamp": "2025-12-22T19:52:24Z",
                    "source_doi": "10.5281/zenodo.1234567",
                    "epistemic_status": "competing",
                    "metadata": {}
                },
                {
                    "state_id": "3i_atlas_001",  # Duplicate
                    "timestamp": "2025-12-22T19:52:24Z",
                    "source_doi": "10.5281/zenodo.1234568",
                    "epistemic_status": "preliminary",
                    "metadata": {}
                }
            ]
        }
        is_valid, errors = validate_registry(registry)
        assert not is_valid
        assert any("Duplicate state_id" in error for error in errors)


class TestRegistryOperations:
    """Tests for registry operations."""
    
    def test_load_schema(self):
        """Test loading the JSON schema."""
        schema = load_schema()
        assert schema is not None
        assert "$schema" in schema
        assert schema["title"] == "Epistemic State Schema"
    
    def test_load_registry(self):
        """Test loading the 3I/ATLAS registry."""
        project_root = Path(__file__).parent.parent
        registry_path = project_root / "registry" / "3i_atlas_states.json"
        
        registry = load_state_registry(str(registry_path))
        assert registry is not None
        assert registry["system"] == "3i_atlas"
        assert isinstance(registry["states"], list)
    
    def test_get_state_by_id_not_found(self):
        """Test retrieving non-existent state."""
        registry = {
            "states": []
        }
        state = get_state_by_id(registry, "3i_atlas_999")
        assert state is None
    
    def test_get_state_by_id_found(self):
        """Test retrieving existing state."""
        registry = {
            "states": [
                {
                    "state_id": "3i_atlas_001",
                    "timestamp": "2025-12-22T19:52:24Z",
                    "source_doi": "10.5281/zenodo.1234567",
                    "epistemic_status": "competing",
                    "metadata": {}
                }
            ]
        }
        state = get_state_by_id(registry, "3i_atlas_001")
        assert state is not None
        assert state["state_id"] == "3i_atlas_001"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
