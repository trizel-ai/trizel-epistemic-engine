from __future__ import annotations

from pathlib import Path

PHASE3_ALLOWED_OUTPUT_DIRS = {"analysis_artifacts", "releases"}


def assert_phase3_output_path(path: Path) -> None:
    parts = path.parts
    if not parts:
        raise ValueError("Empty output path.")
    if parts[0] not in PHASE3_ALLOWED_OUTPUT_DIRS:
        raise ValueError(
            "Phase-3 outputs must be written only under "
            f"{sorted(PHASE3_ALLOWED_OUTPUT_DIRS)}. Got: {path}"
        )


def main() -> int:
    # Placeholder runner.
    # Phase-3 will implement deterministic analysis here, without network access.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
