from pathlib import Path
import pytest

from src.phase4.validate.validate_json import validate_or_raise

REPO_ROOT = Path(__file__).resolve().parents[1]


def require_file(path: str) -> Path:
    p = REPO_ROOT / path
    assert p.exists() and p.is_file(), f"Missing required file: {path}"
    return p


def test_tcrl_tcp_schema_validation():
    validate_or_raise(
        require_file("tcrl/tcp/TEMPLATE_TCP.json"),
        require_file("schema/tcrl/tcp.schema.json")
    )


def test_phase4_method_registry_validation():
    validate_or_raise(
        require_file("phase4/methods/method_registry.json"),
        require_file("schema/phase4/method_registry.schema.json")
    )


def test_validation_determinism():
    schema = require_file("schema/tcrl/tcp.schema.json")
    instance = require_file("tcrl/tcp/TEMPLATE_TCP.json")

    try:
        validate_or_raise(instance, schema)
        validate_or_raise(instance, schema)
    except ValueError as e1:
        with pytest.raises(ValueError) as e2:
            validate_or_raise(instance, schema)
        assert str(e1) == str(e2.value)
