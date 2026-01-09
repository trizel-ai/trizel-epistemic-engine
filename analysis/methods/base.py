from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Protocol


@dataclass(frozen=True)
class MethodSpec:
    method_id: str
    method_version: str
    level: int
    outputs: List[str]  # relative paths under the run directory


class AnalysisMethod(Protocol):
    spec: MethodSpec

    def run(self, *, inputs: Dict[str, object]) -> Dict[str, bytes]:
        """
        Must return a mapping: relative_output_path -> file_bytes (UTF-8 for text).
        Outputs MUST be deterministic for the same inputs.
        """
        ...
