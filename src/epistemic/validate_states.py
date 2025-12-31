from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

from .io import read_json
from .registry import load_registry

LOCKED_INGEST_DOI = "10.5281/zenodo.18012859"

ALLOWED_DETERMINACY = {
    "confirmed",
    "plausible",
    "underdetermined",
    "unfalsified",
    "falsified",
}

FORBIDDEN_TOP_LEVEL_KEYS = {
    "timestamp",
    "source_doi",
    "epistemic_status",
    "interpretation",
}


def _require_non_empty_str(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string.")


def _require_non_empty_str_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or len(value) == 0:
        raise ValueError(f"{field} must be a non-empty list.")
    if not all(isinstance(x, str) and x.strip() for x in value):
        raise ValueError(f"{field} must be a list of non-empty strings.")


def _require_str_list(value: Any, field: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list.")
    if not all(isinstance(x, str) and x.strip() for x in value):
        raise ValueError(f"{field} must be a list of non-empty strings.")


def validate_state_object(obj: Dict[str, Any]) -> None:
    if not isinstance(obj, dict):
        raise ValueError("State file must contain a JSON object.")

    for k in FORBIDDEN_TOP_LEVEL_KEYS:
        if k in obj:
            raise ValueError(f"Forbidden top-level key present: {k}")

    required = [
        "state_id",
        "label",
        "assumptions",
        "required_observations",
        "incompatibilities",
        "determinacy",
        "provenance",
    ]
    for k in required:
        if k not in obj:
            raise ValueError(f"Missing required field: {k}")

    _require_non_empty_str(obj["state_id"], "state_id")
    _require_non_empty_str(obj["label"], "label")
    _require_non_empty_str_list(obj["assumptions"], "assumptions")
    _require_non_empty_str_list(obj["required_observations"], "required_observations")

    _require_str_list(obj["incompatibilities"], "incompatibilities")

    determinacy = obj["determinacy"]
    if determinacy not in ALLOWED_DETERMINACY:
        raise ValueError(f"determinacy must be one of {sorted(ALLOWED_DETERMINACY)}")

    prov = obj["provenance"]
    if not isinstance(prov, dict):
        raise ValueError("provenance must be an object.")
    if "ingest_doi" not in prov:
        raise ValueError("provenance.ingest_doi is required.")
    if prov["ingest_doi"] != LOCKED_INGEST_DOI:
        raise ValueError(f'provenance.ingest_doi must equal "{LOCKED_INGEST_DOI}".')
    if "record_ids" not in prov:
        raise ValueError("provenance.record_ids is required.")
    if not isinstance(prov["record_ids"], list) or not all(isinstance(x, str) for x in prov["record_ids"]):
        raise ValueError("provenance.record_ids must be a list of strings (may be empty).")


def validate_repo(root: Path) -> None:
    registry_path = root / "states" / "3I_ATLAS" / "state_registry.json"
    registry = load_registry(registry_path)

    base = registry_path.parent
    for rel in registry:
        state_path = (base / rel).resolve()
        if base.resolve() not in state_path.parents:
            raise ValueError(f"Registry entry escapes base directory: {rel}")

        obj = read_json(state_path)
        validate_state_object(obj)


def main(argv: List[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[2]
    try:
        validate_repo(root)
    except Exception as e:
        print(f"VALIDATION FAILED: {e}", file=sys.stderr)
        return 1

    print("OK: Phase-2 deterministic validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())