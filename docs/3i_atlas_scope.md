# 3I/ATLAS Scope

## Overview

The **3I/ATLAS** (Three Interpretations - Atlas) dataset represents a carefully curated collection of astronomical observations that can be interpreted through multiple epistemic frameworks. This document defines the scope, boundaries, and interpretation space for 3I/ATLAS epistemic states.

## Dataset Context

### Source Domain
- **Field**: Astronomy / Astrophysics
- **Type**: Observational data
- **Instruments**: Multiple telescope arrays
- **Time Period**: [To be specified]
- **Coverage**: [Spatial/spectral coverage to be specified]

### Data Characteristics
- **Format**: Tabular, time-series, imaging (mixed)
- **Volume**: [To be specified]
- **Quality**: Peer-reviewed, calibrated
- **Access**: Zenodo DOI (immutable)

## Interpretation Dimensions

### 1. Measurement Framework
Different approaches to measuring astronomical phenomena:

**Classical Photometry**
- Direct brightness measurements
- Magnitude systems
- Calibration assumptions

**Bayesian Photometry**
- Probabilistic flux estimates
- Prior-informed measurements
- Uncertainty propagation

**Model-Free Photometry**
- Raw instrumental readings
- Minimal processing
- Maximum information retention

### 2. Temporal Analysis
How time-series data is interpreted:

**Periodic Signal Detection**
- Assumes underlying periodicity
- Fourier/wavelet methods
- False positive control

**Stochastic Process Modeling**
- Treats variation as random process
- Correlation structure
- Noise characterization

**Hybrid Approaches**
- Combined deterministic + stochastic
- Model selection criteria
- Complexity penalties

### 3. Source Classification
How objects are categorized:

**Physical Classification**
- Theory-driven categories
- Based on astrophysical models
- Requires physical assumptions

**Phenomenological Classification**
- Observation-based grouping
- Minimal theory
- Pattern recognition

**Probabilistic Classification**
- Soft assignments
- Multiple class memberships
- Uncertainty quantification

## Scope Boundaries

### In Scope

The 3I/ATLAS epistemic states cover:
- ✅ Data interpretation methodologies
- ✅ Framework assumptions
- ✅ Statistical approaches
- ✅ Measurement philosophies
- ✅ Epistemic uncertainty

### Out of Scope

The following are **not** included:
- ❌ Raw data processing (Phase-1)
- ❌ Astrophysical theory (separate domain)
- ❌ Instrument calibration details
- ❌ Policy recommendations
- ❌ Priority rankings of interpretations

## Standard Interpretation Scenarios

### Scenario A: Variable Star Analysis

**Context**: Time-series photometry of potentially variable stars

**Interpretation 1: Frequentist**
- Null hypothesis: Constant brightness
- Test statistic: χ² goodness-of-fit
- Conclusion: Reject H₀ or fail to reject

**Interpretation 2: Bayesian**
- Model: Variable vs. constant
- Prior: Based on catalog frequencies
- Conclusion: Bayes factor, posterior odds

**Interpretation 3: Model-Agnostic**
- Metric: Variance, range, periodogram power
- Threshold: Empirical percentile
- Conclusion: Variability index

### Scenario B: Transient Detection

**Context**: Identifying new or changing sources

**Interpretation 1: Template Matching**
- Assumes known transient types
- Classification via similarity
- Confidence based on match quality

**Interpretation 2: Anomaly Detection**
- No type assumptions
- Deviation from baseline
- Statistical outlier identification

**Interpretation 3: Probabilistic**
- Multiple possible classes
- Class probabilities
- Expected classification loss

### Scenario C: Multi-Band Photometry

**Context**: Color-based object characterization

**Interpretation 1: SED Fitting**
- Physical model (spectral energy distribution)
- Parameter estimation (temperature, etc.)
- Goodness-of-fit metrics

**Interpretation 2: Color-Color Diagrams**
- Empirical color relationships
- Phenomenological classification
- Comparison populations

**Interpretation 3: Machine Learning**
- Data-driven clustering
- No physical model
- Predictive accuracy focus

## Epistemic Assumptions

Common assumptions that differentiate interpretations:

### About Data
- **Assumption**: Measurement errors are Gaussian
- **Impact**: Affects statistical tests, confidence intervals
- **Alternatives**: Non-parametric, robust methods

### About Nature
- **Assumption**: Physical processes are stationary
- **Impact**: Enables long-term averaging, modeling
- **Alternatives**: Non-stationary models, local analysis

### About Models
- **Assumption**: Simpler models are more likely true
- **Impact**: Penalizes complexity, favors parsimony
- **Alternatives**: Complexity-neutral, data-driven selection

### About Inference
- **Assumption**: Long-run error control is primary goal
- **Impact**: Frequentist methods preferred
- **Alternatives**: Bayesian (coherence), decision-theoretic

## State Granularity

Epistemic states can be defined at multiple levels:

**Coarse-Grained**: Framework level
- "Bayesian interpretation of 3I/ATLAS"
- Broad assumptions
- Applied to entire dataset

**Medium-Grained**: Scenario level
- "Bayesian variable star analysis in 3I/ATLAS"
- Scenario-specific assumptions
- Applied to subset

**Fine-Grained**: Parameter level
- "Bayesian variable star analysis with Beta(2,2) prior"
- Complete specification
- Fully reproducible

**Recommendation**: Use medium-grained states for main registry.

## Versioning Strategy

As 3I/ATLAS evolves:

**Data Versioning**
- Each data release gets new Zenodo DOI
- States reference specific DOI version
- No retroactive updates

**Interpretation Versioning**
- Framework refinements → new state version
- Bug fixes in code → patch version bump
- Assumption changes → minor version bump
- Framework changes → major version bump

## Comparison Criteria

When comparing interpretations:

**Objective Criteria**
- Computational efficiency
- Reproducibility
- Code availability
- Documentation quality

**Subjective Criteria** (acknowledge as subjective)
- Intuitive appeal
- Alignment with theory
- Community acceptance
- Historical precedent

**Note**: The engine stores states, it does not rank them.

## Example State Metadata

```json
{
  "state_id": "2025-12-22_3iatlat_bayesian_variables",
  "interpretation": {
    "framework": "Bayesian inference",
    "assumptions": [
      "Gaussian measurement errors",
      "Stationary light curves",
      "Informative period priors from GCVS"
    ],
    "scope": "Variable star detection in 3I/ATLAS Field 1"
  }
}
```

## Related Documentation

- [Epistemic Overview](epistemic_overview.md) - General framework
- [Data Contract](../DATA_CONTRACT.md) - Format specifications
- [Zenodo Links](../ZENODO_LINKS.md) - DOI references

## Future Extensions

Potential scope expansions (Phase-3+):
- Cross-matching interpretations
- Multi-dataset epistemic states
- Temporal evolution of interpretations
- Interpretation genealogies

---

**Document Version**: 1.0.0  
**Last Updated**: 2025-12-22  
**Scope Status**: Initial definition, subject to refinement
