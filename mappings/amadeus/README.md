# HEW alignment with Amadeus

All definitions, validation and mappings live in HEW. Amadeus remains unchanged.
`linkml_to_amadeus.yaml` is a transformation specification for adapter authors;
it does not execute transformations or promise lossless round trips.

## Dependency direction

```text
hew.yaml -> existing HEW extension modules -> hew_core -> linkml:types
profiles/hew_amadeus.yaml -> hew_ext_geospatial -> hew_core -> linkml:types
```

Core owns GeographicLocation, Geometry, BoundingBox, SpatialExtent,
TemporalExtent, resolution value classes, shared slots and calendar/duration
types. The geospatial extension owns grids, value supports, variable deliveries
and exposure classes. Core never imports an extension or profile. Amadeus is
referenced only through mapping URIs. Every schema is checked for cycles,
duplicate definitions and unresolved class-slot ranges in
`tests/test_amadeus_alignment.py`.

## Metadata semantics

Optional structured extents now apply to every HEW resource and Distribution.
Coverage strings remain display descriptions. Geographic coordinates and
BoundingBox are always WGS84; extent and geometry CRS values do not change that.
Native projected coordinates belong in Geometry or GridDefinition. An explicit
geometry CRS overrides its parent extent CRS. GeoJSON is WGS84 longitude/latitude.
West greater than east denotes an antimeridian-crossing box; adapters must split
or otherwise explicitly handle it when constructing a geometry.

GridDefinition has a stable ID, native axis spacing, units, dimensions, outer
corner origin, row direction, projection and optional vertical levels. HEW embeds
definitions; export extracts one Amadeus entity per stable grid ID. Repeated IDs
must describe the same grid. Positive axis spacing is a magnitude. Rotated or
curvilinear grids require an external definition; these fields do not describe
them fully. CRS normalization accepts authority strings and OGC definition URIs.
Numeric SRIDs are checked automatically only for EPSG; other authorities need
an explicit lookup. Full projection definitions are retained even when they
cannot be exported to Amadeus's authority-code CRS field.

Dataset spatial_support and temporal_support are defaults. Each explicit
EnvironmentalVariableDelivery support object replaces the corresponding default
as a whole. EnvironmentalVariable can remain a legacy embedded description, or
serve as the quantity identity referenced by a delivery. The containing dataset
provides the Amadeus Product reference during export. Legacy variable support
must be reconciled explicitly before exporting through the strict profile.

temporal_resolution exclusively uses Amadeus's TemporalResolutionEnum:
instantaneous, subhourly, hourly, three_hourly, daily, monthly, seasonal, annual,
multi_year_epoch and timeless. It maps directly to Amadeus temporal_resolution.
There is no companion category or duration-valued resolution field. Duration
strings such as P1D, PT1H and P3D are invalid resolution values. Aggregation
windows, update cadence and latency continue to use ISO 8601 durations.
Calendar values and day boundaries use matching controlled values.

Datetime coverage uses [start, end). coverage_status distinguishes bounded,
ongoing, unknown and timeless intervals. Distribution coverage represents the
actual asset; dataset coverage represents the whole product. reference_time is
forecast initialization, never a replacement for valid time. Publication dates,
update cadence and latency remain separate facts.

Amadeus product coverage fields are dates and do not specify end-date
inclusivity. Export requires an explicit date-boundary policy; converting them
back into datetimes is not lossless without the original precision, timezone
and policy. Non-Gregorian dates require source calendar adapters; Python's
datetime checker cannot validate dates such as a 360-day-calendar February 30.

## Validation and migration

Validate structural constraints against `hew-model/schema/profiles/hew_amadeus.yaml`
as `AmadeusGeospatialResource`, then call
`hew_model.amadeus.validate_amadeus_metadata(record)` for semantic checks.
The function returns errors without changing the record. Schema validation must
run first. The general HEW schema does not require complete Amadeus metadata.

Resolution values must use the enum; duration-valued resolution is not supported.
BoundingBox requires all four bounds. Old end-of-day examples have been migrated
to the following midnight for exclusive interval semantics; other existing
records require the same review, never an automatic one-second adjustment.

HEW mappings use `https://w3id.org/niehs/amadeus/`. Existing Amadeus references
to HEW use a different namespace from HEW's term namespace; this crosswalk
does not depend on those reverse annotations. Class correspondences with
different scopes use close_mappings. No changes to Amadeus are needed.
