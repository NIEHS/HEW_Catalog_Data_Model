# HEW Data Commons Model

A LinkML-based canonical resource knowledge base for Health and Extreme Weather
(HEW), designed to catalog and connect publications, datasets, surveys, tools,
software, models, geospatial resources, cohorts, dictionaries, people, projects,
programs, and provenance. Systematic-review coding is one supported input stream,
not the whole model.

The current schema is version `2.0.0`. It has a small core (`schema/hew.yaml`) for
publications and surveys, and opt-in extensions composed in `schema/hew-extended.yaml`.
The model is organized around four separable ideas:

1. **HEW resources**: literature, survey instruments, and datasets (including survey datasets and their data dictionaries) in the core; cohorts, geospatial and exposome datasets, software, models, tools, and collections in the extensions.
2. **Review annotations**: structured coding outputs over HEW resources, initially using the HEW Resource Library Coding Guide and LaserAI-assisted systematic-review workflows.
3. **Domain concepts and coding values**: exposures, health impacts, geography, data tools and methods, special topics, and mappings to external ontologies such as BioLink, ECTO, ENVO, MONDO, HPO, schema.org, DCAT, PROV-O, and Dublin Core.
4. **Coordination and provenance**: people, organizations, and software agents in the core; programs, projects, funding sources, and role-bearing associations in the projects extension.

## Repository layout

```text
.
|-- README.md
|-- ../docs/SCHEMA_DESIGN.md
|-- pyproject.toml
|-- Makefile
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
|-- terms/
|   |-- exposure_terms.yaml
|   |-- health_impact_terms.yaml
|   |-- geography_terms.yaml
|   |-- data_tools_methods_terms.yaml
|   `-- special_topics_terms.yaml
|-- examples/
|   |-- example_literature_annotation.yaml
|   |-- example_dataset_resource.yaml
|   |-- example_spatiotemporal_exposure.yaml
|   |-- publication_resource.yaml
|   |-- survey_instrument.yaml
|   |-- survey_dataset.yaml
|   |-- tool_resource.yaml
|   |-- resource_collection.yaml
|   |-- environmental_variable.yaml
|   |-- amadeus_covariate_calculation.yaml
|   |-- omop_gaia_external_exposure_linkage.yaml
|   `-- example_program_project_people.yaml
|-- scripts/
|   `-- validate_examples.sh
|-- ../docs/
|   |-- ontology_alignment_notes.md
|   |-- people_projects_programs.md
|   |-- exposome_alignment.md
|   |-- amadeus_alignment.md
|   |-- envar_profile.md
|   `-- omop_gaia_external_exposure.md
`-- HEW Geospatial Metadata Enhancement Strategy.md
```

The consolidated schema design, geospatial architecture, and EnVar integration
are documented in [`docs/SCHEMA_DESIGN.md`](../docs/SCHEMA_DESIGN.md). The longer
geospatial strategy is in [`HEW Geospatial Metadata Enhancement Strategy.md`](HEW%20Geospatial%20Metadata%20Enhancement%20Strategy.md).

## Quick start

```bash
python3 -m pip install -e .
make validate
make artifacts
```

## Current scope

The core supports publications with systematic-review annotations, survey instruments (constructs, ordered questions, coded response options, populations), survey datasets with data dictionaries, and the people and organizations credited on them. Extensions add structured geospatial and temporal extents, EnVar-aligned environmental variables, optional exposure estimates and covariate methods, OMOP/Gaia linkage status, programs and projects, and additional resource types.

## Design stance

The coding guide is modeled as a **coding profile over a general HEW resource model**, not as the entire ontology. This lets HEW systematic-review records serve immediate needs while keeping the commons open to future exposure datasets, cohorts, survey instruments, geospatial assets, exposome data, tools, software, notebooks, and dictionaries.

## Added coordination layer

The core includes `Agent`, `Person`, `Organization`, and `SoftwareAgent`; the projects extension adds `Program`, `Project`, `FundingSource`, and `AgentAssociation`. These classes are mapped to schema.org, PROV-O, BioLink, and DCAT where appropriate. The intent is to represent who created, reviewed, funded, maintained, used, or produced HEW resources without hard-coding every possible role as a separate slot.
