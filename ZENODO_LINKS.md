# ZENODO_LINKS.md

## Immutable DOI References for TRIZEL Epistemic Engine

This document maintains the authoritative list of permanent Zenodo DOI references used throughout the TRIZEL Epistemic Engine. All data references in epistemic states **must** use DOIs from this list or follow the specified rules for new additions.

## Purpose

**Why Zenodo?**
- Permanent, immutable storage
- Academic-grade archiving
- Version-controlled datasets
- Citeable with DOI
- Free for open science

**Why DOIs?**
- Never change (immutable)
- Globally unique
- Resolvable indefinitely
- Standard in scientific publishing

## Core Dataset References

### 3I/ATLAS Main Dataset

**Dataset**: 3I/ATLAS Primary Observational Data  
**Zenodo DOI**: `10.5281/zenodo.PLACEHOLDER`  
**Version**: 1.0.0  
**Description**: Primary astronomical observations from 3I/ATLAS survey  
**Status**: Placeholder - to be replaced with actual DOI  
**Date Added**: 2025-12-22

### 3I/ATLAS Calibration Data

**Dataset**: 3I/ATLAS Calibration Frames  
**Zenodo DOI**: `10.5281/zenodo.PLACEHOLDER_CAL`  
**Version**: 1.0.0  
**Description**: Calibration data for 3I/ATLAS observations  
**Status**: Placeholder - to be replaced with actual DOI  
**Date Added**: 2025-12-22

## Rules for DOI References

### 1. DOI Format Requirements

All DOIs must:
- ✅ Use Zenodo (zenodo.org)
- ✅ Follow format: `10.5281/zenodo.XXXXXXX` (where X is numeric)
- ✅ Point to specific version (not concept DOI)
- ✅ Be publicly accessible
- ❌ NOT use preprint servers (arXiv, bioRxiv) - may change
- ❌ NOT use institutional repositories - may not be permanent
- ❌ NOT use personal websites - not permanent

**Correct Examples**:
```
10.5281/zenodo.1234567
10.5281/zenodo.7654321
```

**Incorrect Examples**:
```
10.48550/arXiv.2301.12345  # Preprint, may be updated
https://example.com/data   # Not a DOI
10.5281/zenodo.1234567/latest  # Concept DOI, not version-specific
```

### 2. Version Specificity

- **Always** use the version-specific DOI, not the concept DOI
- Zenodo provides both:
  - **Concept DOI**: Points to latest version (changes over time)
  - **Version DOI**: Points to specific version (immutable)
- **Use**: Version DOI only

**Example**:
```
Concept DOI: 10.5281/zenodo.1234567  ❌ (points to latest)
Version DOI: 10.5281/zenodo.1234568  ✅ (points to v1.0.0)
Version DOI: 10.5281/zenodo.1234569  ✅ (points to v1.1.0)
```

### 3. Adding New DOI References

When adding a new dataset reference:

1. **Verify** the DOI is active and accessible
2. **Check** it's a version-specific DOI
3. **Document** in this file with:
   - Dataset name
   - Full DOI
   - Version number
   - Description
   - Date added
4. **Update** this document via pull request
5. **Validate** the epistemic state passes schema

**Template**:
```markdown
### [Dataset Name]

**Dataset**: [Full dataset name]
**Zenodo DOI**: `10.5281/zenodo.XXXXXXX`
**Version**: [semver version]
**Description**: [Brief description]
**Status**: Active
**Date Added**: [YYYY-MM-DD]
```

### 4. Updating Dataset Versions

When a dataset is updated on Zenodo:

1. **Do NOT** modify existing DOI entries
2. **Add NEW** entry with new version DOI
3. **Mark** old version as "Superseded by [new DOI]"
4. **Create NEW** epistemic states referencing new DOI
5. **Keep** old epistemic states unchanged

**Example**:
```markdown
### 3I/ATLAS Main Dataset v1.0.0
**Zenodo DOI**: `10.5281/zenodo.1234568`
**Status**: Superseded by 10.5281/zenodo.1234570
**Date Added**: 2025-01-01

### 3I/ATLAS Main Dataset v1.1.0
**Zenodo DOI**: `10.5281/zenodo.1234570`
**Status**: Active
**Date Added**: 2025-06-01
```

### 5. Forbidden Practices

**Never**:
- ❌ Delete DOI entries from this file
- ❌ Modify existing DOI values
- ❌ Use mutable URLs instead of DOIs
- ❌ Reference non-Zenodo repositories (without justification)
- ❌ Use concept DOIs
- ❌ Skip version numbers

**Why**: Breaks reproducibility and immutability guarantees

## Validation

### Automated Checks

The validation script (`src/epistemic/validate_states.py`) checks:
- DOI format matches `10.5281/zenodo.XXXXXXX`
- DOI is listed in this document (for strict mode)
- DOI is accessible (network check, optional)

### Manual Checks

Before adding a DOI:
1. Visit `https://doi.org/[YOUR_DOI]`
2. Verify it resolves to Zenodo
3. Confirm it's a version DOI (not concept)
4. Check dataset is complete and correct
5. Download and verify checksums if provided

## Emergency Procedures

### If a DOI Becomes Inaccessible

1. **Document** the issue in this file
2. **Contact** Zenodo support
3. **Do NOT** remove or change the DOI
4. **Mark** status as "Inaccessible - under investigation"
5. **Create** issue in repository
6. **Notify** all epistemic state authors

### If a Dataset is Retracted

1. **Mark** DOI status as "Retracted"
2. **Document** reason and date
3. **Deprecate** all epistemic states using that DOI
4. **Do NOT** delete states (preserve audit trail)
5. **Create** migration plan if replacement exists

## Related Standards

- **DOI**: ISO 26324 (Digital Object Identifier)
- **Zenodo**: CERN-operated repository, part of OpenAIRE
- **Schema**: JSON Schema validation in `schema/epistemic_state.schema.json`
- **Contract**: Data contract in `DATA_CONTRACT.md`

## Supplementary Datasets

### Catalog Cross-References

**Dataset**: GCVS Variable Star Catalog (for priors)  
**Zenodo DOI**: `10.5281/zenodo.PLACEHOLDER_GCVS`  
**Version**: 1.0.0  
**Description**: General Catalog of Variable Stars subset  
**Status**: Placeholder - to be replaced with actual DOI  
**Date Added**: 2025-12-22

### Calibration Standards

**Dataset**: Photometric Standard Stars  
**Zenodo DOI**: `10.5281/zenodo.PLACEHOLDER_STD`  
**Version**: 1.0.0  
**Description**: Standard star measurements for calibration  
**Status**: Placeholder - to be replaced with actual DOI  
**Date Added**: 2025-12-22

## Changelog

### 2025-12-22
- Initial version
- Added placeholder DOIs for 3I/ATLAS datasets
- Established DOI rules and validation procedures
- Documented emergency procedures

---

**Document Version**: 1.0.0  
**Last Updated**: 2025-12-22  
**Maintainer**: TRIZEL Project Team

## Notes for Future Maintainers

1. This file is **critical infrastructure** - handle with care
2. Every DOI addition should be reviewed by at least 2 people
3. Never batch-delete or batch-modify DOIs
4. Keep historical record even for deprecated DOIs
5. When in doubt, add more documentation, not less
6. Preserve complete audit trail

**Remember**: Immutability is not just a feature, it's a guarantee.
