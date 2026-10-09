# HEW Schema Handbook

The single reference for the Health and Extreme Weather (HEW) Data Commons
schema, version 2.0.0: what it models, how it is organized, how it aligns with
external standards, and how it is projected into other systems.

- [1. Purpose and scope](#1-purpose-and-scope)
- [2. Schema layout](#2-schema-layout)
- [3. Model layers](#3-model-layers)
- [4. Resources](#4-resources)
- [5. Agents, programs, and projects](#5-agents-programs-and-projects)
- [6. Systematic-review coding](#6-systematic-review-coding)
- [7. Surveys](#7-surveys)
- [8. Geospatial and exposure extension](#8-geospatial-and-exposure-extension)
- [9. Identifiers and ontology alignment](#9-identifiers-and-ontology-alignment)
- [10. Projections](#10-projections)
- [11. Version 2.0.0 changes](#11-version-200-changes)
- [12. Roadmap](#12-roadmap)
- [13. Related documents](#13-related-documents)

## 1. Purpose and scope

HEW is a domain-specific slice of the broader exposome, focused on extreme
weather, weather-related disasters, and weather-mediated environmental harms.

```text
Exposome
  └── External exposures
        └── Environmental / climate / weather / disaster exposures
              └── Health and Extreme Weather resources
```

The schema is **catalog-first**. It describes resources (publications, surveys,
datasets, tools) and their reuse context: enough exposure, health, geographic,
temporal, method, and provenance metadata to make them discoverable, reusable,
and interoperable. It is not a warehouse for every exposure observation or
derived value; detailed exposure-estimate modeling is an optional extension.

Systematic-review coding, initially from the HEW Resource Library Coding Guide
and LaserAI-assisted workflows, is one input stream and a coding profile over the
general resource model, not the whole ontology.

The model is meant to answer researcher questions such as:

- What resources exist for studying extreme weather and human health?
- Which datasets, tools, surveys, and publications address a given exposure,
  health impact, geography, population, or special topic?
- What variables, methods, spatial supports, temporal supports, and dictionaries
  are available?
- Which resources can be projected into Dataverse, DCAT, Schema.org, DataCite,
  STAC, RDF, or knowledge-graph outputs?

### Data model approach

| Concern | Technology |
|---|---|
| Canonical model | LinkML |
| Structural interchange | JSON |
| Semantic layer | Generated JSON-LD context |
| Application validation | LinkML validator / generated JSON Schema |
| Database validation | MongoDB-specific reduced JSON Schema |
| Operational storage | MongoDB BSON documents |
| Knowledge-graph export | JSON-LD/RDF, SHACL, and ontology mappings |

### Controlled vocabularies and concept mappings

HEW keeps the catalog schema and controlled vocabularies separate. The
`HEW_Measures` project remains a standalone schema/vocabulary and is referenced
by HEW resources via reusable concept-mapping metadata rather than imported into
HEW directly.

The shared concept-mapping contract is a `ConceptMappingMixin` in the core schema:

- `aliases`: display synonyms and user-facing search terms
- `exact_mappings`: canonical equivalent identifiers from external vocabularies
- `close_mappings`: near-equivalent identifiers that may need review
- `related_mappings`: related concepts for search, navigation, and faceting
- `source_vocabularies`: the URI(s) of the taxonomy providing the mapping

This is intentionally reusable across resource types, survey constructs,
annotations, and future concept-bearing classes. It lets downstream services
project clean facet values such as canonical label, aliases, and equivalent
URIs/CURIEs without flattening a separate measure taxonomy into the HEW core
schema.

For a complete, schema-validated example showing a survey construct mapped to a
standalone HEW_Measures term, see
[`survey_measure_mappings.yaml`](../hew-model/examples/survey_measure_mappings.yaml).

## 2. Schema layout

There are two validation entry points in `hew-model/schema/`:

| Schema | Contents |
|---|---|
| `hew.yaml` | **Core**: publications, systematic-review coding, surveys, agents, variables, and data dictionaries. |
| `hew-extended.yaml` | The core plus all extension modules. |

```text
modules/hew_core.yaml            HEWResource, DatasetResource, Distribution, DataDictionary,
                                 Variable, GeographicLocation, Agent and its subclasses
modules/hew_review_coding.yaml   HEWSystematicReviewAnnotation, ConceptAnnotation,
                                 GeographyAnnotation, DataToolMethodAnnotation, MentionedResource
modules/hew_publication.yaml     LiteratureResource
modules/hew_survey.yaml          SurveyInstrument, SurveyConstruct, SurveyQuestion,
                                 ResponseOption, SurveyDataset, Population
modules/hew_ext_geospatial.yaml  GeospatialResource, EnvironmentalVariable, extents, supports,
                                 SpatiotemporalExposure, CovariateCalculation, OMOP/Gaia linkage
modules/hew_ext_projects.yaml    Program, Project, FundingSource, AgentAssociation
modules/hew_ext_resources.yaml   CohortResource, SoftwareResource, ModelResource,
                                 ToolResource, ResourceCollection
```

Every module imports `hew_core`, and each class and slot is defined in exactly
one module. New capabilities are added as extension modules, not as slots on
`HEWResource`.

Generated artifacts are committed next to the schemas and refreshed with
`make artifacts`:

| Artifact | Generated from |
|---|---|
| `hew.schema.json` | `hew.yaml` |
| `hew-extended.schema.json` | `hew-extended.yaml` |
| `hew.context.jsonld` | `hew-extended.yaml` (a superset, so it covers every module) |

`make validate` validates both schemas and every example: core examples against
`hew.yaml`, extension examples against `hew-extended.yaml`. Examples live in
`hew-model/examples/`; coding-guide vocabularies live in `hew-model/terms/`.

## 3. Model layers

HEW keeps these questions separate:

| Layer | Question | Main alignment |
|---|---|---|
| Resource | What dataset, paper, model, or software is this? | HEW, DCAT, Schema.org |
| Place | What named place is involved? | BioLink, GeoNames, GAZ |
| Geometry | Where exactly is it? | GeoSPARQL, GeoJSON, WKT, CRS |
| Environment | What environmental entity or setting is involved? | ENVO |
| Exposure | What environmental exposure occurred? | ECTO |
| Variable | What was measured or derived, and how? | EnVar-aligned HEW profile |
| Clinical binding | How does it map into clinical workflows? | OMOP, Gaia |

Exposure information appears at three depths:

- **Catalog topic**: a resource is tagged with an exposure, health impact,
  geography, population, or special topic for discovery.
- **Resource metadata**: a resource describes variables, methods, extent,
  support, temporal coverage, dictionary, and access conditions for reuse.
- **Exposure-ready semantics**: a resource or optional exposure object
  identifies property, exposure concept, context, unit, support, aggregation,
  provenance, and external-vocabulary mappings without storing every value.

## 4. Resources

`HEWResource` is the abstract root for every cataloged resource; it is an
information entity, not necessarily a data-bearing object. It carries only the
descriptive, rights, and attribution slots shared by all resource types:
identifiers, title, description, keywords, themes, catalog `status`, license,
access rights, authors, contributors, contacts, funding sources, related
resources, and free-text spatial and temporal coverage. Each subclass adds its
own slots, and every concrete subclass pins its `resource_type` value.

| Class | Module | `resource_type` |
|---|---|---|
| `LiteratureResource` | `hew_publication` | `literature` |
| `DatasetResource` | `hew_core` | not pinned; normally `dataset` or `exposome_dataset` |
| `SurveyInstrument` | `hew_survey` | `survey_instrument` |
| `SurveyDataset` | `hew_survey` | `survey_dataset` |
| `GeospatialResource` | `hew_ext_geospatial` | `geospatial_dataset` |
| `CohortResource`, `SoftwareResource`, `ModelResource`, `ToolResource`, `ResourceCollection` | `hew_ext_resources` | `cohort`, `software_code_library`, `model`, `tool`, `resource_collection` |

- `LiteratureResource` adds DOI, PMID, PMCID, abstract, citation, publication
  type, journal, study objective, and review annotations. `publication_date` is
  shared by all resources and accepts `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.
- `DatasetResource` adds a `DataDictionary` of `Variable`s. `Distribution`s are
  shared by all resources so instruments can expose uploaded files as well.
- `status` is the catalog record lifecycle: `draft`, `active`, or `archived`.

See `hew-model/examples/publication_resource.yaml` for a publication record.

## 5. Agents, programs, and projects

`Agent` and its subclasses `Person`, `Organization`, and `SoftwareAgent` are in
the core. `authors` are inlined agents whose `agent_type` selects the class they
validate against; every other agent slot (`contributors`, `contacts`,
`affiliations`, `coded_by`, …) references agents by identifier.

The projects extension adds `Program`, `Project`, `FundingSource`, and
`AgentAssociation`:

```text
Program
  agent_associations -> AgentAssociation

Project
  part_of_programs   -> Program
  agent_associations -> AgentAssociation
  uses_resources     -> HEWResource
  produces_resources -> HEWResource

AgentAssociation
  agent           -> Person | Organization | SoftwareAgent
  associated_with -> Program | Project | Resource | Annotation | FundingSource
  role            -> AgentRoleEnum
```

The same person may be a principal investigator on one project, a curator of a
systematic-review annotation, and a maintainer of a software resource.
`AgentAssociation` lets each relationship carry a role, date range, source,
affiliation context, and contribution description, instead of a fixed slot per
role. See `hew-model/examples/example_program_project_people.yaml`.

## 6. Systematic-review coding

`HEWSystematicReviewAnnotation` records one coding pass over a literature
resource: coding scheme and version, coders and reviewers, coding method,
information source, reference type, evidence, confidence, and review status.

| Coding | Class | Slot |
|---|---|---|
| Exposure pathway | `ConceptAnnotation` | `exposure_annotations` |
| Health impact | `ConceptAnnotation` | `health_impact_annotations` |
| Special topic | `ConceptAnnotation` | `special_topic_annotations` |
| Geography | `GeographyAnnotation` | `geography_annotations` |
| Data, tools, and methods | `DataToolMethodAnnotation` | `data_tool_method_annotations` |

Annotations are catalog assertions about what a paper reports, not exposure
measurements or causal claims. Review-management values such as `Not Reported`,
`General Exposure`, or `Other Exposure, Specify` are coding states, not domain
entities, and must not be forced into ontology mappings. See
`hew-model/examples/example_literature_annotation.yaml`.

## 7. Surveys

```text
SurveyInstrument
  survey_constructs -> SurveyConstruct
  survey_questions  -> SurveyQuestion (ordered by position)
                         response_options   -> ResponseOption (code, label)
                         construct          -> SurveyConstruct
                         response_variables -> Variable
  target_population -> Population
  population_tags   -> controlled population concepts
  source_organization -> Organization
  distributions     -> Distribution

  administered_by, administration_mode, administration_time
  ease_of_use, electronic_data_capture, readability_level
  question_count, language, cde_integration
  adapted_from, research_program
  event_types, exposure_agents, health_impacts, special_topics

SurveyDataset (a DatasetResource)
  survey_instruments -> SurveyInstrument
  population         -> Population
  data_dictionary    -> DataDictionary -> Variable
```

`response_variables` links each question to the dataset variables that hold its
answers, so an instrument and the data collected with it can be joined.
`administration_mode` uses `AdministrationModeEnum`, `administered_by` uses
`AdministeredByEnum`, `ease_of_use` uses `EaseOfUseEnum`, and
`electronic_data_capture` uses `ElectronicDataCaptureEnum`. `response_type`
uses `ResponseTypeEnum`, and `language` is a BCP 47 tag. See
`hew-model/examples/survey_instrument.yaml` and `survey_dataset.yaml`.

## 8. Geospatial and exposure extension

Everything in this section validates against `hew-extended.yaml`.
`GeographicLocation` is the exception: it is in the core because geography
annotations use it. The design rationale is in the
[geospatial strategy](../hew-model/HEW%20Geospatial%20Metadata%20Enhancement%20Strategy.md).

### Places and extents

- **`GeographicLocation`**: a named or coordinate-defined place with a
  gazetteer identifier, coordinates, additional identifiers, and ENVO context.
  Explicit shapes belong on `SpatialExtent.geometry` or
  `SpatiotemporalExposure.exposure_geometry`.
- **`Geometry`**: an explicit footprint as WKT (GeoSPARQL/RDF interchange) or
  GeoJSON (API, web, and GIS interchange).
- **`BoundingBox`**: `west`, `south`, `east`, `north`, range-constrained.
- **`SpatialExtent`**: the overall footprint of a resource: named locations,
  geometry, bounding box, centroid, environmental context, resolution, and CRS.

`GeospatialResource` carries `spatial_extent`, `temporal_extent`,
`environmental_variables`, spatial resolution, and CRS metadata. Human-readable
fields are kept alongside their structured companions: `spatial_coverage` (every
resource), `spatial_resolution` and `coordinate_reference_system`,
`measured_variables` alongside `environmental_variables`, and
`geographic_locations`, `geographic_features`, and `spatial_text` on
`GeographyAnnotation`. New records should prefer `spatial_extent` and
`coordinate_reference_system_uri` when structured metadata is available.

### Environmental variables (EnVar profile)

`EnvironmentalVariable` specializes `Variable` as an HEW integration profile over
EnVar-style metadata; HEW does not copy or fork the EnVar micro-schema.

- `measured_property`: the environmental quantity or phenomenon;
- `measurement_method`: how it was measured or derived;
- `aggregation_method`: instantaneous, mean, maximum, cumulative, and related;
- `SpatialSupport`: the unit represented by one value;
- `TemporalSupport`: value resolution, aggregation window, and alignment;
- `concept_mappings`: ENVO, ECTO, CHEBI, LOINC, SNOMED CT, or related terms;
- `OMOPConceptBinding`: a standard, nonstandard, candidate, unevaluated, or
  missing (`vocabulary_gap`) OMOP mapping, kept separate from generic mappings so
  a gap can be recorded without inventing an identifier.

`SpatialSupport` is deliberately different from `SpatialExtent`:

| Concept | Meaning | Example |
|---|---|---|
| `spatial_extent` | Overall resource footprint | Continental United States |
| `spatial_support` | Area represented by one value | 1 km raster cell |
| Study geography | Research scope | Maricopa County |
| Observation location | Measurement site | Weather station |
| Exposure location | Assignment unit | Census tract |

ISO 8601 durations such as `PT1H`, `P1D`, and `P1M` are recommended for temporal
resolution and aggregation windows. Use ontology CURIEs for scientific concepts
and reserve enums for closed method, processing, alignment, and value-type
vocabularies.

### Exposure estimates and covariates

- **`SpatiotemporalExposure`**: a measured, modeled, derived, assigned, or
  summarized exposure estimate with exposure concept, source dataset, location
  or geometry, temporal extent, support, value semantics, and optional health or
  OMOP/Gaia context.
- **`CovariateCalculation`**: how a source dataset and variables became that
  estimate: software and version, function or workflow step, inputs and
  outputs, extraction, spatial-join, and temporal-join methods, buffer and CRS
  parameters, and aggregation and temporal-window semantics.

This covers Amadeus-derived covariates (reanalysis extraction, raster summaries,
monitor assignment, buffers, overlays, model predictions) without restricting
other derivation systems. See `hew-model/examples/example_spatiotemporal_exposure.yaml`
and `amadeus_covariate_calculation.yaml`.

### OMOP/Gaia external exposure linkage

`ExternalExposureLinkage` records readiness for OMOP/Gaia external-exposure
workflows without person-level data in the catalog: an exposure estimate and
OMOP concept binding, a location-history or cohort reference, exposure start and
end dates, spatial and temporal join methods, privacy-preserving geography, and
implementation notes. See `omop_gaia_external_exposure_linkage.yaml`.

### Example

This record validates against `hew-extended.yaml` as a `GeospatialResource`.

```yaml
id: HEWRES:example-heat-dataset
title: Example Daily Maximum Temperature Dataset
resource_type: geospatial_dataset
spatial_coverage: Continental United States
spatial_extent:
  bounding_box:
    west: -125.0
    south: 24.0
    east: -66.0
    north: 50.0
  coordinate_reference_system_uri: epsg:4326
environmental_variables:
  - id: HEWVAR:tmax
    name: tmax
    title: Daily Maximum Air Temperature
    data_type: float
    unit: UCUM:Cel
    measured_property: envo:01000254
    aggregation_method: maximum
    spatial_support:
      support_type: raster_grid_cell
      spatial_resolution: 1 km
      geometry_type: polygon
      coordinate_reference_system_uri: epsg:4326
    temporal_support:
      temporal_resolution: P1D
      aggregation_window: P1D
      temporal_alignment: end
    concept_mappings:
      - ecto:0000000
    omop_concept_binding:
      concept_status: vocabulary_gap
```

## 9. Identifiers and ontology alignment

Records use HEW-local identifiers first, as CURIEs whose prefixes are declared
in `modules/hew_core.yaml` (for example `HEWRES:` resources, `PERSON:` people,
`ORG:` organizations, `HEWVAR:` variables). External mappings are added
cautiously and explicitly as evidence improves.

Preferred vocabularies:

- ENVO for environmental context, materials, and processes;
- ECTO for exposure concepts;
- GeoNames, Wikidata, GAZ, GNIS, or other authoritative gazetteers for places;
- MONDO or DOID for diseases, and HPO for phenotypes where useful;
- OBI and IAO for information artifacts, study processes, and measurements;
- BioLink for broad biomedical categories and relationships;
- Schema.org, DCAT, Dublin Core, and PROV-O for catalog and provenance metadata.

HEW keeps its own classes, mapped to external ones, so it can support
commons-specific governance and curation while exporting useful RDF:

| HEW class | Mapped to |
|---|---|
| `LiteratureResource` | `schema:ScholarlyArticle`, close to `biolink:Publication` |
| `DatasetResource` | `schema:Dataset`, close to `dcat:Dataset` |
| `Distribution` | `dcat:Distribution` |
| `Person` | `schema:Person`, `biolink:Person`, `prov:Person` |
| `Organization` | `schema:Organization`, `biolink:Organization`, `prov:Organization` |
| `SoftwareAgent` | `prov:SoftwareAgent` |
| `Program`, `Project` | `schema:Project`, close to `prov:Activity` |
| `FundingSource` | `schema:Grant` |
| `AgentAssociation` | `prov:Association`, close to `schema:Role`, `schema:OrganizationRole`, `biolink:Association` |

These mappings live in the schema as `class_uri`, `slot_uri`, and `*_mappings`
and flow into the generated `hew.context.jsonld`, so HEW JSON-LD is already
readable as Schema.org, DCAT, Dublin Core, and PROV-O RDF.

## 10. Projections

The LinkML model is the source of truth. External systems are purpose-specific
projections that preserve HEW identifiers; none of them is the source model.

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

| Target | Primary use | Status |
|---|---|---|
| CAFE Dataverse | Searchable repository metadata blocks | Implemented for publications ([accel-dataverse-hew](https://github.com/NIEHS/accel-dataverse-hew), `assets/crosswalks/publication/v1/`) |
| Schema.org, DCAT, Dublin Core, PROV-O | Web discovery and catalogs | Via the generated JSON-LD context |
| DataCite | DOI registration | Design note: `mappings/datacite/` |
| STAC | Geospatial collections, extents, and assets | Design note: `mappings/stac/` |
| GeoSPARQL/RDF | Geometry, topology, and knowledge graphs | Via `geo:` slot URIs in the context |
| ROBOKOP/Translator | Selected, policy-controlled graph edges | Design note: `mappings/kg/` |
| OMOP/Gaia, EnVar, Amadeus | External-exposure workflows | Design note: `mappings/omop_gaia/` |

Files under `mappings/` are design notes for projections not yet implemented; no
code reads them.

### Dataverse

Dataverse metadata blocks expose a curated, searchable subset: resource type,
exposure and health-impact concepts, geography, time, environmental variables,
access, license, provenance, and external links. Nested geometries, derivation
graphs, role associations, and rich ontology context stay in the canonical
model, and the original JSON-LD record is deposited as a preservation
attachment. The block design and field-level guidance are in
`assets/metadata_blocks_guidance.md` in accel-dataverse-hew.

### Knowledge-graph export

Initial exports represent catalog edges: a resource about an exposure or health
impact, scoped to a location, or with an environmental variable; a tool that
computes a variable; software that implements a covariate calculation; a project
that produces or uses a resource; and an agent that contributes to a resource or
project. The edge list is in `mappings/kg/hew_kg_edges.yaml`.

### Catalog assertions vs scientific assertions

The catalog records statements such as "this paper studies wildfire smoke and
asthma" or "this dataset provides daily heat-index values." These are not causal
claims. Every projection, and especially a knowledge-graph export, must keep
resource-topic tagging distinct from claims about causation, association
strength, or clinical effect. Causal or clinical-effect edges require a
separate, explicitly curated assertion model and must not be inferred from
review coding or resource tags.

## 11. Version 2.0.0 changes

Version 2.0.0 restructures the 1.3.0 single-file schema into the core and
extensions above. Breaking changes for existing records:

- `HEWResource` is abstract and carries only shared descriptive, rights, and
  attribution slots. Type-specific slots (for example `doi`, `programming_language`,
  `spatial_extent`) are accepted only on the matching subclass.
- `resource_type` is required, and each resource class pins its value.
  `program`, `project`, `funding_source`, `data_dictionary`, `tutorial`, and
  `notebook` are no longer resource types; `survey_dataset` and
  `resource_collection` were added.
- `status` on resources uses `CatalogStatusEnum` (`draft`, `active`, `archived`);
  `ProjectStatusEnum` applies only to programs and projects.
- `publication_date` is shared by all resources and accepts `YYYY`, `YYYY-MM`,
  or `YYYY-MM-DD`.
- `authors` are inlined agents with a required `agent_type`.
- `ExposureAnnotation`, `HealthImpactAnnotation`, and `SpecialTopicAnnotation` are
  merged into `ConceptAnnotation`; the slot names are unchanged.
- Surveys: questions have `position`, `ResponseTypeEnum` `response_type`, coded
  `response_options`, and `response_variables` linking to dataset variables.
  `administration_mode` is an enum, `language` is a BCP 47 tag, and
  `SurveyDataset.population_or_cohort` is renamed `population`.
- Removed duplicates: resource `name` (use `title`), `produced_by_projects`,
  `used_by_projects`, `has_projects` (use the project-side slots),
  `spatiotemporal_exposures` (use `SpatiotemporalExposure.source_dataset`),
  `principal_investigators` and `participating_organizations` (use
  `agent_associations` with a role), `Person.roles`, `Organization.members`
  (inverse of `affiliations`), `FundingSource.sponsor` (use
  `sponsoring_organizations`), `Variable.mappings` (use `concept_mappings`), and
  `SurveyDataset.variables` (use `data_dictionary`).
- RDF property collisions removed: `title` maps to `dcterms:title`;
  `spatial_extent`, `part_of_programs`, and `award_number` no longer share a
  `slot_uri` with another slot.

## 12. Roadmap

The core covers Phase 1. Phases 2–5 are drafted as extension modules; each moves
into active use, and into the core where needed, when a catalog workflow depends
on it. Remaining duplicate fields in an extension are cleaned up at that point.

1. **Core catalog and Dataverse**: publications with review annotations, survey
   instruments and datasets, authorship, the Dataverse publication projection,
   and JSON-LD round-tripping. Grow survey support from real instruments.
2. **Exposome compatibility**: EnVar-aligned variables, structured temporal and
   spatial resolution, processing levels, and ENVO/ECTO/OMOP mappings.
3. **Covariate workflows**: tools, collections, Amadeus and other software, and
   derivation methods, parameters, source data, joins, temporal windows, CRS,
   and outputs.
4. **Optional exposure estimates**: `SpatiotemporalExposure` linked to
   variables, locations, intervals, methods, and sources.
5. **External exposure linkage**: `ExternalExposureLinkage` for OMOP/Gaia
   readiness without patient-level data.
6. **Knowledge-graph export**: selected catalog edges to RDF/JSON-LD and
   ROBOKOP/Translator views, preserving the tagging-versus-causal distinction.

Ontology and gazetteer mapping practices, and the DataCite, STAC, GeoSPARQL, and
OMOP/Gaia projections, develop alongside these phases.

## 13. Related documents

- [Geospatial Metadata Enhancement Strategy](../hew-model/HEW%20Geospatial%20Metadata%20Enhancement%20Strategy.md):
  standards roles and design rationale behind section 8.
- [HEW Resource Library Coding Guide](HEW%20Resource%20Library%20Coding%20Guide.pdf):
  the coding scheme modeled in section 6.
- [Model package README](../hew-model/README.md): files in `hew-model/`.
- [Contributing](../CONTRIBUTING.md): schema change rules and development commands.
- [accel-dataverse-hew](https://github.com/NIEHS/accel-dataverse-hew): the
  Dataverse crosswalk, metadata blocks, and block guidance.
