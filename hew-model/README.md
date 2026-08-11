# HEW Data Commons Model

A LinkML-based data model for cataloging Health and Extreme Weather (HEW) resources, beginning with systematic-review literature coding from LaserAI and designed to grow into a broader HEW data commons model.

The model is organized around three separable ideas:

1. **HEW resources**: literature, datasets, cohorts, survey instruments, software, models, geospatial resources, exposome resources, tutorials, notebooks, tools, and data dictionaries.
2. **Review annotations**: structured coding outputs over HEW resources, initially using the HEW Resource Library Coding Guide and LaserAI-assisted systematic-review workflows.
3. **Domain concepts and coding values**: exposures, health impacts, geography, data tools and methods, special topics, and mappings to external ontologies such as BioLink, ECTO, ENVO, MONDO, HPO, schema.org, DCAT, and Dublin Core.

## Repository layout

```text
.
|-- README.md
|-- SCHEMA_DESIGN.md
|-- pyproject.toml
|-- Makefile
|-- schema/
|   |-- hew.yaml
|   `-- modules/
|       |-- hew_core.yaml
|       |-- hew_literature.yaml
|       |-- hew_review_coding.yaml
|       `-- hew_resource_types.yaml
|-- terms/
|   |-- exposure_terms.yaml
|   |-- health_impact_terms.yaml
|   |-- geography_terms.yaml
|   |-- data_tools_methods_terms.yaml
|   `-- special_topics_terms.yaml
|-- examples/
|   |-- example_literature_annotation.yaml
|   `-- example_dataset_resource.yaml
|-- scripts/
|   `-- validate_examples.sh
|-- docs/
|   `-- ontology_alignment_notes.md
`-- .github/workflows/
    `-- ci.yml
```

## Quick start

```bash
python -m pip install linkml
make validate
make jsonschema
```

## Current scope

Version 0.1 focuses on literature resources, LaserAI/manual systematic-review annotations, coding guide fields, free-text `Other/Specify` values, annotation provenance, and a path for promoting mentioned datasets, cohorts, surveys, tools, software, and models into first-class HEW commons resources.

## Design stance

The coding guide is modeled as a **coding profile over a general HEW resource model**, not as the entire ontology. This lets HEW systematic-review records serve immediate needs while keeping the commons open to future exposure datasets, cohorts, survey instruments, geospatial assets, exposome data, tools, software, notebooks, and dictionaries.
