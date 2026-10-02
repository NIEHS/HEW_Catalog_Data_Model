# HEW Data Commons Schema Design

## Purpose and scope

The Health and Extreme Weather (HEW) Data Commons model is a LinkML schema for
cataloging resources relevant to health and extreme weather. The core schema,
`hew-model/schema/hew.yaml`, covers publications with systematic-review coding
and survey instruments with their datasets. `hew-model/schema/hew-extended.yaml`
adds extension modules for geospatial and exposure metadata, programs and
projects, and cohort, software, model, tool, and collection resources.

The model begins with systematic-review coding and remains extensible enough to
support exposure-health research and machine-actionable environmental datasets.
The coding guide is a profile over a general resource model, not the whole
ontology.

## Model layers

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

## Resource and annotation model

`HEWResource` is the abstract root for every cataloged resource. It carries only
the descriptive, rights, and attribution slots shared by all resource types:
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

`DatasetResource` adds a `DataDictionary` of `Variable`s and `Distribution`s.
`authors` are inlined `Agent`s whose `agent_type` (`Person`, `Organization`, or
`SoftwareAgent`) selects the class they validate against; other agent slots
reference agents by identifier.

`HEWSystematicReviewAnnotation` records a coding pass over a literature
resource. Exposure, health-impact, and special-topic coding share one
`ConceptAnnotation` class, distinguished by the slot that holds them;
geography and data-tool/method coding have their own classes. Annotations
preserve coding context, evidence, confidence, and review status. Review coding
values such as `not_reported` remain distinct from real-world domain concepts.

The projects extension represents `Program`, `Project`, `FundingSource`, and
`AgentAssociation`. Role-bearing associations record who led, curated,
participated in, or funded work without adding a fixed slot per role.

## Survey model

```text
SurveyInstrument
  survey_constructs -> SurveyConstruct
  survey_questions  -> SurveyQuestion (ordered by position)
                         response_options   -> ResponseOption (code, label)
                         construct          -> SurveyConstruct
                         response_variables -> Variable
  target_population -> Population

SurveyDataset (a DatasetResource)
  survey_instruments -> SurveyInstrument
  population         -> Population
  data_dictionary    -> DataDictionary -> Variable
```

`response_variables` links each question to the dataset variables that hold its
answers, so an instrument and the data collected with it can be joined.
`administration_mode` uses `AdministrationModeEnum`, `response_type` uses
`ResponseTypeEnum`, and `language` is a BCP 47 tag.

## Geospatial model

`GeographicLocation` is in the core because geography annotations use it. The
other geospatial classes are in the `hew_ext_geospatial` extension, where
`GeospatialResource` carries `spatial_extent`, `temporal_extent`,
`environmental_variables`, spatial resolution, and CRS metadata.

### `GeographicLocation`

A named or coordinate-defined place associated with a resource, study, exposure,
observation, project, or annotation. It may contain a gazetteer identifier,
coordinates, additional identifiers, and ENVO context. Explicit shapes belong on
`SpatialExtent.geometry` or `SpatiotemporalExposure.exposure_geometry`.

### `Geometry`

An explicit spatial footprint represented as WKT or GeoJSON. GeoJSON supports
API, web, and GIS interchange; WKT supports GeoSPARQL and RDF interchange.

### `BoundingBox`

An axis-aligned search/indexing extent with `west`, `south`, `east`, and `north`
coordinates. Longitude and latitude are constrained to valid ranges.

### `SpatialExtent`

The overall geographic footprint of a resource. It can contain named locations,
geometry, a bounding box, centroid, environmental context, spatial resolution,
and a normalized CRS identifier.

Free-text `spatial_coverage` is available on every resource.
`GeospatialResource` also accepts the free-text `coordinate_reference_system`;
new records should prefer `spatial_extent` and `coordinate_reference_system_uri`
when structured metadata is available.

## Environmental-variable model

`EnvironmentalVariable` (geospatial extension) specializes `Variable` with
EnVar-aligned metadata:

