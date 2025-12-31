# Phase-3 Release Contract (Deep Analysis Releases, Deterministic)

## Release Output Location (Exclusive)
releases/<RELEASE_ID>/

## RELEASE_ID Format (Exact)
RELEASE_ID MUST be:
R__YYYYMMDD__<SHORT_GIT_SHA>

Example:
R__20260101__a1b2c3d

## Deep Analysis Release Definition (Precise)
A “deep analysis release” is a deterministic package that contains:
1) Full run manifest with SHA256 for every file.
2) Method registry snapshot (copied into the release).
3) Input registry hash:
   - SHA256 of the canonical states registry file for the target object.
4) Level 0–2 outputs (as defined in PHASE3_ANALYSIS_CONTRACT).
5) A single human-readable summary report.

## Minimum Required Files (Exact)
releases/<RELEASE_ID>/release_manifest.json
releases/<RELEASE_ID>/inputs/input_hashes.json
releases/<RELEASE_ID>/methods/PHASE3_METHOD_REGISTRY.md
releases/<RELEASE_ID>/reports/summary.md
releases/<RELEASE_ID>/tables/state_inventory.csv
releases/<RELEASE_ID>/tables/field_completeness.csv

## Prohibited
- Any file not referenced in release_manifest.json.
- Any release build that depends on network access.
- Any modification of Phase-2 artifacts during release construction.
