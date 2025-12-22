# Examples

This directory contains example scripts demonstrating the usage of the TRIZEL epistemic engine.

## Available Examples

### usage_example.py

Comprehensive demonstration of all validation utilities including:
- Loading and validating JSON schemas
- Loading and validating state registries
- Creating and validating epistemic states
- Searching for states by ID
- Handling validation errors

**Run it:**
```bash
python3 examples/usage_example.py
```

## Adding New Examples

When adding new example scripts:
1. Follow the existing pattern of importing from `src.validation`
2. Add clear documentation at the top of the script
3. Include proper error handling
4. Demonstrate both success and failure cases
5. Update this README with a description
