# Schema overview

The HEW schema is a canonical resource knowledge base. `HEWResource` is a
cataloged information or resource entity; it is not necessarily a data-bearing
object or an exposure observation.

## Layers

1. **Resource catalog core** — `HEWResource`, `DatasetResource`,
   `LiteratureResource`, `SurveyInstrument`, `SurveyDataset`, `ToolResource`,
   `SoftwareResource`, `ModelResource`, `GeospatialResource`, `DataDictionary`,
   `Distribution`, and `ResourceCollection`.
2. **HEW domain indexing** — `ExposureAnnotation`, `HealthImpactAnnotation`,
   `GeographyAnnotation`, `SpecialTopicAnnotation`, and
   `DataToolMethodAnnotation`.
3. **Exposome compatibility** — `EnvironmentalVariable`, `SpatialSupport`,
   `TemporalSupport`, `SpatialExtent`, `TemporalExtent`, `ValueSpecification`,
   resolution classes, `OMOPConceptBinding`, and `SpatiotemporalExposure`.
4. **Provenance and organization** — `Agent`, `Person`, `Organization`,
   `Program`, `Project`, `FundingSource`, `AgentAssociation`, and
   `CovariateCalculation`.
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
