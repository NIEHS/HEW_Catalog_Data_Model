# Amadeus alignment

Amadeus-derived environmental covariates are represented with
`SpatiotemporalExposure` and `CovariateCalculation` from the geospatial
extension; records validate against `hew-model/schema/hew-extended.yaml`.

`SpatiotemporalExposure` identifies the exposure concept, source dataset,
location or geometry, temporal extent, support, value semantics, and optional
OMOP/Gaia linkage. Its `calculation_method` points to a `CovariateCalculation`
that can record:

- the software and version;
- the function or workflow step;
- input resources and output variables;
- extraction, spatial-join, and temporal-join methods;
- buffer and CRS parameters; and
- aggregation and temporal-window semantics.

This supports reanalysis extraction, raster summaries, monitor assignment,
buffer operations, spatial overlays, and model predictions. Amadeus is an
important workflow profile, not a restriction on other derivation systems.

See `hew-model/examples/example_spatiotemporal_exposure.yaml` for a complete
Amadeus-style heat covariate record.
