# CAFE Dataverse projection

CAFE Dataverse custom HEW metadata blocks are a curated projection of the HEW
canonical knowledge base. They should prioritize searchable discovery and reuse:
resource type, exposure and health-impact concepts, geography, time,
environmental variables, access, license, provenance, and external links.

Nested geometries, derivation graphs, role associations, and rich ontology
context remain in the canonical model. The projection is implemented by the
publication crosswalk in the `accel-dataverse-hew` repository
(`assets/crosswalks/publication/v1/`), which preserves the HEW identifier for
round-tripping to the source knowledge base.
