from pathlib import Path
from jsonschema import Draft202012Validator
import json

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_directive_schema_self_consistency():
    schema_path = REPO_ROOT / "schema/phase4/directive.schema.json"
    assert schema_path.exists()

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
