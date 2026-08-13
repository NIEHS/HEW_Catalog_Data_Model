# HEW Data Commons Model

A LinkML-based data model for cataloging Health and Extreme Weather (HEW) resources, beginning with systematic-review literature coding from LaserAI and designed to grow into a broader HEW data commons model.

The model is organized around three separable ideas:

1. **HEW resources**: literature, datasets, cohorts, survey instruments, software, models, geospatial resources, exposome resources, tutorials, notebooks, tools, and data dictionaries.
2. **Review annotations**: structured coding outputs over HEW resources, initially using the HEW Resource Library Coding Guide and LaserAI-assisted systematic-review workflows.
3. **Domain concepts and coding values**: exposures, health impacts, geography, data tools and methods, special topics, and mappings to external ontologies such as BioLink, ECTO, ENVO, MONDO, HPO, schema.org, DCAT, PROV-O, and Dublin Core.
4. **Coordination and provenance**: people, organizations, software agents, programs, projects, funding sources, and role-bearing associations among them.

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
|       |-- hew_resource_types.yaml
|       `-- hew_agents_projects.yaml
|-- terms/
|   |-- exposure_terms.yaml
|   |-- health_impact_terms.yaml
|   |-- geography_terms.yaml
|   |-- data_tools_methods_terms.yaml
|   `-- special_topics_terms.yaml
|-- examples/
|   |-- example_literature_annotation.yaml
|   |-- example_dataset_resource.yaml
|   `-- example_program_project_people.yaml
|-- scripts/
|   `-- validate_examples.sh
|-- docs/
|   |-- ontology_alignment_notes.md
|   `-- people_projects_programs.md
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

## Added coordination layer

The schema now includes `Agent`, `Person`, `Organization`, `SoftwareAgent`, `Program`, `Project`, `FundingSource`, and `AgentAssociation`. These classes are mapped to schema.org, PROV-O, BioLink, and DCAT where appropriate. The intent is to represent who created, reviewed, funded, maintained, used, or produced HEW resources without hard-coding every possible role as a separate slot.
