# Schema overview

The HEW schema is a canonical resource knowledge base. `HEWResource` is a
cataloged information or resource entity; it is not necessarily a data-bearing
object or an exposure observation.

## Layers

1. **Core resources** (`hew.yaml`) — `HEWResource`, `DatasetResource`,
   `LiteratureResource`, `SurveyInstrument`, `SurveyDataset`, `DataDictionary`,
   `Variable`, and `Distribution`.
2. **HEW domain indexing** (core) — `HEWSystematicReviewAnnotation` with
   `ConceptAnnotation` (exposure, health impact, and special topic coding),
   `GeographyAnnotation`, and `DataToolMethodAnnotation`.
3. **Attribution** (core) — `Agent`, `Person`, `Organization`, and `SoftwareAgent`.
4. **Extensions** (`hew-extended.yaml`) — exposome and geospatial
   (`GeospatialResource`, `EnvironmentalVariable`, `SpatialSupport`,
   `TemporalSupport`, `SpatialExtent`, `TemporalExtent`, `ValueSpecification`,
   resolution classes, `OMOPConceptBinding`, `SpatiotemporalExposure`,
   `CovariateCalculation`); programs and projects (`Program`, `Project`,
   `FundingSource`, `AgentAssociation`); and other resource types
   (`CohortResource`, `ToolResource`, `SoftwareResource`, `ModelResource`,
   `ResourceCollection`).
5. **Projections** — Dataverse, DCAT, Schema.org, DataCite, STAC, JSON-LD/RDF,
   knowledge-graph, and OMOP/Gaia mapping views.

## Exposure depth

- **Catalog topic:** a resource is tagged with an exposure, health impact,
  geography, population, or special topic for discovery.
- **Resource metadata:** a resource describes variables, methods, extent,
  support, temporal coverage, dictionary, and access conditions for reuse.
- **Exposure-ready semantics:** a resource or optional exposure object identifies
  property, exposure concept, context, unit, support, aggregation, provenance,
  and external-vocabulary mappings without requiring every value to be stored.

Systematic-review annotations remain an input stream and coding profile over
resources; they are not direct causal or biomedical truth statements.
