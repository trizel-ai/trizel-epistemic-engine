from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class ValidationIssue:
    json_path: str
    message: str


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_instance_against_schema(
    instance: Any,
    schema: dict[str, Any],
) -> List[ValidationIssue]:
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda e: (list(e.absolute_path), e.message)
    )

    issues: List[ValidationIssue] = []
    for e in errors:
        path = "/" + "/".join(str(p) for p in e.absolute_path) if e.absolute_path else "/"
        issues.append(ValidationIssue(json_path=path, message=e.message))

    return sorted(issues, key=lambda x: (x.json_path, x.message))


def validate_json_file(instance_path: str | Path, schema_path: str | Path) -> List[ValidationIssue]:
    instance = _load_json(Path(instance_path))
    schema = _load_json(Path(schema_path))
    return validate_instance_against_schema(instance, schema)


def validate_or_raise(instance_path: str | Path, schema_path: str | Path) -> None:
    issues = validate_json_file(instance_path, schema_path)
    if issues:
        lines = [f"Validation failed ({len(issues)} issues):"]
        for i, issue in enumerate(issues, start=1):
            lines.append(f"{i:02d}. {issue.json_path}: {issue.message}")
        raise ValueError("\n".join(lines))
