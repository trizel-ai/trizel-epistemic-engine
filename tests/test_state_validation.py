import unittest
from pathlib import Path

from src.epistemic.registry import load_registry
from src.epistemic.validate_states import validate_repo


class TestDeterministicGates(unittest.TestCase):
    def test_registry_sorted_required(self):
        repo_root = Path(__file__).resolve().parents[1]
        registry_path = repo_root / "states" / "3I_ATLAS" / "state_registry.json"
        data = load_registry(registry_path)
        self.assertEqual(data, sorted(data))

    def test_repo_validates(self):
        repo_root = Path(__file__).resolve().parents[1]
        validate_repo(repo_root)


if __name__ == "__main__":
    unittest.main()
