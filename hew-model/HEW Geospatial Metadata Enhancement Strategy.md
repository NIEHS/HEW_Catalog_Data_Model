# HEW Geospatial Metadata Enhancement Strategy

## Overview

The HEW LinkML schema is being extended to support richer, machine-actionable geospatial metadata while preserving compatibility with the existing ontology and systematic-review model.

The goal is to support geospatial discovery, spatial querying, environmental context, and exposure analysis across datasets, literature, models, and other HEW resources without forcing all geographic information into a single representation.

The enhanced strategy separates four related but distinct concerns:

1. **Named geographic places**
2. **Spatial geometry and extent**
3. **Environmental and exposure semantics**
4. **Dataset and catalog interoperability**

This provides a cleaner foundation for integration with Biolink, ENVO, ECTO, GeoSPARQL, STAC, DCAT, DataCite, and Schema.org.

---

## Core Design Principle

Geospatial metadata should distinguish:

```text
WHAT PLACE?
    GeographicLocation
        |
WHERE EXACTLY?
    Geometry / SpatialExtent
        |
WHAT KIND OF ENVIRONMENT?
    ENVO environmental context
        |
WHAT EXPOSURE OCCURRED?
    ECTO exposure concepts
```

No single ontology or metadata standard should be expected to represent all of these concerns.

---

# Standards and Ontology Roles

## Biolink Model

Biolink provides the biomedical knowledge-graph semantics for geographic entities.

HEW geographic locations can map to:

```text
biolink:GeographicLocation
```

and, where temporal context is important:

```text
biolink:GeographicLocationAtTime
```

Biolink provides the semantic connection between geographic information and the broader biomedical knowledge graph.

Typical uses include:

- study locations
- participant locations
- exposure locations
- healthcare or population locations
- named geographic areas

---

## GeoSPARQL

GeoSPARQL provides the primary semantic model for explicit geometry.

It distinguishes a geographic **feature** from its geometric representation and supports spatial operations and relationships.

HEW uses concepts such as:

```text
geo:Geometry
geo:hasGeometry
geo:asWKT
geo:asGeoJSON
```

Geometry types may include:

```text
Point
MultiPoint
LineString
MultiLineString
Polygon
MultiPolygon
```

GeoSPARQL provides the foundation for future operations such as:

```text
within
contains
intersects
overlaps
touches
distance
```

This makes HEW spatial metadata suitable for RDF stores and spatially enabled knowledge graphs.

---

## ENVO

ENVO should describe the **environmental context of a geographic location**, rather than its coordinates or geometry.

Examples include concepts related to:

```text
urban environments
wetlands
forests
deserts
freshwater environments
coastal environments
built environments
grasslands
```

Instead of relying exclusively on local string enums such as:

```yaml
geographic_features:
  - wetland
  - urban
```

HEW can progressively support ontology identifiers:

```yaml
environmental_context:
  - ENVO:...
```

This enables richer semantic reasoning and interoperability.

The existing `GeographicFeatureEnum` can remain for backward compatibility and systematic-review coding.

---

## ECTO

ECTO represents **environmental exposure concepts**.

ECTO should therefore be connected primarily to HEW exposure annotations rather than used to represent geographic locations themselves.

Conceptually:

```text
ExposureAnnotation
    |
    +-- exposure concept        ECTO
    |
    +-- environmental context  ENVO
    |
    +-- location               GeographicLocation
    |
    +-- geometry               GeoSPARQL
    |
    +-- time                   temporal extent
```

This is particularly useful for HEW use cases involving:

- extreme heat
- wildfire smoke
- air pollution
- flooding
- hurricanes
- drought
- extreme cold
- environmental contaminants

---

# Structured Geographic Model

The enhanced schema introduces reusable geographic objects instead of relying only on free-text spatial coverage.

The primary classes are:

```text
GeographicLocation
Geometry
SpatialExtent
BoundingBox
```

---

## GeographicLocation

`GeographicLocation` represents a named or identifiable place.

Example:

```yaml
location_id: geonames:5303754
name: Maricopa County
location_type: administrative_area
latitude: 33.35
longitude: -112.49
```

Locations may reference external geographic authority systems such as:

- GeoNames
- Wikidata
- GAZ
- Census geographic identifiers
- other authoritative gazetteers

A location can also reference ENVO concepts describing its environmental context.

---

## Geometry

