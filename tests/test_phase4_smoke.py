import unittest
from pathlib import Path

class TestPhase4Smoke(unittest.TestCase):
    def test_phase4_files_exist(self):
        repo = Path(__file__).resolve().parents[1]
        required = [
            repo / "docs" / "PHASE4_BUILD_PLAN.md",
            repo / "docs" / "PHASE4_EXECUTION_DIRECTIVE.md",
            repo / "docs" / "TCRL_CONTRACT.md",
            repo / "docs" / "PHASE4_PROJECT_TREE.md",
            repo / "tcrl" / "tcp" / "TEMPLATE_TCP.json",
            repo / "phase4" / "pipelines" / "run_phase4.py",
            repo / "phase4" / "methods" / "method_registry.json",
        ]
        for p in required:
            self.assertTrue(p.exists(), f"Missing required Phase-4 file: {p}")

if __name__ == "__main__":
    unittest.main()
