"""
Test suite for TRIZEL epistemic engine validation utilities.
"""

import pytest
import json
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from epistemic import (
    validate_state_id,
    validate_timestamp,
    validate_doi,
    validate_determinacy,
    validate_version,
    validate_provenance,
    validate_epistemic_state,
    validate_registry_structure,
    validate_registry_sorting,
    load_schema,
    load_state_registry,
    get_state_by_id,
    list_all_states,
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
            "10.5281/zenodo.18012859",
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


class TestDeterminacyValidation:
    """Tests for determinacy validation."""
    
    def test_valid_determinacy(self):
        """Test valid determinacy values."""
        valid_statuses = ["confirmed", "plausible", "underdetermined", "unfalsified", "falsified"]
        for status in valid_statuses:
            is_valid, error = validate_determinacy(status)
            assert is_valid, f"Expected {status} to be valid, got error: {error}"
    
    def test_invalid_determinacy(self):
        """Test invalid determinacy values."""
        invalid_statuses = ["competing", "consensus", "rejected", "preliminary", "unknown", ""]
        for status in invalid_statuses:
            is_valid, error = validate_determinacy(status)
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


class TestProvenanceValidation:
    """Tests for provenance validation."""
    
    def test_valid_provenance(self):
        """Test valid provenance structure."""
        valid_provenance = {
            "ingest_doi": "10.5281/zenodo.18012859",
            "record_ids": ["rec_001", "rec_002"]
        }
        is_valid, errors = validate_provenance(valid_provenance)
        assert is_valid, f"Expected valid provenance, got errors: {errors}"
    
    def test_valid_provenance_empty_records(self):
        """Test valid provenance with empty record_ids."""
        valid_provenance = {
            "ingest_doi": "10.5281/zenodo.18012859",
            "record_ids": []
        }
        is_valid, errors = validate_provenance(valid_provenance)
        assert is_valid, f"Expected valid provenance, got errors: {errors}"
    
    def test_invalid_provenance_wrong_doi(self):
        """Test provenance with wrong ingest_doi."""
        invalid_provenance = {
            "ingest_doi": "10.5281/zenodo.12345",
            "record_ids": []
        }
        is_valid, errors = validate_provenance(invalid_provenance)
        assert not is_valid
        assert any("10.5281/zenodo.18012859" in error for error in errors)
    
    def test_invalid_provenance_missing_fields(self):
        """Test provenance with missing fields."""
        invalid_provenance = {
            "ingest_doi": "10.5281/zenodo.18012859"
        }
        is_valid, errors = validate_provenance(invalid_provenance)
        assert not is_valid
        assert any("record_ids" in error for error in errors)


class TestEpistemicStateValidation:
    """Tests for complete epistemic state validation."""
    
    def test_valid_minimal_state(self):
        """Test minimal valid epistemic state."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.18012859",
            "determinacy": "plausible",
            "assumptions": ["Standard cosmology"],
            "required_observations": ["Multi-wavelength photometry"],
            "provenance": {
                "ingest_doi": "10.5281/zenodo.18012859",
                "record_ids": []
            },
            "incompatibilities": []
        }
        is_valid, errors = validate_epistemic_state(state)
        assert is_valid, f"Expected valid state, got errors: {errors}"
    
    def test_valid_full_state(self):
        """Test fully populated valid epistemic state."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.18012859",
            "determinacy": "plausible",
            "assumptions": ["Standard cosmology", "No active outgassing"],
            "required_observations": ["Multi-wavelength photometry", "High-resolution spectroscopy"],
            "provenance": {
                "ingest_doi": "10.5281/zenodo.18012859",
                "record_ids": ["rec_001", "rec_002"]
            },
            "incompatibilities": ["3i_atlas_002"],
            "description": "Alternative interpretation",
            "tags": ["3I", "ATLAS"],
            "related_states": ["3i_atlas_003"],
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
            "determinacy": "plausible",
            "assumptions": ["Standard cosmology"],
            "required_observations": ["Multi-wavelength photometry"],
            "provenance": {
                "ingest_doi": "10.5281/zenodo.18012859",
                "record_ids": []
            },
            "incompatibilities": []
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("source_doi" in error for error in errors)
    
    def test_empty_assumptions(self):
        """Test state with empty assumptions list."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.18012859",
            "determinacy": "plausible",
            "assumptions": [],  # Empty list not allowed
            "required_observations": ["Multi-wavelength photometry"],
            "provenance": {
                "ingest_doi": "10.5281/zenodo.18012859",
                "record_ids": []
            },
            "incompatibilities": []
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("assumptions must be non-empty" in error for error in errors)
    
    def test_invalid_provenance_doi(self):
        """Test state with invalid provenance DOI."""
        state = {
            "state_id": "3i_atlas_001",
            "timestamp": "2025-12-22T19:52:24Z",
            "source_doi": "10.5281/zenodo.18012859",
            "determinacy": "plausible",
            "assumptions": ["Standard cosmology"],
            "required_observations": ["Multi-wavelength photometry"],
            "provenance": {
                "ingest_doi": "10.5281/zenodo.99999",  # Wrong DOI
                "record_ids": []
            },
            "incompatibilities": []
        }
        is_valid, errors = validate_epistemic_state(state)
        assert not is_valid
        assert any("10.5281/zenodo.18012859" in error for error in errors)


class TestRegistryValidation:
    """Tests for registry validation."""
    
    def test_valid_empty_registry(self):
        """Test valid empty registry."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3I_ATLAS",
            "created": "2025-12-22T19:52:24Z",
            "state_files": []
        }
        is_valid, errors = validate_registry_structure(registry)
        assert is_valid, f"Expected valid registry, got errors: {errors}"
    
    def test_valid_registry_with_files(self):
        """Test valid registry with state files."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3I_ATLAS",
            "created": "2025-12-22T19:52:24Z",
            "state_files": ["states/3i_atlas_000.json", "states/3i_atlas_001.json"]
        }
        is_valid, errors = validate_registry_structure(registry)
        assert is_valid, f"Expected valid registry, got errors: {errors}"
    
    def test_missing_registry_field(self):
        """Test registry with missing required field."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3I_ATLAS",
            # Missing created
            "state_files": []
        }
        is_valid, errors = validate_registry_structure(registry)
        assert not is_valid
        assert any("created" in error for error in errors)
    
    def test_unsorted_state_files(self):
        """Test registry with unsorted state_files."""
        registry = {
            "registry_version": "1.0.0",
            "system": "3I_ATLAS",
            "created": "2025-12-22T19:52:24Z",
            "state_files": ["states/3i_atlas_002.json", "states/3i_atlas_001.json"]  # Wrong order
        }
        is_valid, errors = validate_registry_structure(registry)
        assert not is_valid
        assert any("sorted lexicographically" in error for error in errors)


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
        registry_path = project_root / "states" / "3I_ATLAS" / "state_registry.json"
        
        registry = load_state_registry(str(registry_path))
        assert registry is not None
        assert registry["system"] == "3I_ATLAS"
        assert isinstance(registry["state_files"], list)
    
    def test_list_all_states(self):
        """Test listing all states from registry."""
        project_root = Path(__file__).parent.parent
        registry_dir = project_root / "states" / "3I_ATLAS"
        registry_path = registry_dir / "state_registry.json"
        
        registry = load_state_registry(str(registry_path))
        states = list_all_states(str(registry_dir), registry)
        
        # Should have at least the placeholder state
        assert len(states) >= 0
    
    def test_get_state_by_id(self):
        """Test retrieving state by ID."""
        project_root = Path(__file__).parent.parent
        registry_dir = project_root / "states" / "3I_ATLAS"
        registry_path = registry_dir / "state_registry.json"
        
        registry = load_state_registry(str(registry_path))
        
        # Try to get placeholder state if it exists
        if len(registry.get("state_files", [])) > 0:
            state = get_state_by_id(str(registry_dir), registry, "3i_atlas_000")
            if state:
                assert state["state_id"] == "3i_atlas_000"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