`Geometry` represents the explicit spatial shape of a location or resource.

Supported serializations include:

```yaml
wkt: "POLYGON((...))"
```

and:

```yaml
geojson: |
  {
    "type": "Polygon",
    "coordinates": [...]
  }
```

These representations serve different purposes:

- **GeoJSON** is convenient for APIs, web applications, and GIS tools.
- **WKT / GeoSPARQL** is convenient for RDF knowledge graphs and spatial databases.

The schema may support either or both.

---

## SpatialExtent

`SpatialExtent` describes the geographic footprint of a dataset or other resource.

It may include:

```text
named locations
geometry
bounding box
centroid
spatial resolution
coordinate reference system
environmental context
```

Example:

```yaml
spatial_extent:
  named_locations:
    - location_id: geonames:5303754
      name: Maricopa County

  bounding_box:
    west: -113.33
    south: 32.50
    east: -111.04
    north: 34.05

  geometry:
    geometry_type: polygon
    wkt: "POLYGON((...))"

  coordinate_reference_system_uri: epsg:4326
```

---

## BoundingBox

A bounding box provides a simple spatial extent suitable for indexing and search.

```yaml
bounding_box:
  west: -113.33
  south: 32.50
  east: -111.04
  north: 34.05
```

Longitude and latitude constraints can be validated directly in LinkML.

---

# Coordinate Reference Systems

The existing schema represents coordinate reference systems as strings.

For backward compatibility, this remains supported.

The enhancement adds a normalized identifier form:

```yaml
coordinate_reference_system_uri: epsg:4326
```

The preferred long-term representation is a CURIE or URI corresponding to an OGC/EPSG coordinate reference system.

This permits gradual migration from records such as:

```yaml
coordinate_reference_system: "WGS84"
```

toward normalized identifiers.

---

# Dataset Spatial Coverage

The existing HEW field:

```yaml
spatial_coverage:
  range: string
```

remains useful for human-readable descriptions.

It should not, however, be the only source of spatial information.

The enhanced model uses both:

```yaml
spatial_coverage: "Maricopa County, Arizona"
```

and:

```yaml
spatial_extent:
  ...
```

This provides:

- human-readable metadata
- precise geometry
- spatial indexing
- semantic identifiers
- GIS interoperability

---

# Systematic Review Geography

The existing `GeographyAnnotation` model remains useful for systematic-review coding.

It currently captures broad concepts such as:

```text
United States
Europe
Asia
urban
wetland
forest
coastal
```

These categories should remain available because they support consistent review coding and legacy data.

Structured geographic information should be added alongside them.

For example:

```yaml
geography_annotations:
  - geographic_locations:
      - united_states

    geographic_features:
      - urban

    locations:
      - location_id: geonames:5303754
        name: Maricopa County
        geographic_identifiers:
          - geonames:5303754
        environmental_context:
          - ENVO:...

    spatial_text: "Maricopa County, Arizona"
```

This preserves three distinct representations:

```text
review coding
    united_states

original evidence
    "Maricopa County, Arizona"

machine-actionable geography
    GeoNames identifier + geometry + ENVO
```

These should not be collapsed into a single field.

---

# Different Types of Geographic Relationships

The enhanced strategy also recognizes that not every geographic relationship means the same thing.

For example:

```text
dataset spatial coverage
study population geography
observation location
exposure location
model domain
```

may all refer to different geographic areas.

Future extensions should therefore support explicit relationships such as:

```text
spatial_extent
study_geography
observation_location
exposure_location
```

rather than treating every location as generic `spatial_coverage`.

This distinction will become particularly important for exposure modeling and environmental health studies.

---

# Spatial Resolution

Spatial resolution should eventually distinguish quantitative raster/grid resolution from administrative or categorical geographic resolution.

Examples of quantitative resolution:

```text
1 km
250 m
30 arc-second
```

Examples of administrative resolution:

```text
state
county
ZIP code
census tract
block group
```

These represent different concepts.

A future HEW model could therefore distinguish:

```text
spatial_resolution
administrative_resolution
```

with quantitative resolution represented by a structured value and unit.

---

# STAC Compatibility

STAC is particularly well aligned with HEW geospatial resources.

Conceptually:

```text
HEW DatasetResource      ~ STAC Collection
HEW GeospatialResource   ~ STAC Collection or Item
HEW Distribution         ~ STAC Asset
HEW SpatialExtent        ~ STAC spatial extent
HEW temporal_coverage    ~ STAC temporal extent
```

