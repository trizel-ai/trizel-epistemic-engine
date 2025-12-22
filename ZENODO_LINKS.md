# Zenodo Links

**Purpose**: Read-only DOI references to external datasets  
**Last Updated**: 2025-12-22  
**Status**: Awaiting initial DOI registrations

## Overview

This document maintains a curated list of DOI references to external datasets used in the TRIZEL epistemic engine. All references are **read-only** and point to immutable, published datasets on Zenodo or other DOI-issuing repositories.

## Hard Rules

1. **No Data Ingestion**: This repository does not fetch, download, or parse data from these DOIs
2. **Immutable References**: DOIs are permanent identifiers; links never change
3. **Read-Only**: All references are informational; no write operations to external repositories
4. **Audit Trail**: All DOI additions are tracked via git history

## 3I/ATLAS Dataset References

### Primary Datasets

**Status**: Awaiting initial DOI registrations

Example format:
```markdown
#### Dataset Name
- **DOI**: 10.5281/zenodo.XXXXXXX
- **Title**: [Full dataset title]
- **Published**: YYYY-MM-DD
- **Description**: Brief description of dataset content
- **Used In States**: [List of state_id references]
```

<!-- Placeholder for future DOI entries -->

---

### Secondary/Reference Datasets

**Status**: Awaiting initial DOI registrations

<!-- Placeholder for future DOI entries -->

---

## DOI Format Guidelines

All DOI references in this document must follow these conventions:

1. **Format**: `10.xxxx/suffix` (standard DOI format)
2. **Resolvability**: All DOIs must resolve via https://doi.org/
3. **Permanence**: Only reference published, immutable datasets
4. **Accessibility**: Prefer open-access datasets when available

## Example DOI Entry

```markdown
#### 3I/ATLAS Observational Data v1.0
- **DOI**: 10.5281/zenodo.1234567
- **Title**: 3I/ATLAS Multi-wavelength Observations (2024 Campaign)
- **Published**: 2024-11-15
- **Description**: Photometric and spectroscopic observations of interstellar object 3I/ATLAS
- **Used In States**: 3i_atlas_001, 3i_atlas_002, 3i_atlas_005
- **License**: CC BY 4.0
- **Size**: ~2.3 GB
- **Format**: FITS, CSV
```

## Contributing DOI References

When adding new DOI references:

1. Verify the DOI resolves correctly
2. Confirm the dataset is published and immutable
3. Add complete metadata (title, date, description)
4. Link to specific epistemic states that reference this DOI
5. Follow the template format above

## DOI Verification

Before adding a DOI to this list:

```bash
# Test DOI resolution
curl -I https://doi.org/10.5281/zenodo.XXXXXXX

# Expected: HTTP 302 redirect to dataset landing page
```

## Repository Types

We accept DOI references from:

- ✅ **Zenodo**: https://zenodo.org
- ✅ **Figshare**: https://figshare.com  
- ✅ **Dataverse**: https://dataverse.org
- ✅ **OSF**: https://osf.io
- ✅ Other DOI-issuing scientific repositories

We do **not** accept:
- ❌ URLs without DOIs
- ❌ DOIs for non-dataset resources (papers only)
- ❌ Proprietary/restricted access datasets (prefer open access)

## Notes

- This file is part of the epistemic layer's **read-only** interface to external data
- No code in this repository fetches or processes data from these DOIs
- DOIs serve as provenance markers for epistemic state source attribution
- Analytical operations on DOI data occur in separate layers (not here)

## Change Log

### 2025-12-22
- Initial ZENODO_LINKS.md structure
- Defined DOI format guidelines
- Established hard rules for read-only references
- Awaiting first DOI registrations
