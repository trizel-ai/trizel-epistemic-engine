# Phase-3 Method Registry (Authoritative)

## Rule
Only methods listed here are allowed to run in the deterministic pipeline.

## Method IDs (Initial Set)
M00_STRUCTURAL_AUDIT
- Level: 0
- Output: reports/structural_audit.md, tables/state_inventory.csv

M10_DESCRIPTIVE_STATS
- Level: 1
- Output: tables/field_completeness.csv, reports/descriptive_stats.md

M20_CONSISTENCY_CHECKS
- Level: 2
- Output: reports/consistency_checks.md, tables/consistency_events.csv

## Versioning
Each method MUST declare:
- method_id
- method_version (semantic version)
- deterministic_inputs list
- deterministic_outputs list

Any change to outputs or logic requires method_version bump.
