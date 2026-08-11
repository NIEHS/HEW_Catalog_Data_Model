# Contributing

This model is early and should evolve carefully.

## Principles

- Preserve the distinction between HEW resources, review annotations, and domain concepts.
- Do not turn review-management values such as `Not Reported` into exposure or health entities.
- Keep LaserAI output provenance explicit.
- Prefer local HEW identifiers first, then add ontology mappings as evidence improves.
- Add examples for every meaningful schema change.

## Development

```bash
python -m pip install linkml
make validate
```
