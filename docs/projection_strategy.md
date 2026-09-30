# Projection strategy

The canonical HEW LinkML model is authoritative. Projection formats expose
purpose-specific subsets and should remain traceable to canonical identifiers.

| Target | Primary use |
|---|---|
| CAFE Dataverse | searchable repository metadata blocks |
| DCAT | dataset and distribution catalogs |
| Schema.org | web discovery and linked metadata |
| DataCite | DOI-oriented publication and dataset metadata |
| STAC | geospatial collections, items, extents, and assets |
| GeoSPARQL/RDF | geometry, topology, and knowledge graphs |
| ROBOKOP/Translator | selected, policy-controlled graph edges |
| OMOP/Gaia/EnVar/Amadeus | external-exposure workflow alignment |

Projections should preserve HEW IDs and distinguish catalog assertions from
scientific assertions. They should not make Dataverse or any external standard
the source model.
