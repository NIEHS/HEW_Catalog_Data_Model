# Exposome alignment

The HEW model is an integration profile for exposome-facing catalog metadata.
It keeps distinct objects for place, geometry, environmental context, exposure
semantics, variables, derivation methods, temporal coverage, and linkage context.

## Exposure objects

- `ExposureAnnotation` records a literature-review coding assertion. Values such
  as `not_reported` and broad geography codes describe what a paper reports;
  they are not exposure measurements.
- `EnvironmentalVariable` describes what a variable represents, how it was
  measured or derived, and its spatial and temporal support.
- `SpatiotemporalExposure` describes a measured, modeled, assigned, or summarized
  exposure estimate with explicit place, geometry, interval, value semantics,
  derivation, source, and optional health or OMOP/Gaia context.
- `CovariateCalculation` records the computational method used to create a
  derived exposure covariate.

The existing `spatial_coverage`, `temporal_coverage`, `spatial_resolution`,
`coordinate_reference_system`, and `measured_variables` fields remain valid
compatibility fields. New records should add structured companions when the
metadata is available.

## Interoperability

ENVO is preferred for environmental context, ECTO for exposure concepts, and
GeoNames/Wikidata/GAZ/GNIS or other authoritative identifiers for places. The
profile can project to EnVar, STAC, DCAT, GeoSPARQL, PROV-O, and OMOP/Gaia
workflows without treating any one standard as the complete HEW model.
