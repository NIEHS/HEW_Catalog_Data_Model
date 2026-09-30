# OMOP/Gaia external exposure linkage

`ExternalExposureLinkage` records readiness for downstream OMOP/Gaia-style
external exposure workflows. It keeps linkage assumptions explicit without
requiring person-level data in the catalog.

The profile can identify:

- an exposure estimate and OMOP concept binding;
- a location-history or cohort reference;
- exposure start and end dates;
- spatial and temporal join methods;
- privacy-preserving geography; and
- implementation notes.

The same `OMOPConceptBinding` structure is available on environmental variables
and spatiotemporal exposures. A vocabulary gap can therefore be represented
without inventing a concept identifier.
