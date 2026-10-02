# HEW Data Commons Model package

The LinkML schema, examples, coding vocabularies, and helper code for the HEW
Data Commons model (schema version `2.0.0`). The model itself is described in
the [HEW Schema Handbook](../docs/schema_handbook.md).

## Layout

```text
hew-model/
|-- schema/
|   |-- hew.yaml                  # core schema
|   |-- hew-extended.yaml         # core + extensions
|   |-- hew.schema.json           # generated from hew.yaml
|   |-- hew-extended.schema.json  # generated from hew-extended.yaml
|   |-- hew.context.jsonld        # generated from hew-extended.yaml
|   `-- modules/
|       |-- hew_core.yaml            # resource base, agents, variables, locations
|       |-- hew_review_coding.yaml   # systematic-review annotations
|       |-- hew_publication.yaml     # LiteratureResource
|       |-- hew_survey.yaml          # survey instruments, questions, datasets
|       |-- hew_ext_geospatial.yaml  # geospatial and exposure extension
|       |-- hew_ext_projects.yaml    # programs, projects, funding extension
|       `-- hew_ext_resources.yaml   # cohort, software, model, tool, collection extension
|-- examples/                     # example records, all validated by `make validate`
|-- terms/                        # HEW Resource Library Coding Guide vocabularies
|-- hew_model/jsonld.py           # JSON-LD context generation and serialization helpers
|-- scripts/validate_examples.sh  # validates schemas and examples
`-- HEW Geospatial Metadata Enhancement Strategy.md
```

Core examples (`publication_resource.yaml`, `example_literature_annotation.yaml`,
`survey_instrument.yaml`, `survey_dataset.yaml`) validate against `hew.yaml`; the
rest validate against `hew-extended.yaml`. See
`scripts/validate_examples.sh` for the class each example is checked as.

## Quick start

Run from the repository root:

```bash
python3 -m pip install -e .
make validate
make artifacts
```
