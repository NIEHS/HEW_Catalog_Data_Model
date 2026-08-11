# Ontology alignment notes

This repository starts with HEW-local identifiers and coding values. External mappings should be added cautiously and explicitly.

Candidate alignment targets:

- BioLink Model: broad biomedical categories and relationships.
- ECTO: exposure events and exposure-related classes.
- ENVO: environmental features, environmental materials, and environmental processes.
- MONDO / DOID: disease terms.
- HPO: phenotypic abnormalities where useful.
- OBI / IAO: information artifacts, study processes, data items, measurements.
- schema.org, DCAT, and Dublin Core Terms: web catalog and dataset metadata.

Do not force exact mappings for review-management values such as `Not Reported`, `General Exposure`, or `Other Exposure, Specify`. These are coding states or coding constructs, not domain entities.
