# Contributing

This model is early and should evolve carefully.

Read the [HEW Schema Handbook](docs/schema_handbook.md) before changing the schema.

## Principles

- Preserve the distinction between HEW resources, review annotations, and domain concepts.
- Do not turn review-management values such as `Not Reported` into exposure or health entities.
- Keep LaserAI output provenance explicit.
- Prefer local HEW identifiers first, then add ontology mappings as evidence improves.
- Add examples for every meaningful schema change.
- Keep the core (`hew.yaml`) small. Add new capabilities as extension modules,
  and do not add type-specific slots to `HEWResource`.
- Define each class and slot in exactly one module, and regenerate the committed
  artifacts with `make artifacts` after schema changes.

## Development

```bash
python3 -m pip install -e .
make validate
make artifacts
```
