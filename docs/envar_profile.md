# EnVar profile

`EnvironmentalVariable` is an HEW integration profile over EnVar-style
environmental variable metadata. It captures:

- the measured property and measurement or derivation method;
- aggregation semantics;
- spatial and temporal support;
- cross-vocabulary mappings; and
- optional OMOP concept binding and processing level.

HEW does not copy or fork an authoritative EnVar micro-schema. It preserves
legacy `measured_variables` strings while allowing structured variables in
`environmental_variables`. Quantitative and administrative spatial resolution
objects complement the existing human-readable `spatial_resolution` field.

Use ontology CURIEs for scientific concepts and reserve enums for closed
method, processing, alignment, and value-type vocabularies.
