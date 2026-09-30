# HEW_Catalog_Data_Model

The HEW Data Commons Model is a LinkML schema for building a canonical
knowledge base of resources relevant to Health and Extreme Weather. It catalogs
publications, datasets, survey instruments, tools, software, models, geospatial
resources, cohorts, data dictionaries, people, projects, programs, and
provenance for researchers studying human health and extreme weather as a
domain-specific subset of the broader exposome.

The canonical schema is [`hew-model/schema/hew-geospatial.yaml`](hew-model/schema/hew-geospatial.yaml).
See the [consolidated schema design](docs/SCHEMA_DESIGN.md) for the resource,
review-coding, geospatial, EnVar, and interoperability model.

The current schema version is `1.3.0`. Install the project and run the checks with:

```bash
python3 -m pip install -e .
make validate
make jsonschema
make jsonld-context
```

## Exposome and Geo-Temporal Exposure Alignment

The HEW schema supports exposome-facing metadata through environmental
variables, structured spatial and temporal support, exposure concepts,
covariate calculation methods, and optional OMOP/Gaia external exposure
bindings. The profile is designed to interoperate with EnVar, Amadeus-derived
covariates, ENVO, ECTO, GeoSPARQL, STAC, DCAT, Schema.org, DataCite, and PROV-O.

See the [exposome alignment](docs/exposome_alignment.md),
[Amadeus alignment](docs/amadeus_alignment.md), [EnVar profile](docs/envar_profile.md),
and [OMOP/Gaia linkage](docs/omop_gaia_external_exposure.md) notes.

## Catalog-first design

This schema begins as a resource catalog and knowledge base, not as a warehouse
for all exposure observations or derived exposure values. It captures enough
exposure, health, geographic, temporal, method, and provenance metadata to make
resources discoverable, reusable, and interoperable. Detailed exposure-estimate
modeling is available as an optional expansion layer.

## Canonical model and projections

The LinkML schema is the canonical internal representation. External systems are
projections of that model, beginning with CAFE Dataverse custom HEW metadata
blocks and expanding to portal/API views, Schema.org JSON-LD, DCAT, DataCite,
STAC, GeoSPARQL/RDF, knowledge-graph edges, and exposome workflows.

```text
                    HEW Canonical Knowledge Base
                              |
        ------------------------------------------------
        |                 |                 |            |
   Dataverse          Portal/API        KG/RDF       Exposome
 metadata blocks      search views      export       workflows
        |                 |                 |            |
 CAFE Dataverse       HEW portal       ROBOKOP       Amadeus/
 dataset records      discovery UX     Translator    EnVar/Gaia
```

## Relationship to the exposome ecosystem

HEW is a domain-specific slice of the broader exposome focused on extreme
weather, weather-related disasters, and weather-mediated environmental harms.
It aligns environmental variables, spatial and temporal support, exposure
concepts, context, provenance, and health links with EnVar, ENVO, ECTO,
Amadeus, OMOP/Gaia, and related standards without replacing them.

```text
Exposome
  └── External exposures
        └── Environmental / climate / weather / disaster exposures
              └── Health and Extreme Weather resources
```

## Researcher-facing questions

- What resources exist for studying extreme weather and human health?
- Which datasets, tools, surveys, and publications address a given exposure,
  health impact, geography, population, or special topic?
- What variables, methods, spatial supports, temporal supports, and dictionaries
  are available?
- Which resources can be projected into Dataverse, DCAT, Schema.org, DataCite,
  STAC, RDF, or future knowledge-graph outputs?


# Data Model Approach

Canonical model:          LinkML
Structural interchange:  JSON
Semantic layer:          Generated JSON-LD context
Application validation:  LinkML validator / generated JSON Schema
Database validation:     MongoDB-specific reduced JSON Schema
Operational storage:     MongoDB BSON documents
Knowledge-graph export:  JSON-LD/RDF, SHACL and ontology mappings

# References 

* [ECTO MODEL](https://github.com/EnvironmentOntology/environmental-exposure-ontology)
* [LinkML](https://linkml.io/)
* [Schema.org](https://schema.org/)
