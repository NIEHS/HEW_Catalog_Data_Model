# HEW metadata strategy

The HEW metadata strategy uses the canonical LinkML model as the source of truth
for cataloging resources relevant to Health and Extreme Weather. It captures
resource metadata, domain indexing annotations, geospatial and temporal metadata,
environmental-variable metadata, provenance, people, projects, programs, and
funding.

HEW is a domain-specific slice of the broader exposome, focused on extreme
weather, weather-related disasters, and weather-mediated environmental harms.
The catalog-first model describes resources and their reuse context; it is not a
warehouse for every exposure observation or derived value.

## Canonical model vs endpoint projections

- The HEW LinkML model stores the rich internal knowledge graph.
- Dataverse metadata blocks expose a curated, searchable subset.
- Portal/API views expose researcher-facing search and browsing.
- DCAT and Schema.org support broad catalog and web discovery.
- DataCite supports DOI-oriented dataset metadata.
- STAC supports geospatial asset discovery and spatial/temporal search.
- GeoSPARQL/RDF supports spatial knowledge graphs and topology.
- ROBOKOP/Translator-style exports may expose selected graph edges later.
- OMOP/Gaia, EnVar, and Amadeus support external-exposure workflows.

## CAFE Dataverse projection

CAFE Dataverse is an endpoint projection, not the source model. Its custom HEW
metadata blocks should expose discovery and reuse fields while preserving rich
graph semantics in the canonical model.

| Dataverse group | HEW content |
|---|---|
| HEW domain | exposure, health-impact, and special-topic concepts |
| Resource type | publication, dataset, survey, tool, software, model, cohort |
| Geography | coverage, regions, features, and place identifiers |
| Time | legacy and structured temporal coverage |
| Environmental variables | property, unit, aggregation, spatial and temporal support |
| Reuse | access rights, license, dictionary, distributions |
| Provenance | project, generator, curator, reviewer |
| External links | DOI, PMID, repository, website, related resources |

The first mapping artifacts live under `mappings/dataverse/`. Nested graph
associations should remain in the canonical model rather than being flattened
into Dataverse fields.

## Catalog assertions vs scientific assertions

The catalog records assertions such as “this paper studies wildfire smoke and
asthma” or “this dataset provides daily heat-index values.” These are not causal
claims. A future knowledge-graph export must distinguish resource-topic tagging
from claims about causation, association strength, or clinical effect.
