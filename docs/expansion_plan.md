# Expansion plan

The core schema (`hew.yaml`) covers Phase 1. Phases 2–5 are already drafted as
extension modules composed in `hew-extended.yaml`; each phase moves into active
use, and into the core where needed, when a catalog workflow depends on it.

## Phase 1: Core catalog and Dataverse

Stabilize publications with systematic-review annotations, survey instruments
and survey datasets, authorship, and the Dataverse publication projection.

## Phase 2: Exposome compatibility

Strengthen EnVar-aligned variables, structured temporal and spatial resolution,
processing levels, and ENVO/ECTO/OMOP mappings.

## Phase 3: Covariate workflows

Catalog tools, collections, Amadeus and other software resources, and describe derivation methods,
parameters, source data, spatial joins, temporal windows, CRS, and outputs.

## Phase 4: Optional exposure estimates

Use `SpatiotemporalExposure` for measured, modeled, derived, or assigned
estimates linked to variables, locations, intervals, methods, and sources.

## Phase 5: External exposure linkage

Use `ExternalExposureLinkage` to describe OMOP/Gaia readiness without storing
patient-level clinical data.

## Phase 6: Knowledge-graph export

Export selected HEW catalog edges to RDF/JSON-LD and future ROBOKOP/Translator
views while preserving the distinction between resource tagging and causal claims.
