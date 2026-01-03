from pathlib import Path
from typing import List
from jsonschema import Draft202012Validator
import json


def lint_directive(instance_path: str | Path, schema_path: str | Path) -> List[str]:
    instance = json.loads(Path(instance_path).read_text(encoding="utf-8"))
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))

    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda e: (list(e.absolute_path), e.message)
    )

    return [
        f"/{'/'.join(str(p) for p in e.absolute_path)}: {e.message}"
        if e.absolute_path else f"/: {e.message}"
        for e in errors
    ]
