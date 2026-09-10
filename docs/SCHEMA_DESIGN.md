# HEW Data Commons Schema Design

## Purpose and scope

The Health and Extreme Weather (HEW) Data Commons model is a LinkML schema for
cataloging literature, datasets, cohorts, surveys, software, models, geospatial
resources, environmental variables, projects, and provenance-bearing
annotations. The canonical schema is `hew-model/schema/hew-geospatial.yaml`.

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

`HEWResource` is the root class for literature, datasets, cohorts, surveys,
software, models, and related catalog resources. `DatasetResource` supports
legacy human-readable metadata as well as structured data dictionaries and
environmental variables. `GeospatialResource` adds spatial resolution and CRS
metadata.

`HEWSystematicReviewAnnotation` records a coding pass over a literature
resource. Exposure, health impact, geography, data-tool/method, and special
topic annotations preserve coding context, evidence, confidence, and review
status. Review coding values such as `not_reported` remain distinct from
real-world domain concepts.

The coordination layer represents `Agent`, `Person`, `Organization`,
`SoftwareAgent`, `Program`, `Project`, `FundingSource`, and
`AgentAssociation`. Role-bearing associations preserve who created, reviewed,
funded, maintained, or used a resource without adding dozens of fixed slots.

## Geospatial model

The schema introduces four reusable resource-geography objects:

### `GeographicLocation`

A named or coordinate-defined place associated with a resource, study, exposure,
observation, project, or annotation. It may contain a gazetteer identifier,
coordinates, geometry, additional identifiers, and ENVO context.

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

The legacy `spatial_coverage` and `coordinate_reference_system` strings remain
valid for backward compatibility. New records should prefer `spatial_extent`
and `coordinate_reference_system_uri` when structured metadata is available.

## Environmental-variable model

`EnvironmentalVariable` specializes `Variable` with EnVar-aligned metadata:

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

## Backward compatibility

The geospatial enhancement is additive. Existing fields remain supported:
`spatial_coverage`, `spatial_resolution`, `coordinate_reference_system`,
`measured_variables`, `geographic_locations`, `geographic_features`,
`spatial_text`, and generic `Variable`. New records may progressively add
structured extents, locations, geometries, environmental variables, support
objects, semantic mappings, and OMOP status.

## Module organization

The combined schema is the validation entry point. Schema fragments are kept in
`hew-model/schema/modules/` for the intended future split:

```text
hew_core.yaml
hew_literature.yaml
hew_review_coding.yaml
hew_resource_types.yaml
hew_agents_projects.yaml
hew_geospatial.yaml
```

The geospatial module owns the location, geometry, extent, support, temporal,
environmental-variable, and OMOP binding structures. The core module owns the
generic `Variable` and `DataDictionary` structures used by those additions.

## Example integrated resource

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

1. Validate the core geospatial objects and geographic constraints.
2. Validate EnVar-aligned variable semantics and OMOP status handling.
3. Establish ontology and gazetteer mapping practices.
4. Add explicit exposure, study-geography, observation-location, and temporal relationships.
5. Develop GeoSPARQL, STAC, DCAT, DataCite, Schema.org, and OMOP/Gaia projections.

