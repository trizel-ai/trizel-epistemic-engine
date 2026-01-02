import unittest
from pathlib import Path

FORBIDDEN_PHRASES = [
    "superior",
    "validated theory",
    "Theory of Everything",
    "STOE",
    "ToE",
]

class TestPhase4Contract(unittest.TestCase):
    def test_no_forbidden_phrases_in_phase4_directive(self):
        repo = Path(__file__).resolve().parents[1]
        directive = (repo / "docs" / "PHASE4_EXECUTION_DIRECTIVE.md").read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PHRASES:
            self.assertNotIn(phrase, directive)

if __name__ == "__main__":
    unittest.main()
