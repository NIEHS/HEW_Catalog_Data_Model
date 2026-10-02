# HEW_Catalog_Data_Model

The HEW Data Commons Model is a LinkML schema for building a canonical
knowledge base of resources relevant to Health and Extreme Weather (HEW), a
domain-specific slice of the broader exposome. It catalogs publications, survey
instruments, datasets, and related resources, with the people, organizations,
and systematic-review coding attached to them.

**📘 Start with the [HEW Schema Handbook](docs/schema_handbook.md)**: the single
reference for the model, its modules, ontology alignment, projections to
Dataverse and other standards, and the 2.0.0 changes.

## Schemas

The current schema version is `2.0.0`. The model is split into a small core and
opt-in extensions:

| Schema | Contents |
|---|---|
| [`hew-model/schema/hew.yaml`](hew-model/schema/hew.yaml) | **Core.** Publications with systematic-review coding, survey instruments and survey datasets, agents, variables, and data dictionaries. |
| [`hew-model/schema/hew-extended.yaml`](hew-model/schema/hew-extended.yaml) | Core plus extensions: geospatial and exposure metadata, programs and projects, and cohort, software, model, tool, and collection resources. |

Each schema composes modules from `hew-model/schema/modules/`; see
[schema layout](docs/schema_handbook.md#2-schema-layout).

## Quick start

```bash
python3 -m pip install -e .
make validate
make artifacts   # regenerate hew.schema.json, hew-extended.schema.json, hew.context.jsonld
```

## Documentation

- [HEW Schema Handbook](docs/schema_handbook.md): the model reference.
- [Model package README](hew-model/README.md): files in `hew-model/`.
- [Geospatial Metadata Enhancement Strategy](hew-model/HEW%20Geospatial%20Metadata%20Enhancement%20Strategy.md):
  design rationale for the geospatial and exposure extension.
- [HEW Resource Library Coding Guide](docs/HEW%20Resource%20Library%20Coding%20Guide.pdf):
  the systematic-review coding scheme.
- [Contributing](CONTRIBUTING.md) and [Security](SECURITY.md).

## References

* [ECTO MODEL](https://github.com/EnvironmentOntology/environmental-exposure-ontology)
* [LinkML](https://linkml.io/)
* [Schema.org](https://schema.org/)