- `measured_property` identifies the primary environmental quantity or phenomenon;
- `measurement_method` identifies how it was measured or derived;
- `aggregation_method` describes instantaneous, mean, maximum, cumulative, and related summaries;
- `SpatialSupport` describes the unit represented by one value;
- `TemporalSupport` describes value resolution, aggregation window, and alignment;
- `concept_mappings` connects to ENVO, ECTO, CHEBI, LOINC, SNOMED CT, or related vocabularies;
- `OMOPConceptBinding` records a standard, nonstandard, candidate, unevaluated, or missing mapping.

`SpatialSupport` is deliberately different from dataset-level `SpatialExtent`:

| Concept | Meaning | Example |
|---|---|---|
| `spatial_extent` | Overall resource footprint | Continental United States |
| `spatial_support` | Area represented by one value | 1 km raster cell |
| Study geography | Research scope | Maricopa County |
| Observation location | Measurement site | Weather station |
| Exposure location | Assignment unit | Census tract |

ISO 8601 durations such as `PT1H`, `P1D`, and `P1M` are recommended for
temporal resolution and aggregation windows. OMOP bindings remain separate from
generic ontology mappings so a vocabulary gap can be recorded without inventing
an identifier.

`SpatiotemporalExposure` combines these concerns for a measured, modeled,
derived, assigned, or summarized exposure estimate. `CovariateCalculation`
records how a source dataset and its variables were transformed into that
estimate, while `TemporalExtent` captures the structured start/end interval.

## Interoperability

HEW LinkML provides structural validation. External standards are projections:

- BioLink and gazetteers support place identity and biomedical graph alignment.
- GeoSPARQL, GeoJSON, WKT, and EPSG/OGC identifiers support geometry operations.
- ENVO supplies environmental context; ECTO supplies exposure semantics.
- EnVar supplies the environmental-variable metadata pattern.
- STAC supports geospatial collection, item, extent, and asset discovery.
- DCAT supports generic dataset and distribution catalogs.
- DataCite and Schema.org support DOI and web-facing metadata exports.
- OMOP/Gaia support clinical and external-exposure workflows.

## Compatibility fields

Version 2.0.0 is a breaking release; see the changes listed below. Within the
geospatial extension, human-readable fields are kept alongside their structured
companions: `spatial_resolution` and `coordinate_reference_system` on
`GeospatialResource`, `measured_variables` alongside `environmental_variables`,
and `geographic_locations`, `geographic_features`, and `spatial_text` on
`GeographyAnnotation`. New records may progressively add structured extents,
locations, geometries, environmental variables, support objects, semantic
mappings, and OMOP status.

## Module organization

The model has two validation entry points in `hew-model/schema/`:

- `hew.yaml` is the **core**: publications, systematic-review coding, surveys,
  agents, variables, and data dictionaries.
- `hew-extended.yaml` imports the core plus the extension modules.

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

Every module imports `hew_core`; each class and slot is defined in exactly one
module. New capabilities should be added as extension modules rather than as
slots on `HEWResource`.

## Version 2.0.0 changes

Version 2.0.0 restructures the 1.3.0 single-file schema into the core and
extensions above. Breaking changes for existing records:

- `HEWResource` is abstract and carries only shared descriptive, rights, and
  attribution slots. Type-specific slots (for example `doi`, `programming_language`,
  `spatial_extent`) are accepted only on the matching subclass.
- `resource_type` is required, and each resource class pins its value
  (`LiteratureResource` requires `literature`, `SurveyDataset` requires
  `survey_dataset`, `GeospatialResource` requires `geospatial_dataset`).
  `program`, `project`, `funding_source`, `data_dictionary`, `tutorial`, and
  `notebook` are no longer resource types; `survey_dataset` and
  `resource_collection` were added.
- `status` on resources uses `CatalogStatusEnum` (`draft`, `active`, `archived`);
  `ProjectStatusEnum` applies only to programs and projects.
- `publication_date` accepts `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.
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

## Example integrated resource

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

## Implementation priorities

1. Stabilize the core: publication and survey records, their Dataverse
   projection, and JSON-LD round-tripping.
2. Grow survey support from real instruments: constructs, response scales, and
   question-to-variable links.
3. Promote extension content into the core only when a catalog workflow needs
   it, cleaning up its remaining duplicate fields at that point.
4. Establish ontology and gazetteer mapping practices.
5. Develop GeoSPARQL, STAC, DCAT, DataCite, Schema.org, and OMOP/Gaia
   projections from the extensions.
