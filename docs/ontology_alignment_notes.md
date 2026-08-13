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

## Agent, project, program, and funding alignments

The coordination layer uses local HEW classes with external mappings:

- `Person`: `schema:Person`, `biolink:Person`, `prov:Person`
- `Organization`: `schema:Organization`, `biolink:Organization`, `prov:Organization`
- `SoftwareAgent`: `prov:SoftwareAgent`
- `Project`: `schema:Project`, close to `prov:Activity`
- `Program`: `schema:Project`, close to `prov:Activity`
- `FundingSource`: `schema:Grant`
- `AgentAssociation`: `prov:Association`, close to `schema:Role`, `schema:OrganizationRole`, and `biolink:Association`
- `DatasetResource`: `schema:Dataset`, close to `dcat:Dataset`
- `Distribution`: `dcat:Distribution`

HEW-specific classes are retained so the schema can support commons-specific governance, curation, and provenance needs while still exporting useful JSON-LD/RDF for discovery and integration.