A STAC-compatible representation would make HEW resources easier to integrate with modern geospatial catalogs and APIs.

STAC support would enable operations such as:

```text
search by bounding box
search by geometry intersection
search by date range
discover raster/vector assets
retrieve cloud-hosted geospatial resources
```

HEW does not need to become a STAC schema. Instead, the internal model should be designed so that STAC import and export are straightforward.

---

# DataCite Compatibility

DataCite provides a useful minimum interchange model for published datasets.

Its geographic model includes:

```text
place
point
box
polygon
```

HEW's `SpatialExtent`, `BoundingBox`, and `Geometry` structures can therefore be mapped naturally into DataCite metadata.

This is particularly useful when HEW resources have DOIs.

---

# Schema.org and DCAT

HEW already maps resources to Schema.org and DCAT concepts.

These mappings should continue to support broad dataset discovery.

Schema.org is useful for web-oriented metadata such as:

```text
spatialCoverage
Place
GeoCoordinates
GeoShape
```

DCAT remains appropriate for dataset catalogs and distributions.

GeoSPARQL should provide the more precise spatial semantics underneath these discovery-oriented mappings.

---

# Recommended Interoperability Stack

The enhanced HEW geospatial model can be viewed as:

```text
                         HEW LinkML
                             |
          +------------------+------------------+
          |                  |                  |
       Biolink             ENVO/ECTO         GeoSPARQL
       biomedical          environment       geometry
       semantics           + exposure        + topology
          |                                      |
          +------------------+-------------------+
                             |
                        SpatialExtent
                             |
               +-------------+-------------+
               |             |             |
             STAC           DCAT        Schema.org
               |             |             |
            GIS/API        catalogs     web discovery
               |
            DataCite
               |
         DOI metadata
```

This approach allows HEW to maintain one coherent internal model while supporting several external representations.

---

# Backward Compatibility Strategy

The enhanced schema is intentionally additive.

Existing fields remain valid:

```text
spatial_coverage
coordinate_reference_system
GeographicLocationEnum
GeographicFeatureEnum
spatial_text
```

New structured fields are added alongside them.

This allows existing HEW metadata to continue working while new records progressively adopt richer geospatial metadata.

A migration can therefore proceed incrementally:

```text
Phase 1
free text + legacy enums

Phase 2
named geographic identifiers

Phase 3
coordinates and bounding boxes

Phase 4
explicit geometry

Phase 5
ENVO/ECTO semantic enrichment

Phase 6
STAC / GeoSPARQL spatial services
```

---

# Example Target Record

A mature HEW geospatial dataset might eventually look like:

```yaml
id: HEWRES:example-heat-dataset
title: Maricopa County Extreme Heat Dataset
resource_type: geospatial_dataset

spatial_coverage: "Maricopa County, Arizona"

spatial_extent:
  named_locations:
    - location_id: geonames:5303754
      name: Maricopa County
      location_type: administrative_area
      latitude: 33.35
      longitude: -112.49
      geographic_identifiers:
        - geonames:5303754
      environmental_context:
        - ENVO:...

  bounding_box:
    west: -113.33
    south: 32.50
    east: -111.04
    north: 34.05

  geometry:
    geometry_type: polygon
    wkt: "POLYGON((...))"
    coordinate_reference_system_uri: epsg:4326

  spatial_resolution: "1 km"
  coordinate_reference_system_uri: epsg:4326

temporal_coverage: "2020-01-01/2025-12-31"
```

---

# Recommended Next Steps

The geospatial patch establishes the basic spatial object model.

The next logical enhancement is a **spatiotemporal exposure model** connecting:

```text
ECTO exposure
    |
    +-- exposure location
    +-- exposure geometry
    +-- environmental context / ENVO
    +-- temporal interval
    +-- measured variable
    +-- unit
    +-- population or cohort
```

This would provide a strong semantic foundation for representing extreme-weather exposures and linking them directly to health outcomes.

In practical terms, the HEW model would then support queries such as:

```text
Find studies involving extreme heat exposure
within Maricopa County
between 2018 and 2025
in urban environments
using datasets with <= 1 km spatial resolution.
```

That is the major payoff of moving from simple geographic strings to structured, ontology-backed geospatial metadata.