# HEW_Catalog_Data_Model
HEW data model and data model documentation

The canonical schema is [`hew-model/schema/hew-geospatial.yaml`](hew-model/schema/hew-geospatial.yaml).
See the [consolidated schema design](docs/SCHEMA_DESIGN.md) for the resource,
review-coding, geospatial, EnVar, and interoperability model.


# Data Model Approach

Canonical model:          LinkML
Structural interchange:  JSON
Semantic layer:          Generated JSON-LD context
Application validation:  LinkML validator / generated JSON Schema
Database validation:     MongoDB-specific reduced JSON Schema
Operational storage:     MongoDB BSON documents
Knowledge-graph export:  JSON-LD/RDF, SHACL and ontology mappings

# References 

* [ECTO MODEL](https://github.com/EnvironmentOntology/environmental-exposure-ontology)
* [LinkML](https://linkml.io/)
* [Schema.org](https://schema.org/)
