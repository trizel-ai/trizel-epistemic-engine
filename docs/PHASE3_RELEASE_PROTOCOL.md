# Phase-3 Release Protocol — TRIZEL (Authoritative)

## Repository
trizel-ai/trizel-epistemic-engine

## Purpose
Define what constitutes an auditable "analysis release" in Phase-3.

## Release Boundary
A "release" is a deterministic bundle generated from:
- A specific git commit
- A specific METHOD_ID
- A specific RUN_ID
- A specific input scope (states/3I_ATLAS)

## Release Output Location (Exclusive)
All release bundles MUST be written ONLY under:
releases/

## Release Directory Naming (Deterministic)
Each release MUST be stored at:

releases/<RUN_ID>/

No timestamps. No auto-versioning.

## Mandatory Release Files
Every release MUST include:

1) releases/<RUN_ID>/RELEASE_MANIFEST.json
2) releases/<RUN_ID>/RELEASE_NOTES.md

The RELEASE_MANIFEST.json MUST be a copy (or strict superset) of:
analysis_artifacts/<RUN_ID>/manifest.json

## Release Notes Constraints
RELEASE_NOTES.md MUST:
- Cite the METHOD_ID and RUN_ID
- Cite the git commit
- Describe produced artifacts only
- Contain no interpretive conclusions unless authorized by the method specification

## Prohibited Content
A release MUST NOT:
- Modify Phase-2 artifacts
- Include network-fetched data
- Include timestamps or non-deterministic values

## Effective Lock
This protocol is authoritative for Phase-3 releases.
No release generation is permitted until Phase-3 contract tests pass in CI.
