from pathlib import Path
from typing import List

from .io import read_json


def load_registry(registry_path: Path) -> List[str]:
    data = read_json(registry_path)
    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError("state_registry.json must be a JSON array of strings.")

    # Determinism rule: registry must be lexicographically sorted (strict)
    if data != sorted(data):
        raise ValueError("state_registry.json must be lexicographically sorted.")

    return data